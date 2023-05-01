from os import getenv
from typing import NamedTuple

ROOT_TEMP_DIR = "temp"


class TtsOptions(NamedTuple):
    # Online
    api_key: str = getenv("ELEVENLABS_API_KEY")
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    stability: float = 0.30
    similarity_boost: float = 0.90

    force_offline: bool = False

    # Offline
    rate: int = 200
    volume: float = 1.0
    engine: str = "nsss"
    voice: str = "com.apple.voice.compact.en-US.Samantha"

    save_folder = f"{ROOT_TEMP_DIR}/audio/"


class VideoOptions(NamedTuple):
    backgrounds_options_folder = "assets/backgrounds/"
    backgrounds_folder = f"{ROOT_TEMP_DIR}/backgrounds/"

    fade_in_rate: float = 0.3
    fade_out_rate: float = 0.2
    full_video_fade_rate: float = 0
    duration_between_videos: float = 0.8

    # Export Settings
    bitrate: str = "50000k"


class ScreenshotOptions(NamedTuple):
    screenshot_folder: str = f"{ROOT_TEMP_DIR}/screenshots/"

    headless: bool = True
    timeout: int = 10
    retry_amount: int = 3
    dpi: float = 5.0
    transparency: float = 0.0
    # Find through about:support in firefox.
    # Make sure you log into reddit in this profile.
    firefox_profile: str = getenv("PROFILE_FOLDER")

    cookies_button_path: str = '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div/section/div/section[2]/section[1]/form/button'
    title_path: str = '//*[@id="t3_{}"]'
    title_text_path: str = '//*[@id="t3_{}"]/div/div[3]/div[1]/div/h1'
    subtitle_root_path: str = '//*[@id="t3_{}"]/div/div[5]/div/*'

    comment_path: str = '//*[@id="t1_{}"]'
    comment_text_path: str = '//*[@id="t1_{}"]/div[2]/div[3]/div[2]/div/*'

    comment_url: str = "https://www.reddit.com/r/{}/comments/{}/comment/{}"


class Options(NamedTuple):
    video_options = VideoOptions()
    screenshot_options = ScreenshotOptions()
    tts_options = TtsOptions()
