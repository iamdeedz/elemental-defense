from datetime import datetime


def write_to_log(severity, msg):
    time = str(datetime.utcnow())
    with open("./elemental-defense-log.txt", "a") as log:
        log.write(f"[{severity}] - {msg} - {time.split('.')[0]}\n")
