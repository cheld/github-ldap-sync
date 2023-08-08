from shared.storage_service import StorageService
from shared.ldap_service import LdapService
from shared.github_service import GithubService
from dotenv import load_dotenv
from croniter import croniter
import time
import os


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
        # Validate if members still have existing emails
        self.ldap.open()
        self.github.open()
        for account, email in self.storage.get_onboarded_users():
            print(f"Validating email '{email}' for Github account '{account}'")
            if not self.ldap.validate_email(email):
                result, msg = self.github.remove_from_organization(account)
                if result:
                    self.storage.set_status_to_offboarded(email)
                else:
                    print(msg)
        self.ldap.close()
        self.github.close()


if __name__ == '__main__':
    
    # Load environment variables from the .env file
    load_dotenv()
    
    # Initialize objects
    ldap = LdapService()
    github = GithubService()
    storage = StorageService.create()

    sync_manager = SyncManager(ldap, github, storage)
    sync_manager.run()

