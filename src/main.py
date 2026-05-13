import sys
import os
import customer_kickoff

customer_list = ["Allied", "Signify", "Locus"]

def menu():
    print("-----Welcome to AXCA passmark----")
    for index, customer in enumerate(customer_list, start=1):
        print(f"          {index}. {customer}")
    print("          Any other number to exit")
    print("---------------------------------")
    selection = None
    while selection is None:
        try:
            user_input = int(input("Please select customer"))
        except ValueError:
            print("Please Enter a number")
        else:
            if user_input < 1 or user_input > len(customer_list):
                selection = 0
            else:
                selection = user_input
    return selection

def main():
    selection = menu()
    if selection == 0:
        sys.exit()
    customer_kickoff.customer_specification(customer_list[selection-1])


if __name__ == '__main__':
    running = True
    while running:
        os.system("cls")
        main()
