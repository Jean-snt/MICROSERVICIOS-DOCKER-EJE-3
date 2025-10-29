import requests
from loans.application.ports.user_service import UserService

class UserServiceAdapter(UserService):
    def __init__(self, base_url: str = "http://localhost:8001/api"):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        try:
            response = requests.get(f"{self.base_url}/users/{user_id}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting user {user_id}: {e}")
            return None