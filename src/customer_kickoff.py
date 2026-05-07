"""
This will suffice as the script to point to specific customer
"""
import os
import sys
import subprocess
import re
import time
import json
from pathlib import Path
import shutil

## functions to be used again  

def check_passmark(product_info , modelNum , serialNum ):
    ## basic burnin report
    burnin_report = "X:\\Program Files\\BurnInTest\\BIT_log.log"
    unit_passed = True
    ## see if fail exists
    with open(burnin_report, "r", encoding="utf-16") as file:
        lines = file.read().splitlines()
    for line in lines:
        if "FAIL" in line:
            print("FAILURE-> " , line)
            unit_passed = False
            
    ## if no failures put in pass directory
    if unit_passed:
        print(f"{serialNum} passed and was saved to passmark directory on server")
        shutil.copy(burnin_report , f"{product_info[modelNum]["PASSED"]}\\{serialNum}.txt")
    else:
        print(f"{serialNum} failed and was saved to passmark directory on server")
        shutil.copy(burnin_report , f"{product_info[modelNum]["FAILED"]}\\{serialNum}.txt")

def compare_files( requiredParts ):
    localLog = r"X:\Program Files\BurnInTest\TempSysInfo.txt"
    found = True
    # Added encoding="utf-16" and kept errors="ignore" for safety
    if not os.path.exists(localLog):
        print(f"Could not find {localLog}")
        sys.exit()
    with open(localLog, "r", encoding="utf-8", errors="ignore") as f:
        log_lines = list(f)

    for part in requiredParts:
        if not any(part in line for line in log_lines):
            print("Could not find", part)
            found = False

    return found
        
## verify the serial number
def verify_serial_number( serialNum , regEx ):
    if re.match( regEx , serialNum ):
        return True
    return False

## check if model exists
def model_number_exists( configFile ):
    ## Verify config file exists
    if not os.path.exists( configFile ):
        return False

    return True

def run_burnin( bitcfg ):
    bit = r"X:\Program Files\BurnInTest\bit.exe"

    subprocess.run([bit, "-c", bitcfg , "-r"])

def run_hardware_check():
    bit = r"X:\Program Files\BurnInTest\bit.exe"
    hardwareCheck = r"Y:\Passmark-Menu\src\HardwareCheck\HardWareCheck.bitcfg"

    subprocess.run([bit, "-c", hardwareCheck , "-r"])

## Split each line so I can get the first character to compare to 
## Bit log later on
def parse_file(configFile):
    localFile = Path(r"X:\log.txt")
    if os.path.exists(localFile):
        subprocess.run(f'del "{localFile}"', shell=True)
    subprocess.run(f'type "{configFile}" >> "{localFile}"', shell=True)
    with localFile.open("r") as file:
        return [line[2:].strip() for line in file]


# Customer kickoff specification
def customer_specification( customer ):
    ## open JSON file for future use
    with open(f"Y:\\Passmark-Menu\\src\\product_info.json" , 'r') as file:
        product_info = json.load(file)
    ## Verify model number exists
    modelNum = input(f"Please enter model number for {customer}: ")
    if not modelNum in product_info:
        ## if model number does not exist in JSON file
        print("Model Number not in JSON file: contact Engineering")
        return
    configFile = (product_info[modelNum]["CONFIG"])
    if not model_number_exists( configFile ):
        print("Please verify model number exists, contact Engineering if having issues")
        input()
        return ## if model number does not exists put back at menu selection
    
    # put cfg file into a hashmap
    requiredPart = parse_file( configFile )

    # verify the serial number regEx
    serialNum = input(f"Please enter serial number for {customer}: ")
    if not verify_serial_number( serialNum  , product_info[modelNum]["RegEX"] ):
        print("Please verify serial number is correct, contact Engineering if having issues")
        input()
        return ## if model number does not exists put back at menu selection
    
    ## Prompt user to start hardware test, don't let them out of loop
    ## until they confirmed there selection
    while True:
        y_or_n = input("Would you like to start hardware check(y/n)?: ")
        if y_or_n.lower() == 'y':
            run_hardware_check()
            break
        elif y_or_n.lower() == 'n':
            return
        else:
            print("Please type y or n\n")
    
    ## if we made it here user selected yes on hardware check
    time.sleep(3) ## sleep for the 3 seconds
    if not compare_files( requiredPart ):
        input("Press enter to return to Menu screen")
        return
    else:
        #if everything is good kick off burnin test!
        print(f"Hardware checked passed running burnin test for {customer} -- {modelNum}")
        run_burnin(product_info[modelNum]["BITCFG"])
        check_passmark(product_info , modelNum  , serialNum )
        input()


    


    