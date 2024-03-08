from json import dumps, loads

default_settings = {
  "graphics": {
    "screen_mode": "borderless"
  }
}

settings = default_settings.copy()


def save_settings():
    f = open('settings.txt', 'w')
    f.write(dumps(settings))
    f.close()


def load_settings():
    global settings
    f = open('settings.txt', 'r')
    settings = loads(f.read())
    f.close()
