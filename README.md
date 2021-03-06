# Volunteer-Student Flask App

### Motivation
This Udacity Capstone project is a Flask app backend built for volunteers in the United States to connect with students in China to teach/learn English, as well as other subjects. The project is inspired by a real project that I worked with CWB Foundation in Feburary and March 2020, during the COVID peak in China. CWB Foundation runs a program every summer to send US volunteers to some of China's most rural areas to teach English. However, the program was suspended in 2020 due to the pandemic. CWB Foundation decided to take the program online and run the volunteering program virtually.

All the volunteers and students registered through Wechat, a Chinese messaging and social media app. Volunteer and student information were then manually collected by program organizers, and stored in Excel sheets. At the time, I wrote a python program to pair volunteers and students by age and interests [(Project Link: Pairing)](https://github.com/wenxingliu/pairing_students). The python program also manages email communication with students and volunteers.

One big challenge I had back then was the quality of data. Since all information was collected from Wechat in free form, many times we ran into typos in emails, or personal informations. At that time, I thought to myself - if we have a web interface to take user inputs, we would have avoided most of the messy data.

This project is the backend of such a web interface.


### Backend

The `./backend` directory contains a Flask server with endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

[View the API Document.md within ./backend for more details on API endpoints.](./backend/API.md)

There are three types of roles: Admin, Volunteer and Student. 
Admin has the following permissions:
```
get:classrooms
get:students
get:volunteers
post:classroom
post:student
post:volunteer
patch:classroom
patch:student
patch:volunteer
delete:classroom
delete:student
delete:volunteer
```
Volunteer has the following permissions:
```
get:classrooms
get:students
get:volunteers
post:classroom
post:volunteer
patch:classroom
patch:volunteer
delete:classroom
delete:volunteer
```
a student role has the following permissions:
```
get:classrooms
get:students
get:volunteers
patch:student
post:student
delete:student
```
Admin have permissions to post, delete or update all any resources.

### Tests


### Setup

1. cd into `backend`, run `pip install -r requirements.txt` to install the dependencies, and then activate the environment by running `source env/bin/activate`.
```
$ cd backend
$ pip install -r requirements.txt
$ source env/bin/activate
```
2. Run `settings.sh` file to export variables `AUTH0_DOMAIN` `AUTH0_CLIENT_ID` and `AUTH0_CLIENT_SECRET`.
```
source settings.sh
```
3. Run `python app.py` to start the backend.
4. Open a browser and go to the link to log in. 
```
https://find-a-volunteer.us.auth0.com/authorize?audience=volunteer&response_type=token&client_id=JPFdgL5PK21ity4fQ2SrEmnujSnUC0it&redirect_uri=http://127.0.0.1:8002/home
```
5. The redirect url will be in the following format. Extract token from the redirect url.
```
http://127.0.0.1:8002/home#access_token=<token>&scope=openid%20profile%20email&expires_in=7200&token_type=Bearer&state=<state>
```
6. Open Postman, import [Postman Collection](./backend/Capstone_Project-volunteer_flask_app.postman_collection.json). Set `admin_token`, `volunteer_token` and `student)token` in project variables.
7. Test APIs in the Postman collection.
