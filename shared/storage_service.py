
from abc import ABC, abstractmethod
import boto3


class StorageService(ABC):

    @staticmethod
    def create():
        #from shared.storage_test import TestStorage 
        #return TestStorage('shared/test-emails.txt')

        from shared.storage_dynamodb import DynamoDbStorage 
        return DynamoDbStorage()
    

    @abstractmethod
    def list_all_emails(self):
        pass
    
    @abstractmethod
    def set_status_to_offboarded(self, ldap_email):
        pass
    
    @abstractmethod
    def set_last_event(self, ldap_email, msg):
        pass
    
    @abstractmethod
    def onboard_gh_account(self, ldap_email, gh_account_id, gh_account_login):
        pass
    
    @abstractmethod
    def search_account(self, ldap_email):
        pass
    
    @abstractmethod
    def search_email(self, gh_account_login):
        pass
    
    @abstractmethod
    def list_all_accounts(self):
        pass
    
    @abstractmethod
    def update_account(self, gh_account_id, new_gh_account_login):
        pass

    @abstractmethod
    def init():
        pass
