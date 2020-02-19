import requests

import pandas as pd


class ViewPlans:
    def __init__(self):
        self._url_view_plans = "http://0.0.0.0:8000/get_plans"
    
    def _fetch_plans(self):
        try:
            result = requests.get(self._url_view_plans)
            return result.text
        except Exception as e:
            print("Couldn't fetch plans "+str(e))
            return None

    def view(self):
        plans = self._fetch_plans()
        cols = ['Plan code', 'Plan Name', 'Validity', 'Daily limit', "Price"]
        if plans != []:
            df = pd.DataFrame(eval(plans))
            df = df.iloc[:,:-1]
            df.columns = cols
            print(df.head())
            print("\n\n\n")
        else:
            print("\nNo plans found\n")
        