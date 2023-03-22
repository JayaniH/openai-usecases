import logging

import openai

from question_answering_service.constants import EMBEDDING_MODEL


def count_tokens(text, tokenizer):
    return len(tokenizer.encode(text))


def get_embedding(text):
    try:
        result = openai.Embedding.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return result["data"][0]["embedding"]

    except Exception as e:
        logging.error("Error getting embedding: " + str(e), exc_info=True)


# function to read the data from the google sheet
def read_documents(gsclient, sheet_id, sheet_name):
    try:
        sheet = gsclient.open_by_key(sheet_id)
        sheet = sheet.worksheet(sheet_name)
        data = sheet.get_all_records()
        return data

    except Exception as e:
        logging.error("Error reading documents from google sheet: " + str(e), exc_info=True)
