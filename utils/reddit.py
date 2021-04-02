import praw
import os
import time
from flask import Flask

def reddit_login(app: Flask) -> [praw.Reddit, None]:
    """attempts to log in to reddit, retries 3 times"""
    attemps = 0
    reddit = None
    app.logger.info("logging in to reddit")
    while attempts < 3:
        try:
            reddit = praw.Reddit(
                client_id = os.getenv("client_id"),
                client_secret = os.getenv("client_secret"),
                user_agent = 'PRAW API tutorial Python Script',
                username = os.getenv("reddit_username"),
                password = os.getenv("reddit_password")
            )
            app.logger.info(f"successfully logged into reddit user: {os.getenv('reddit_username')}")
            break
        except:
            app.logger.exception(f"failed to log in to reddit, attempt: {attempts + 1}/3")
        attemps += 1
        time.sleep(10)
    return reddit

def reddit_make_post(subreddit: str, title: str, url: str, app: Flask) -> praw.models.Submission:
    app.logger.info(f"making post to subreddit: {subreddit}, title: {title}, url: {url}")
    reddit = reddit_login(app=app)
    sub_obj = reddit.subreddit(subreddit)
    post = sub_obj.submit(
       title=title,
       url=url
    )
    return post

