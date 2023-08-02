from filestorage import FileStorage
from ldap import LDAP
from githubmanager import GithubManager
from syncmanager import SyncManager
from dotenv import load_dotenv

if __name__ == '__main__':
    
    # Load environment variables from the .env file
    load_dotenv()
    
    # Initialize objects
    ldap = LDAP()
    github = GithubManager()
    storage = FileStorage('emails.txt')

    sync_manager = SyncManager(ldap, github, storage)
    sync_manager.run()
