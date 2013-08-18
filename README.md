Fail2BanGoogleMap
=================

Map the locations of hosts logged or emailed by fail2ban.

Initial Set Up
--------------

You can either install pygeoip and python-dateutil for your main python
installation or you can use a segregated virtual environment and install via
the requirements file I supplied.

```bash
virtualenv --no-site-packages venv
pip install -r venv/requirements.txt
```

Set Up
------

I haven't set up an installable package or anything, so just run it "manually".

Skip the source line if you are not using the virtual environment.

```bash
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:src
```

Edit the constants file.

```bash
./run.py
```

Example
-------
TODO
