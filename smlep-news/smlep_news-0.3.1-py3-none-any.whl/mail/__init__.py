import json
import os
import smtplib

from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .format import format_figaro, format_gh, format_guardian, format_ph, format_weather


today = datetime.now()
yesterday = today - timedelta(1)
paris_lat, paris_lon = 48.8566, 2.3522
paris_name = "Paris"


def send(target, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_PASSWORD"])

    server.sendmail(os.environ["EMAIL_NAME"], target, msg)
    server.quit()


def prepare_mail(target, size, lg="en"):
    subject = "SmlepNews on " + today.strftime("%Y-%m-%d")

    msg = MIMEMultipart()
    msg["From"] = os.environ["EMAIL_USERNAME"]
    msg["To"] = target
    msg["Subject"] = subject
    msg["Charset"] = "UTF-8"
    msg["Content-Type"] = "text/plain; charset=UTF-8"

    body = ""
    body += format_weather(
        os.environ.get("WEATHER_CITY", paris_name),
        os.environ.get("WEATHER_LAT", paris_lat),
        os.environ.get("WEATHER_LON", paris_lon),
        size,
        lg,
    )
    body += "<br>"
    body += format_ph(size, lg)
    body += "<br>"
    body += format_gh(size, lg)
    body += "<br>"
    if lg == "en":
        body += format_guardian(size)
    if lg == "fr":
        body += format_figaro(size)

    msg.attach(MIMEText(body, "html", "utf-8"))

    send(target, msg.as_string())
