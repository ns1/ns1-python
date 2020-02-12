import re

from threading import Lock


class SingletonMixin(object):
    """double-locked thread safe singleton"""

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


def get_next_page(headers):
    headers = {k.lower(): v for k, v in headers.items()}
    links = _parse_header_links(headers.get("link", ""))
    for link in links:
        if link.get("rel") == "next":
            return link.get("url").replace("http://", "https://")


# cribbed from requests, since we don't want to require it as a dependency
def _parse_header_links(value):
    """Return a dict of parsed link headers proxies.
    i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"
    """
    links = []
    replace_chars = " '\""
    for val in re.split(", *<", value):
        try:
            url, params = val.split(";", 1)
        except ValueError:
            url, params = val, ""
        link = {}
        link["url"] = url.strip("<> '\"")
        for param in params.split(";"):
            try:
                key, value = param.split("=")
            except ValueError:
                break
            link[key.strip(replace_chars)] = value.strip(replace_chars)
        links.append(link)
    return links
