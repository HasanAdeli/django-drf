from validators import InputValidator


class PostmanToDjango:

    def __init__(self):
        self._input_validator = InputValidator()

    def postman_to_django(self, collection_file: str, destination: str, environment_file: str | None = None) -> None:
        # 1) validation of inputs
        self._input_validator.validate(collection_file, destination, environment_file)
