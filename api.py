import json


class ApiConfigurationError(Exception):
    """Raised when the input value is too large"""
    pass


class EndpointNotFoundError(Exception):
    """Raised when the input value is too large"""
    pass


class Api:

    def __init__(self, file_name, key):
        try:
            with open(file_name) as api_file:
                api = json.load(api_file)[key]
            self.__protocol = api['protocol']
            self.__baseurl = api['baseurl']
            self.__version = api['version']
            self.__endpoints = api['endpoints']
        except KeyError:
            raise ApiConfigurationError

    def get_endpoints(self):
        return self.__endpoints.keys()

    def get_url(self, endpoint):
        try:
            url = self.__protocol + '://' + self.__baseurl + '/' + self.__version + '/' + self.__endpoints[endpoint]
            return url
        except KeyError:
            raise EndpointNotFoundError(endpoint)
