# HackTech2019
Project for hackathon

1. install pipenv 
2. start pipenv from Pipfile 
3. Set the flask environment variable
Note: do not enable development mode in 
production environment  

Linux: 

```
export FLASK_APP=main.py
export FLASK_ENV=development
flask run 
```

Windows: 

```
set FLASK_APP=main.py
set FLASK_ENV=development
flask run 
```

4. Website is at 127.0.0.1 

5. To SSH into REMOTE: 
```
ssh hackathon@198.199.94.88
```
password: mudd 

NGINX configuration is in etc/nginx/sites-available (or sites-enabled), name: hacktech

```
sudo service nginx restart
```

Project is stored in /home/hacktech (contains .sock that NGINX routes to).
