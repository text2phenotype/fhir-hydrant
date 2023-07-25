import json

from flask.testing import FlaskClient
from flask.wrappers import Response


class JSONResponseWrapper(Response):
    """ Extends the BaseResponse to add a get_json method.
    This should be used as the response wrapper in the TestClient.
    """

    def get_json(self, force=False, silent=False, cache=True):
        """ Return the json decoded content. """
        return json.loads(self.get_data(as_text=True))


class JSONTestClient(FlaskClient):
    """Extends the FlaskClient request methods by adding json support.
    This should be used like so::
        app.test_client_class = JSONTestClient
        client = app.test_client()
        client.post(url, json=data)
    Note that this class will override any response_wrapper you wish to use.
    """

    def __init__(self, *args, **kwargs):
        """This ensures the response_wrapper is JSONResponseWrapper."""
        super().__init__(args[0], response_wrapper=JSONResponseWrapper, **kwargs)
        self._headers = {}

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    def open(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers

        json_data = kwargs.pop('json', None)
        if json_data is not None:
            if 'data' in kwargs:
                raise ValueError('Use either `json` or `data`, not both.')

            if 'content_type' not in kwargs:
                kwargs['content_type'] = 'application/json'
            kwargs['data'] = json.dumps(json_data)

        return super().open(*args, **kwargs)
