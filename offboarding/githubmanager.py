from github import Github, GithubIntegration, Auth, GithubException
import os

class GithubManager:
    def __init__(self):
        self.org_name = os.getenv('GITHUB_ORG_NAME')
        self.app_id = int(os.getenv('GITHUB_APP_ID'))
        self.private_key = os.getenv('GITHUB_PRIVATE_KEY')
        self.github = None

    def open(self):
        # Authenticate with the Github API using the Github App ID and private key
        auth = Auth.AppAuth(self.app_id, self.private_key)
        gi = GithubIntegration(auth=auth)
        installation = gi.get_installations()[0]
        self.github = installation.get_github_for_installation()


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