# #!/bin/bash

# # SSH into the EC2 instance and execute deployment steps
# sudo chmod 400 /Users/apple/Downloads/commdem_warriors_key_pair.pem
# ssh -i '/Users/apple/Downloads/commdem_warriors_key_pair.pem' ubuntu@3.108.56.217 << EOF
#   cd /home/ubuntu/commdem_warriors_django
#   git pull origin master
#   source env/bin/activate
#   pip install -r requirements.txt
#   python3 manage.py makemigrations
#   python3 manage.py migrate
#   python3 manage.py collectstatic
#   sudo systemctl restart gunicorn.service
# EOF

#!/bin/bash

# Navigate to the project directory on your EC2 instance
cd /home/ubuntu/commdem_warriors_django

# Pull the latest code from the main branch
git pull origin master

# Activate the virtual environment
source /home/ubuntu/commdem_warriors_django/env/bin/activate

# Install/update dependencies
pip install -r requirements.txt

python manage.py makemigrations
# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Gunicorn or your web server
# sudo systemctl restart gunicorn.service

python manage.py runserver 0.0.0.0:8000 &

sudo systemctl restart nginx
