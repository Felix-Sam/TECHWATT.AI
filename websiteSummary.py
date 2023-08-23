from gtts import gTTS
import os
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import openai
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv('apis.env')
key = os.getenv("API_KEY")
openai.api_key = key


class Blogpost:
    def __init__(self, link):
        pass

    def webtext(link):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = ''
        for paragraph in paragraphs:
            text += paragraph.get_text()

        task = 'Rewrite, summarize this transcript and remove all unnecessary data from it. '
        mainpoint = 'list the main points in this transcript.dont list them with numbers '
        prompts = mainpoint + text
        transcript_correction = task + text

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=transcript_correction,
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=[";"]
        )
        summary = response.choices[0].text
        # print(summary)

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompts,
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=[";"]
        )
        mainpoints = response.choices[0].text
        # print(mainpoints)
        return (summary, mainpoints)

    def Audio(summary):
        tts = gTTS(summary)
        audio_file = "website.mp3"
        tts.save(os.path.join('static', audio_file))


# link = 'https://medium.com/analytics-vidhya/image-classification-techniques-83fd87011cac'
# result = Blogpost.webtext(link)
# print(result)
