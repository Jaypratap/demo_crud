# demo_crud
This is the assignments for task-1 and task-3
There are two urls.py file

one in CRUD and one in otp

API End point

for generate otp: method=['POST']
http://127.0.0.1:8000/otp/generate/
for verify otp: method=['POST']
http://127.0.0.1:8000/otp/verify/
for register: method=['POST']
http://127.0.0.1:8000/otp/register/
{
    "first_name": "jay",
    "last_name": "pratap",
    "email": "abcd@gmail.com",
    "userType": 1,
    "userRole": 1,
    "password1": "demoproject1",
    "password2": "demoproject1"

}

for register final: method=['PUT']
http://127.0.0.1:8000/registerfinal

for update usertype
http://127.0.0.1:8000/updatetype/


Note:
Please change the db password and smptp password in settings.py
