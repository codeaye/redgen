#!/usr/bin/env python3
from beaupy import prompt, console
from dotenv import load_dotenv

load_dotenv()

from config import Options
from utils import setup, cleanup, tag, App
from reddit import fetch_comments, fetch_post
from screenshot import compose_screenshots
from audio import create_audio_for_post
from video import create_video_for_post

if __name__ == "__main__":
    setup()
    not_top = prompt(
        "Do you want to specify a post?",
        target_type=bool,
        initial_value="False",
    )
    min_comment_length = prompt(
        f"How long should each {tag('comment', 'blue bold underline')} at least be?",
        target_type=int,
        initial_value="100",
    )
    max_comment_length = prompt(
        f"How long can each {tag('comment', 'yellow bold underline')} be?",
        target_type=int,
        initial_value="200",
    )
    should_clean = prompt(
        "Should I remove any temporary files after?",
        target_type=bool,
        initial_value="True",
    )

    post = None

    if not_top:
        post_id = prompt(
            f"What is the id of the {tag('post', 'blue bold underline')}?",
        )
        post = App.reddit().submission(post_id)
    else:
        subreddit = prompt(
            f"What {tag('subreddit', 'yellow bold underline')} should i fetch?",
            initial_value="AskReddit",
        )
        min_comments = prompt(
            f"How many {tag('comments', 'blue bold underline')} should it at least have?",
            target_type=int,
            initial_value="100",
        )
        allow_nsfw = prompt(
            f"Should nsfw {tag('posts', 'red bold underline')} be allowed?",
            target_type=bool,
            initial_value="False",
        )
        post = fetch_post(min_comments, subreddit, allow_nsfw)
    comments = fetch_comments(post, (min_comment_length, max_comment_length))
    options = Options()

    compose_screenshots(post, comments, options.screenshot_options)
    create_audio_for_post(post, comments, options.tts_options)
    create_video_for_post(len(comments), options)
    if should_clean:
        cleanup()
    quote = tag('"', "yellow bold")
    console.print(
        f"\n\n{tag('Video Title', 'blue bold underline')}: {quote}{post.title}{quote}"
    )
