import json


class FileManager:

    @staticmethod
    def read_json(file_name: str):
        if file_name is None:
            return
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def write_in_test_file(file_name: str, content: str):
        if file_name is None:
            return
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)
