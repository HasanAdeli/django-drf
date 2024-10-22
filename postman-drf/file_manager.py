import json


class FileManager:

    @staticmethod
    def read_json(file_name: str):
        if file_name is None:
            return
        with open(file_name, 'r', encoding='utf8') as file:
            return json.load(file)
