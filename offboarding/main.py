from filestorage import FileStorage
from ldap import LDAP

if __name__ == '__main__':
    # Create an LDAP object for email validation
    ldap = LDAP()

    # Initialize the FileStorage component
    file_storage = FileStorage('emails.txt')

    # Get the emails from the FileStorage component
    emails_to_validate = file_storage.get_emails()

    # Validate emails
    ldap.open()
    for email in emails_to_validate:
        ldap.validate_email(email)
    ldap.close()
