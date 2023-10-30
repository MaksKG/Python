import pytest
from Task7.main import charivna_kulka

def test_charivna_kulka_correct_answer():
    # Перевірка на повернення коректних значень
    result = charivna_kulka("Чи завтра буде сонячно?")
    assert result in ["Так", "Ні", "Можливо", "Не можу сказати зараз"]

def test_charivna_kulka_return_str():
    # Перевірка на повернення типу str
    result = charivna_kulka("Чи завтра буде сонячно?")
    assert isinstance(result, str)

def test_charivna_kulka_empty_str():
    # Перевірка реакції на пусте питання
    result = charivna_kulka("")
    assert result == "Кулька мовчить...(спробуйте задати питання)"

def test_charivna_kulka_uncorrect_type():
    # Перевірка реакції на невірний тип введення
    with pytest.raises(TypeError):
        charivna_kulka(100)
