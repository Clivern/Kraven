<p align="center">
  <img height="150" src="https://raw.githubusercontent.com/Clivern/Kraven/master/static/assets/images/logo.png">
</p>

# Kraven
Docker Management Dashboard

[![Build Status](https://travis-ci.org/Clivern/Kraven.svg?branch=master)](https://travis-ci.org/Clivern/Kraven)

Installation
------------

In order to run this app do the following:

### Default Install

1. Get the application code

```bash
git clone https://github.com/Clivern/Kraven.git kraven
cd kraven
cp .env.example .env
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Edit the .env file manually or use command for that

```bash
# Set DB Host
python manage.py kraven update_env DB_HOST=127.0.0.1

# Set DB Port
python manage.py kraven update_env DB_PORT=3306

# Set DB Name
python manage.py kraven update_env DB_DATABASE=kraven

# Set DB Username
python manage.py kraven update_env DB_USERNAME=root

# Set DB Password
python manage.py kraven update_env DB_PASSWORD=

# Create a new app key (Required)
python manage.py kraven update_app_key

# Set DB Type (mysql or sqlite supported till now)
python manage.py kraven update_env DB_CONNECTION=mysql
```

4. Migrate The Database.

```bash
python manage.py migrate
```

5. Run The Server

```bash
python manage.py runserver
```

6. Run the Jobs Schedule.

```bash
python manage.py schedule run < /dev/null
# Or as a process
python manage.py schedule run </dev/null &
```

7. Go to `http://127.0.0.1:8000/install` to install the application.


### With Docker

1. Get the application code

```bash
git clone https://github.com/Clivern/Kraven.git kraven
cd kraven
cp .env.docker .env
```

2. Then run our docker containers

```bash
docker-compose build
docker-compose up -d
```

3. Open your browser and access the `http://127.0.0.1:8000/`.

4. Also you can add `http://kraven.com` to your `/etc/hosts` file.

```bash
127.0.0.1:8000       kraven.com
```

5. To Check our containers, use the following command:

```bash
docker-compose ps
```

6. To stop our containers

```bash
docker-compose down
```


### Running on production

Currently kraven is still under development and for sure we will explain how to run it on production after the first release.


Misc
====

Changelog
---------
Version 1.0.0:
```
Coming Soon.
```

Acknowledgements
----------------

© 2018, Clivern. Released under [The Apache Software License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt).

**Kraven** is authored and maintained by [@clivern](http://github.com/clivern).
