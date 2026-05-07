"""
This will suffice as the script to point to specific customer
"""
import os
import sys
import subprocess
import re
import time
from pathlib import Path
from collections import defaultdict

## functions to be used again  

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

## CUSTOMERS ##

# signy kickoff
def signify():
    ## Verify model number exists
    modelNum = input("Please enter model number for Signify: ")
    configFile = (f"Y:\\Signify\\configs\\{modelNum}.cfg")
    if not model_number_exists( configFile ):
        print("Please verify model number exists, contact Engineering if having issues")
        input()
        return ## if model number does not exists put back at menu selection
    
    # put cfg file into a hashmap
    requiredPart = parse_file( configFile )

    # verify the serial number regEx
    serialNum = input("Please enter serial number for Signify: ")
    if not verify_serial_number( serialNum  , r"^ATS\d{8}" ):
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
    
    ##if everything is good kick off burnin test!
    print("Hardware checked passed running burnin test for Signify")
    run_burnin(r"Y:\Signify\iPLAYER4.bitcfg")

    


    