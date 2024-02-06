# All commands must be ran from root repository

## Prerequirements to run
```console
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo apt install redis
```

## Instruction to run:

### Terminal 1
```console
source venv/bin/activate
cd umschool
python3 manage.py runserver
```

### Terminal 2
```console
source venv/bin/activate
cd umschool
python3 -m celery -A umschool worker -l info
```
