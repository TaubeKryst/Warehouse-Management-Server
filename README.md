# WMS - Warehouse Management Server
Django REST implementation for client authentication and warehouse management, e.g. adding, removing or updating product properties. 

Two types of authentication available: bearer authentication and OpenID.

## Installation
To run locally:
1. Create a Python 3.6 virtualenv
2. Install dependencies:
   
    `pip install -r requirements.txt`
3. Apply migrations:

   `./manage.py migrate --run-syncdb`
4. Create a superuser:

   `./manage.py createsuperuser`
5. Finally, run the server:

   `./manage.py runserver`
   
   
