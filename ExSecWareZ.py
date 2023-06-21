#!/usr/bin/python3
# Author: Exploit Security Team
# Name: exsecwarez
# Web: exploitsecurity.io
# Git Repo: https://github.com/exploitsecurityio/
# Function: 
# This toolset incorporates an all round utility envisaged to be used by security researchers in the field.
# - UART-Exploiter - Interactive UART passthrough and Baud Scanner used over FTDI (Requires FTDI cable of choice)
# - ExploitToolFinder - Scowers the internet for commonly used software tools

from pyftdi.ftdi import Ftdi
import pyftdi.serialext
from pyftdi import FtdiLogger
from pyftdi.ftdi import Ftdi
from pyftdi.misc import to_bool
import pyftdi.serialext
from pyftdi.serialext import serial_for_url
import sys
import os
import signal
import threading
from time import sleep
from threading import Thread
from threading import Semaphore
from random import random
import time
import subprocess
import openai

global uart_interface
global baud_rate
global clr_cmd
global baudRates
global test_type
global connect_status

def handler(signum, frame):
    return

def console_write(semaphore, uart):
    try:
        with semaphore:
            for buffer in sys.stdin:
                try:
                    uart.write(buffer)
                except IOError as e:
                    return
                except KeyboardInterrupt as kb:
                    Semaphore.release()
                    return
    except KeyboardInterrupt:
        Semaphore.release()
        return
    finally:
        Semaphore.release()
        return
        
def uart_connect(uart):
    baud_rate = get_baud()
    port = pyftdi.serialext.serial_for_url(uart, baudrate=baud_rate, bytesize=8, parity='N', stopbits=1)
    connect_status = port.is_open
    sleep(1)
    try:
        semaphore = Semaphore(1)
        worker = Thread(target=console_write, args=(semaphore, port))
        worker.start()
        print("[Connected to UART]")
        while connect_status:
            data = port.readline()
            print (str(data.decode("ISO-8859-1")), flush=True, end='')
        semaphore.release()
        port.reset_input_buffer()
        port.reset_output_buffer()
        port.cancel_write()
        port.close()
        sys.exit(0)
    except KeyboardInterrupt:
        semaphore.release()
        port.reset_input_buffer()
        port.reset_output_buffer()
        port.cancel_write()
        port.close()
        sys.exit(0)

def baud_scan(uart):
    try:
        baudRates = [300, 600, 1200, 2400, 4800, 9600, 14400, 28800, 36400, 57600, 115200]
        validRates = []
        print("[Estimating Baud Rate]")
        print ("[Power Cycle Device]")
        input("[Enter to begin]")
        for baud in baudRates:
            try:
                port = pyftdi.serialext.serial_for_url(uart, baudrate=baud, bytesize=8, parity='N', stopbits=1, timeout=1)
                connect_status = port.is_open
                sleep (2)
                data = port.read(8)
                print (f"\n[Checking baud {baud}]\n" + ("[Data]: " + str(data.decode("ISO-8859-1"))), flush=True, end='')
            except IOError as e:
                return
            except KeyboardInterrupt as kb:
                return
        print ("\n")
        input("[Enter to continue]")
    except EOFError:
        return
    except KeyboardInterrupt as e:
        return

def get_baud():
    try:
        while True:
            baud = (input("[Baud Rate]: "))
            if baud.isdigit():
                if len(baud) < 10:
                    return int(baud.strip())
                else:
                    print ("[Invalid Option]")
                    sleep(1)
                    return
            else:
                try:
                    return
                except EOFError:
                    return
    except EOFError:
        return
    except KeyboardInterrupt as e:
        return
    
def initialise_uart():
    try:
        device = str(Ftdi.list_devices())
        device_details = device.split(",")
        vid = (device_details[0].strip()[22:])
        pid = (device_details[1].strip())
        bus = (device_details[2].strip())
        address = (device_details[3].strip())
        sn = (device_details[4].strip()[4:-1])
        description = (device_details[6].strip()[:-1])
        interface = (device_details[7].strip()[:-2])
        uart_interface = ("ftdi://ftdi:232:"+sn+"/"+interface)
        return uart_interface
    except IOError:
        print ("[No FTDI devices found]")
        sleep(2)
        banner_uart()
        menu_uart()
        return
    except:
        print("[No FTDI device found]")
        sleep(2)
        banner_uart()
        menu_uart()
        return

def banner_uart():
    if os.name == 'posix':
        clr_cmd = ('clear')
    elif os.name == 'nt':
        clr_cmd = ('cls')
    os.system(clr_cmd)
    print(" _   _   _    ____ _____   _____            _       _ _")            
    print("| | | | / \  |  _ \_   _| | ____|_  ___ __ | | ___ (_) |_ ___ _ __") 
    print("| | | |/ _ \ | |_) || |   |  _| \ \/ / '_ \| |/ _ \| | __/ _ \ '__|")
    print("| |_| / ___ \|  _ < | |   | |___ >  <| |_) | | (_) | | ||  __/ |")   
    print(" \___/_/   \_\_| \_\|_|   |_____/_/\_\ .__/|_|\___/|_|\__\___|_|")   
    print("[by exploitsecurity.io]              |_|\n")                           

def menu_uart(uart):
    try:
        while True:
            banner_uart()
            print("      __  __                  ")
            print("     |  \/  | ___ _ __  _   _ ")
            print("     | |\/| |/ _ \ '_ \| | | |")
            print("     | |  | |  __/ | | | |_| |")
            print("     |_|  |_|\___|_| |_|\__,_|")
            print("+───────────+───────────+─────────+")
            print("|    1. UART Connect              |")
            print("|    2. UART Scan                 |")
            print("|    3. Quit                      |")
            print("+───────────+───────────+─────────+")
            option = (input("[Option]: "))
            if option == '1':
                uart_connect(uart)
                return
            elif option == '2':
                baud_scan(uart)
                return
            elif option == '3':
                return
            else:
                print ("[Invalid Option]")
                sleep(1)
    except KeyboardInterrupt as e:
        print ("\n[Curiosity Drives Our Very Fabric]")
        return
    except ValueError as ve:
        return
    except EOFError:
        return

def uartexploiter():
    signal.signal(signal.SIGTSTP, handler)
    uart_device = initialise_uart()
    menu_uart(uart_device)

def menu_etf():
    try:
        while True:
            banner_etf()
            print("      __  __                  ")
            print("     |  \/  | ___ _ __  _   _ ")
            print("     | |\/| |/ _ \ '_ \| | | |")
            print("     | |  | |  __/ | | | |_| |")
            print("     |_|  |_|\___|_| |_|\__,_|")
            print("+───────────+───────────+─────────+")    
            print("|  1. IoT/Embedded Systems Tools  |")
            print("|  2. Web Application Tools       |")
            print("|  3. Infrastructure Tools        |")
            print("|  4. Mobile Application Tools    |")
            print("|  5. Wireless Tools              |")
            print("|  6. General Tools               |")
            print("|  7. Quit                        |")
            print("+───────────+───────────+─────────+")
            option = (input("[Option]: "))
            if option == '1':
                doTheThing(test_type="iot or embedded system")
            elif option == '2':
                doTheThing(test_type="web application")
            elif option == '3':
                doTheThing(test_type="infrastructure")
            elif option == '4':
                doTheThing(test_type="mobile application")
            elif option == '5':
                doTheThing(test_type="wireless")
            elif option == '6':
                doTheThing(test_type="general")
            elif option == '7':
                return
            else:
                print ("[Invalid Option]")
                sleep(1)
    except KeyboardInterrupt as e:
        print ("\n[Curiosity Drives Our Very Fabric]")
        return
    except ValueError as ve:
        return
    except EOFError:
        return
    
def doTheThing(test_type):
    openai.api_key = "<API KEY>"
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "list websites that reference software tools used for " + test_type + " penetration testing"},
        ],
        temperature=0,
    )
    print("[Here a list of websites that might help you on your quest]\n")
    answer = response['choices'][0]['message']['content']
    print(answer)
    input("[Enter to continue]")

def banner_etf():
    if os.name == 'posix':
        clr_cmd = ('clear')
    elif os.name == 'nt':
        clr_cmd = ('cls')
    os.system(clr_cmd)
    print(" _____            _       _ _  _____           _ _____ _           _")           
    print("| ____|_  ___ __ | | ___ (_) ||_   _|__   ___ | |  ___(_)_ __   __| | ___ _ __") 
    print("|  _| \ \/ / '_ \| |/ _ \| | __|| |/ _ \ / _ \| | |_  | | '_ \ / _` |/ _ \ '__|")
    print("| |___ >  <| |_) | | (_) | | |_ | | (_) | (_) | |  _| | | | | | (_| |  __/ |")   
    print("|_____/_/\_\ .__/|_|\___/|_|\__||_|\___/ \___/|_|_|   |_|_| |_|\__,_|\___|_|")   
    print("           |_|")                                                                 
    print("[by exploitsecurity.io]\n")

def ExploitToolFinder():
    banner_etf()
    menu_etf()

def menu():
    try:
        while True:
            banner()
            print("      __  __                  ")
            print("     |  \/  | ___ _ __  _   _ ")
            print("     | |\/| |/ _ \ '_ \| | | |")
            print("     | |  | |  __/ | | | |_| |")
            print("     |_|  |_|\___|_| |_|\__,_|")
            print("+───────────+───────────+─────────+")
            print("|    1. UART Exploiter            |")
            print("|    2. Exploit Tool Finder       |")
            print("|    3. Quit                      |")
            print("+───────────+───────────+─────────+")
            option = (input("[Option]: "))
            if option == '1':
                uartexploiter()
            elif option == '2':
                ExploitToolFinder()
            elif option == '3':
                print ("\n[Curiosity Drives Our Very Fabric]")
                sys.exit(1)
            else:
                print ("[Invalid Option]")
                sleep(1)
    except KeyboardInterrupt as e:
        print ("\n[Curiosity Drives Our Very Fabric]")
        sys.exit(1)
    except ValueError as ve:
        return
    except EOFError:
        return
    finally:
        sys.exit(1)
    

def banner():
    if os.name == 'posix':
        clr_cmd = ('clear')
    elif os.name == 'nt':
        clr_cmd = ('cls')
    os.system(clr_cmd)
    print(" _____       ____          __        __             _____")
    print("| ____|_  __/ ___|  ___  __\ \      / /_ _ _ __ ___|__  /")
    print("|  _| \ \/ /\___ \ / _ \/ __\ \ /\ / / _` | '__/ _ \ / /") 
    print("| |___ >  <  ___) |  __/ (__ \ V  V / (_| | | |  __// /_") 
    print("|_____/_/\_\|____/ \___|\___| \_/\_/ \__,_|_|  \___/____|")                                                   
    print("[by exploitsecurity.io]\n")

def main():
    banner()
    menu()

if __name__ == '__main__':
    main()
