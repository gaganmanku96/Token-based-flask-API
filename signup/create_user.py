import requests
import json
from datetime import datetime


class CreateUser:
    def __init__(self):
        self.__url_verify_phone_number = "http://0.0.0.0:8000/check_phone_number/"
        self.__url_create_user = "http://0.0.0.0:8000/create_user"
        self.success_msg = '''
    Thank you for using our service\n\
    We hope you have a great time with it\n\
    Here is your token:
                           '''

    def __check_phone_number(self, phone_number):
        result = requests.get(self.__url_verify_phone_number+str(phone_number))
        if result.status_code == 200:
            return True
        else:
            return False

    def __get_input(self, text, dtype, input_value=None):
        while True:
            try:
                temp = dtype(input(text))
                if input_value == 'ph':
                    if self.__check_phone_number(temp):
                        return temp
                    else:
                        print("Phone number already exits please try again\n")
                else:
                    return temp
            except Exception:
                raise TypeError("Please enter"+str(dtype)+"values only")
            
    def __get_phone_number(self):
        text = "Please enter phone number: "
        dtype = int
        result = self.__get_input(text, dtype, input_value='ph')
        return result

    def __get_name(self):
        text = "Please enter name: "
        dtype = str
        result = self.__get_input(text, dtype)
        return result

    def __get_plan_code(self):
        text = "Please enter code of the plan: "
        dtype = str
        result = self.__get_input(text, dtype)
        return result

    def __get_start_date(self):
        return str(datetime.now().strftime("%Y-%m-%d"))

    def __create_user(self, phone_number, name, plan_code, start_date):
        data = {"phone_number": phone_number,
                "name": name,
                "plan_code": plan_code,
                "start_date": start_date}
        try:
            result = requests.post(self.__url_create_user,
                                   json.dumps(data,
                                              indent=4,
                                              sort_keys=True,
                                              default=str))
            return eval(result.text)
        except Exception as e:
            print("Error while saving data to DB "+str(e))

    def create(self):
        phone_number = self.__get_phone_number()
        name = self.__get_name()
        plan_code = self.__get_plan_code()
        start_date = self.__get_start_date()
        result = self.__create_user(phone_number, name, plan_code, start_date)
        if result['token'] != "":
            print(self.success_msg+result['token'])
            temp = input("The program will now return to main screen.\nTo quit press q ")
            if temp == 'q':
                exit(0)
        else:
            return "Something went wrong while generating token"
