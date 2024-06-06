#!/bin/bash

python manage.py migrate

user_exists=$(python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())")

if [[ $user_exists != "True" ]]
then
    echo "Creating superuser"
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
else
    echo "Superuser with username $DJANGO_SUPERUSER_USERNAME exists"
fi

python manage.py runserver 0.0.0.0:8000

exec "$@"
