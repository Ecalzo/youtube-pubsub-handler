from enum import unique
import json
from flask_login.utils import login_required

import requests
from flask import Blueprint, request, current_app, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user

from yt_pubsub_handler import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_DISCOVERY_URL, client
from . import models
from .user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_google_provider_cfg():
    # TODO: make this more resilient
    return requests.get(GOOGLE_DISCOVERY_URL, timeout=60).json()


@bp.route("/login")
def login():
    # find out which URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    auth_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construc tht request for Google login
    # and provide scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri=request.url_root + "auth/login/callback",
        scope=["openid", "email"]
    )
    return redirect(request_uri)


@bp.route("/login/callback")
def callback():
    # Get authorization code Google sends back
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    )

    # parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))
    # get user info
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # ensure that email is verified
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
    else:
        return "User email not available or not verified by Google.", 400

    # create a user in the db
    user = User(
        id_=unique_id,
        email=users_email
    )

    if not User.get(unique_id):
        User.create(unique_id, users_email)

    login_user(user)
    return redirect(url_for("index"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
