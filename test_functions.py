from functions import validate_exercise, calculate_volume

def test_logic():
    # Başarılı durum
    assert validate_exercise(10, 10, 3) == True
    # Hatalı durum (Testin hatayı yakalamasını bekliyoruz)
    try:
        validate_exercise(10, 0, 3)
    except ValueError:
        print(" Geçersiz veri başarıyla engellendi!")

test_logic()