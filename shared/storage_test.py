from shared.storage_service import StorageService

class TestStorage(StorageService):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_onboarded_users(self):
        try:
            emails = []
            with open(self.file_path, 'r') as file:
                for line in file:
                    github_account, email = line.strip().split(',')
                    emails.append((github_account, email))
            return emails
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def set_user_offboarded(self, email, msg):
        print(msg)