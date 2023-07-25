from flask import abort, make_response, Response, jsonify


def error_handler(error, req, schema, error_status_code, error_headers):
    """
    Request parser error handler
    :param error:
    :param req:
    :param schema:
    :param error_status_code:
    :param error_headers:
    :return:
    """
    response: Response = make_response(
        (
            jsonify(
                {"errors": error.messages}
            ),
            422
        )
    )
    response.headers = {'Content-Type': 'application/json'}
    abort(422, response=response)
