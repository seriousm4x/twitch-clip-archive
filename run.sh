#!/usr/bin/env bash

# Wait for postgresql
if [ "$USE_POSTGRESQL" == "True" ]; then
    /usr/bin/env bash ./wait-for-it.sh db:"${DB_PORT}"
fi

# DB migration
python -u manage.py makemigrations
python -u manage.py migrate

# Create superuser if none exists
python -u manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPERUSER_USER', password='$DJANGO_SUPERUSER_PASSWORD') if not User.objects.filter(username='$DJANGO_SUPERUSER_USER').exists() else print('Django user exists')"

# Create twitch settings if none exists
python -u manage.py shell -c "from clips.models import TwitchSettings; TwitchSettings(broadcaster_name='$TWITCH_CHANNEL', client_id='$TWITCH_CLIENT_ID', client_secret='$TWITCH_CLIENT_SECRET').save() if TwitchSettings.objects.filter().count() == 0 else print('Twitch settings exists')"

# Run server
gunicorn django-twitch-archive.wsgi:application --bind 0.0.0.0:8000 --workers $(($(nproc) + 1)) &
env_hosts=("${DJANGO_ALLOWED_HOSTS//,/ }")

printf "\n\n"
printf "Listening on:\n"
for address in "${env_hosts[@]}"; do 
    echo "${address}":"${WEB_PORT}"
done
printf "\n\n"

# Download from twitch
while :; do
    python -u manage.py updateDB && \
    python -u manage.py download && \
    python -u manage.py collectstatic --noinput
    if [ -n "$DB_BACKUP_DIR" ]; then
        python -u manage.py dumpdata > "${DB_BACKUP_DIR}dump_$(date +%Y-%m-%d"_"%H_%M_%S).json"
    fi
    sleep $(( 6 * 60 * 60 )) # 6 hours
done
