from filestorage import FileStorage
from ldap import LDAP
from githubmanager import GithubManager
from dotenv import load_dotenv

if __name__ == '__main__':
    
    # Load environment variables from the .env file
    load_dotenv()
    
    # Initialize objects
    ldap = LDAP()
    github = GithubManager()
    storage = FileStorage('emails.txt')

    # Validate is members still have exiting emails
    ldap.open()
    github.open()
    for account, email in storage.get_members():
        print(f"Validating email '{email}' for Github account '{account}'")
        if not ldap.validate_email(email):
            result, msg = github.remove_from_organization(account) 
            if result:
                storage.member_offboarded(email,msg)
            else:
                print(msg)
    ldap.close()
    github.close()
