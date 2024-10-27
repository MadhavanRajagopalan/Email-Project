import smtplib
import pandas as pd
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENT_EMAILS_FILE = 'sent_emails.json'

try:
    with open(SENT_EMAILS_FILE, 'r') as file:
        sent_emails = json.load(file)
except FileNotFoundError:
    sent_emails = []

def save_sent_emails():
    with open(SENT_EMAILS_FILE, 'w') as file:
        json.dump(sent_emails, file, indent=4)

def send_email(to_address, subject, body_html):
    msg = MIMEMultipart()
    msg['From'] = 'madhavanrajagopalan@aidworksfoundation.org'
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body_html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login('madhavanrajagopalan@aidworksfoundation.org', 'hczr gsuo oifh idnx')

    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    sent_emails.append({
        'to': to_address,
        'subject': subject,
        'body': body_html
    })
    save_sent_emails()


def send_bulk_emails(csv_file):
    data = pd.read_csv(csv_file)
    filtered_data = data[data['Confidence score'] > 80]

    for _, row in filtered_data.iterrows():
        email = row['Email address']
        name = row.get('Name', 'Valued Customer')
        organization = row.get('Organization', 'Your Company')

        with open('templates/email_templates.html', 'r') as file:
            body_html = file.read()
            body_html = body_html.replace('{{ name }}', name).replace('{{ organization }}', organization)

        send_email(email, "Your Subject Here", body_html)

# def send_test_email():
#     test_email = 'trungnguyen@aidworksfoundation.org'

#     with open('templates/email_templates.html', 'r') as file:
#         body_html = file.read()
    
#     body_html = body_html.replace('{{ name }}', 'Madhavan Rajagopalan').replace('{{ organization }}', 'AidWorks Foundation')
    
#     send_email(test_email, "Test Subject: HTML Email", body_html)

if __name__ == '__main__':
    # send_bulk_emails()
    print("Sent emails:", sent_emails)  # Verify that the test email is added to the list
