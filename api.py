# api.py
import requests
from datetime import datetime
import uuid

ALLOWED_USER_IDS = [11111111] # get it from https://t.me/userinfobot
ADMIN_UUID = "Admin-UUID"
ADMIN_URLAPI = "Admin-UURL"
SUBLINK_URL = "subscription_URL"
TELEGRAM_TOKEN = "BOT-TOKEN"

class HiddifyApi:
    def __init__(self):
        self.admin_secret = ADMIN_UUID
        self.base_url = f"{ADMIN_URLAPI}{self.admin_secret}"
        self.allowed_user_ids = ALLOWED_USER_IDS
        self.telegram_token = TELEGRAM_TOKEN
        self.sublinkurl = SUBLINK_URL

    def generate_uuid(self):
        return str(uuid.uuid4())

    def is_connected(self):
        try:
            response = requests.get(f"{self.base_url}/admin/get_data/")
            return isinstance(response.json(), dict)
        except requests.RequestException as e:
            print(f"Error in is_connected: {e}")
            return False

    def get_system_status(self):
        try:
            response = requests.get(f"{self.base_url}/admin/get_data/")
            data = response.json()
            stats = data.get("stats", {})
            usage_history = data.get("usage_history", {})
            stats["usage_history"] = usage_history
            return stats
        except requests.RequestException as e:
            print(f"Error in get_system_status: {e}")
            return {}

    def get_user_list(self):
        try:
            response = requests.get(f"{self.base_url}/api/v1/user/")
            return response.json()
        except requests.RequestException as e:
            print(f"Error in get_user_list: {e}")
            return []

    def add_service(self, uuid, comment, name, day, traffic, telegram_id):
        if telegram_id not in self.allowed_user_ids:
            print("Unauthorized user tried to add a service.")
            return False

        data = {
            "added_by_uuid": self.admin_secret,
            "comment": comment,
            "current_usage_GB": 0,
            "last_online": None,
            "last_reset_time": None,
            "mode": "no_reset",
            "name": name,
            "package_days": day,
            "start_date": None,
            "telegram_id": telegram_id,
            "usage_limit_GB": traffic,
            "uuid": uuid,
        }

        try:
            response = requests.post(f"{self.base_url}/api/v1/user/", json=data)
            return uuid if response.json() else False
        except requests.RequestException as e:
            print(f"Error in add_service: {e}")
            return False

    def reset_user_last_reset_time(self, uuid):
        try:
            user_data = self.find_service(uuid)

            if not user_data:
                print("User not found.")
                return False

            user_data['last_reset_time'] = datetime.now().strftime('%Y-%m-%d')
            user_data['start_date'] = None
            user_data['current_usage_GB'] = 0
            response = requests.post(f"{self.base_url}/api/v1/user/?uuid={uuid}", json=user_data)
            if response.status_code == 200:
                print("User data reset successfully.")
                return True
            else:
                print(f"Failed to reset user data. Status code: {response.status_code}")
                print(f"Response content: {response.content}")
                return False
        except requests.RequestException as e:
            print(f"Error in reset_user_last_reset_time: {e}")
            return False

    def find_service(self, uuid):
        user_list = self.get_user_list()
        user_data = next((user for user in user_list if user.get("uuid") == uuid), None)

        if not user_data:
            return False

        user_uuid = user_data.get("uuid")
        user_data["subData"] = self.get_data_from_sub(f"{self.sublinkurl}/{user_uuid}")
        return user_data

    def backup_file(self):
        try:
            response = requests.get(f"{self.base_url}/admin/backup/backupfile/")
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to retrieve backup file. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error in backup_file: {e}")
            return None

    def get_data_from_sub(self, url):
        try:
            response = requests.get(f"{url}/sub/")
            lines = response.text.split("\n")
            servers = [line for line in lines if line.startswith(("vless://", "trojan://", "vemss://"))]
            return servers
        except requests.RequestException as e:
            print(f"Error in get_data_from_sub: {e}")
            return []
