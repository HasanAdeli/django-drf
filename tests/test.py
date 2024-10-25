from postman_drf.main import PostmanToDjango


if __name__ == '__main__':
    p2d = PostmanToDjango()
    print('start ...')
    p2d.postman_to_django(
        collection_file='FakeStoreCollection.json',
        destination='result.py'
    )
    print('completed.')
