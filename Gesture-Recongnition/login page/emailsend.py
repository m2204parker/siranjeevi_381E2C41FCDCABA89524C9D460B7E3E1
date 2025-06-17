from flask import Flask, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Mail Settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    username = data.get('username')
    email = "receiver-email@example.com"  # Change to the actual receiver's email

    try:
        msg = Message("Login Notification",
                      recipients=[email],
                      body=f"User '{username}' just logged in!")
        mail.send(msg)
        return jsonify({"success": True, "message": "Email sent successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
