while ! mysqladmin ping -h"$DB_HOST" --silent; do
    sleep 1
done
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:6001