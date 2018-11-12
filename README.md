# RSVP Web App by De Lan

![alt text](https://github.com/Alanlande/RSVP_WebApp/blob/master/sample2_pending_page.png "The main pending page")


## Description:

This is a toy proxy server software built in Django framework that helps people manage their RSVP events. People can create events and invite others as guests, vendors and share owner\
s with different level of privileges.

- Play with it by visiting: YOURSERVER:80000 after you launch it on your onw server.

## Usage:
cd erss-hwk1-dl261-ys205/docker-deploy

sudo docker-compose up

## If you met ERROR like: PermissionError: [Errno 13] Permission denied: '/code/RSVP/migrations/0006_auto_20180223_1640.py’

## TRY:
From your web-app dir  (assuming that your app is called RSVP, if not replace RSVP below)

chmod o+w RSVP/migrations

cd ..
## now you are in the directory with docker-compose.yml
sudo docker-compose run web python3 manage.py makemigrations


## Then:
cd erss-hwk1-dl261-ys205/docker-deploy
sudo docker-compose up

## More examples:
![alt text](https://github.com/Alanlande/RSVP_WebApp/blob/master/sample1_owner_page.png "The main owner page")

