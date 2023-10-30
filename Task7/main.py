import random
def charivna_kulka(qustion):
    # Перевірка на пусте питання
    if not qustion:
        return "Кулька мовчить...(спробуйте задати питання)"

    # Перевірка на тип введення
    if not isinstance(qustion, str):
        raise TypeError("Введіть рядок (string)")

    # Список можливих відповідей
    responses = ["Так", "Ні", "Можливо", "Не можу сказати зараз"]

    # Вибір випадкової відповіді
    return random.choice(responses)

#print(charivna_kulka("Hello"))
#print(charivna_kulka(""))
#print(charivna_kulka(100))
