from github import Github, GithubIntegration, Auth, GithubException
import os

class GithubService:

    def __init__(self):
        self.github = None

        # Ensure that the required environment variables are set
        required_env_variables = ['GITHUB_ORG_NAME', 'GITHUB_APP_ID', 'GITHUB_PRIVATE_KEY']
        for env_variable in required_env_variables:
            if not os.getenv(env_variable):
                raise ValueError(f"Required environment variable {env_variable} is not set.")
            
        # Get Github access params   
        self.org_name = os.getenv('GITHUB_ORG_NAME')
        self.app_id = int(os.getenv('GITHUB_APP_ID'))
        self.private_key = os.getenv('GITHUB_PRIVATE_KEY')


    def open(self):
        # Authenticate with the Github API using the Github App ID and private key
        auth = Auth.AppAuth(self.app_id, self.private_key)
        gi = GithubIntegration(auth=auth)
        installation = gi.get_installations()[0]
        self.github = installation.get_github_for_installation()


    def join_organization(self, github_account):
        try: 
            # Get user to be removed
            user_to_add = None
            try:
                user_to_add = self.github.get_user(github_account)
            except GithubException as e:
                if e.status == 404:
                    # User deleted his account himself. Ignore
                    return False, (f"User '{github_account}' does not exist.")
                else:
                    raise e
            #print(user_to_add.id)
            # Check if user is already org member
            org=self.github.get_organization(self.org_name)
            if org.has_in_members(user_to_add):
                return False, (f"User '{github_account}' is already a member of '{self.org_name}'.")
            
            # Add user to org
            org.invite_user(user_to_add)
            return True, (f"User '{github_account}' successfully removed from {self.org_name}.")

        except Exception as e:
            raise Exception(f"User '{github_account}' could not join to {self.org_name}. Reason: {e}")
        


    def remove_from_organization(self, github_account):
        try: 
            # Get user to be removed
            user_to_remove = None
            try:
                user_to_remove = self.github.get_user(github_account)
            except GithubException as e:
                if e.status == 404:
                    # User deleted his account himself. Ignore
                    return True, (f"User '{github_account}' does not exist any longer.")
                else:
                    raise e

            # Check if user is still member of org
            org=self.github.get_organization(self.org_name)
            if not  org.has_in_members(user_to_remove):
                # User removed himself from organization. Ignore
                return True, (f"User '{github_account}' is already removed from {self.org_name}.")

            # Remove user from org
            #org.remove_from_members(user_to_remove)
            return True, (f"User '{github_account}' successfully removed from {self.org_name}.")

        except Exception as e:
            return False, (f"User '{github_account}' could not be removed from {self.org_name}. Reason: {e}")
        

    def close(self):
        pass