# RSVP_WebApp

## Usage:
cd erss-hwk1-dl261-ys205/docker-deploy
sudo docker-compose up

## If you met ERROR like: 
PermissionError: [Errno 13] Permission denied: '/code/RSVP/migrations/0006_auto_20180223_1640.py’

## TRY:
From your web-app dir  (assuming that your app is called RSVP, if not replace RSVP below)
 
chmod o+w RSVP/migrations
cd ..
// now you are in the directory with docker-compose.yml
sudo docker-compose run web python3 manage.py makemigrations


## Then:
cd erss-hwk1-dl261-ys205/docker-deploy
sudo docker-compose up
