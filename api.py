# api.py
import requests
from datetime import datetime
import uuid
import qrcode
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer

ALLOWED_USER_IDS = [11111111] # get it from https://t.me/userinfobot
ADMIN_UUID = "Admin-UUID"
ADMIN_URLAPI = "https://Admin-UURL"
SUBLINK_URL = "https://subscription_URL"
TELEGRAM_TOKEN = "BOT-TOKEN"

class HiddifyApi:
    def __init__(self):
        self.admin_secret = ADMIN_UUID
        self.base_url = f"{ADMIN_URLAPI}{self.admin_secret}"
        self.allowed_user_ids = ALLOWED_USER_IDS
        self.telegram_token = TELEGRAM_TOKEN
        self.sublinkurl = SUBLINK_URL

    def generate_uuid(self) -> str:
        """Generate a UUID."""
        return str(uuid.uuid4())

    def is_connected(self) -> bool:
        """Check if the API is connected."""
        try:
            response = requests.get(f"{self.base_url}/admin/get_data/")
            return isinstance(response.json(), dict)
        except requests.RequestException as e:
            print(f"Error in is_connected: {e}")
            return False

    def get_system_status(self) -> dict:
        """Get the system status."""
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

    def make_post_request(self, endpoint: str, json_data: dict) -> bool:
        """Make a POST request."""
        try:
            response = requests.post(endpoint, json=json_data)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error in making POST request: {e}")
            return False

    def get_user_list(self) -> list:
        """Get the list of users."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/user/")
            return response.json()
        except requests.RequestException as e:
            print(f"Error in get_user_list: {e}")
            return []

    def get_user_list_name(self, query_name) -> list:
        """Get the list of users and filter by name containing the query."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/user/")
            user_list = response.json()
            filtered_users = [user for user in user_list if query_name.lower() in user.get('name', '').lower()]
            return filtered_users
        except requests.RequestException as e:
            print(f"Error in get_user_list_name: {e}")
            return []

    def add_service(self, uuid: str, comment: str, name: str, day: int, traffic: int, telegram_id: int) -> bool:
        """Add a new service."""
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

        endpoint = f"{self.base_url}/api/v1/user/"
        return self.make_post_request(endpoint, data)

    def reset_user_last_reset_time(self, uuid: str) -> bool:
        """Reset the user's last reset time."""
        try:
            user_data = self.find_service(uuid)
            if not user_data:
                print("User not found.")
                return False
            user_data['last_reset_time'] = datetime.now().strftime('%Y-%m-%d')
            user_data['start_date'] = None
            user_data['current_usage_GB'] = 0
            endpoint = f"{self.base_url}/api/v1/user/?uuid={uuid}"
            return self.make_post_request(endpoint, user_data)
        except requests.RequestException as e:
            print(f"Error in reset_user_last_reset_time: {e}")
            return False

    def update_package_days(self, uuid: str, new_days: int) -> bool:
        """Update the package days for a user."""
        try:
            user_data = self.find_service(uuid)
            if not user_data:
                print("User not found.")
                return False
            user_data['package_days'] = new_days
            endpoint = f"{self.base_url}/api/v1/user/?uuid={uuid}"
            return self.make_post_request(endpoint, user_data)
        except requests.RequestException as e:
            print(f"Error in update_package_days: {e}")
            return False

    def update_traffic(self, uuid: str, new_traffic: int) -> bool:
        """Update the traffic limit for a user."""
        try:
            user_data = self.find_service(uuid)
            if not user_data:
                print("User not found.")
                return False
            user_data['usage_limit_GB'] = new_traffic
            endpoint = f"{self.base_url}/api/v1/user/?uuid={uuid}"
            return self.make_post_request(endpoint, user_data)
        except requests.RequestException as e:
            print(f"Error in update_traffic: {e}")
            return False

    def find_service(self, uuid: str) -> dict:
        """Find a service by UUID."""
        user_list = self.get_user_list()
        user_data = next((user for user in user_list if user.get("uuid") == uuid), None)

        if not user_data:
            return False

        user_uuid = user_data.get("uuid")
        user_data["subData"] = self.get_data_from_sub(f"{self.sublinkurl}/{user_uuid}")
        return user_data

    def backup_file(self) -> bytes:
        """Backup the file."""
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

    def get_data_from_sub(self, url: str) -> list:
        """Get data from a sub URL."""
        try:
            response = requests.get(f"{url}/sub/")
            lines = response.text.split("\n")
            servers = [line for line in lines if line.startswith(("vless://", "trojan://", "vemss://"))]
            return servers
        except requests.RequestException as e:
            print(f"Error in get_data_from_sub: {e}")
            return []

    def generate_qr_code(self, data: str) -> BytesIO:
        """Generate a QR code for the given data."""
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="White", back_color="Transparent", image_factory=StyledPilImage, module_drawer=CircleModuleDrawer(), color_mask=RadialGradiantColorMask())
        
        qr_byte_io = BytesIO()
        qr_img.save(qr_byte_io, format='PNG')
        qr_byte_io.seek(0)
        
        return qr_byte_io
