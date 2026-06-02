def calculate_volume(weight, reps, sets):
    return weight * reps * sets

def validate_exercise(weight, reps, sets):
    """Business logic kuralları burada tanımlı."""
    if float(weight) < 0: raise ValueError("Ağırlık negatif olamaz!")
    if int(reps) < 1: raise ValueError("Tekrar sayısı en az 1 olmalı!")
    if int(sets) < 1: raise ValueError("Set sayısı en az 1 olmalı!")
    return True