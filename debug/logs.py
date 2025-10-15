from datetime import datetime, UTC

# ERROR CODES:
# 00xx = \main.py
# 01xx = \constants.py
# 02xx = \server.py
# 03xx = \gameplay\game_loop.py
# 04xx = \gameplay\multiplayer_game_loop.py
# 05xx = \gameplay\levels\path.py
# 06xx = \gameplay\levels\waves.py
# 07xx = \gameplay\towers\base_tower.py
# 08xx = \gameplay\towers\towers.py
# 09xx = \gameplay\towers\attack.py
# 10xx = \gameplay\enemies\base_enemy.py
# 11xx = \gameplay\enemies\enemies.py
# 12xx = \gameplay\enemies\spawn_handler.py
# 13xx = \ui\text.py
# 14xx = \ui\upgrades.py
# 15xx = \ui\main_menu\main.py
# 16xx = \ui\main_menu\page.py
# 17xx = \ui\main_menu\page_buttons.py
# 18xx = \ui\main_menu\button_on_clicks.py
# 19xx = \ui\shop\shop.py
# 20xx = \ui\shop\shop_window.py
# 21xx = \ui\shop\button_on_clicks.py
# 22xx = \ui\transfer\transfer.py
# 23xx = \ui\transfer\button_on_clicks.py

# Refer to each file for 3rd and 4th digits (xx00 is the global scope of each file though)

error_code = "0000"
prev_error_codes = ["0000"]


def set_error_code(code: str):
    global error_code, prev_error_codes
    error_code = code
    prev_error_codes.append(code)


def reset_error_code():
    global error_code
    error_code = prev_error_codes[-2]


def write_to_log(severity, msg):
    time = str(datetime.now(UTC))
    with open("./elemental-defense-log.txt", "a") as log:
        log.write(f"[{severity}] - {time.split('.')[0]} - {msg}\n")


def write_error_to_log(error, where):
    time = str(datetime.now(UTC))
    with open("./elemental-defense-log.txt", "a") as log:
        error_data = f"{type(error).__name__}: {error}"
        log.write(f"[ERROR] - {time.split('.')[0]} - {error_data} - during {where} - error_code: {error_code}\n")
        # - error_code: {code}


def check_log_length():
    with open("./elemental-defense-log.txt", "r") as log:
        reset_log = len(log.readlines()) > 1000

    if reset_log:
        with open("./elemental-defense-log.txt", "w") as log:
            log.write("")
