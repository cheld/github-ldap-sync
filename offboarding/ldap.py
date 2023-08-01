from ldap3 import Server, Connection, NTLM, SUBTREE
import getpass
import os

class LDAP:
    def __init__(self):
        self.connection = None

        # Ensure that the required environment variables are set
        required_env_variables = ['LDAP_HOST', 'LDAP_PORT', 'LDAP_BASE_DN', 'LDAP_USER', 'LDAP_SEARCH_DN', 'LDAP_SEARCH_ATTRIBUTES']
        for env_variable in required_env_variables:
            if not os.getenv(env_variable):
                raise ValueError(f"Required environment variable {env_variable} is not set.")


    def open(self):

        # Connection parameters  
        host = os.getenv('LDAP_HOST')
        port = int(os.getenv('LDAP_PORT', 636))
        base_dn = os.getenv('LDAP_BASE_DN')
        user =  os.getenv('LDAP_USER')
        password = getpass.getpass("Enter your password: ")

        # Establish the connection using GSS Negotiate (Kerberos)
        server = Server(host, port=port, use_ssl=True)
        self.connection = Connection(server, user=user, password=password, authentication=NTLM, auto_bind='NO_TLS')
 
    
    def validate_email(self, email):

        # Search parameters
        search_dn = os.getenv('LDAP_SEARCH_DN')
        search_attributes = [os.getenv('LDAP_SEARCH_ATTRIBUTES')]
        search_filter = f'(mail={email})'

        try:
            # Bind the connection if not already bound
            if not self.connection.bound:
                self.connection.bind()

            # Perform the search
            self.connection.search(search_base=search_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=search_attributes)

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
            
        