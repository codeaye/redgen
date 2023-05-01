"""
This module provides functions for text censorship and formalization.
It also provides acces to logging and configuration
"""

from logging import info
from logging.config import fileConfig
from os import getenv
from shutil import rmtree
from typing import Callable
from praw import Reddit
from better_profanity import profanity

from config import ROOT_TEMP_DIR


class App:
    __reddit = None

    @staticmethod
    def reddit():
        if App.__reddit is None:
            App.__reddit = Reddit(
                client_id=getenv("CLIENT_ID"),
                client_secret=getenv("CLIENT_SECRET"),
                user_agent=getenv("USER_AGENT"),
            )
        return App.__reddit


def ignore_exceptions(lamda: Callable):
    try:
        lamda()
    except Exception:
        pass


def retry(num_trys: int, lamda: Callable):
    for _ in range(num_trys):
        try:
            lamda()
            break
        except Exception:
            pass


def setup():
    profanity.load_censor_words()
    fileConfig("logging.ini")
    info("Setup Complete")


def cleanup():
    info("Cleaning Up")
    rmtree(ROOT_TEMP_DIR)


def tag(taggable: str, tags: str):
    return f"[{tags}]{taggable}[/{tags}]"
