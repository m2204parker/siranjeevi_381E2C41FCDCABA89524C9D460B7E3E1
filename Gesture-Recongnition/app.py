from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import random

app = Flask(__name__)
app.secret_key = 'supersecret123'

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="silent_talk"
)
cursor = db.cursor()

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'silenttalk2025@gmail.com'
app.config['MAIL_PASSWORD'] = 'eauigaepfxjzkajm'  #  Paste your 16-character App Password here
mail = Mail(app)

# Gesture Recognition Setup
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
offset, imgSize = 20, 300
labels = ["Hello", "Hand gesture detection","Okay", "Please", "Thank you", "Yes"]
sentence = []

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['uname']
        email = request.form['mail']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            db.commit()
            flash('Signup Successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')

    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user'] = user[1]

            # ✅ Email Sending with try-except
            try:
                msg = Message('Silent Talk AI - Login Success',
                              sender='silenttalk2025@gmail.com',
                              recipients=[email])
                msg.body = 'Login successfully of Silent Talk AI.'
                mail.send(msg)
            except Exception as e:
                print("Mail Sending Error:", e)

            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Credentials', 'danger')

     return render_template('login.html')
# Home Page Route
@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))


# About Page Route
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



# Gesture Page
@app.route('/gesture')
def gesture_page():
    if 'user' in session:
        return render_template('gesture.html')
    return redirect(url_for('login'))

@app.route('/video')
def video():
    if 'user' in session:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for('login'))

@app.route('/get-word')
def get_word():
    if sentence:
        word = sentence[-1]
        current_sentence = ' '.join(sentence)
        return jsonify({"word": word, "sentence": current_sentence})
    return jsonify({"word": "", "sentence": ""})

@app.route('/clear-sentence', methods=['POST'])
def clear_sentence():
    sentence.clear()
    return jsonify({"message": "Sentence cleared!"})

# Gesture Frame Generator
def generate_frames():
    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        detected_word = None

        hands, img = detector.findHands(img)
        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

                if imgCrop.shape[0] > 0 and imgCrop.shape[1] > 0:
                    aspectRatio = h / w
                    if aspectRatio > 1:
                        k = imgSize / h
                        wCal = math.ceil(k * w)
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wGap + wCal] = imgResize
                    else:
                        k = imgSize / w
                        hCal = math.ceil(k * h)
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hGap + hCal, :] = imgResize

                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    detected_word = labels[index]
                    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

                    cv2.rectangle(imgOutput, (x, y), (x + w, y + h), color, 4)
                    cv2.rectangle(imgOutput, (x, y + h + 10), (x + w, y + h + 50), color, cv2.FILLED)
                    cv2.putText(imgOutput, detected_word, (x + 10, y + h + 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if detected_word:
            if not sentence or sentence[-1] != detected_word:
                sentence.append(detected_word)

        ret, buffer = cv2.imencode('.jpg', imgOutput)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)