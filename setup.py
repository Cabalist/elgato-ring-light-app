from setuptools import setup

APP = ['main.py']
DATA_FILES = [('icons', ["icons/taskbar_icon.png"])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps',
                 'requests'],
    'iconfile': 'icons/app_icon.icns',

}

setup(
        name="Ring Light Controls",
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
)
