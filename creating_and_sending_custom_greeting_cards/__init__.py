import logging
import os
import sys

import openai
from flask import Flask
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

email_client = None


def create_app():
    global email_client

    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        creds = Credentials.from_authorized_user_info(info={
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "refresh_token": os.getenv("REFRESH_TOKEN"),
        })
        email_client = build('gmail', 'v1', credentials=creds)

    except Exception as e:
        logging.error("Error authorizing gmail client : " + str(e), exc_info=True)
        sys.exit(1)

    app = Flask(__name__)

    with app.app_context():

        from . import service

        return app
