import random
from dsa import Stack, GuessHistory
import hints
import messages

class Game:
    def __init__(self, code_length=4, max_attempts=6, secret_code=None):
        self.code_length = code_length
        self.max_attempts = max_attempts
        
        self.guess_stack = Stack()
        self.history = GuessHistory()
        
        self.secret_code = ""
        self.is_won = False
        self.is_lost = False
        
        if secret_code:
            self.secret_code = secret_code
        else:
            self.generate_code()

    def generate_code(self):
        digits = random.sample(range(10), self.code_length)
        self.secret_code = "".join(str(d) for d in digits)

    @property
    def attempts_left(self):
        return self.max_attempts - self.history.size()

    @property
    def is_over(self):
        return self.is_won or self.is_lost

    def validate_guess(self, guess):
        if len(guess) != self.code_length:
            return False, messages.ERR_LENGTH
        if not guess.isdigit():
            return False, messages.ERR_NON_DIGIT
        if len(set(guess)) != self.code_length:
            return False, messages.ERR_REPEATED
        return True, ""

    def make_guess(self, guess):
        if self.is_over:
            return {"valid": False, "message": "Game over"}
            
        is_valid, err = self.validate_guess(guess)
        if not is_valid:
            return {"valid": False, "message": err}

        statuses, c, m = hints.get_digit_statuses(guess, self.secret_code)
        score = c
        is_won = (c == self.code_length)
        
        prev_entry = self.history.get_last()
        prev_score = prev_entry["score"] if prev_entry else None
        
        if is_won:
            trend = "CORRECT"
        elif prev_score is None:
            trend = "INCORRECT"
        elif score > prev_score:
            trend = "WARMER"
        elif score < prev_score:
            trend = "COLDER"
        else:
            trend = "SAME"
        
        entry = {
            "guess": guess,
            "statuses": statuses,
            "correct_count": c,
            "misplaced_count": m,
            "score": score,
            "trend": trend
        }
        
        self.guess_stack.push(guess)
        self.history.add(entry)
        
        if c == self.code_length:
            self.is_won = True
            msg = messages.MSG_WIN
        elif self.attempts_left <= 0:
            self.is_lost = True
            msg = messages.get_loss_message(self.secret_code)
        else:
            msg = hints.get_detailed_summary(c, m, self.code_length)
            
        return {
            "valid": True,
            "message": msg,
            "won": self.is_won,
            "lost": self.is_lost,
            "entry": entry
        }

    def undo(self):
        if self.guess_stack.is_empty():
            return None
        self.is_won = False
        self.is_lost = False
        guess = self.guess_stack.pop()
        self.history.remove_last()
        return guess

    def restart(self, code_length=None, max_attempts=None, secret_code=None):
        if code_length:
            self.code_length = code_length
        if max_attempts:
            self.max_attempts = max_attempts
            
        self.guess_stack.clear()
        self.history.clear()
        self.is_won = False
        self.is_lost = False
        
        if secret_code:
            self.secret_code = secret_code
        else:
            self.generate_code()
