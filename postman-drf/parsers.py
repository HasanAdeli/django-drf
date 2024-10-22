from abc import ABC, abstractmethod


class AbstractParser(ABC):

    @abstractmethod
    def parse(self, *args, **kwargs):
        raise NotImplementedError


class PostmanParser(AbstractParser):

    def __init__(self):
        self._collection_parser = CollectionParser()
        self._environment_parser = EnvironmentParser()

    def parse(self, collection, environment):
        return {
            'collection': self._collection_parser.parse(collection),
            'environment': self._environment_parser.parse(environment)
        }


class EnvironmentParser(AbstractParser):

    def parse(self, file):
        if file is None:
            return {}
        return {
            'name': file['name'],
            'variables': [{'key': item['key'], 'value': item['value']} for item in file['values']]
        }


class NullParser(AbstractParser):

    def parse(self, *args, **kwargs):
        return {}


class CollectionParser(AbstractParser):

    def __init__(self):
        self._parser_factory = ParserFactory()

    def parse(self, file: dict) -> dict:
        data = {}
        for key, value in file.items():
            parser_class_name = key.capitalize() + 'Parser'
            parser = self._parser_factory.get_parser(parser_class_name)
            parser_result = parser.parse(value)
            data.update(parser_result)
        return data


class InfoParser(CollectionParser):

    def parse(self, info: dict) -> dict:
        return {
            'collection_name': info.get('name'),
            'description': info.get('description')
        }


class EventParser(CollectionParser):

    def parse(self, event: dict) -> dict:
        return {

        }


class AuthParser(CollectionParser):

    def parse(self, auth: dict) -> dict:
        return {

        }


class VariableParser(CollectionParser):

    def parse(self, variable: dict) -> dict:
        return {
            'variable': [{var['key']: var['value']} for var in variable]
        }


class ItemParser(CollectionParser):

    def parse(self, items: list) -> dict:
        parsed_items = []
        for item in items:
            data = {'type': 'folder' if 'item' in item else 'request'}
            for key, value in item.items():
                parser_class_name = 'Item' + key.capitalize() + 'Parser'
                parser = self._parser_factory.get_parser(parser_class_name)
                parser_result = parser.parse(value)
                data.update(parser_result)
            parsed_items.append(data)
        return {
            'items': parsed_items
        }


class ItemNameParser(ItemParser):

    def parse(self, name: str) -> dict:
        return {
            'name': name
        }


class ItemDescriptionParser(ItemParser):

    def parse(self, description: str) -> dict:
        return {
            'description': description
        }


class ItemEventParser(ItemParser):

    def parse(self, name: str) -> dict:
        return {
        }


class ItemItemParser(ItemParser):

    def parse(self, items: list) -> dict:
        return super().parse(items)


# class ItemItemNameParser(ItemItemParser):
#
#     def parse(self, name: str) -> dict:
#         return {
#             'name': '_'.join([n.lower() for n in name.split(' ')])
#         }


class ItemRequestParser(ItemParser):

    def parse(self, request: dict) -> dict:
        data = {}
        for key, value in request.items():
            parser_class_name = 'Request' + key.capitalize() + 'Parser'
            parser = self._parser_factory.get_parser(parser_class_name)
            parser_result = parser.parse(value)
            data.update(parser_result)
        return data


class RequestUrlParser(ItemRequestParser):

    def parse(self, url: dict | str) -> dict:
        parsed_url: str = ''
        if isinstance(url, str):
            parsed_url = url
        if isinstance(url, dict):
            parsed_url = self._get_parsed_url(url)
        return {
            'url': parsed_url
        }

    def _get_parsed_url(self, url: dict) -> str:
        parsed_url = url['raw']
        if 'variable' not in url:
            return parsed_url
        parsed_url = self._replace_url_variables(parsed_url, url['variable'])
        return parsed_url

    @staticmethod
    def _replace_url_variables(url: str, variables: list) -> str:
        variables = [{var['key']: var['value']} for var in variables]
        for variable in variables:
            for key, val in variable.items():
                url = url.replace(f':{key}', val)
        return url


class RequestMethodParser(ItemRequestParser):

    def parse(self, method: str) -> dict:
        return {
            'method': method.lower()
        }


class RequestBodyParser(ItemRequestParser):

    def parse(self, body: dict) -> dict:
        data = {}
        for key, value in body.items():
            if key == 'mode':
                parser_class_name = 'ItemRequestBody' + value.capitalize() + 'Parser'
                parser = self._parser_factory.get_parser(parser_class_name)
                parser_result = parser.parse(body)
                data.update(parser_result)
        return {
            'body': data
        }


class RequestBodyFormdataParser(RequestBodyParser):

    def parse(self, body: dict) -> dict:
        formdata = body['formdata']
        body = {}
        for data in formdata:
            if data['type'] == 'text':
                body[data['key']] = data['value']
            elif data['type'] == 'file':
                body[data['key']] = data['src']
        return body


class ItemRequestBodyRawParser(RequestBodyParser):

    def parse(self, body: dict) -> dict:
        raw = body['raw'].replace(' ', '').replace('\n', '').replace('\r', '')
        if raw:
            return eval(raw)
        return {}


class RequestHeaderParser(ItemRequestParser):

    def parse(self, headers: list) -> dict:
        return {header['key']: header['value'] for header in headers}


class RequestDescriptionParser(ItemRequestParser):

    def parse(self, description: str) -> dict:
        return {
            'description': description
        }


class ItemResponseParser(ItemParser):

    def parse(self, name: str) -> dict:
        return {
        }


class ParserFactory:

    @staticmethod
    def get_parser(class_name: str):
        try:
            parser = eval(class_name)
        except NameError:
            print(f'There is no parser named {class_name}')
            parser = NullParser
        return parser()

