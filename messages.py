ERR_LENGTH = "ERROR: WRONG LENGTH"
ERR_REPEATED = "ERROR: REPEATED DIGITS"
ERR_NON_DIGIT = "ERROR: NON-NUMERIC"

MSG_WIN = "ACCESS GRANTED. VAULT UNLOCKED."
MSG_UNDO_SUCCESS = "ATTEMPT REVERTED."
MSG_UNDO_EMPTY = "Stack is empty. No attempts to undo."
MSG_RESTART = "SYSTEM REBOOTED."

def get_loss_message(secret):
    return f"ACCESS DENIED. SYSTEM LOCKED. CODE: {secret}"

TREND_MSGS = {
    "FIRST": "First guess logged.",
    "WARMER": "Warmer than last guess!",
    "COLDER": "Colder than last guess.",
    "SAME": "Same closeness as last guess."
}

APP_TITLE = "VAULT BREAKER"
STATUS_ONLINE = "SYSTEM ONLINE"
