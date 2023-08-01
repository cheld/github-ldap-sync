from storage import Storage

class FileStorage(Storage):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_emails(self):
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
