import urllib.request


class RequestUrlError(Exception):
    ...


def request_url(url, headers=None):
    try:
        request = urllib.request.Request(url, headers=headers)
        result = urllib.request.urlopen(request)
    except Exception as e:
        raise RequestUrlError(e)

    return result
