from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def get_members(self):
        pass

    @abstractmethod
    def member_offboarded(self, email, msg):
        pass