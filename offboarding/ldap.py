from ldap3 import Server, Connection, NTLM, SUBTREE
import os

class LDAP:
    def __init__(self):
        self.connection = None

        # Ensure that the required environment variables are set
        required_env_variables = ['LDAP_HOST', 'LDAP_PORT', 'LDAP_USER', 'LDAP_PASSWORD', 'LDAP_SEARCH_DN', 'LDAP_SEARCH_ATTRIBUTES']
        for env_variable in required_env_variables:
            if not os.getenv(env_variable):
                raise ValueError(f"Required environment variable {env_variable} is not set.")
            
        # Get Ldap access params
        self.host = os.getenv('LDAP_HOST')
        self.port = int(os.getenv('LDAP_PORT', 636))
        self.user =  os.getenv('LDAP_USER')
        self.password = os.getenv('LDAP_PASSWORD')
        self.search_dn = os.getenv('LDAP_SEARCH_DN')
        self.search_attributes = [os.getenv('LDAP_SEARCH_ATTRIBUTES')]


    def open(self):
        # Establish the connection using GSS Negotiate (Kerberos)
        server = Server(self.host, port=self.port, use_ssl=True)
        self.connection = Connection(server, user=self.user, password=self.password, authentication=NTLM, auto_bind='NO_TLS')
 
    
    def validate_email(self, email):

        # Search parameters
        search_filter = f'(mail={email})'

        try:
            # Bind the connection if not already bound
            if not self.connection.bound:
                self.connection.bind()

            # Perform the search
            self.connection.search(search_base=self.search_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=self.search_attributes)
            if self.connection.entries:
                return True
            else:
                return False

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        
        
    def close(self):
        if self.connection and self.connection.bound:
            self.connection.unbind()
            self.connection = None
            
        