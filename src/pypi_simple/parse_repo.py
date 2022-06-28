from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from mailbits import ContentType
import requests
from .classes import DistributionPackage, IndexPage, Link, ProjectPage
from .util import UnsupportedContentTypeError, basejoin, check_repo_version


def parse_repo_links(
    html: Union[str, bytes],
    base_url: Optional[str] = None,
    from_encoding: Optional[str] = None,
) -> Tuple[Dict[str, str], List[Link]]:
    """
    .. versionadded:: 0.7.0

    Parse an HTML page from a simple repository and return a ``(metadata,
    links)`` pair.

    The ``metadata`` element is a ``Dict[str, str]``.  Currently, the only key
    that may appear in it is ``"repository_version"``, which maps to the
    repository version reported by the HTML page in accordance with :pep:`629`.
    If the HTML page does not contain a repository version, this key is absent
    from the `dict`.

    The ``links`` element is a list of `Link` objects giving the hyperlinks
    found in the HTML page.

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        links' URLs (usually the URL of the page being parsed)
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes` (usually the ``charset``
        parameter of the response's :mailheader:`Content-Type` header)
    :rtype: Tuple[Dict[str, str], List[Link]]
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    soup = BeautifulSoup(html, "html.parser", from_encoding=from_encoding)
    base_tag = soup.find("base", href=True)
    if base_tag is not None:
        if base_url is None:
            base_url = base_tag["href"]
        else:
            base_url = urljoin(base_url, base_tag["href"])
    metadata = {}
    pep629_meta = soup.find(
        "meta",
        attrs={"name": "pypi:repository-version", "content": True},
    )
    if pep629_meta is not None:
        metadata["repository_version"] = pep629_meta["content"]
        check_repo_version(metadata["repository_version"])
    links = []
    for link in soup.find_all("a", href=True):
        links.append(
            Link(
                text="".join(link.strings).strip(),
                url=basejoin(base_url, link["href"]),
                attrs=link.attrs,
            )
        )
    return (metadata, links)


def parse_repo_project_page(
    project: str,
    html: Union[str, bytes],
    base_url: Optional[str] = None,
    from_encoding: Optional[str] = None,
) -> ProjectPage:
    """
    .. versionadded:: 0.7.0

    Parse a project page from a simple repository into a `ProjectPage`.  Note
    that the `~ProjectPage.last_serial` attribute will be `None`.

    :param str project: The name of the project whose page is being parsed
    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        packages' URLs (usually the URL of the page being parsed)
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes` (usually the ``charset``
        parameter of the response's :mailheader:`Content-Type` header)
    :rtype: ProjectPage
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    metadata, links = parse_repo_links(html, base_url, from_encoding)
    return ProjectPage(
        project=project,
        packages=[DistributionPackage.from_link(link, project) for link in links],
        repository_version=metadata.get("repository_version"),
        last_serial=None,
    )


def parse_repo_project_json(data: Any, base_url: Optional[str] = None) -> ProjectPage:
    """
    .. versionadded:: 0.10.0

    Parse a project page from an object decoded from an
    :mimetype:`application/vnd.pypi.simple.v1+json` response (See :pep:`691`).
    The `~ProjectPage.last_serial` attribute will be set to the value of the
    ``.meta._last-serial`` field, if any.

    :param data: The decoded body of the JSON response
    :param Optional[str] base_url: an optional URL to join to the front of any
        relative file URLs (usually the URL of the page being parsed)
    :rtype: ProjectPage
    :raises TypeError: if ``data`` is not a `dict`
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    if not isinstance(data, dict):
        raise TypeError("JSON project details response is not a dict")
    repository_version = data["meta"]["api-version"]
    check_repo_version(repository_version)
    try:
        last_serial = str(data["meta"]["_last-serial"])
    except KeyError:
        last_serial = None
    return ProjectPage(
        project=data["name"],
        packages=[
            DistributionPackage.from_pep691_details(filedata, data["name"], base_url)
            for filedata in data["files"]
        ],
        repository_version=repository_version,
        last_serial=last_serial,
    )


def parse_repo_project_response(project: str, r: requests.Response) -> ProjectPage:
    """
    .. versionadded:: 0.7.0

    Parse a project page from a `requests.Response` returned from a
    (non-streaming) request to a simple repository, and return a `ProjectPage`.

    :param str project: The name of the project whose page is being parsed
    :param requests.Response r: the response object to parse
    :rtype: ProjectPage
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    :raises ValueError: if the response has an unsupported
        :mailheader:`Content-Type`
    """
    ct = ContentType.parse(r.headers.get("content-type", "text/html"))
    if ct.content_type == "application/vnd.pypi.simple.v1+json":
        page = parse_repo_project_json(r.json(), r.url)
    elif (
        ct.content_type == "application/vnd.pypi.simple.v1+html"
        or ct.content_type == "text/html"
    ):
        charset: Optional[str]
        if "charset" in ct.params:
            charset = r.encoding
        else:
            charset = None
        page = parse_repo_project_page(
            project=project,
            html=r.content,
            base_url=r.url,
            from_encoding=charset,
        )
    else:
        raise UnsupportedContentTypeError(r.url, str(ct))
    if page.last_serial is None:
        page = page._replace(last_serial=r.headers.get("X-PyPI-Last-Serial"))
    return page


def parse_repo_index_page(
    html: Union[str, bytes],
    from_encoding: Optional[str] = None,
) -> IndexPage:
    """
    .. versionadded:: 0.7.0

    Parse an index/root page from a simple repository into an `IndexPage`.
    Note that the `~IndexPage.last_serial` attribute will be `None`.

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes` (usually the ``charset``
        parameter of the response's :mailheader:`Content-Type` header)
    :rtype: IndexPage
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    metadata, links = parse_repo_links(html, from_encoding=from_encoding)
    return IndexPage(
        projects=[link.text for link in links],
        repository_version=metadata.get("repository_version"),
        last_serial=None,
    )


def parse_repo_index_json(data: Any) -> IndexPage:
    """
    .. versionadded:: 0.10.0

    Parse an index/root page from an object decoded from an
    :mimetype:`application/vnd.pypi.simple.v1+json` response (See :pep:`691`).
    The `~IndexPage.last_serial` attribute will be set to the value of the
    ``.meta._last-serial`` field, if any.

    :param data: The decoded body of the JSON response
    :rtype: IndexPage
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    :raises TypeError: if ``data`` is not a `dict`
    """
    if not isinstance(data, dict):
        raise TypeError("JSON project list response is not a dict")
    repository_version = data["meta"]["api-version"]
    check_repo_version(repository_version)
    try:
        last_serial = str(data["meta"]["_last-serial"])
    except KeyError:
        last_serial = None
    return IndexPage(
        projects=[p["name"] for p in data["projects"]],
        repository_version=repository_version,
        last_serial=last_serial,
    )


def parse_repo_index_response(r: requests.Response) -> IndexPage:
    """
    .. versionadded:: 0.7.0

    Parse an index page from a `requests.Response` returned from a
    (non-streaming) request to a simple repository, and return an `IndexPage`.

    :param requests.Response r: the response object to parse
    :rtype: IndexPage
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    :raises ValueError: if the response has an unsupported
        :mailheader:`Content-Type`
    """
    ct = ContentType.parse(r.headers.get("content-type", "text/html"))
    if ct.content_type == "application/vnd.pypi.simple.v1+json":
        page = parse_repo_index_json(r.json())
    elif (
        ct.content_type == "application/vnd.pypi.simple.v1+html"
        or ct.content_type == "text/html"
    ):
        charset: Optional[str]
        if "charset" in ct.params:
            charset = r.encoding
        else:
            charset = None
        page = parse_repo_index_page(html=r.content, from_encoding=charset)
    else:
        raise UnsupportedContentTypeError(r.url, str(ct))
    if page.last_serial is None:
        page = page._replace(last_serial=r.headers.get("X-PyPI-Last-Serial"))
    return page
