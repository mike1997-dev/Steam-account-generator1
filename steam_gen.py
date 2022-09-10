# Title: BattleNet generator
#
# Description: Goes to battle net website an makes accounts
#
# Author: Mr_bond#2732

import email
import imaplib
import quopri
import random
import string
import time
import tkinter as tkr
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from tkinter import * 
from PIL import ImageTk,Image
from tkinter import messagebox
import json
import sys

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

token = sys.argv[1]
custom_username = sys.argv[2]
custom_password = sys.argv[3]
API = f"https://api.hotmailbox.me/mail/buy?apikey={token}&mailcode=HOTMAIL&quantity=1"


def generate_hotmail_account():
    resp = requests.get(API)
    if resp.status_code == 200:
        # extract the email address and password from the response
        resp = resp.json()
        # check if json contains 'Data' key
        if 'Data' in resp:
            generated_email_credentials = resp['Data']['Emails'][0]
            return generated_email_credentials['Email'], generated_email_credentials['Password']
        else:
            time.sleep(random.randint(4, 6))
            generate_hotmail_account()
    else:
        time.sleep(random.randint(4, 6))
        generate_hotmail_account()


def process_payload(payload):
    body = quopri.decodestring(payload)
    try:
        body = body.decode()
    except UnicodeDecodeError:
        body = body.decode('cp1252')

    return body

def random_char(char_num):
    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))

def randomnum(charnum1):
    return "".join(random.choice(string.digits) for _ in range(charnum1))
    
def extract_emails_for_verification_link(username, email_password):
    # use your email provider's IMAP server: For hotmail, outlook and office 365, it's this:
    imap_server = "outlook.office365.com"

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(imap_server)

    # authenticate
    imap.login(username, email_password)

    # check if the connection was successful
    if imap.state == 'AUTH':
        verification_link = None
        # select messages folder
        imap.select('Inbox')
        # search for UNSEEN messages
        (resp_code, messages) = imap.search(None, '(UNSEEN)')
        # if there are emails
        if resp_code == 'OK':
            # get the emails
            emails = messages[0].split()

            # if there are emails
            if len(emails) > 0:
                # for each email
                for email_id in emails:
                    # fetch the email
                    (resp_code, data) = imap.fetch(email_id, '(RFC822)')

                    for response_part in data:
                        if isinstance(response_part, tuple):
                            # convert the email to a string
                            msg = email.message_from_bytes(response_part[1])

                            # get the email subject
                            subject = msg['subject']

                            if str(subject).lower() == ("New Steam Account Email Verification".lower()):
                                # get the email body
                                email_body = msg.get_payload()

                                html_string = process_payload(email_body[1].as_bytes())

                                soup = BeautifulSoup(html_string, 'html.parser')

                                verification_link = soup.find('span', {'class': 'link c-grey4'}).parent.get('href')
                            else:
                                verification_link = None
            else:
                verification_link = None
        else:
            verification_link = None
    else:
        verification_link = None

    return verification_link


def random_num(char_num1):
    return ''.join(random.choice(string.digits) for _ in range(char_num1))


def create_account():
    playwright = sync_playwright().start()

    browser = playwright.firefox.launch(headless=False)

    context = browser.new_context(viewport={ 'width': 550, 'height': 700 },device_scale_factor=2)
    #viewport={ 'width': 500, 'height': 400 },device_scale_factor=2,
    page = context.new_page()
    page.set_default_navigation_timeout(5000000)

    page.goto("https://store.steampowered.com/join")
    time.sleep(2)
    page.locator("//input[@id='email']").type(email_address,delay = 100)
    time.sleep(2)
    page.locator("//input[@id='reenter_email']").type(email_address,delay = 100)
    time.sleep(2)
    page.locator("//select[@id='country']").select_option("US")

    time.sleep(2)
    page.locator("//input[@id='i_agree_check']").click()

    time.sleep(2)
    # page.click("//button[@id='createAccountButton']//span[contains(text(),'Continue')]")

    tkr = Tk()
    tkr.title("Captcha Message")
    Label(tkr,text="Solve the captcha! \n Click exit once captcha is solved!").pack()
    mainloop()

    # wait for click
    time.sleep(2)
    page.locator('//*[@id="createAccountButton"]').click()
    
    # wait for the email to be sent
    time.sleep(5)
    # read the email and extract the verification link from it
    while True:
        verification_link = extract_emails_for_verification_link(email_address, password)
        if verification_link is not None:
            break
        else:
            time.sleep(5)

    # send response to the server to verify the account by extracted verification link
    verification_response = requests.get(verification_link)

    if verification_response.status_code == 200:
        custom_username1 = custom_username + random_num(7)
        # Next page after email verification
        page.locator('//*[@id="accountname"]').type(custom_username1,delay = 100)
        time.sleep(2)
        page.locator('//*[@id="password"]').type(custom_password,delay = 100)
        time.sleep(2)
        page.locator('//*[@id="reenter_password"]').type(custom_password,delay = 100)
        time.sleep(5)
        page.locator('//*[@id="createAccountButton"]').click()
        time.sleep(6)
    data_list = [email_address, custom_username1, custom_password]
    with open("SteamAccounts.txt", "a") as f:
        json.dump(data_list, f, indent=4)
        f.write("\n")
    f.close


email_address, password = generate_hotmail_account()

rand_month1 = random.choice(range(1, 12))
rand_day1 = random.choice(range(1, 28))
rand_year1 = random.choice(range(1980, 2003))
rand_month = str(rand_month1)
rand_day = str(rand_day1)
rand_year = str(rand_year1)

create_account()
