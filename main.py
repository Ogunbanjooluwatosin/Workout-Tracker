# -----------------------------imports-----------------------------
import datetime

import json
import os
import requests
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
app_id = os.environ["APP_ID"]
app_key = os.environ["APP_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
header = {
    "x-app-id": app_id,
    "x-app-key": app_key,

}
params = {
    "query": input("Tell me which exercises you did: "),
    "gender": "male",
    "weight_kg": 72.5,
    "height_cm": 180.64,
    "age": 18
}
response = requests.post(exercise_endpoint, headers=header, json=params)
data = response.json()
with open("nutritionix.json", mode="w") as file:
    json.dump(data, file, indent=15)

# -----------------------------date and time-----------------------------

now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year
today = datetime.datetime(day=day, month=month, year=year)

today_date = today.strftime("%x")
time = now.time()
new_time = time.strftime("%X")
# ---------------------------------------Sheety---------------------------
sheety_endpoint = "https://api.sheety.co/4a8ad4b912bdd4012c8e77babc3e6c2f/workoutTracker/workouts"
sheety_header = {
    "Content-Type": "application/json",
    "Authorization": os.environ["basic_auth"]
}
for exercise in data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": new_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheety_response = requests.post(sheety_endpoint,
                                    json=sheet_inputs,
                                    headers=header,
                                    auth=(
                                        username,
                                        password)
                                    )
    print(sheety_response.text)
