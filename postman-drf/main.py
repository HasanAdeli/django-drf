from validators import InputValidator
from file_manager import FileManager


class PostmanToDjango:

    def __init__(self):
        self._input_validator = InputValidator()
        self._file_manager = FileManager()

    def postman_to_django(self, collection_file: str, destination: str, environment_file: str | None = None) -> None:
        # 1) validation of inputs
        self._input_validator.validate(collection_file, destination, environment_file)

        # 2) open postman files
        collection = self._file_manager.read_json(collection_file)
        environment = self._file_manager.read_json(environment_file)
