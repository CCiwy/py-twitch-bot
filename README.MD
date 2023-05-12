Twitch Bot written in Python.
Connecting to twitch-IRC and responding to some commands.

#Setup

create .env file with your twitch access data
.env
```
export CLIENT_ID=''
export CLIENT_SECRET=''
export ACCESS_TOKEN=''
export CHANNEL=''
```

```
source .env
```

```
create environment and install requirements
```
python3 -m venv .venv
source .venv/bin/actitvate
python3 -m pip install -r requirements.txt
```

#Run
```
python3 run.py
```

