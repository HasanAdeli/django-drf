
class TestGenerator:

    def __init__(self):
        self.tests: dict = dict()
        self.test_file_content: str = ''

    def generate_tests_from_postman(self, collection: dict):
        environment = collection.pop('environment', {})
        collection = collection.pop('collection', {})
        variables = collection.pop('variable', [])
        class_name = collection.get('collection_name')
        class_description = collection.get('description', '')
        items = collection.get('items', [])
        self.generate_tests(class_name, class_description, items)
        self.generate_test_file_content()
        self.replace_variables(variables)

        return self.test_file_content

    def generate_tests(self, class_name, description, items):
        if class_name not in self.tests:
            self.tests[class_name] = [self.generate_class(class_name, description)]
        for item in items:
            if item['type'] == 'request':
                self.tests[class_name].append(self.generate_test(item))
            elif item['type'] == 'folder':
                folder_name = item['name']
                folder_description = item.get('description', '')
                folder_items = item['items']
                self.generate_tests(folder_name, folder_description, folder_items)

    def generate_test(self, item):
        name = '_'.join([n.lower() for n in item['name'].split(' ')])
        url = item['url']
        headers = item.get('headers')
        body = item.get('headers')
        test = None
        if item['method'] == 'get':
            test = self.generate_get_test(name, url, headers)
        elif item['method'] == 'post':
            test = self.generate_post_test(name, url, headers, body)
        elif item['method'] == 'put':
            test = self.generate_put_test(name, url, headers, body)
        elif item['method'] == 'delete':
            test = self.generate_delete_test(name, url, headers)
        return test

    @staticmethod
    def generate_class(name: str, description: str) -> str:
        name = ''.join([word.capitalize() for word in name.split(' ')])
        name = ''.join([word.capitalize() for word in name.split('_')])
        class_str = f'\nclass {name}Test(TestCase):\n'
        if description:
            class_str += f'    # {description}\n'
        return class_str

    @staticmethod
    def generate_get_test(name, url, headers):
        headers = str(headers) if headers else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.get("{url}", headers={headers})
        self.assertEqual(response.status_code, 200)
        '''

    @staticmethod
    def generate_post_test(name, url, headers, body):
        headers_str = str(headers) if headers else "{}"
        body_str = str(body).replace('\n', '\\n') if body else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.post("{url}", data={body_str}, content_type='application/json', headers={headers_str})
        self.assertEqual(response.status_code, 201)
        '''

    @staticmethod
    def generate_put_test(name, url, headers, body):
        headers = str(headers) if headers else "{}"
        body = str(body).replace('\n', '\\n') if body else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.put("{url}", data={body}, content_type='application/json', headers={headers})
        self.assertEqual(response.status_code, 200)
        '''

    @staticmethod
    def generate_delete_test(name, url, headers):
        headers = str(headers) if headers else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.delete("{url}", headers={headers})
        self.assertEqual(response.status_code, 204)
        '''

    def generate_test_file_content(self):
        self.test_file_content += 'from django.test import TestCase\n'
        self.test_file_content += 'from rest_framework.test import APIClient\n\n'
        for tests in self.tests.values():
            if len(tests) <= 1:
                continue
            self.test_file_content += ''.join([text for text in tests]) + '\n'

    def replace_variables(self, variables):
        import re
        for variable in variables:
            for key, value in variable.items():
                pattern = r'{{' + key + '}}'
                self.test_file_content = re.sub(pattern, value, self.test_file_content)
