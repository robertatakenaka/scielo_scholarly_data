import urllib.request


class RequestUrlError(Exception):
    ...


def request_url(URL, headers={'User-Agent':'Mozilla/5.0'}):
    try:
        req = urllib.request.Request(URL, headers=headers)
        result = urllib.request.urlopen(req)
    except Exception as e:
        raise RequestUrlError(e)

    return result
