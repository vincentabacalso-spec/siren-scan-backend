import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def send_email(email_address: str):
  params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": [email_address],
    "subject": "hello world",
    "html": "<p>it works!</p>",
    "reply_to": "onboarding@resend.dev"
  }
  resend.Emails.send(params)

