
# Django-Twitch-Archive

This project creates a complete off side backup of the clips of a Twitch streamer. Top clips on the start page per week/month/ever, search function, sorting and statistics. [A live demo can be seen here](https://clips.itssoley.de/).

# Screenshots

### Font page
![images/screenshot1.png](images/screenshot1.png)

### Single clip
![images/screenshot2.png](images/screenshot2.png)

### Search
![images/screenshot3.png](images/screenshot3.png)

### Statistics
![images/screenshot4.png](images/screenshot4.png)

# Installation process

## 1. Clone repo and cd into it

```
git clone https://github.com/seriousm4x/django-twitch-archive.git
cd django-twitch-archive
```

## 2. Run setup script

This script will setup your python venv, generate a .env file and setup the django database.

```
./setup.sh
```

After that, load your python venv to use django

```
source .venv/bin/activate
```

## 3. Add clips to database

```
python manage.py updateDB
```

This will search for all clips from the streamer. Not just Twitch's limit of 1000 clips but all clips available. Python will search for clips by week until the channel creation date is reached. This might take a while, since it's using the twitch api.

By now you can see the website at [http://localhost:8000/](http://localhost:8000/) when you run the server. But there are no clips or images yet. Just metadata.

## 4. Download clips and thumbnails

```
python manage.py download
```

This will download all data available in our database to the MEDIA_ROOT path.

## 5. Run the server

```
python manage.py runserver
```

Congrats, we are up and running for development or private use. If you want to publish your archive, go on reading.

# Going for production

If you deploy for production, you shouldn't use the default django key in your .env file. Go ahead and generate a new one.

```
python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

Edit and paste the generated key in your .env file under "SECRET_KEY".

Also set DEBUG=False and enter your domain under ALLOWED_HOSTS.

Run `python manage.py collectstatic` to copy the static files to your webroot.

Next, setup your reverse proxy to forward everything to django except our STATIC_ROOT and MEDIA_ROOT files.

## Caddy Server config

```
yourdomain.com {
    root * /var/www/
    @notStatic {
        not path /static/* /media/*
    }
    reverse_proxy @notStatic localhost:8000
    file_server
    encode gzip
}
```

## Run it as a system service

I attached a file [django-twitch-archive.service](django-twitch-archive.service). Copy it to `/etc/systemd/system/django-twitch-archive.service` and modify the user, group and paths.

Next, run 

```
sudo systemctl daemon-reload
sudo systemctl enable --now django-twitch-archive.service
```

## Automatically update database and download clips

I've created a cronjob which does this automatically every hour.

```
0 */6 * * * /bin/bash /home/max/git/django-twitch-archive/crontab.sh 2>&1
```

# Todo

* Docker container
* Dark/Light toggle
* Maybe change to a "youtube-like" grid without cards and horizontal sliders?