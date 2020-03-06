import requests
import json
from datetime import datetime


class CreateUser:
    def __init__(self):
        self._url_verify_phone_number = "http://0.0.0.0:8000/check_phone_number/"
        self._url_create_user = "http://0.0.0.0:8000/create_user"
        self.success_msg = '''
    Thank you for using our service\n\
    We hope you have a great time with it\n\
    Here is your token:
                           '''

    def _check_phone_number(self, phone_number):
        result = requests.get(self._url_verify_phone_number+str(phone_number))
        if result.status_code == 200:
            return True
        else:
            return False

    def _get_input(self, text, dtype, input_value=None):
        while True:
            try:
                temp = dtype(input(text))
                if input_value == 'ph':
                    if self._check_phone_number(temp):
                        return temp
                    else:
                        print("Phone number already exits please try again\n")
                else:
                    return temp
            except Exception:
                raise TypeError("Please enter "+str(dtype)+" values only")
            
    def _get_phone_number(self):
        text = "Please enter phone number: "
        dtype = int
        result = self._get_input(text, dtype, input_value='ph')
        return result

    def _get_name(self):
        text = "Please enter name: "
        dtype = str
        result = self._get_input(text, dtype)
        return result

    def _get_plan_code(self):
        text = "Please enter code of the plan: "
        dtype = str
        result = self._get_input(text, dtype)
        return result

    def _get_start_date(self):
        return str(datetime.now().strftime("%Y-%m-%d"))

    def _create_user(self, phone_number, name, plan_code, start_date):
        data = {"phone_number": phone_number,
                "name": name,
                "plan_id": plan_code,
                "start_date": start_date}
        try:
            result = requests.post(self._url_create_user,
                                   json.dumps(data,
                                              indent=4,
                                              sort_keys=True,
                                              default=str))
            return eval(result.text)
        except Exception as e:
            print("Error while saving data to DB "+str(e))

    def create(self):
        phone_number = self._get_phone_number()
        name = self._get_name()
        plan_code = self._get_plan_code()
        start_date = self._get_start_date()
        result = self._create_user(phone_number, name, plan_code, start_date)
        if result['token'] != "":
            print(self.success_msg+result['token'])
            temp = input("The program will now return to main screen.\nTo quit press q ")
            if temp == 'q':
                exit(0)
        else:
            return "Something went wrong while generating token"
