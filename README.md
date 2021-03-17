Instructions
Download
Extract in a folder
Open with visual studio code
Commands:

py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py manage.py runserver
In core /settings.py the stripe is commented out - just put your own details in here (not all of these are connected to the project)

Stripe Payment
PUBLISHABLE_KEY = '' SECRET_KEY = ''

Admin login
http://127.0.0.1:8000/admin
username and password = admin
