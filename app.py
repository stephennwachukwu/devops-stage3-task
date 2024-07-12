from flask import Flask, request
from tasks import send_mail, log_message
import logging

app = Flask(__name__)

logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    if sendmail:
        send_mail.delay(sendmail)
        return f"Email to {sendmail} queued."
    
    if talktome:
        log_message.delay()
        return "Message logged."

    return "Hello, use ?sendmail=<email> or ?talktome"

if __name__ == '__main__':
    app.run(debug=True)

