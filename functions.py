def calculate_volume(weight, reps, sets):
    return weight * reps * sets

def is_new_pr(current_weight, best_weight):
    return current_weight > best_weight