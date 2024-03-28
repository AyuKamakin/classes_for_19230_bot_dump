from pydantic import BaseModel

class Request(BaseModel):
    id: int
    equipment: str
    status: str
    number: int
    postamat_id: int
    user_id: int

    def __str__(self):
        return f"ID: {self.id}, Equipment: {self.equipment}, Status: {self.status}, Number: {self.number}, Postamat ID: {self.postamat_id}, User ID: {self.user_id}"
