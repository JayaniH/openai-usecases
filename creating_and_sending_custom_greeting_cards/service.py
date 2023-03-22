import base64
import logging
from concurrent.futures import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import openai
from flask import current_app as app
from flask import request

from creating_and_sending_custom_greeting_cards import email_client

COMPLETIONS_API_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 100,
    "model": "text-davinci-003",
}

IMAGE_API_PARAMS = {
    "n": 1,
    "size": "1024x1024"
}


@app.route('/send_greeting', methods=['POST'])
def create_and_send_greeting():
    try:
        json_body = request.json
        occasion = json_body.get('occasion')
        recipient_email = json_body.get('recipient_email')
        email_subject = json_body.get('email_subject')
        special_notes = json_body.get('special_notes', "")

        if occasion is None or recipient_email is None or email_subject is None:
            logging.error("Request is not properly formatted")
            return "Request is not properly formatted", 400

        with ThreadPoolExecutor() as executor:
            greeting_prompt = "Generate a greeting for a/an" + occasion + "\nSpecial notes: " + special_notes
            design_prompt = "Greeting card design for" + occasion + ", " + special_notes

            greeting_thread = executor.submit(generate_greeting, greeting_prompt)
            design_thread = executor.submit(generate_design, design_prompt)

            greeting = greeting_thread.result()
            image_url = design_thread.result()

            if greeting is None or image_url is None:
                logging.error("Error generating greeting or design.")
                return "Error generating greeting or design.", 500

            send_email(greeting, image_url, recipient_email, email_subject)
            return "Successfully created and sent greeting."

    except Exception as e:
        logging.error("Error creating and sending greeting: " + str(e), exc_info=True)
        return "Error creating and sending greeting.", 500


def send_email(greeting, image_url, recipient, subject):
    # Create a message object
    body = f'<html><body><p>{greeting}</p><br/> <img src={image_url}></body></html>'
    msg = MIMEMultipart()
    msg['to'] = recipient
    msg['subject'] = subject

    # Add the HTML content to the message
    html_message = MIMEText(body, 'html')
    msg.attach(html_message)

    try:
        raw_message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
        message = email_client.users().messages().send(userId='me', body=raw_message).execute()
        logging.info("Email sent successfully: " + message['id'])

    except Exception as e:
        logging.error("Error sending email: " + str(e), exc_info=True)
        raise e


def generate_greeting(prompt):
    try:
        response = openai.Completion.create(
            prompt=prompt,
            **COMPLETIONS_API_PARAMS
        )
        return response["choices"][0]["text"].strip(" \n")

    except Exception as e:
        logging.error("Error generating greeting: " + str(e), exc_info=True)


def generate_design(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            **IMAGE_API_PARAMS
        )
        image_url = response['data'][0]['url']
        return image_url

    except Exception as e:
        logging.error("Error generating design: " + str(e), exc_info=True)
