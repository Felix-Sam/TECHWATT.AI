from gtts import gTTS
import os
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import openai

# API KEY FROM OPEN AI
openai.api_key = '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'

# Getting Youtube ID
link = 'https://youtu.be/WPr1TaOF6Tg'
id = link.split('/')

# Preprocessing Youtube transcript
vid_id = id[-1]
data = yta.get_transcript(vid_id)
final_data = ''
for val in data:
    for key,value in val.items():
        if key == 'text':
            final_data += value
processed_data = final_data.splitlines()
clean_data = ' '.join(processed_data)

task = 'Rewrite,correct summarize this transcript with heading Summary. '
mainpoint = 'list the main points in this transcript with heading Main Points.'
transcript_correction = task + clean_data
transcript_points = mainpoint + clean_data
# print(clean_data)
# print(transcript_correction)
# print(transcript_points)

# Making grammatical Correction in transcript
response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=transcript_correction,
    temperature=0,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=[";"]
)
corrected_text = response.choices[0].text
print(corrected_text)

# Getting main points from the corrected transcript
response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=transcript_points,
    temperature=0,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=[";"]
)
mainpoints = response.choices[0].text
print(mainpoints)

total_result = corrected_text + mainpoints


#Writting the resulted text into a file
with open('transcript.txt','w') as f:
    f.write(total_result)

# Converting the resulted text to audio file
tts = gTTS(total_result)
audio_file = "output.mp3"
tts.save(audio_file)
# os.system(f"start {audio_file}")
