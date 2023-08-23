from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
from youtubeSummary import *
from websiteSummary import *
from DetechOnImage import *
from barcode import *
from bot import *
import os
import cv2
from ultralytics import YOLO
import numpy as np


app = Flask(__name__)
app.config["UPLOAD_DIRECTORY"] = 'static/images'
app.config["MAX_CONTENT_LENGHT"] = 20*1024*1024
app.config["ALLOWED_EXTENTIONS"] = ['.jpg', '.png', '.jpeg', '.gif']

# For placing Home page images


@app.route("/", methods=['POST', 'GET'])
def hompage():
    logo = os.path.join(app.config["UPLOAD_DIRECTORY"], 'LOGO.png')
    felix = os.path.join(app.config["UPLOAD_DIRECTORY"], 'felix.jpg')
    beatrice = os.path.join(app.config["UPLOAD_DIRECTORY"], 'beatrice.jpg')
    nice = os.path.join(app.config["UPLOAD_DIRECTORY"], 'nice1.jpg')
    imgdiv = os.path.join(app.config["UPLOAD_DIRECTORY"], 'objdetect.jpg')
    autoai = os.path.join(app.config["UPLOAD_DIRECTORY"], 'computer.jpg')
    vision = os.path.join(app.config["UPLOAD_DIRECTORY"], 'vision.jpg')
    vision1 = os.path.join(app.config["UPLOAD_DIRECTORY"], 'vision2.jpg')
    return render_template('index.html', logo=logo, felix=felix,
                           beatrice=beatrice, nice=nice,
                           imgdivs=imgdiv, autoai=autoai,
                           vision=vision, vision1=vision1)

# For receiving messages from user


@app.route('/message', methods=['POST', 'GET'])
def messageus():
    if request.method == 'POST':
        message = request.form.get('messageus')
        print(message)
    return redirect('/')


# For Youtube summary page
@app.route("/youtubesummary", methods=['POST', 'GET'])
def youtubesummary():
    logo = os.path.join(app.config["UPLOAD_DIRECTORY"], 'LOGO.png')
    try:
        if request.method == 'POST':
            youtubelink = request.form.get('youtubelink')
            clean_data = Youtube.processLink(link=youtubelink)
            summary = Youtube.GptSummary(clean_data)
            mainpoints = Youtube.GptMainPoints(clean_data)
            Youtube.Audio(summary)
            # print(clean_data)
            # print(youtubelink)
            # print(summary)
            # print(mainpoints)
            return render_template('youtubesummary.html', logo=logo, clean_data=clean_data,
                                   summary=summary, mainpoints=mainpoints)

        return render_template('youtubesummary.html', logo=logo)
    except Exception:
        return 'Connection error or Video file too Large'


# For websites summary page
@app.route("/websitesummary", methods=['POST', 'GET'])
def websitesummary():
    try:
        logo = os.path.join(app.config["UPLOAD_DIRECTORY"], 'LOGO.png')
        if request.method == 'POST':
            text = request.form.get('websitelink')
            webtext = Blogpost.webtext(link=text)
            summary = webtext[0]
            mainpoints = webtext[1]
            audio = Blogpost.Audio(summary)
            return render_template('websitesummary.html', logo=logo,
                                   summary=summary, mainpoints=mainpoints)

        return render_template('websitesummary.html', logo=logo)
    except Exception:
        return 'Connection error'


# For uploading audio files
@app.route('/audio/<path:filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory('static', filename)

# For receiving image for object detection


@app.route('/detectonimage', methods=['POST', 'GET'])
def detectOnImages():
    logo = os.path.join(app.config["UPLOAD_DIRECTORY"], 'LOGO.png')
    if request.method == 'POST':
        image = request.files['images']
        extentions = os.path.splitext(image.filename)[1].lower()
        if image:
            if extentions not in app.config["ALLOWED_EXTENTIONS"]:
                return 'Unsupported Image Format'

            img = cv2.imdecode(np.fromstring(
                image.read(), np.uint8), cv2.IMREAD_COLOR)

            DetectOnImage().detect(img)
            return render_template('DetectOnImage.html', logo=logo)
        return 'Choose an image file'
    return render_template('DetectOnImage.html', logo=logo)


# For uploading detected image files on the site
@app.route('/audio/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('static', filename)

# FOR CHAT BOT


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        botmessage = request.form.get('botmessages')
        text = botmessage
        response = Bot.chatbot(text)
        return render_template("chatbot.html", response=response, usertext=text)
    return render_template("chatbot.html")

# Receiving User image for scanner


@app.route('/barcode', methods=['POST', 'GET'])
def barcode():
    logo = os.path.join(app.config["UPLOAD_DIRECTORY"], 'LOGO.png')
    if request.method == 'POST':
        image = request.files['scanimage']
        extentions = os.path.splitext(image.filename)[1].lower()
        if image:
            if extentions not in app.config["ALLOWED_EXTENTIONS"]:
                return 'Unsupported Image Format'

            image = cv2.imdecode(np.fromstring(
                image.read(), np.uint8), cv2.IMREAD_COLOR)
            result = Decode.barcode(image)
            if result == None:
                text = 'Empty barcode'

            else:
                text = result.split()
                text = text[0]

            return render_template('barcodescanner.html', logo=logo, text=text)
        return 'Choose an image file'
    return render_template('barcodescanner.html', logo=logo)


if __name__ == "__main__":
    app.run(debug=True)