from shared.storage_service import StorageService
from shared.ldap_service import LdapService
from shared.github_service import GithubService
from dotenv import load_dotenv
from croniter import croniter
import time
import os
import traceback


class SyncManager:
    def __init__(self, ldap, github, storage):
        self.ldap = ldap
        self.github = github
        self.storage = storage
        self.cron_schedule = os.getenv('CRON_SCHEDULE')


    def run(self):
        if self.cron_schedule:
            self.schedule()
        else:
            self.sync()

    def schedule(self):
        # Create a croniter object with the cron-like schedule
        cron = croniter(self.cron_schedule)

        # Run the validation loop based on the cron-like schedule
        while True:
            # Sleep until the next run time
            next_run_time = cron.get_next()
            current_time = time.time()
            time.sleep(max(0, next_run_time - current_time))

            # Execute
            self.sync()

    def sync(self):
        try:
            # Validate if members still have existing emails
            print("Validate if Github organization members still have valid emails.")
            self.ldap.open()
            self.github.open()
            for item in self.storage.list_onboarded_gh_accounts():
                gh_account_id = item.get('gh_account_id')
                gh_account_login = item.get('gh_account_login')
                ldap_email = item.get('ldap_email')
                print(f"{ldap_email}...")
                if not self.ldap.validate_email(ldap_email):
                    print(f"Email '{ldap_email}' is not Valid. Removing Github account '{gh_account_login}' from org.")
                    result, msg = self.github.remove_from_organization(gh_account_login)
                    if result:
                        self.storage.set_status_to_offboarded(ldap_email)
                    else:
                        print(msg)
            self.ldap.close()
            self.github.close()
        except Exception as e:
            traceback.print_exc() 


if __name__ == '__main__':
    
    # Load environment variables from the .env file
    load_dotenv()
    
    # Initialize objects
    ldap = LdapService()
    github = GithubService()
    storage = StorageService.create()

    sync_manager = SyncManager(ldap, github, storage)
    sync_manager.run()

