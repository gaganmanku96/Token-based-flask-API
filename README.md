# Token authenticated Flask API

This project aims to cover some of the concepts required to build an API that works using Token.
Everytime a user signs up a token is generated depending on the type of user.

### Components
- MainApp - resposible for all database operations like creating user, creating plans.
- ML_app - machine learning models run in this component(docker container). They can only be accessed by Token generated during sign up.
- Migration - Every night a migration job is done to store the requests made by a token on that day.
- ChatBot - Telegram bot is used to query various things like how many users sign up on a day.

### Database used
- Postgres - It is the main database that contains all the information about user, plans, logs.
- Redis - It is used as a caching database to store tokens along with there daily limit.

### Plans Structure
```
{
    "plan_id":{
        "plan_code": str,
        "plan_name": str,
        "validity": str,
        "daily_limit": int,
        "price": str,
        "description": str
}
```
#### Plans are inserted into table when the container starts. To add new plans change plan_code and run "docker-compose up --build".


### How to begin
1. #### Start by cloning the repo
```
$ git clone git@github.com:gaganmanku96/Token-based-flask-API.git
$ cd Token-based-flask-API
```
2. #### Use docker-compose
```
$ docker-compose up --build
```
#### On successful completion you'll see 5 docker containers running (2 for database and 3 for apps).
3. #### Signup
```
$ cd signup
$ pip install -r requirements.txt
$ python3 signup.py
```
4. #### Post signup
After signup you'll get a token. This token will be used to the API.