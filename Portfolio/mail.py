from flask import Flask, request, redirect, flash, render_template
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'supersecret'

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'siranjmmus2204@gmail.com'
app.config['MAIL_PASSWORD'] = 'jwdrpeircgcznatj'  # Gmail App Password
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

# 👉 Home Page (renders index.html)
@app.route('/')
def index():
    return render_template('index.html')


# 👉 Form submission
@app.route('/send-message', methods=['POST'])
def send_message():
    hr_name = request.form['name']
    hr_email = request.form['email']
    hr_msg = request.form['message']

    # Mail to you (Siranjeevi)
    msg_to_me = Message(subject=f"New message from {hr_name}",
                        sender=app.config['MAIL_USERNAME'],
                        recipients=['siranjmmus2204@gmail.com'])
    msg_to_me.body = f"Name: {hr_name}\nEmail: {hr_email}\nMessage:\n{hr_msg}"
    mail.send(msg_to_me)

    # Auto-reply to HR
    msg_to_hr = Message(subject="Thank you for reviewing my profile",
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[hr_email])
    
    msg_to_hr.body = f"""Dear {hr_name},

Thank you for taking the time to review my profile.  
I truly appreciate the opportunity and I’m excited about the possibility of working with your team.

Please let me know if any further information is required from my side.  
Looking forward to hearing from you.

Regards,  
Siranjeevi M  
📞 6369721823  
🔗 https://www.linkedin.com/in/siranjeevi-m-770769299?
"""
    mail.send(msg_to_hr)

    flash("Your message has been sent successfully!")
    return redirect('/')


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
