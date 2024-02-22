
import requests
from bs4 import BeautifulSoup
import html
import re
import time
import pygame

path = os.getcwd() 
def play_notification_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(f'{path}\Dad\mixkit-ow-exclamation-of-pain-2204.wav')  # Replace with the path to your notification sound file (WAV format)
    pygame.mixer.music.play()
    time.sleep(5)  # Adjust the duration the script should wait before continuing (in seconds)
    pygame.mixer.music.stop()

def make_request_with_retry(url):
    max_retries = 5
    delay = 32  # initial delay in seconds

    for _ in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses

            # Check if the response status code is 404 (Not Found)
            if response.status_code == 404:
                print(f"404 Error: Resource not found - {url}")
                return None

            # Return response for successful requests
            return response

        except requests.exceptions.ConnectionError as ce:
            print(f"ConnectionError: {ce}")

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")

            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code != 404:
                # Retry for non-404 HTTP errors
                print(f"Retrying in {delay} seconds.")
                time.sleep(delay)
                delay *= 2  # exponential backoff
            else:
                # Return None for other errors
                print("Failed to make request after retries.")
                # play_notification_sound()  # Play notification sound
                return None

    print("Failed to make request after retries.")
    play_notification_sound()  # Play notification sound
    return None

def scrape_stock_data(stock_symbol):
    url_relative_valuation = f'https://www.alphaspread.com/security/nse/{stock_symbol.lower()}/relative-valuation'
    url_dcf_valuation = f'https://www.alphaspread.com/security/nse/{stock_symbol.lower()}/dcf-valuation/base-case'
    
    # Scrape data for Relative Valuation
    response_relative_valuation = make_request_with_retry(url_relative_valuation)
    if response_relative_valuation is not None:
        soup_relative_valuation = BeautifulSoup(response_relative_valuation.text, 'html.parser')

        valuation_element = soup_relative_valuation.find('div', class_='ui relative-value-color no-margin valuation-scenario-value header restriction-sensitive-data')
        valuation_data = valuation_element.text.strip() if valuation_element else "N/A"

        relative_valuation_element = soup_relative_valuation.find('span', class_='opacity-90')
        relative_valuation_data = relative_valuation_element.text.strip() if relative_valuation_element else "N/A"
       
        # Check if price_div is not None before accessing its attributes
        price_div_ = soup_relative_valuation.find('div', class_='ui price progress on-hover-tooltip')
        price_ = re.search(r'<b>(.*?)</b>', html.unescape(price_div_.get('data-html', ''))).group(1) if price_div_ else "N/A"
        # print(price_)
    else:
        print(f" Failed to fetch data for Relative Valuation.")
        return "N/A","N/A","N/A","N/A","N/A","N/A"

    # Scrape data for DCF Valuation
    response_dcf_valuation = make_request_with_retry(url_dcf_valuation)
    if response_dcf_valuation is not None:
        soup_dcf_valuation = BeautifulSoup(response_dcf_valuation.text, 'html.parser')

        dcf_valuation_element = soup_dcf_valuation.find('div', class_='ui dcf-value-color no-margin valuation-scenario-value header restriction-sensitive-data')
        dcf_valuation_data = dcf_valuation_element.text.strip() if dcf_valuation_element else "N/A"

        dcf_currency_element = soup_dcf_valuation.find('span', class_='opacity-90')
        dcf_currency_data = dcf_currency_element.text.strip() if dcf_currency_element else "N/A"

        # Check if price_div is not None before accessing its attributes
        price_div = soup_dcf_valuation.find('div', class_='ui price progress on-hover-tooltip')
        price = re.search(r'<b>(.*?)</b>', html.unescape(price_div.get('data-html', ''))).group(1) if price_div else "N/A"
        # print(price)

    else:
        print(f" Failed to fetch data for DCF Valuation.")
        return "N/A","N/A","N/A","N/A","N/A","N/A"

    return valuation_data, relative_valuation_data, dcf_valuation_data, dcf_currency_data, price, price_
