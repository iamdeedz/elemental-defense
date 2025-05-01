from datetime import datetime, UTC


def write_to_log(severity, msg):
    time = str(datetime.now(UTC))
    with open("./elemental-defense-log.txt", "a") as log:
        log.write(f"[{severity}] - {time.split('.')[0]} - {msg}\n")


def write_error_to_log(error, where):
    time = str(datetime.now(UTC))
    with open("./elemental-defense-log.txt", "a") as log:
        error_data = f"{type(error).__name__}: {error}"
        log.write(f"[ERROR] - {time.split('.')[0]} - {error_data} - during {where}\n")


def check_log_length():
    with open("./elemental-defense-log.txt", "r") as log:
        reset_log = len(log.readlines()) > 1000

    if reset_log:
        with open("./elemental-defense-log.txt", "w") as log:
            log.write("")
