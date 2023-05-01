#!/usr/bin/env python3
from sys import platform
from time import sleep
from beaupy import console, prompt as prompt_or
from pytube import YouTube
from pytube.cli import on_progress


def tag(taggable: str, tags: str):
    return f"[{tags}]{taggable}[/{tags}]"


def prompt(que: str):
    value = None
    while True:
        try:
            value = prompt_or(
                que,
                validator=lambda inp: not not inp,
            )
            break
        except Exception:
            pass
    return value


def main():
    console.print(f"You should only have to run this script {tag('once', 'red bold')}.")
    console.print(
        "Be aware that this only configures the bare neccessities to get you going."
    )
    console.print(
        "If you plan to use offline tts, you will need to manually change values in src/config.py"
    )
    sleep(2)
    console.print("Lets set up the reddit api, so follow these steps")
    console.print(
        f"""
            Follow these steps https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
            and copy the Client {tag('id', 'yellow bold')} and Client {tag('secret', 'blue bold')}.
            """
    )
    client_id = prompt(
        f"Client {tag('id', 'yellow bold')}: ",
    )
    client_secret = prompt(
        f"Client {tag('secret', 'blue bold')}: ",
    )
    console.clear()

    console.print("Now lets set up the eleven labs api")
    sleep(2)
    console.print(
        f"""
        Sign up at https://beta.elevenlabs.io/sign-up
        Then click on your profile image on the top right
        Then click profile and from there copy your {tag('api key', 'green bold')}.
        """
    )
    elevenlabs_api_key = prompt(
        f"Elevenlabs {tag('api key', 'green bold')}: ",
    )
    console.clear()

    console.print("Now lets set up the browser")
    sleep(2)
    console.print("Make sure you have firefox installed.")
    console.print(
        f"""
            Visit https://www.reddit.com/ and log in
            Then make sure dark mode is disabled
            Then visit about:support and copy the value for {tag('Profile Folder', 'violet bold')}
        """
    )
    profile_folder = prompt(
        f"{tag('Profile Folder', 'violet bold')}: ",
    )
    console.clear()

    console.print("Now some custom stuff")
    sleep(2)
    name = (
        prompt(
            f"What is your first {tag('name', 'blue bold')}: ",
        )
        .lower()
        .replace(" ", "_")
    )
    reddit_name = prompt(
        f"What is your reddit {tag('username', 'red bold')}: ",
    )
    console.clear()

    with open(".env", "w", encoding="utf8") as env:
        env.writelines(
            f"""CLIENT_ID={client_id}
    CLIENT_SECRET={client_secret}
    USER_AGENT={platform}:com.{name}.redgen:v0.0.1 (by /u/{reddit_name})
    ELEVENLABS_API_KEY={elevenlabs_api_key}
    PROFILE_FOLDER={profile_folder}"""
        )

    console.print(f"Wrote to {tag('.env', 'green bold underline')} file")
    console.print(f"Downloading {tag('sample', 'blue bold')} background video.")
    YouTube(
        "https://www.youtube.com/watch?v=Pt5_GSKIWQM",
        use_oauth=True,
        allow_oauth_cache=True,
        on_progress_callback=on_progress,
    ).streams.filter(progressive=True, file_extension="mp4").order_by(
        "resolution"
    ).desc().first().download(
        "./assets/backgrounds/", filename="minecraft_sample.mp4"
    )
    console.clear()
    console.print(
        f"""Setup completed
    Read the `{tag('Usage', 'blue bold underline')}` in readme for next steps"""
    )


if __name__ == "__main__":
    main()
