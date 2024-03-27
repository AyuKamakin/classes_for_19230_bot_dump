class Request:
    def __init__(self, new_id: int, equipment: str, status: str, number: int, postamat_id: int, user_id: int):
        self.id = new_id
        self.equipment = equipment
        self.status = status
        self.number = number
        self.postamat_id = postamat_id
        self.user_id = user_id

    def __str__(self):
        return f"ID: {self.id}, Equipment: {self.equipment}, Status: {self.status}, Number: {self.number}, Postamat ID: {self.postamat_id}, User ID: {self.user_id}"
