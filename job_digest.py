import os, smtplib, requests
from email.mime.text import MIMEText
from pypdf import PdfReader

resume = "\n".join(pg.extract_text() or "" for pg in PdfReader("resume.pdf").pages)
prompt = open("prompt.txt").read()

def ask_llm(text):
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-2.5-flash:generateContent?key=" + os.environ["GEMINI_API_KEY"])
    body = {"contents": [{"parts": [{"text": text}]}],
            "tools": [{"google_search": {}}]}
    r = requests.post(url, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

result = ask_llm(f"{prompt}\n\nMy resume:\n{resume}")

msg = MIMEText(result)
msg["Subject"] = "Daily job digest"
msg["From"] = os.environ["SMTP_USER"]
msg["To"] = os.environ["EMAIL_TO"]
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
    s.login(os.environ["SMTP_USER"], os.environ["SMTP_APP_PASSWORD"])
    s.send_message(msg)
print("Email sent")