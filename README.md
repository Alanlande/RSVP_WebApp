# RSVP_Django_Web_App by De Lan

## Make sure that you download into a linux environment and have installed python3 and django packages

## Usage:
cd docker-deploy

sudo docker-compose up

### If you met ERROR like: 

#### PermissionError: [Errno 13] Permission denied: '/code/RSVP/migrations/0006_auto_20180223_1640.py’

## TRY:
From your web-app dir  (assuming that your app is called RSVP, if not replace RSVP below)
 
chmod o+w RSVP/migrations

cd ..
## now you are in the directory with docker-compose.yml
sudo docker-compose run web python3 manage.py makemigrations

## Then:
cd docker-deploy

sudo docker-compose up
