Elgato Ring Light MacOS Taskbar App
--

I was unhappy with Elgato's existing app for thier otherwise very nice [Ring Light](https://www.elgato.com/en/ring-light).  This one is written in Python to work as a macOS taskbar app.  

Tested with Python 3.10 on a M1 Macbook Pro running macOS 12.1.  Uses py2app, rumps and requests.



## Steps to build:

Create a virtualenv.  
Install dependencies:
```sh
pip install -r requirements
```

Change values in `config.py` to match your IP.

Build the app:  
```sh
python setup.py py2app
```

Move the app from `dist/` into your Applications directory.


## ToDo

1. Automate discovery and/or fix IP address config
2. Add more graceful error checking when it can't communicate with the light.