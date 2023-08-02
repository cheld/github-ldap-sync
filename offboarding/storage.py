from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def get_onboarded_users(self):
        pass

    @abstractmethod
    def set_user_offboarded(self, email, msg):
        pass