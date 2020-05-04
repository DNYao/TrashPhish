import requests
import os
import sys
import string
import json
from threading import Thread
from random import randint, choice, seed
from random_username.generate import generate_username
from lxml.html import fromstring

url = '#URL HERE#'

chars = string.ascii_letters + string.digits + '!@#$%^&*()'
seed = (os.urandom(1024))
names = json.loads(open('names.json').read())
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

def trash_poster():
    """
    Spits out two flavors of junk to make detection and differentation from legit account info a tiny bit harder. "User" and "password" form sections should be filled in with the appropriate form data from the html of the phishing page.
    """

    while True:
        if randint(0,2) % 2 == 0:
            for name in names:

                name_extra = ''.join(choice(string.digits))
                username = name.lower() + name_extra
                password = id_generator(randint(6,21))
        else:
            username = generate_username(1)[0]
            password = id_generator(randint(6,21))

        requests.post(url, proxies = get_proxies(), header = headers, allow_redirects=False, data={
            '#USER FORM': username,
            '#PASSWORD FORM': password
        })

        print('sending username %s and password %s' % (username, password))

def id_generator(size=21, chars=string.ascii_uppercase + string.digits):
	return ''.join(choice(chars) for _ in range(size))

if __name__ == "__main__":
    for k in range(0, num):
        thread = Thread(target = trash_poser)
        thread.start()
        print('Launched thread '+str(k))
