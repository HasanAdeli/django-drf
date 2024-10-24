from validators import InputValidator
from file_manager import FileManager
from parsers import PostmanParser
from generator import TestGenerator


class PostmanToDjango:

    def __init__(self):
        self._input_validator = InputValidator()
        self._file_manager = FileManager()
        self._parser = PostmanParser()
        self._generator = TestGenerator()

    def postman_to_django(self, collection_file: str, destination: str, environment_file: str | None = None) -> None:
        # 1) validation of inputs
        self._input_validator.validate(collection_file, destination, environment_file)

        # 2) open postman files
        collection = self._file_manager.read_json(collection_file)
        environment = self._file_manager.read_json(environment_file)

        # 3) parse postman file and extract data
        data = self._parser.parse(collection, environment)

        # 4) Generate python code
        tests = self._generator.generate_tests_from_postman(data)

        # 5) Save test codes into python file
        self._file_manager.write_in_test_file(destination, tests)


if __name__ == '__main__':
    p2d = PostmanToDjango()
    p2d.postman_to_django(
        collection_file='EIA APIv2.postman_collection.json',
        destination='test2.py'
    )
