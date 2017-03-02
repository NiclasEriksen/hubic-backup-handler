# hubic-backup-handler
A small tool for setting up and running backups to the Hubic cloud.
It depends on [hubic-backup](https://github.com/frachop/hubic-backup), but there's a helper script `setup.sh` to install dependencies, compile and install it.

#Usage
Before running, edit settings.cfg to match your preferences, then write:
`./backup.py`

#Scheduling
You need the Python3 version of python-crontab for scheduling to work.
`sudo apt install python3-crontab` or `pip install -r requirements.txt`
