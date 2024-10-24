from abc import ABC, abstractmethod

from postman_drf.exceptions import FileOrDirectoryNotFoundError, FileIsNotJsonError


class AbstractValidator(ABC):

    @abstractmethod
    def validate(self, *args):
        raise NotImplementedError


class BaseValidator(AbstractValidator):

    @staticmethod
    def is_exists(file_name):
        try:
            with open(file_name, 'r'):
                pass
        except FileNotFoundError:
            raise FileOrDirectoryNotFoundError(file_name=file_name)

    def validate(self, file_name):
        methods = [method for method in self.__dir__() if method.startswith('is_')]
        for method in methods:
            eval(f'self.{method}')(file_name)


class PostmanFileValidator(BaseValidator):

    @staticmethod
    def is_json(file_name):
        if not file_name.endswith('.json'):
            raise FileIsNotJsonError(file_name=file_name)


class DestinationValidator(BaseValidator):
    ...


class InputValidator:

    def __init__(self):
        self._postman_file_validator = PostmanFileValidator()
        self._destination_validator = DestinationValidator()

    def validate(self, collection_file, destination, environment_file):
        self._postman_file_validator.validate(collection_file)
        if environment_file:
            self._postman_file_validator.validate(environment_file)
        self._destination_validator.validate(destination)
