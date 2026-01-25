from debug.logs import set_error_code, reset_error_code
set_error_code("2300")

def toggle_transfer(is_open):
    return not is_open


def send(amount):
    set_error_code("2301")
    print(f"Sent {amount} money")
    reset_error_code()


reset_error_code()
