from ldap3 import Server, Connection, NTLM, SUBTREE
import getpass

class LDAP:
    def __init__(self):
        self.connection = None

    def open(self):
        # Connection parameters
        host = 'gids.srv.allianz'
        port = 636
        base_dn = 'DC=GIDS,DC=Allianz,DC=COM'

        # Credentials
        user = 'ALLIANZDE\\oejdwqy'
        password = getpass.getpass("Enter your password: ")

        # Establish the connection using GSS Negotiate (Kerberos)
        server = Server(host, port=port, use_ssl=True)
        self.connection = Connection(server, user=user, password=password, authentication=NTLM, auto_bind='NO_TLS')
 
    
    def validate_email(self, email):

        # Search parameters
        search_dn = 'ou=users,DC=GIDS,DC=Allianz,DC=COM'
        filter_str = f'(mail={email})'
        attributes = ['allianz-GlobalID']

        try:
            # Bind the connection if not already bound
            if not self.connection.bound:
                self.connection.bind()

            # Perform the search
            self.connection.search(search_base=search_dn, search_filter=filter_str, search_scope=SUBTREE, attributes=attributes)

            if self.connection.entries:
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
        
        
    def close(self):
        if self.connection and self.connection.bound:
            self.connection.unbind()
            self.connection = None
            
        