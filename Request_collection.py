import random
from Request import Request

arduino_devices = [
    "Arduino UNO",
    "ESP 8266",
    "Arduino MEGA",
    "Arduino NANO",
    "Rfid-считыватель RDM 6300",
    "Rfid-считыватель RC 522",
    "Ультразвуковой дальномер HC-SR04",
    "Видеокарта Nvidia RTX Quadro 4000",
    "Инфракрасный дальномер 10-80 см",
    "Raspberry Pi Zero",
    "Raspberry Pi 4",
    "Raspberry Pi 5",
    "Xiaomi Mi Router 4C",
    "Кабель ethernet 20 метров",
    "Геркон",
    "Реле SRD-12VDC-SL-C",
    "Макетная плата",
    "DE-10 Lite",
    "Плата расширения Relay Shield",
    "Матричная клавиатура 4x4",
    "DHT-11 Датчик температуры и влажности",
    "Датчик водорода VQ-8",
    "Датчик угарного газа MQ-9",
    "Пьезоэлемент",
    "LCD Дисплей",
    "Экран сенсорный 6 дюймов"
]
statuses = ['accepted', 'awaiting', 'ready', 'declined']


# Что сделано:
# Обращение с объектом класса как словарем
# создание и добавление объекта разными способами
# вынимание списка запросов по id пользователя, статусу запроса (пока не разделял на отдельные значения)
# по постамату/шкафу
# Создание коллекции из списка, возвращаемого одной из предыдущих функций
# Переписал данные методы для возвращения не списка объектов, а списка id объектов
# Переписал копирование для вынимания из объекта такого же класса
#
#
#
#
class Requests:
    def __init__(self):
        self._requests = {}

    def __getitem__(self, key):
        return self._requests[key]

    def __setitem__(self, key, value):
        self._requests[key] = value

    def __delitem__(self, key):
        del self._requests[key]

    def __iter__(self):
        return iter(self._requests)

    # Добавление существующего/заранее созданного объекта класса в коллекцию
    def add_existing_request(self, new_request):
        if isinstance(new_request, Request) and new_request.id not in self._requests.keys():
            self._requests[new_request.id] = new_request
            return True
        else:
            return False

    # Создание объекта класса Request
    def create_and_add_request(self, new_id: int, equipment: str, status: str, number: int, postamat_id: int,
                               user_id: int):
        req = Request(new_id, equipment, status, number, postamat_id, user_id)
        self.add_existing_request(req)

    # Защищенная версия получения объекта по id
    def get_request_by_request_id(self, new_id: int):
        if new_id in self._requests.keys():
            return self._requests.get(new_id)
        else:
            return False

    # Получение объектов по пользователю (user_id)
    def get_requests_by_user_id(self, user_id: int):
        user_requests = [request for request in self._requests.values() if request.user_id == user_id]
        if user_requests:
            return user_requests
        else:
            return False

    # Получение объектов по статусу (status)
    def get_requests_by_status(self, status: str):
        status_requests = [request for request in self._requests.values() if request.status == status]
        if status_requests:
            return status_requests
        else:
            return False

    # Полная замена содержимого запроса на инфу из объекта с таким же id
    def update_request_by_id(self, changable_id: int, new_info: Request):
        if new_info.id == changable_id:
            self._requests[changable_id] = new_info
            return True
        else:
            return False

    # Копирование из списка объектов
    def create_from_list(self, requests_list):
        for request in requests_list:
            self.add_existing_request(request)

    # Далее идут переписанные методы, которые возвращают не списки объектов, а только id в оригинальной коллекции

    # Получение объектов по postamat_id
    def get_requests_by_postamat_id(self, postamat_id: int):
        postamat_status_requests = [request for request in self._requests.values() if
                                    request.postamat_id == postamat_id]
        if postamat_status_requests:
            return postamat_status_requests
        else:
            return False

    # Получение id объектов по пользователю (user_id)
    def get_requests_id_by_user_id(self, user_id: int):
        user_requests = [request.id for request in self._requests.values() if request.user_id == user_id]
        if user_requests:
            return user_requests
        else:
            return False

    # Получение id объектов по статусу (status)
    def get_requests_id_by_status(self, status: str):
        status_requests = [request.id for request in self._requests.values() if request.status == status]
        if status_requests:
            return status_requests
        else:
            return False

    def create_from_id_list(self, old_collection, keys):
        for key in keys:
            request = old_collection.get_request(key)
            if request:
                self.add_existing_request(request)

    # Получение id объектов по postamat_id
    def get_requests_id_by_postamat_id_and_status(self, postamat_id: int, status):
        postamat_status_requests = [request.id for request in self._requests.values() if
                                    request.postamat_id == postamat_id]
        if postamat_status_requests:
            return postamat_status_requests
        else:
            return False

    def generate_random_requests(self, num):
        for _ in range(num):
            new_id = random.randint(1, 1000000)  # Простое число в пределах от 1 до 1000000
            equipment = random.choice(arduino_devices)
            status = random.choice(statuses)
            number = random.randint(0, 100)
            postamat_id = random.randint(0, 5)
            new_id2 = random.randint(1, 1000000)

            request_new = Request(new_id, equipment, status, number, postamat_id, new_id2)
            self.add_existing_request(request_new)


requests_collection = Requests()

# Добавляем запросы
requests_collection.create_and_add_request(1, "Arduino UNO", "ready", 10, 2, 1001)
requests_collection.create_and_add_request(2, "Raspberry Pi Zero", "accepted", 20, 4, 1002)
requests_collection.create_and_add_request(3, "DHT-11 Датчик температуры и влажности", "awaiting", 30, 1, 1003)

# Получаем запрос по ID
print(requests_collection[2])

# Удаляем запрос
del requests_collection[2]

# Выводим все запросы
for id in requests_collection:
    print(requests_collection[id])
