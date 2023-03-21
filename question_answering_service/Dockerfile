FROM python:3.8-slim-buster

WORKDIR /question_answering_service

COPY requirements.txt requirements.txt

# install rust compiler to build tiktoken
RUN apt-get update && apt-get install -y curl gcc
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
ENV RUST_BACKTRACE=1

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5005"]