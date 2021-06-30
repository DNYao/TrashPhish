'''
get_proxies() taken from https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/

trash_poster() and id_generator() code modified from https://github.com/ginward/FloodPhishingSite/blob/master/goodbye.py
'''

import requests
from requests.exceptions import HTTPError
import os
import sys
import string
import json
import random

from threading import Thread
from random import randint
from random_username.generate import generate_username
from lxml.html import fromstring
from itertools import cycle
from utils import passwords, names, header_info
from time import sleep

# Phishing URL here
url = ''
# If you need to click on a link to get to the actual fake login
referrer = None

#Number of cycles for TrashPhish to run against the phishing site
num = 5

def trash_poster():
    """
    Spits out two flavors of junk to make detection and differentation from legit account info a tiny bit harder
    """

    proxydict = [{'http':'213.137.240.243:81', 'http':'103.103.3.6:8080'},
                {'http':'157.230.103.189:43844', 'http':'187.19.207.195:3128'},
                {'http':'45.160.224.97:8080','http':'141.94.106.133:8080'},
                {'http':'121.244.213.162:8080','http':'34.254.255.177:4001'}
                ]

    print("Posting trash")
    sleep(randint(1,4))
    while True:
        #If the site takes an email address, otherwise remove the choice(domains) from user generation
        domains = ["@yahoo.com","@hotmail.com","@gmail.com","@aol.com","@mail.com"]
        variable = randint(0,20)
        password = passwords[randint(0,10000)]

        if variable % 2 == 0:
            username = str(names[randint(0,100)] + str(randint(0,5000)))
            if len(password) < 6:
                password += str(randint(0,100))

        elif variable % 3 == 0:
            username = generate_username(1)[0].lower()
            if len(password) < 6:
                password += str(randint(0,100))

        else:
            username = str(names[randint(0,100)].lower() + str(names[randint(0,100)].lower()) + str(randint(0,5000)))
            if len(password) < 6:
                password += str(randint(0,100))

        for _ in range(1, 11):
            #Fill in user form and password form with appropriate form data
            try:
                # comment out if no referrer
                r = requests.get(referrer)
                sleep(randint(1,4))

                # Change 'username' and 'password' depending on html
                r = requests.get(url)
                requests.post(url, headers = header_info(referrer), proxies=random.choice(proxydict), allow_redirects=False, data={
                    'username': username,
                    'password': password
                })
            except HTTPError:
                print(HTTPError)
                break

        print('sending username %s and password %s' % (username, password))

if __name__ == "__main__":
    for k in range(0, num):
        thread = Thread(target = trash_poster)
        thread.start()
        print('Launched thread '+str(k))
