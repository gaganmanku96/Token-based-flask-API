import requests
import json
from datetime import datetime
import os

from create_user import CreateUser
from view_plans import ViewPlans


def main():
    while True:
        choice = input("Please select what do you want to do\n\
                        1. Sign-up\n\
                        2. View plans\n\
                        3. View usage status\n\
                        4. Exit\n")
        if choice.isdigit() is not True:
            raise ValueError("Selected choice must be an integer")
        choice = int(choice)
        if choice == 1:
            new_user = CreateUser()
            print(new_user.create())
        elif choice == 2:
            plans = ViewPlans()
            plans.view()
        elif choice == 3:
            pass
        elif choice == 4:
            print("\nThank you\n")
            exit(1)
        else:
            raise ValueError("Option not valid")


if __name__ == '__main__':
    main()