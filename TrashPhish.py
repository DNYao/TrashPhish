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
from threading import Thread
from random import randint, choice, seed
from random_username.generate import generate_username
from lxml.html import fromstring
from itertools import cycle

url = 'http://www.clgthh.org'

chars = string.ascii_letters + string.digits + '!@#$%^&*()'
seed = (os.urandom(1024))
names = json.loads(open('names.json').read())

#Number of cycles for TrashPhish to run against the phishing site
num = int (sys.argv[1]) 

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36", 
    "Accept-Encoding":"gzip, deflate, br", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
    }

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

proxies = get_proxies()
proxy_pool = cycle(proxies)

def trash_poster():
    """
    Spits out two flavors of junk to make detection and differentation from legit account info a tiny bit harder
    """
    #length of password
    size = 21

    while True:
        #If the site takes an email address, otherwise remove the choice(domains) from user generation
        domains = ["@yahoo.com","@hotmail.com","@gmail.com","@aol.com","@mail.com"]

        if randint(0,2) % 2 == 0:
            for name in names:
                name_extra = ''.join(choice(string.digits))
                username = name.lower() + name_extra + choice(domains)
                password = id_generator(chars, size)
        else:
            username = generate_username(1)[0] + choice(domains)
            password = id_generator(chars, size)

        for _ in range(1, 11):
            #Fill in user form and password form with appropriate form data
            try:
                proxy = next(proxy_pool)
            except:
                print("Connection error. Skipping proxy.")
            try:
                r = requests.get(url)
                requests.post(url, proxies = {"http": proxy, "https": proxy}, headers = headers, allow_redirects=False, data={
                    '#USER FORM': username,
                    '#PASSWORD FORM': password
                })
            except HTTPError:
                print(HTTPError)
                break

        print('sending username %s and password %s' % (username, password))

def id_generator(chars, size):
	return ''.join(choice(chars) for i in range(size))

if __name__ == "__main__":
    for k in range(0, num):
        thread = Thread(target = trash_poster)
        thread.start()
        print('Launched thread '+str(k))
