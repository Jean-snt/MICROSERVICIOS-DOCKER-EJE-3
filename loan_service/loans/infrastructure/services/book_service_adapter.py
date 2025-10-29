import requests
from loans.application.ports.book_service import BookService

class BookServiceAdapter(BookService):
    def __init__(self, base_url: str = "http://localhost:8002/api"):
        self.base_url = base_url

    def get_book(self, book_id: int) -> dict:
        try:
            response = requests.get(f"{self.base_url}/books/{book_id}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting book {book_id}: {e}")
            return None

    def update_book_status(self, book_id: int, status: str):
        try:
            response = requests.patch(f"{self.base_url}/books/{book_id}/", json={"status": status})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error updating book {book_id} status: {e}")