import logging

import openai

from question_answering_service.constants import EMBEDDING_MODEL


def count_tokens(text, tokenizer):
    return len(tokenizer.encode(text))


def get_embedding(text):
    result = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return result["data"][0]["embedding"]


# function to read the data from the google sheet
def read_documents(gsclient, sheet_id, sheet_name):
    sheet = gsclient.open_by_key(sheet_id)
    sheet = sheet.worksheet(sheet_name)
    data = sheet.get_all_records()
    return data
