import ast
import requests
import datetime
import logging
import os
from decouple import config
from bs4 import BeautifulSoup
from twilio.rest import Client

# this is my cat grabber, it gets a cat image and sends it to my girlfriend every morning

LOG_FOLDER = 'log_files'
LOG_FILENAME = f'Logfile - cat_messanger ({datetime.date.today()}).log'


# Initialize the logging system (debug, info, warning, error, and critical)
def setup_logging():
    try:
        os.makedirs(LOG_FOLDER, exist_ok=True)
        log_file = os.path.join(LOG_FOLDER, LOG_FILENAME)
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f'Log file created/accessed at {datetime.datetime.now()}')

    except Exception as e:
        logging.error(f'Error setting up log: {e}', exc_info=True)


def get_cat_image():
    try:
        # Send a photo on M, W, F:
        if datetime.date.today().isoweekday() in [1, 3, 5]:
            print(1)
            # The base URL for The Cat API
            base_url = "https://api.thecatapi.com/v1/"

            # The endpoint to get a random cat image
            endpoint = "images/search"

            # Get API key from .env file
            api_key = config('CAT_API_KEY')

            # Set the headers with the API key
            headers = {"x-api-key": api_key}

            # Get cat image
            response = requests.get(base_url + endpoint, headers=headers)
            cat = response.json()[0]["url"]
            print(cat)

        # Send a gif on the rest of the days
        else:
            cat = "https://cataas.com/cat/gif.gif"

        return cat

    except Exception as e:
        logging.error(f'Error getting cat image: {e}', exc_info=True)


def get_fact():
    try:
        # The base URL for The Joke API
        base_url = "https://meowfacts.herokuapp.com/"

        # Get cat fact
        response = requests.get(base_url)
        soup = str(BeautifulSoup(response.text, 'html.parser'))
        fact = f"I love you! - {ast.literal_eval(soup)['data'][0]}"
        return fact

    except Exception as e:
        logging.error(f'Error getting fact: {e}', exc_info=True)

    # send girlfriend a message with the cat image using Twilio


def send_message(url, message):
    try:
        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token = config('TWILIO_AUTH_TOKEN')

        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=message,
            from_=config('FROM_NUMBER'),
            media_url=[url],
            to=config('TO_NUMBER')
        )
    except Exception as e:
        logging.error(f'Error sending message image: {e}', exc_info=True)


def main():
    setup_logging()

    try:
        send_message(get_cat_image(), get_fact())

    except Exception as e:
        logging.error(f'Error occurred in main function: {e}', exc_info=True)

    finally:
        logging.info('Completed run')


### Run ###
if __name__ == '__main__':
    main()
