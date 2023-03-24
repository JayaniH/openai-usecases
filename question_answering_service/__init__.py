import logging
import os
import sys

import gspread
import openai
from flask import Flask
from google.oauth2.credentials import Credentials
from transformers import GPT2TokenizerFast

from question_answering_service.utils import get_embedding, read_documents

gsclient = None
tokenizer = None
documents = {}
document_embeddings = {}


def create_app():
    global gsclient
    global tokenizer
    global documents
    global document_embeddings

    openai.api_key = os.getenv("OPENAI_API_KEY")

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    try:
        credentials = Credentials.from_authorized_user_info(info={
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "refresh_token": os.getenv("REFRESH_TOKEN"),
        })
        gsclient = gspread.authorize(credentials)

    except Exception as e:
        logging.error("Error authorizing google sheets client : " + str(e), exc_info=True)
        sys.exit(1)

    logging.info("Reading documents from google sheet")
    try:
        data = read_documents(gsclient, os.getenv("SHEET_ID"), os.getenv("SHEET_NAME"))

        for item in data:
            content_embedding = get_embedding(item['content'])
            documents[item['heading']] = item['content']
            document_embeddings[item['heading']] = content_embedding

    except Exception as e:
        logging.error("Error reading documents from google sheet : " + str(e), exc_info=True)
        sys.exit(1)

    app = Flask(__name__)

    with app.app_context():

        from . import question_answering

        return app
