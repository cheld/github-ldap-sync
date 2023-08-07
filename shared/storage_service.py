
from abc import ABC, abstractmethod

class StorageService(ABC):

    @staticmethod
    def create():
        from shared.storage_test import TestStorage 
        return TestStorage('shared/test-emails.txt')
    
    @abstractmethod
    def set_user_offboarded(self, email, msg):
        pass