import os
import config
import requests
import logging
from dataclasses import asdict
from dotenv import load_dotenv

load_dotenv()

ENGINE_KEY = os.getenv("ENGINE_KEY")

logging.basicConfig(
    filename = config.LOG_FILE, 
    level = logging.INFO, 
    format = "%(asctime)s - %(levelname)s - %(message)s"
    )

if ENGINE_KEY is None:
    logging.warning("ENGINE_KEY not set - requests to the backend will be sent without auth and likely rejected")

def send_alert(attack):
    payload = asdict(attack)
    headers = {"X-Engine-Key": ENGINE_KEY} if ENGINE_KEY else {}

    try:
        response = requests.post(
            config.API_URL, json=payload, headers=headers, timeout=config.API_TIMEOUT
        )
        response.raise_for_status()
        logging.info(f"Alert sent: {payload}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to reach API({e}). Alert kept locally: {payload}")
        print(f"[API] Backend unreachable, alert logged locally insted: {e}")