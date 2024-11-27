class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None
import threading
import random

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        delay = random.randint(3, 11)  # Случайная задержка от 3 до 10 секунд
        time.sleep(delay)
import queue
import time

class Cafe:
    def __init__(self, *tables):
        self.queue = queue.Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:
                free_table.guest = guest
                print(f'{guest.name} сел(-а) за стол номер {free_table.number}')
                guest.start()
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    table.guest = None
                    print(f'Стол номер {table.number} свободен')
                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        print(f'{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                        new_guest.start()
            time.sleep(0.01)  # Небольшая пауза для предотвращения слишком частого опроса состояния очереди и столов
# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()
