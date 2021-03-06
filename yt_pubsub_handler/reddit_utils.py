import praw
import os
import time
from flask import Flask, current_app


def reddit_login() -> [praw.Reddit, None]:
    """attempts to log in to reddit, retries 3 times"""
    attempts = 0
    reddit = None
    current_app.logger.info("logging in to reddit")
    while attempts < 3:
        try:
            reddit = praw.Reddit(
                client_id=os.getenv("client_id"),
                client_secret=os.getenv("client_secret"),
                user_agent='PRAW API tutorial Python Script',
                username=os.getenv("reddit_username"),
                password=os.getenv("reddit_password")
            )
            current_app.logger.info(
                f"successfully logged into reddit user: {os.getenv('reddit_username')}")
            print("successfully logged into reddit user:")
            break
        except:
            current_app.logger.exception(
                f"failed to log in to reddit, attempt: {attempts + 1}/3")
        attempts += 1
        time.sleep(10)
    return reddit


def reddit_make_post(subreddit: str, title: str, url: str) -> praw.models.Submission:
    current_app.logger.info(
        f"making post to subreddit: {subreddit}, title: {title}, url: {url}")
    post = None
    try:
        reddit = reddit_login()
        sub_obj = reddit.subreddit(subreddit)
        post = sub_obj.submit(
            title=title,
            url=url
        )
        current_app.logger.info(
            f"post successful, view: https://reddit.com/{post.permalink}")
    except:
        current_app.logger.exception(
            "failed to make post, something went wrong")
    return post
