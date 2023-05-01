from io import BytesIO
from os import devnull
from pathlib import Path
from logging import getLogger
from multiprocessing import Pool, cpu_count
from PIL import Image
from tqdm import tqdm
from better_profanity import profanity
import numpy as np
from praw.models import Submission, Comment

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from config import ScreenshotOptions
from utils import ignore_exceptions


def add_transparency(image: Image, transparency: float) -> Image:
    data = np.array(image.convert("RGBA"))
    red, green, blue, _alpha = data.T

    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[...][white_areas.T] = (
        255,
        255,
        255,
        (255 - (255 * transparency)),
    )

    im2 = Image.fromarray(data)
    return im2


def setup_driver(url: str, options: ScreenshotOptions):
    driver_options = webdriver.FirefoxOptions()
    driver_options.headless = options.headless
    driver_options.service_log_path = devnull
    profile = webdriver.FirefoxProfile(options.firefox_profile)
    profile.set_preference("layout.css.devPixelsPerPx", str(options.dpi))
    driver = webdriver.Firefox(
        options=driver_options,
        firefox_profile=profile,
    )
    driver.set_page_load_timeout(60)
    driver.set_window_size(width=500, height=800)
    driver.get(url)
    ignore_exceptions(
        lambda: WebDriverWait(driver, options.timeout // 2)
        .until(EC.element_to_be_clickable((By.XPATH, options.cookies_button_path)))
        .click()
    )
    return driver


def get_title_screenshot(post: Submission, options: ScreenshotOptions):
    Path(options.screenshot_folder).mkdir(parents=True, exist_ok=True)
    driver = setup_driver(post.shortlink, options)
    try:
        element = WebDriverWait(driver, options.timeout).until(
            lambda x: x.find_element(By.XPATH, options.title_path.format(post.id))
        )
        title_text = WebDriverWait(driver, options.timeout).until(
            lambda x: x.find_element(By.XPATH, options.title_text_path.format(post.id))
        )
        driver.execute_script(
            f"arguments[0].innerText = '{profanity.censor(title_text.text)}'",
            title_text,
        )

        sub_elements = WebDriverWait(driver, options.timeout).until(
            lambda x: x.find_elements(
                By.XPATH, options.subtitle_root_path.format(post.id)
            )
        )
        for i in sub_elements:
            censored = f'arguments[0].innerText = "{profanity.censor(i.text)}"'
            driver.execute_script(censored, i)

        driver.execute_script("window.focus();")
        screenshot = element.screenshot_as_png
        scr = Image.open(BytesIO(screenshot))
        im2 = add_transparency(scr, options.transparency)
        im2.save(f"{options.screenshot_folder}title.png")
    finally:
        driver.close()


def get_comment_screenshot(
    post: Submission, options: ScreenshotOptions, comment: Comment, file_name: str
):
    Path(options.screenshot_folder).mkdir(parents=True, exist_ok=True)
    driver = setup_driver(
        options.comment_url.format(post.subreddit.display_name, post.id, comment.id),
        options,
    )
    try:
        element = WebDriverWait(driver, options.timeout).until(
            lambda x: x.find_element(By.XPATH, options.comment_path.format(comment.id))
        )

        sub_elements = WebDriverWait(driver, options.timeout).until(
            lambda x: x.find_elements(
                By.XPATH, options.comment_text_path.format(comment.id)
            )
        )
        for i in sub_elements:
            censored = f'arguments[0].innerText = "{profanity.censor(i.text)}"'
            try:
                driver.execute_script(censored, i)
            except Exception:
                pass

        driver.execute_script("window.focus();")

        screenshot = element.screenshot_as_png
        scr = Image.open(BytesIO(screenshot))
        im2 = add_transparency(scr, options.transparency)
        im2.save(f"{options.screenshot_folder}/{file_name}.png")
    finally:
        driver.close()


def compose_screenshots(
    post: Submission, comments: list[Comment], options: ScreenshotOptions
):
    n_iters = len(comments) + 1
    logger = getLogger(__name__)
    logger.info("Composing %s screenshots.", n_iters)

    with Pool(cpu_count()) as pool, tqdm(
        total=n_iters, bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}"
    ) as pbar:
        process_list = [
            pool.apply_async(
                get_title_screenshot,
                args=(post, options),
                callback=lambda _: pbar.update(),
            )
        ] + [
            pool.apply_async(
                get_comment_screenshot,
                args=(post, options, comment, str(i)),
                callback=lambda _: pbar.update(),
            )
            for i, comment in enumerate(comments)
        ]

        try:
            for process in process_list:
                process.get()
        except Exception as error:
            logger.error(error)
            raise IOError
