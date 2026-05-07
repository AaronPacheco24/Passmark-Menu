"""
This will be the main file to kick off passmark files for AXCA
Rev 1.00
By Hayden Fortunata
"""

## Libraries
import sys
import os
import customer_kickoff

## Functions
def menu():
    # menu screen for passmark
    print("-----Welcome to AXCA passmark----\
          \n1. Allied\
          \n2. Signify\
          \n99. Exit"\
          "\n---------------------------------")
    menuChoice = int(input("Please select a customer from above: "))
    match menuChoice:
        case 1:
            print("Allied")
        case 2:
            customer_kickoff.signify()
        case 99:
            sys.exit()


if __name__ == '__main__':
    while True:
        os.system("cls")
        menu()