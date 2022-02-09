import requests
import lxml
from bs4 import BeautifulSoup
import urllib.request
import smtplib
import time


def get_link_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    name = soup.select_one(selector="#productTitle").getText()
    name = name.strip()

    price2 = soup.find(class_="a-offscreen").get_text()
    price1 = price2.replace('₹',"")
    price = price1.replace(',',"")
    price =float(price)
    return name, price

def send_email(message,rec_email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('contesteverydayat2005@gmail.com', 'Igi@12345')
    s.sendmail('contesteverydayat2005@gmail.com', rec_email, message)
    s.quit()