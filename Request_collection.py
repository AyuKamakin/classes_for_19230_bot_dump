import json
import random
from Request import Request
import jsonpickle

# переменная arduino_devices используется исключительно в генераторе случайных запросов

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

# следующие 4 переменных используются в методах вынимания запросов по статусу, а их список - в генераторе случайных запросов
APPROVED = 'approved'
READY = 'ready'
DECLINED = 'declined'
AWAITING = 'awaiting'
statuses = [APPROVED, READY, DECLINED, AWAITING]


class Request_collection:
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

    def __str__(self):
        return str(self._requests)

    def __len__(self):
        return len(self._requests)

    def keys(self):
        return self._requests.keys()

    def clear(self):
        self._requests.clear()

    def print(self):
        for key, value in self._requests.items():
            print(f'{key}: {value}')
    #кодировка в красивый json
    def to_json(self):
        return json.dumps(self._requests ,ensure_ascii=False, default=lambda o: o.__dict__, indent=2)
    #разкодировка из красивого json и копирование внутрь коллекции
    def copy_from_json(self, json_str):
        data = json.loads(json_str)
        for key, value in data.items():
            self.create_and_add_request(value['id'], value['equipment'], value['status'], value['number'], value['postamat_id'], value['user_id'])

    # кодировка в страшный json с большим количеством текста
    def to_ugly_json(self):
        return jsonpickle.encode(self._requests)

    # разкодировка из страшного jsonа с большим количеством текста

    def copy_from_ugly_json(self, serialized):
        self.copy_all_from_old(jsonpickle.decode(serialized))

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
        req = Request(id=new_id, equipment=equipment, status=status, number=number, postamat_id=postamat_id,
                      user_id=user_id)
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
            return []

    # Методы извлечения запросов по конкретному статусу, текстовое значнеие переменной лежит наверху
    def get_ready_requests(self):
        return self.get_requests_by_status(READY)

    def get_approved_requests(self):
        return self.get_requests_by_status(APPROVED)

    def get_declined_requests(self):
        return self.get_requests_by_status(DECLINED)

    def get_awaiting_requests(self):
        return self.get_requests_by_status(AWAITING)

    # обновление пареметров у списка запросов
    def update_requests_parameters(self, requests: list, equipment=None, status=None, number=None, postamat_id=None,
                                   user_id=None):
        for req in requests:
            if isinstance(req, Request):
                if equipment is not None:
                    req.equipment = equipment
                if status is not None:
                    req.status = status
                if number is not None:
                    req.number = number
                if postamat_id is not None:
                    req.postamat_id = postamat_id
                if user_id is not None:
                    req.user_id = user_id
        if len(requests) > 0:
            return requests

    # Полная замена содержимого запроса на инфу из объекта с таким же id
    def update_request_by_id(self, changable_id: int, new_info: Request):
        if new_info.id == changable_id:
            self._requests[changable_id] = new_info
            return True
        else:
            return False

    # Замена значения параметра по выбору для запроса/запросов внутри коллекции
    def update_requests_parameters_by_id(self, keys_list, equipment=None, status=None, number=None, postamat_id=None,
                                         user_id=None):
        for key in keys_list:
            if equipment is not None:
                self._requests[key].equipment = equipment
            if status is not None:
                self._requests[key].status = status
            if number is not None:
                self._requests[key].number = number
            if postamat_id is not None:
                self._requests[key].postamat_id = postamat_id
            if user_id is not None:
                self._requests[key].user_id = user_id

    # Копирование из списка объектов
    def copy_from_list(self, requests_list):
        for request in requests_list:
            self.add_existing_request(request)

    def copy_all_from_old(self, old_dict):
        for req in old_dict.values():
            self.add_existing_request(req)

    # Удаление указанных копий объектов из коллекции
    def delete_by_list(self, reqs: list):
        if len(reqs) > 0:
            for key in reqs:
                if key in self._requests.values():
                    del self._requests[key.id]

    # Далее идут переписанные методы, которые возвращают не списки объектов, а только id в оригинальной коллекции
    def get_ids_from_request_list(self):
        return [request.id for request in self]

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
            return []

    # Методы извлечения id запросов по конкретному статусу, текстовое значнеие переменной лежит наверху
    def get_ready_requests_id(self):
        return self.get_requests_id_by_status(READY)

    def get_approved_requests_id(self):
        return self.get_requests_id_by_status(APPROVED)

    def get_declined_requests_id(self):
        return self.get_requests_id_by_status(DECLINED)

    def get_awaiting_requests_id(self):
        return self.get_requests_id_by_status(AWAITING)

    # Копирование содержимого из коллекции по ключам элементов
    def copy_by_id_list(self, old_collection, keys):
        if len(keys) > 0:
            for key in keys:
                request = old_collection[key]
                if request:
                    self.add_existing_request(request)

    # Удалить в нынешней коллекции запросы по списку
    def delete_by_id_list(self, keys: list):
        if len(keys) > 0:
            for key in keys:
                if key in self._requests:
                    del self._requests[key]

    # Получение id объектов по postamat_id
    def get_requests_id_by_postamat_id(self, postamat_id: int):
        postamat_status_requests = [request.id for request in self._requests.values() if
                                    request.postamat_id == postamat_id]
        if postamat_status_requests:
            return postamat_status_requests
        else:
            return False

    # Генератор случайных запросов, сделал чисто для испытаний без API
    def generate_random_requests(self, num, new_id=None, equipment=None, status=None, number=None, postamat_id=None,
                                 user_id=None):
        for _ in range(num):
            request_new_id = random.randint(1, 1000000) if new_id is None else new_id
            request_equipment = random.choice(arduino_devices) if equipment is None else equipment
            request_status = random.choice(statuses) if status is None else status
            request_number = random.randint(0, 100) if number is None else number
            request_postamat_id = random.randint(0, 5) if postamat_id is None else postamat_id
            request_user_id = random.randint(1, 1000000) if user_id is None else user_id

            self.create_and_add_request(request_new_id, request_equipment, request_status,
                                        request_number, request_postamat_id, request_user_id)


'''
reqs = Request_collection()

reqs.generate_random_requests(num=15)
for i in reqs.keys():
    print(reqs[i])

print('Одобренные запросы: ')
print(reqs.get_approved_requests())

print('Одобренные запросы, но только их id: ')
print(reqs.get_approved_requests_id())

print("Попробуем вынуть все одобренные запросы и положить их в новую коллекцию")
approved_reqs = Request_collection()
approved_reqs.copy_from_list(reqs.get_approved_requests())

print(approved_reqs)

print("Попробуем вынуть отправителя первого запроса и вынуть все его отвергнутые запросы, при том только через id")

random_user_reqs_id = reqs.get_requests_id_by_user_id(reqs[list(reqs.keys())[0]].user_id)

print(
    f"идентификаторы запросов от пользователя,: {reqs[list(reqs.keys())[0]].user_id}, которых {len(random_user_reqs_id)} шт, таковы:")
print(random_user_reqs_id)
print("Попробуем скопировать все запросы от этого пользователя в новый словарь")
new_random_reqs_from_that_user = Request_collection()
new_random_reqs_from_that_user.copy_by_id_list(reqs, random_user_reqs_id)
print(
    f"длина словаря: {len(new_random_reqs_from_that_user)}, сгенерируем три случайных запроса от этого же пользователя")
new_random_reqs_from_that_user.generate_random_requests(num=3, user_id=reqs[random_user_reqs_id[0]].user_id)
print(
    f"идентификаторы запросов от пользователя,: {new_random_reqs_from_that_user[list(new_random_reqs_from_that_user.keys())[0]].user_id}, которых {len(new_random_reqs_from_that_user)} шт, таковы:")
print(new_random_reqs_from_that_user)

print('Попробуем сереализацию в стремный Json:')
serzd = new_random_reqs_from_that_user.to_ugly_json()
print(serzd)
print('Попробуем десереализацию в стремный Json:')
requests_obj = Request_collection()
requests_obj.copy_from_ugly_json(serzd)
print(requests_obj)
print('Попробуем сереализацию в норм Json:')
requests_obj.clear()
serzd=new_random_reqs_from_that_user.to_json()
print(serzd)
print('Попробуем десереализацию из Json:')
requests_obj.copy_from_json(serzd)
print(requests_obj)
'''
