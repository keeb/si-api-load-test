import requests
import os

API_TOKEN = os.getenv("SI_API_KEY")
if not API_TOKEN:
    print("Set SI_API_KEY")
    exit(1)

DEBUG = 0

headers = {"Authorization": f"Bearer {API_TOKEN}"}


class Session:
    def __init__(self, user_id=None, user_email=None, workspace_id=None, role=None):
        self.user_id = user_id
        self.user_email = user_email
        self.workspace_id = workspace_id
        self.role = role

    @classmethod
    def from_ret(cls, ret):
        if ret.ok:
            data = ret.json()
            return cls(
                user_id=data["userId"],
                user_email=data["userEmail"],
                workspace_id=data["workspaceId"],
                role=data["token"]["role"],
            )
        else:
            raise Exception(f"Authentication failed: {ret.status_code} - {ret.text}")

    def __str__(self):
        return f"User ID: {self.user_id}\nUser Email: {self.user_email}\nWorkspace ID: {self.workspace_id}\nRole: {self.role}"


def create_session(base_url) -> Session:
    ret = requests.get(f"{base_url}/whoami", headers=headers)
    session_data = Session.from_ret(ret)
    return session_data


class SI:
    def __init__(self, base_url="http://localhost:5380"):
        self.base_url = base_url
        self.session = create_session(base_url)
        if self.session is None:
            raise Exception("failed to create session")

        self.change_set_id = None

    def create_change_set(self, name):
        post_data = {"changeSetName": name}
        data = requests.post(
            f"{self.base_url}/v1/w/{self.session.workspace_id}/change-sets",
            headers=headers,
            json=post_data,
        )
        change_set_data = data.json()
        change_set_id = change_set_data["changeSet"]["id"]
        self.change_set_id = change_set_id
        return change_set_id

    def list_change_sets(self):
        ret = requests.get(
            f"{self.base_url}/v1/w/{self.session.workspace_id}/change-sets",
            headers=headers,
        )
        
        if DEBUG:
            print(ret.text)
            
        if ret.ok:
            return ret.json()
        else:
            raise Exception(f"Failed to list change sets: {ret.status_code} - {ret.text}")

    def find_change_set_by_name(self, name):
        change_sets_data = self.list_change_sets()
        for change_set in change_sets_data.get("changeSets", []):
            if change_set.get("name") == name:
                return change_set.get("id")
        return None

    def create_component(self, component_data):
        if not self.change_set_id:
            raise Exception("change set must be created first")

        ret = requests.post(
            f"{self.base_url}/v1/w/{self.session.workspace_id}/change-sets/{self.change_set_id}/components",
            headers=headers,
            json=component_data,
        )

        if DEBUG:
            print(ret.text)

        return ret.json()

    def execute_management_function(self, component_id, management_function_name):
        mgmt_function_req = {
            "viewName": "Demo network",
            "managementFunction": {"function": management_function_name},
        }
        ret = requests.post(
            f"{self.base_url}/v1/w/{self.session.workspace_id}/change-sets/{self.change_set_id}/components/{component_id}/execute-management-function",
            headers=headers,
            json=mgmt_function_req,
        )

        if DEBUG:
            print(ret.text)

    def delete_change_set(self, change_set_id):
        ret = requests.delete(
            f"{self.base_url}/v1/w/{self.session.workspace_id}/change-sets/{change_set_id}",
            headers=headers,
        )

        if DEBUG:
            print(ret.text)

    def abandon_change_set(self, name=None):
        if not self.change_set_id and not name:
            raise Exception("no change set created and also no name provided.")

        if self.change_set_id:
            self.delete_change_set(self.change_set_id)
