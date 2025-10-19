
##Create Virtual environment

python3 -m venv venv
source venv/bin/activate

#Install Django
pip install django

#Execute migrations
python3 manage.py migrate

#Execute server
python3 manage.py runserver
