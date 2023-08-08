from shared.storage_service import StorageService

class TestStorage(StorageService):
    def __init__(self, file_path):
        self.file_path = file_path


    def list_all_emails(self):
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
    

    def set_status_to_offboarded(self, ldap_email):
        print(f"User {ldap_email} offboarded")
    

    def set_last_event(self, ldap_email, msg):
        pass
    

    def onboard_gh_account(self, ldap_email, gh_account_id, gh_account_login):
        print(f"User {ldap_email} with Github account {gh_account_login} onboarded")
    

    def search_account(self, ldap_email):
        pass
    

    def search_email(self, gh_account_login):
        pass
    

    def list_all_accounts(self):
        pass
    

    def update_account(self, gh_account_id, new_gh_account_login):
        pass


    def init():
        pass