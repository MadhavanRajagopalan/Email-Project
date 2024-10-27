from flask import Flask, render_template
import json

app = Flask(__name__)

def load_sent_emails():
    try:
        with open('sent_emails.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/sent_emails')
def view_sent_emails():
    emails = load_sent_emails()
    return render_template('sent_emails.html', emails=emails)

if __name__ == '__main__':
    app.run(debug=True)
