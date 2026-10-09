def get_digit_statuses(guess, secret):
    statuses = []
    correct_count = 0
    misplaced_count = 0
    
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            statuses.append("correct")
            correct_count += 1
        elif guess[i] in secret:
            statuses.append("misplaced")
            misplaced_count += 1
        else:
            statuses.append("absent")
            
    return statuses, correct_count, misplaced_count

def get_closeness(correct, misplaced, code_length):
    score = (2 * correct) + (1 * misplaced)
    max_score = 2 * code_length
    
    if max_score == 0:
        ratio = 0.0
    else:
        ratio = score / max_score
        
    if ratio == 0:
        level_name = "FREEZING"
    elif ratio <= 0.25:
        level_name = "COLD"
    elif ratio <= 0.50:
        level_name = "WARM"
    elif ratio <= 0.75:
        level_name = "HOT"
    else:
        level_name = "BURNING"
        
    return level_name, ratio, ratio

def get_trend(current_score, previous_score):
    if previous_score is None:
        return "FIRST"
    if current_score > previous_score:
        return "WARMER"
    elif current_score < previous_score:
        return "COLDER"
    else:
        return "SAME"

def get_summary(correct, misplaced):
    if correct == 0 and misplaced == 0:
        return "None of these digits are in the code. Eliminate them!"
    parts = []
    if correct > 0:
        parts.append(f"{correct} right place")
    if misplaced > 0:
        parts.append(f"{misplaced} wrong place")
    return ", ".join(parts).capitalize()

def get_detailed_summary(correct, misplaced, code_length):
    if correct == 0 and misplaced == 0:
        return "None of these digits are in the code. Eliminate them!"
    if correct == 0 and misplaced == code_length:
        return "All digits are correct, but the order is wrong!"
        
    parts = []
    if correct > 0:
        s = "s" if correct > 1 else ""
        parts.append(f"{correct} digit{s} in the right place")
    if misplaced > 0:
        s = "s" if misplaced > 1 else ""
        parts.append(f"{misplaced} correct digit{s} in the wrong place")
        
    return ", ".join(parts).capitalize() + "."
