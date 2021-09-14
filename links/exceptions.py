from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        message = response.data.get('detail')
        response.data["status"] = f"{status_code}, {message}"
        del response.data["detail"]

    return response
