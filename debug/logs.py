from datetime import datetime, UTC


def write_to_log(severity, msg):
    time = str(datetime.now(UTC))
    with open("./elemental-defense-log.txt", "a") as log:
        log.write(f"[{severity}] - {msg} - {time.split('.')[0]}\n")


def check_log_length():
    with open("./elemental-defense-log.txt", "r") as log:
        reset_log = len(log.readlines()) > 1000

    if reset_log:
        with open("./elemental-defense-log.txt", "w") as log:
            log.write("")
