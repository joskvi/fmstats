# FMstats
Pulls and stores Last.fm data.
## Setup
To clone and setup run:
```
git clone https://github.com/joskvi/fmstats
virtualenv flask
flask/bin/pip install -r requirements.txt
mkdir lastfm_data
```
After adding your Last.fm API key to config.py (or config_local.py), the Flask server can be run using:
```
./run.py --flask
```
