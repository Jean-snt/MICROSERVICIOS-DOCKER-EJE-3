from abc import ABC, abstractmethod

class BookService(ABC):
    @abstractmethod
    def get_book(self, book_id: int) -> dict:
        pass

    @abstractmethod
    def update_book_status(self, book_id: int, status: str):
        pass