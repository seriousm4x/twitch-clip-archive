![images/logo.svg](images/logo.svg)
# Django-Twitch-Archive

This project creates a complete off side backup of the clips of a Twitch streamer. Top clips on the start page per week/month/ever, search function, sorting and statistics. [A live demo can be seen here](https://clips.itssoley.de/).

# Screenshots

<details>
<summary>Show me</summary>
<br>

Font page
![images/screenshot1.png](images/screenshot1.png)

Single clip
![images/screenshot2.png](images/screenshot2.png)

Search
![images/screenshot3.png](images/screenshot3.png)

Statistics
![images/screenshot4.png](images/screenshot4.png)
</details>

# Installation

```
git clone https://github.com/seriousm4x/django-twitch-archive.git
cd django-twitch-archive
```

Copy [TEMPLATE.env](TEMPLATE.env) to '.env' and edit it with your variables.

Important note if you already have a running instance: Since the project moved to docker, the database moved from sqlite to postgresql. If you want to keep your old database, export it with `python manage.py dumpdata > datadump.json`. I will do the rest for you.

```
docker-compose up
```

Congrats, we are up and running for development or private use. Open up [http://localhost:8000](http://localhost:8000). If you want to publish your archive, go on reading.

# Going for production

If you deploy for production, you shouldn't use the default django key in your .env file. Go ahead and generate a new one.

```
docker exec -it dta-web python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

Edit and paste the generated key in your .env file under "SECRET_KEY".

Also set DEBUG=False and enter your domain under ALLOWED_HOSTS.

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

# Todo

* Dark/Light toggle
* Maybe change to a "youtube-like" grid without cards and horizontal sliders?