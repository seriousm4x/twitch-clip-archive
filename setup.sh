#!/bin/bash

printf "\n\x1b[35mDjango-Twitch-Archive Setup\x1b[0m\n\n"

# check for python virtual env
if [ -f ".venv/bin/python3" ]; then
    python_venv=".venv/bin/python3"
elif [ -f ".venv/Scripts/python3" ]; then
    python_venv=".venv/Scripts/python3"
else
    printf "\x1b[35mSetting up python virtual environment...\x1b[0m\n"
    /usr/bin/env python3 -m venv .venv
    if [ -f ".venv/bin/python3" ]; then
        python_venv=".venv/bin/python3"
    elif [ -f ".venv/Scripts/python3" ]; then
        python_venv=".venv/Scripts/python3"
    fi
fi

# install pip packages in .venv
printf "\x1b[35mInstalling/Updating pip packages\x1b[0m\n"
$python_venv -m pip install --upgrade -r requirements.txt

# check for .env file
if [ ! -f ".env" ]; then
    printf "\x1b[35mSetting up your .env file\x1b[0m\n"

    # django key
    read -rp "Enter a django SECRET_KEY [secret]: " input_key
    case $input_key in
        "")
            SECRET_KEY=secret
            echo SECRET_KEY="$SECRET_KEY"
            ;;
        *)
            SECRET_KEY=$input_key
            echo SECRET_KEY="$SECRET_KEY"
            ;;
    esac

    # debug
    while true; do
        read -rp "Run django in debug mode? [Y/n]: " input_debug
        case $input_debug in
            Y/y)
                DEBUG=True
                echo DEBUG=$DEBUG
                break
                ;;
            N/n)
                DEBUG=False
                echo DEBUG=$DEBUG
                break
                ;;
            "")
                DEBUG=True
                echo DEBUG=$DEBUG
                break
                ;;
            *)
                echo Please answer y/n
                ;;
        esac
    done

    # django allowed hosts
    read -rp "Enter your ALLOWED_HOSTS. You can add multiple by separating with ',' [*]: " input_hosts
    case $input_hosts in
        "")
            ALLOWED_HOSTS="*"
            echo ALLOWED_HOSTS=$ALLOWED_HOSTS
            ;;
        *)
            ALLOWED_HOSTS=$input_hosts
            echo ALLOWED_HOSTS="$ALLOWED_HOSTS"
            ;;
    esac

    # django language
    read -rp "Enter your language code [en]: " input_lang
    case $input_lang in
        "")
            LANGUAGE_CODE=en
            echo LANGUAGE_CODE=$LANGUAGE_CODE
            ;;
        *)
            LANGUAGE_CODE=$input_lang
            echo LANGUAGE_CODE="$LANGUAGE_CODE"
            ;;
    esac

    # django timezone
    read -rp "Enter your timezone [UTC]: " input_tz
    case $input_tz in
        "")
            TIME_ZONE=UTC
            echo TIME_ZONE=$TIME_ZONE
            ;;
        *)
            TIME_ZONE=$input_tz
            echo TIME_ZONE="$TIME_ZONE"
            ;;
    esac

    # static root
    read -rp "Enter your path for static root [/var/www/static]: " input_static
    case $input_static in
        "")
            STATIC_ROOT="/var/www/static"
            echo STATIC_ROOT=$STATIC_ROOT
            ;;
        *)
            STATIC_ROOT=$input_static
            echo STATIC_ROOT="$STATIC_ROOT"
            ;;
    esac

    # media root
    read -rp "Enter your path for media root [/var/www/media]: " input_media
    case $input_media in
        "")
            MEDIA_ROOT="/var/www/media"
            echo MEDIA_ROOT=$MEDIA_ROOT
            ;;
        *)
            MEDIA_ROOT=$input_media
            echo MEDIA_ROOT="$MEDIA_ROOT"
            ;;
    esac

    # write to file
    {
        echo "SECRET_KEY=$SECRET_KEY"
        echo "DEBUG=$DEBUG"
        echo "ALLOWED_HOSTS=$ALLOWED_HOSTS"
        echo "LANGUAGE_CODE=$LANGUAGE_CODE"
        echo "TIME_ZONE=$TIME_ZONE"
        echo "STATIC_ROOT=\"$STATIC_ROOT\""
        echo "MEDIA_ROOT=\"$MEDIA_ROOT\""
    } >> ".env"

else
    printf "\x1b[35m.env exists\x1b[0m\n"
fi

# check for database
if [ ! -f "db.sqlite3" ]; then
    printf "\x1b[35mSetting up Database\x1b[0m\n"
    $python_venv manage.py migrate
    printf "\x1b[35mSetting up django superuser\x1b[0m\n"
    $python_venv manage.py createsuperuser
    printf "\x1b[35mSetting up twitch channel\x1b[0m\n"

    # twitch channel
    while true; do
        read -rp "Enter the twitch channel you want to download the clips from: " input_channel
        case $input_channel in
            "")
                echo Please enter a twitch channel
                ;;
            *)
                break
                ;;
        esac
    done

    # twitch client id
    while true; do
        read -rp "Enter your twitch client id. You can get it from 'https://dev.twitch.tv/console/apps': " input_clientid
        case $input_clientid in
            "")
                echo Please enter your twitch client id
                ;;
            *)
                break
                ;;
        esac
    done

    # twitch client secret
    while true; do
        read -rp "Enter your twitch client secret. You can get it from 'https://dev.twitch.tv/console/apps': " input_clientsecret
        case $input_clientsecret in
            "")
                echo Please enter your twitch client secret
                ;;
            *)
                break
                ;;
        esac
    done

    # write to database
    $python_venv manage.py shell -c "from clips.models import TwitchSettings; TwitchSettings(broadcaster_name='${input_channel}', client_id='${input_clientid}', client_secret='${input_clientsecret}').save()"

else
    printf "\x1b[35mDatabase exists\x1b[0m\n"
fi

printf "\n\x1b[35mGood bye\x1b[0m\n\n"
