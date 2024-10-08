# module_13_1.py

import asyncio


# Задача "Асинхронные силачи":
# Необходимо сделать имитацию соревнований по поднятию шаров Атласа.
# Напишите асинхронную функцию start_strongman(name, power),
# где name - имя силача, power - его подъёмная мощность.
# Примечание:
# 1. Для обозначения асинхронной функции используйте оператор async.
async def start_strongman(name, power):
    # Реализуйте следующую логику в функции:
    # 1. В начале работы должна выводиться строка - 'Силач <имя силача> начал соревнования.'
    print(f'Силач {name} начал соревнования.')

    # 2. После должна выводиться строка - 'Силач <имя силача> поднял <номер шара>'
    for i in range(1, 6):
        # с задержкой обратно пропорциональной его силе power.
        # Примечание:
        # 3. Для задержки в асинхронной функции используйте функцию sleep из пакета asyncio.
        await asyncio.sleep(1 / power)
        # Для каждого участника количество шаров i одинаковое - 5.
        print(f'Силач {name} поднял {i} шар.')

    # В конце поднятия всех шаров должна выводится строка 'Силач <имя силача> закончил соревнования.'
    print(f'Силач {name} закончил соревнования.')


# Примечание:
# 1. Для обозначения асинхронной функции используйте оператор async.
# Также напишите асинхронную функцию start_tournament,
async def start_tournament():
    # в которой создаются 3 задачи для функций start_strongman.
    tasks = [
        # Имена(name) и силу(power) для вызовов функции start_strongman можете выбрать самостоятельно.
        # Переданные аргументы в функции start_strongman:
        # 'Pasha', 3
        start_strongman('Pasha', 3),
        # 'Denis', 4
        start_strongman('Denis', 4),
        # 'Apollon', 5
        start_strongman('Apollon', 5)
    ]

    # Примечание:
    # 2. Для постановки задачи в режим ожидания используйте оператор await.
    await asyncio.gather(*tasks)


# Примечание:
# 4. Для запуска асинхронной функции используйте функцию run из пакета asyncio.
asyncio.run(start_tournament())

# Вывод на консоль:
# Силач Pasha начал соревнования
# Силач Denis начал соревнования
# Силач Apollon начал соревнования
# Силач Apollon поднял 1 шар
# Силач Denis поднял 1 шар
# Силач Pasha поднял 1 шар
# Силач Apollon поднял 2 шар
# Силач Denis поднял 2 шар
# Силач Apollon поднял 3 шар
# Силач Pasha поднял 2 шар
# Силач Denis поднял 3 шар
# Силач Apollon поднял 4 шар
# Силач Pasha поднял 3 шар
# Силач Apollon поднял 5 шар
# Силач Apollon закончил соревнования
# Силач Denis поднял 4 шар
# Силач Denis поднял 5 шар
# Силач Denis закончил соревнования
# Силач Pasha поднял 4 шар
# Силач Pasha поднял 5 шар
# Силач Pasha закончил соревнования
