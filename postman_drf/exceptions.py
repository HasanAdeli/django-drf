class FileOrDirectoryNotFoundError(Exception):
    def __init__(self, message='file or directory does not exist.', file_name=None):
        self.message = f'({file_name}) {message}'
        super().__init__(self.message)


class FileIsNotJsonError(Exception):
    def __init__(self, message='The postman file must be of json type.', file_name=None):
        self.message = f'({file_name}) {message}'
        super().__init__(self.message)
