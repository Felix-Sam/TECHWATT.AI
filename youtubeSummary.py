from gtts import gTTS
import os
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import openai
from dotenv import load_dotenv


load_dotenv('apis.env')
key = os.getenv("API_KEY")
openai.api_key = key


class Youtube:
    def __init__(self):
        pass

    def processLink(link):
        id = link.split('/')
        # Preprocessing Youtube transcript
        vid_id = id[-1]
        data = yta.get_transcript(vid_id)
        final_data = ''
        for val in data:
            for key, value in val.items():
                if key == 'text':
                    final_data += value
        processed_data = final_data.splitlines()
        clean_data = ' '.join(processed_data)
        return clean_data

    def GptSummary(clean_data):
        task = 'Rewrite,correct and summarize this transcript accurately. '
        transcript_correction = task + clean_data
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
        corrected_text = response.choices[0].text
        return corrected_text

    def GptMainPoints(clean_data):
        mainpoint = 'list the main points in this transcript. dont list them with numbers.'
        transcript_points = mainpoint + clean_data
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=transcript_points,
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=[";"]
        )
        mainpoints = response.choices[0].text
        return mainpoints

    def Audio(summary):
        tts = gTTS(summary)
        audio_file = "youtube.mp3"
        tts.save(os.path.join('static', audio_file))

# link = 'https://youtu.be/Mti1dRhYTPU'
# clean_data = Youtube.processLink(link)
# summary = Youtube.GptSummary(clean_data)
# mainpoints = Youtube.GptMainPoints(clean_data)

# print(summary)