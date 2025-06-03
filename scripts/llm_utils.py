

# --- File: scripts/llm_utils.py ---

import os
import time
import openai
import logging
from dotenv import load_dotenv # Ensure dotenv is loaded here too

load_dotenv() # Load .env variables at the very beginning of this script

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI client (API key will be loaded from environment variable)
# Ensure OPENAI_API_KEY is set in your .env file or system environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_job(description):
    """
    Summarizes a given job description using OpenAI's GPT-3.5-turbo.
    Includes a delay to respect rate limits.
    """
    if not openai.api_key:
        logging.error("OPENAI_API_KEY environment variable not set. Cannot summarize job.")
        return None

    prompt = (
        f"Summarize the following job description very concisely, focusing on key responsibilities, "
        f"required skills, and technologies. Keep it to 2-4 sentences:\n\n{description}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", # Using gpt-3.5-turbo for summarization
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes job descriptions concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        # Introduce a delay to respect OpenAI's rate limits
        # Adjust as needed based on your specific tier and usage patterns
        time.sleep(1) # Start with 1 second, increase if 429 errors persist

        return response.choices[0].message.content.strip()

    except openai.APIError as e:
        logging.error(f"OpenAI API Error during summarization: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during summarization: {e}")
        return None

def get_chat_response(messages):
    """
    Gets a response from OpenAI's GPT-3.5-turbo for a given chat history.
    Messages should be in the format: [{"role": "user", "content": "..."}]
    """
    if not openai.api_key:
        logging.error("OPENAI_API_KEY environment variable not set. Cannot get chat response.")
        return "Error: API key not configured."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", # Using gpt-3.5-turbo for chat
            messages=messages,
            temperature=0.7,
            max_tokens=200 # Adjust max_tokens for chat responses as needed
        )
        # Introduce a delay to respect OpenAI's rate limits
        time.sleep(1) # Start with 1 second, increase if 429 errors persist

        return response.choices[0].message.content.strip()

    except openai.APIError as e:
        logging.error(f"OpenAI API Error during chat: {e}")
        return f"Error: OpenAI API call failed. {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred during chat: {e}")
        return "Error: An unexpected issue occurred."
