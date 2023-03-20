import tiktoken

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

MAX_SECTION_LEN = 1500
SEPARATOR = "\n* "
ENCODING_STR = "cl100k_base"  # encoding for text-embedding-ada-002
ENCODING = tiktoken.get_encoding(ENCODING_STR)
SEPARATOR_LEN = len(ENCODING.encode(SEPARATOR))

COMPLETIONS_API_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 500,
    "model": COMPLETIONS_MODEL,
}
