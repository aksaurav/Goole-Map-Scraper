"""Part 2: Personalized Email Generation using ChatGPT"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai

# Set up OpenAI API
openai.api_key = "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"

# Define the scope and credentials file path for Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials_path = "uplifted-time-269814-92549a3043e6.json"

# Define email credentials
email_address = "workwithaksaurav@gmail.com"
email_password = "******"

# Authenticate with Google Sheets API
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)

# Open the Google Sheets document
spreadsheet_key = "1UTCc5jnghwR1MDmlZ4Nj59eeuO_xxjpKpTKTLcT8fU8"
worksheet = gc.open_by_key(spreadsheet_key).sheet1

# Get the data from Google Sheets
data = worksheet.get_all_records()

# email template
email_template = """
Dear {name},

We are excited to reach out to you regarding our {product}. With your interest in {interest}, we believe our {product} can greatly benefit you.

Please feel free to reach out if you have any questions or would like further information.

Best regards,
Abdul kadir 
"""

# Generate personalized emails using OpenAI API
for lead in data:
    lead_name = lead["Name"]
    lead_interest = lead["Interest"]
    lead_product = lead["Product"]

    prompt = f"Dear {lead_name},\n\nWe are excited to reach out to you regarding our {lead_product}. With your interest in {lead_interest}, we believe our {lead_product} can greatly benefit you. Please feel free to reach out if you have any questions or would like further information.\n\nBest regards,\nYour Name"

    response = openai.Completion.create(
        engine="davinci", prompt=prompt, max_tokens=100, n=1, stop=["\n"]
    )

    email_content = response.choices[0].text.strip()

    """Part 3: Email Sending"""

    subject = "Autometed Email"
    to_email = lead["Email"]

    msg = MIMEMultipart()
    msg["From"] = email_address
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(email_content, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {lead_name} at {to_email}")
    except Exception as e:
        print(f"Error sending email to {lead_name}: {e}")
