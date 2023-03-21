FROM python:3.8-slim-buster

WORKDIR /creating_and_sending_custom_greeting_cards

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5005"]