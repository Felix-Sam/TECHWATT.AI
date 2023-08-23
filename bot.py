import openai
from dotenv import load_dotenv
import os

load_dotenv('apis.env')
key = os.getenv("API_KEY")
openai.api_key = key


class Bot:
    def __init__(self, link):
        pass

    def chatbot(text):
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=text,
            temperature=0,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=[";"]
        )
        bot_result = response.choices[0].text
        return bot_result


# text = 'so whats food in science?'
# response = Bot.chatbot(text)
# print(response)
