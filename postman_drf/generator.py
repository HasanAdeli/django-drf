from abc import ABC, abstractmethod


class AbstractGenerator(ABC):

    @abstractmethod
    def generate(self, *args, **kwargs):
        raise NotImplementedError


class TestGenerator(AbstractGenerator):

    def __init__(self):
        self.tests: dict = dict()
        self.test_file_content: str = ''
        self._class_generator = ClassGenerator()

    def generate(self, collection: dict):
        environment = collection.pop('environment', {'variables': []})
        collection = collection.pop('collection', {})
        variables = collection.pop('variable', [])
        variables += environment['variables']
        class_name = collection.get('collection_name')
        class_description = collection.get('description', '')
        items = collection.get('items', [])
        self.generate_tests(class_name, class_description, items)
        self.generate_test_file_content()
        self.replace_variables(variables)

        return self.test_file_content

    def generate_tests(self, class_name, description, items):
        if class_name not in self.tests:
            self.tests[class_name] = [self._class_generator.generate(class_name, description)]
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
        generator = self.get_generator_according_to_the_method(method=item['method'])
        if item['method'] in ('post', 'put', 'patch'):
            body = item.get('body')
            return generator.generate(name, url, headers, body)
        return generator.generate(name, url, headers)

    @staticmethod
    def get_generator_according_to_the_method(method):
        methods = {
            'get': GetTestGenerator,
            'post': PostTestGenerator,
            'put': PutTestGenerator,
            'delete': DeleteTestGenerator,
            'patch': PatchTestGenerator,
            'head': HeadTestGenerator,
            'options': OptionsTestGenerator
        }
        return methods.get(method)()

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


class ClassGenerator(AbstractGenerator):
    def generate(self, name: str, description: str) -> str:
        name = ''.join([word.capitalize() for word in name.split(' ')])
        name = ''.join([word.capitalize() for word in name.split('_')])
        class_str = f'\nclass {name}Test(TestCase):\n'
        if description:
            class_str += f'    # {description}\n'
        return class_str


class GetTestGenerator(AbstractGenerator):
    def generate(self, name, url, headers):
        headers = str(headers) if headers else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.get("{url}", headers={headers})
        self.assertEqual(response.status_code, 200)
        '''


class PostTestGenerator(AbstractGenerator):
    def generate(self, name, url, headers, body):
        headers_str = str(headers) if headers else "{}"
        body_str = str(body).replace('\n', '\\n') if body else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.post("{url}", data={body_str}, content_type='application/json', headers={headers_str})
        self.assertEqual(response.status_code, 201)
        '''


class PutTestGenerator(AbstractGenerator):
    def generate(self, name, url, headers, body):
        headers = str(headers) if headers else "{}"
        body = str(body).replace('\n', '\\n') if body else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.put("{url}", data={body}, content_type='application/json', headers={headers})
        self.assertEqual(response.status_code, 200)
        '''


class DeleteTestGenerator(AbstractGenerator):
    def generate(self, name, url, headers):
        headers = str(headers) if headers else "{}"
        return f'''
    def test_{name}(self):
        client = APIClient()
        response = client.delete("{url}", headers={headers})
        self.assertEqual(response.status_code, 204)
        '''


class PatchTestGenerator(AbstractGenerator):
    def generate(self, name, url, headers, body):
        headers_str = str(headers) if headers else "{}"
        body_str = str(body).replace('\n', '\\n') if body else "{}"
        return f'''
    def test_{name}_patch(self):
        client = APIClient()
        response = client.patch("{url}", data={body_str}, content_type='application/json', headers={headers_str})
        self.assertEqual(response.status_code, 200)
    '''


class HeadTestGenerator(AbstractGenerator):
    def generate(self, name, url, headers):
        headers_str = str(headers) if headers else "{}"
        return f'''
    def test_{name}_head(self):
        client = APIClient()
        response = client.head("{url}", headers={headers_str})
        self.assertEqual(response.status_code, 200)
    '''


class OptionsTestGenerator(AbstractGenerator):
    def generate(self, name, url, headers):
        headers_str = str(headers) if headers else "{}"
        return f'''
    def test_{name}_options(self):
        client = APIClient()
        response = client.options("{url}", headers={headers_str})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Allow', response.headers)
    '''
