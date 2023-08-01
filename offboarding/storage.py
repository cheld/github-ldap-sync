from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def get_emails(self):
        pass
