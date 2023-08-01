from ldap3 import Server, Connection, ALL, SUBTREE, NTLM
import getpass

def create_connection():
    # Connection parameters
    host = 'gids.srv.allianz'
    port = 636
    base_dn = 'DC=GIDS,DC=Allianz,DC=COM'

    # Credentials
    user = 'ALLIANZDE\\oejdwqy'
    password = getpass.getpass("Enter your password: ")

    # Establish the connection using GSS Negotiate (Kerberos)
    server = Server(host, port=port, use_ssl=True)
    conn = Connection(server, user=user, password=password, authentication=NTLM, auto_bind='NO_TLS')

    # Return the connection object
    return conn

def validate_email(conn, email):
    # Search parameters
    search_dn = 'ou=users,DC=GIDS,DC=Allianz,DC=COM'
    filter_str = f'(mail={email})'
    attributes = ['allianz-GlobalID']

    try:
        # Bind the connection if not already bound
        if not conn.bound:
            conn.bind()

        # Perform the search
        conn.search(search_base=search_dn, search_filter=filter_str, search_scope=SUBTREE, attributes=attributes)

        if conn.entries:
            # Email found, validation successful
            print(f"Email '{email}' is still valid in Active Directory.")
            return True
        else:
            # Email not found, validation failed
            print(f"Email '{email}' is not valid in Active Directory.")
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == '__main__':
    # Create the LDAP connection once
    ldap_conn = create_connection()

    # Replace 'YOURSEARCHMAIL' with the email to be validated
    emails_to_validate = [
        'aaldert.oosthuizen@allianz.de',
        'christoph.held@allianz.de',
        'christoph.rademacher@allianz.com',
        'arnau.oncins-rodriguez@allianz.com'
    ]

    for email in emails_to_validate:
        validate_email(ldap_conn, email)
