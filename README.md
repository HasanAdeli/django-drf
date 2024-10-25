# postman-drf
A package to convert Postman collections to Django rest framework code and vice versa.
## installation
```shell
pip install postman-drf
```
## usage
```shell
python -m postman_drf [OPTIONS] COMMAND [ARGS]
```
To convert a Postman collection to Django rest framework test, you can use the following command:
```shell
python -m postman_drf postman_to_drf Example_collection.json tests.py
```