from filestorage import FileStorage
from ldap import LDAP
from dotenv import load_dotenv

if __name__ == '__main__':
    
    # Load environment variables from the .env file
    load_dotenv()
    
    # Create an LDAP object for email validation
    ldap = LDAP()

    # Initialize the FileStorage component
    storage = FileStorage('emails.txt')

    # Get the emails from the FileStorage component
    emails_to_validate = storage.get_emails()

    # Validate emails
    ldap.open()
    for email in emails_to_validate:
        ldap.validate_email(email)
    ldap.close()
