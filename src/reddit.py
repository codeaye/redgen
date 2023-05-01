import logging
from praw.models import Submission, Comment
from beaupy import select, select_multiple

from utils import App


def fetch_post(num_comments: int, subreddit: str, allow_nsfw: bool) -> Submission:
    logger = logging.getLogger(__name__)
    top = []
    for i in App.reddit().subreddit(subreddit).hot():
        if allow_nsfw:
            if i.over_18 and i.num_comments >= num_comments:
                top.append(i)
        else:
            if not i.over_18 and i.num_comments >= num_comments:
                top.append(i)
    subs: list[Submission] = sorted(
        top,
        key=lambda x: x.score,
        reverse=True,
    )
    item_options = [f"{i+1}. {t.title} ({t.score})" for i, t in enumerate(subs)]
    item = subs[select(item_options, pagination=True, return_index=True)]
    logger.info("Fetched post: `%s`", item.id)
    logger.debug("Fetched post's link: %s", item.shortlink)
    return item


def fetch_comments(
    submission: Submission, comment_length: tuple[int, int]
) -> list[Comment]:
    logger = logging.getLogger(__name__)
    logger.info("Fetching comments")
    submission.comments.replace_more(limit=0)
    r_comments = sorted(
        filter(
            lambda x: len(x.body) >= comment_length[0]
            and len(x.body) <= comment_length[1]
            and x.body.isascii()
            and x.body.lower() != "removed",
            [i for i in submission.comments],
        ),
        key=lambda x: x.score,
        reverse=True,
    )
    nel = "\n"
    comments = select_multiple(
        options=[
            f"{i+1}. ({len(t.body)}) {t.body.split(nel)[0][0:120]+'...'}"
            for i, t in enumerate(r_comments)
        ],
        pagination=True,
        return_indices=True,
    )
    return [r_comments[i] for i in comments]
