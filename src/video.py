from logging import getLogger
from os import cpu_count, listdir
from pathlib import Path
from random import choice, randint
from shutil import copy
from math import floor

from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
)

from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop
from moviepy.video.fx.loop import loop
from proglog import TqdmProgressBarLogger


class MyBarLogger(TqdmProgressBarLogger):
    def callback(self, **changes):
        pass

    def new_tqdm_bar(self, bar):
        if (bar in self.tqdm_bars) and (self.tqdm_bars[bar] is not None):
            self.close_tqdm_bar(bar)
        infos = self.bars[bar]
        self.tqdm_bars[bar] = self.tqdm(
            total=infos["total"],
            leave=self.leave_bars,
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
        )


from config import ROOT_TEMP_DIR, Options, VideoOptions


def select_background(options: VideoOptions):
    Path(options.backgrounds_folder).mkdir(parents=True, exist_ok=True)
    vid = choice(listdir(options.backgrounds_options_folder))
    destination = options.backgrounds_folder + "bg.mp4"
    if not vid:
        raise IOError("Could not find any background videos.")
    copy(options.backgrounds_options_folder + vid, destination)
    return destination


def combine_image_and_audio(
    width: int, audio_path: str, image_path: str, options: VideoOptions
) -> ImageClip:
    audio = AudioFileClip(audio_path)
    image = (
        resize(
            ImageClip(image_path)
            .set_start(0)
            .set_duration(audio.duration)
            .set_pos(("center", "center")),
            width=width,
        )
        .crossfadein(options.fade_in_rate)
        .crossfadeout(options.fade_out_rate)
        .set_audio(audio)
    )
    return image


def create_video_for_post(
    num_comments: int,
    options: Options,
):
    logger = getLogger(__name__)
    base = VideoFileClip(select_background(options.video_options)).without_audio()
    width = base.h * (9 / 16)
    base = crop(base, x1=(base.w - (base.h * (9 / 16))) / 2, width=width)
    title = combine_image_and_audio(
        (9 / 10) * base.w,
        options.tts_options.save_folder + "title.mp3",
        options.screenshot_options.screenshot_folder + "title.png",
        options.video_options,
    )

    total = [
        title,
    ]
    gap = options.video_options.duration_between_videos
    total_duration = title.duration + gap

    for i in range(num_comments):
        nex = combine_image_and_audio(
            (9 / 10) * base.w,
            options.tts_options.save_folder + f"{i}.mp3",
            options.screenshot_options.screenshot_folder + f"{i}.png",
            options.video_options,
        ).set_start(total_duration)
        total.append(nex)
        total_duration += nex.duration + gap

    if total_duration < base.duration:
        base_duration = floor(base.duration - total_duration)
        random_base = randint(0, base_duration)
        base = base.subclip(random_base, random_base + total_duration)
    total = [
        loop(base, duration=total_duration)
        .crossfadein(options.video_options.full_video_fade_rate)
        .crossfadeout(options.video_options.full_video_fade_rate),
    ] + total
    final_clip = CompositeVideoClip(total)
    logger.info("Composing the final video.")
    final_clip.write_videofile(
        "output.mp4",
        codec="mpeg4",
        audio_codec="aac",
        temp_audiofile=ROOT_TEMP_DIR + "/temp-audio.m4a",
        remove_temp=True,
        bitrate=options.video_options.bitrate,
        threads=cpu_count(),
        logger=MyBarLogger(),
    )
