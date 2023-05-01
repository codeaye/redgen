from logging import getLogger
from os import remove, system
from pathlib import Path

from pyttsx3 import init
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from praw.models import Submission, Comment
from requests import post as post_web, get
from better_profanity import profanity

from config import TtsOptions


def online_tts(text: str, file_path: str, options: TtsOptions):
    doc = post_web(
        f"https://api.elevenlabs.io/v1/text-to-speech/{options.voice_id}/stream",
        json={
            "text": text,
            "voice_settings": {
                "stability": options.stability,
                "similarity_boost": options.similarity_boost,
            },
        },
        headers={
            "Content-Type": "application/json",
            "accept": "audio/mpeg",
            "xi-api-key": options.api_key,
        },
        timeout=20,
        stream=True,
    )

    if doc.status_code == 200:
        with open(f"{file_path}.mp3", "wb") as file:
            file.write(doc.content)
        return file_path
    raise ConnectionRefusedError


def offline_tts(text: str, file_path: str, options: TtsOptions):
    engine = init(options.engine)
    engine.setProperty("rate", options.rate)
    engine.setProperty("volume", options.volume)
    engine.setProperty("voice", options.voice)
    engine.save_to_file(text, f"{file_path}.aiff")
    engine.runAndWait()
    system(
        (
            f"ffmpeg -i {file_path}.aiff -filter_complex "
            '"compand=attacks=0:points=-80/-900|-45/-15|-27/-9|0/-7|20/-7:gain=5" '
            f"{file_path}.mp3 -y -hide_banner -loglevel error"
        )
    )
    remove(f"{file_path}.aiff")
    return file_path


def tts(text: str, file_path: str, options: TtsOptions):
    if not options.force_offline:
        try:
            online_tts(text, file_path, options)
        except ConnectionRefusedError:
            offline_tts(text, file_path, options)
    else:
        offline_tts(text, file_path, options)


def create_audio_for_post(
    post: Submission,
    comments: list[Comment],
    options: TtsOptions,
):
    logger = getLogger(__name__)
    logger.info("Composing all the audio files")
    Path(options.save_folder).mkdir(parents=True, exist_ok=True)
    tts(
        post.title + "\n" + post.selftext,
        f"{options.save_folder}/title",
        options,
    )
    with tqdm(
        total=len(comments), bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}"
    ) as pbar:
        for i, comment in enumerate(comments):
            tts(
                profanity.censor(comment.body, ""),
                f"{options.save_folder}/{i}",
                options,
            )
            pbar.update()
    user_info = get(
        "https://api.elevenlabs.io/v1/user/subscription",
        headers={
            "accept": "application/json",
            "xi-api-key": options.api_key,
        },
        timeout=20,
    )
    if user_info.status_code == 200:
        response = user_info.json()
        logger = getLogger(__name__)
        with logging_redirect_tqdm():
            logger.info(
                "API Quota left: %s",
                response["character_limit"] - response["character_count"],
            )
