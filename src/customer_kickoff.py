
import os
import sys
import subprocess
import re
import time
import json
from pathlib import Path
import shutil


def check_passmark(product_info, model_number, serial_number):
    burnin_report = "X:\\Program Files\\BurnInTest\\BIT_log.log"
    result="PASSED"

    with open(burnin_report, "r", encoding="utf-16") as file:
        lines = file.read().splitlines()

    for line in lines:
        if "FAIL" in line:
            print("FAILURE ->", line.strip())
            result = "FAILED"
            break            

    print(f"{serial_number} {result.lower()} and was saved to passmark directory on server")
    shutil.copy(burnin_report , f"{product_info[model_number][result]}\\{serial_number}.txt")


def compare_files(required_parts):
    local_log = r"X:\Program Files\BurnInTest\TempSysInfo.txt"
    found = True
    if not os.path.exists(local_log):
        print(f"Could not find {local_log}")
        sys.exit()
    with open(local_log, "r", encoding="utf-8", errors="ignore") as log_file:
        log_lines = list(log_file)

    for part in required_parts:
        if not any(part in line for line in log_lines):
            print("Could not find", part)
            found = False

    return found
        
def verify_serial_number(serial_number, reg_ex):
    return re.match(reg_ex, serial_number)

def model_number_exists(config_file):
    return os.path.exists(config_file)

def run_burnin(bitcfg):
    bit = r"X:\Program Files\BurnInTest\bit.exe"

    subprocess.run([bit, "-c", bitcfg , "-r"])

def run_hardware_check():
    bit = r"X:\Program Files\BurnInTest\bit.exe"
    hw_check = r"Y:\Passmark-Menu\src\HardwareCheck\HardWareCheck.bitcfg"

    subprocess.run([bit, "-c", hw_check , "-r"])

def parse_file(config_file):
    localFile = Path(r"X:\log.txt")
    if os.path.exists(localFile):
        subprocess.run(f'del "{localFile}"', shell=True)
    subprocess.run(f'type "{config_file}" >> "{localFile}"', shell=True)
    with localFile.open("r") as file:
        return [line[2:].strip() for line in file]


def customer_specification(customer):
    with open(f"Y:\\Passmark-Menu\\src\\product_info.json" , 'r') as file:
        product_info = json.load(file)

    model_number = input(f"Please enter model number for {customer}: ")
    
    if model_number not in product_info:
        print("Model Number not in JSON file: contact Engineering")
        return
    config_file = product_info[model_number]["CONFIG"]
    if not model_number_exists(config_file):
        print("Please verify model number exists, contact Engineering if having issues")
        input()
        return 
    
    required_part = parse_file(config_file)

    serial_number = input(f"Please enter serial number for {customer}: ")
    if not verify_serial_number(serial_number, product_info[model_number]["RegEX"]):
        print("Please verify serial number is correct, contact Engineering if having issues")
        input()
        return 
    
    is_confirmed = False
    while not is_confirmed:
        y_or_n = input("Would you like to start hardware check(y/n)?: ").strip().lower()
        if y_or_n == 'y':
            run_hardware_check()
            is_confirmed = True
        elif y_or_n == 'n':
            return
        else:
            print("Please type y or n\n")
    
    time.sleep(3) ## sleep for the 3 seconds (Why?)
    if not compare_files(required_part):
        input("Press enter to return to Menu screen")
        return
    print(f"Hardware checked passed running burnin test for {customer} -- {model_number}")
    run_burnin(product_info[model_number]["BITCFG"])
    check_passmark(product_info, model_number, serial_number)
    input()
