from abc import ABC, abstractmethod

class UserService(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        pass