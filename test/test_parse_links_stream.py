from   io          import StringIO
import pytest
from   pypi_simple import Link, SUPPORTED_REPOSITORY_VERSION, \
                            UnsupportedRepoVersionError, parse_links_stream

@pytest.mark.parametrize('html,base_url,links', [
    (
        '''
            <html>
            <head><title>Basic test</title></head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link('link1', 'one.html', {'href': 'one.html'}),
            Link('link-two', 'two.html', {'href': 'two.html'}),
        ],
    ),

    (
        '''
            <html>
            <head><title>Test with base_url</title></head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        'https://test.nil/base/',
        [
            Link(
                'link1',
                'https://test.nil/base/one.html',
                {'href': 'one.html'},
            ),
            Link(
                'link-two',
                'https://test.nil/base/two.html',
                {'href': 'two.html'},
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link(
                'link1',
                'https://nil.test/path/one.html',
                {'href': 'one.html'},
            ),
            Link(
                'link-two',
                'https://nil.test/path/two.html',
                {'href': 'two.html'}
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base target="_new"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link('link1', 'one.html', {'href': 'one.html'}),
            Link('link-two', 'two.html', {'href': 'two.html'}),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base/>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link(
                'link1',
                'https://nil.test/path/one.html',
                {'href': 'one.html'},
            ),
            Link(
                'link-two',
                'https://nil.test/path/two.html',
                {'href': 'two.html'},
            ),
        ],
    ),

    # I'm not sure if this is how HTML is supposed to work, but it is how pip
    # works: <https://git.io/fAVZF>
    (
        '''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
                <base href="https://example.invalid/subdir/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link(
                'link1',
                'https://nil.test/path/one.html',
                {'href': 'one.html'},
            ),
            Link(
                'link-two',
                'https://nil.test/path/two.html',
                {'href': 'two.html'},
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test with both base_url and an absolute &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        'https://test.nil/base/',
        [
            Link(
                'link1',
                'https://nil.test/path/one.html',
                {'href': 'one.html'},
            ),
            Link(
                'link-two',
                'https://nil.test/path/two.html',
                {'href': 'two.html'},
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test with both base_url and a relative &lt;base&gt; tag</title>
                <base href="subdir/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        'https://test.nil/base/',
        [
            Link(
                'link1',
                'https://test.nil/base/subdir/one.html',
                {'href': 'one.html'},
            ),
            Link(
                'link-two',
                'https://test.nil/base/subdir/two.html',
                {'href': 'two.html'},
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test with uppercase tags &amp; attributes</title>
                <BASE HREF="https://nil.test/path/"/>
            </head>
            <body>
            <A HREF="one.html">link1</a>
            <A HREF="two.html">link-two</A>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link(
                'link1',
                'https://nil.test/path/one.html',
                {'href': 'one.html'},
            ),
            Link(
                'link-two',
                'https://nil.test/path/two.html',
                {'href': 'two.html'},
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test links with leading &amp; trailing whitespace</title>
            </head>
            <body>
            <a href="one.html"> whitespaced  </a>
            <a href="two.html">multiple words</a>
            <a href="three.html"> <!-- comment -->  preceded by a comment </a>
            </body>
            </html>
        ''',
        None,
        [
            Link('whitespaced', 'one.html', {'href': 'one.html'}),
            Link('multiple words', 'two.html', {'href': 'two.html'}),
            Link(
                'preceded by a comment',
                'three.html',
                {'href': 'three.html'},
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
                <title>Test that &lt;a&gt; tags without href are ignored</title>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a name="two">target</a>
            </body>
            </html>
        ''',
        None,
        [Link('link1', 'one.html', {'href': 'one.html'})],
    ),

    (
        '''
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
        ''',
        None,
        [
            Link('link1', 'one.html', {'href': 'one.html'}),
            Link('link-two', 'two.html', {'href': 'two.html'}),
        ],
    ),

    (
        '<a href="https://files.pythonhosted.org/packages/05/35/'
        'aa8dc452b753bd9b405a0d23ee3ebac693edd2d0a5896bcc2c98f6263039/'
        'txtble-0.1.0-py2.py3-none-any.whl#sha256='
        '25103e370ee304327751856ef5ecd7f59f9be88269838c7b558d4ac692d3e375"'
        ' data-requires-python="&gt;=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*,'
        ' &lt;4">txtble-0.1.0-py2.py3-none-any.whl</a><br/>',
        None,
        [
            Link(
                'txtble-0.1.0-py2.py3-none-any.whl',
                "https://files.pythonhosted.org/packages/05/35/aa8dc452b75"
                "3bd9b405a0d23ee3ebac693edd2d0a5896bcc2c98f6263039/txtble-"
                "0.1.0-py2.py3-none-any.whl#sha256=25103e370ee304327751856"
                "ef5ecd7f59f9be88269838c7b558d4ac692d3e375",
                {
                    "href": "https://files.pythonhosted.org/packages/05/35"
                            "/aa8dc452b753bd9b405a0d23ee3ebac693edd2d0a589"
                            "6bcc2c98f6263039/txtble-0.1.0-py2.py3-none-an"
                            "y.whl#sha256=25103e370ee304327751856ef5ecd7f5"
                            "9f9be88269838c7b558d4ac692d3e375",
                    "data-requires-python":
                        ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
                },
            ),
        ],
    ),

    (
        '<a href="https://test.nil/simple/files/project-0.1.0-p&#xFF;42-none'
        '-any.whl">project-0.1.0-p&#xFF;42-none-any.whl</a>',
        None,
        [
            Link(
                'project-0.1.0-p\xFF42-none-any.whl',
                "https://test.nil/simple/files/project-0.1.0-p\xFF42-none"
                    "-any.whl",
                {
                    "href": "https://test.nil/simple/files/project-0.1.0-"
                            "p\xFF42-none-any.whl",
                },
            )
        ],
    ),

    (
        '<a href="https://test.nil/simple/files/project-0.1.0-p&yuml;42-none'
        '-any.whl">project-0.1.0-p&yuml;42-none-any.whl</a>',
        None,
        [
            Link(
                'project-0.1.0-p\xFF42-none-any.whl',
                "https://test.nil/simple/files/project-0.1.0-p\xFF42-none"
                    "-any.whl",
                {
                    "href": "https://test.nil/simple/files/project-0.1.0-"
                            "p\xFF42-none-any.whl",
                },
            ),
        ],
    ),

    (
        '''
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="1.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link('link1', 'one.html', {'href': 'one.html'}),
            Link('link-two', 'two.html', {'href': 'two.html'}),
        ],
    ),

    (
        '''
            <html>
            <head>
            <title>Basic test</title>
            <meta name="repository-version" content="42.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link('link1', 'one.html', {'href': 'one.html'}),
            Link('link-two', 'two.html', {'href': 'two.html'}),
        ],
    ),

    (
        '''
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        None,
        [
            Link('link1', 'one.html', {'href': 'one.html'}),
            Link('link-two', 'two.html', {'href': 'two.html'}),
        ],
    ),

])
def test_parse_links_stream(html, base_url, links):
    assert list(parse_links_stream(StringIO(html), base_url)) == links

@pytest.mark.parametrize('html,version', [
    (
        '''
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="42.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        '42.0',
    ),

    ### TODO: This one's behavior differs from parse_repo_links; should they be
    ### aligned?
    (
        '''
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="1.0"/>
            <meta name="pypi:repository-version" content="5.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        '5.0',
    ),

    (
        '''
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="5.0"/>
            <meta name="pypi:repository-version" content="1.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''',
        '5.0',
    ),
])
def test_parse_links_stream_unsupported_version(html, version):
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        list(parse_links_stream(StringIO(html)))
    assert excinfo.value.declared_version == version
    assert excinfo.value.supported_version == SUPPORTED_REPOSITORY_VERSION
    assert str(excinfo.value) == (
        f"Repository's version ({version}) has greater major component than"
        f" supported version ({SUPPORTED_REPOSITORY_VERSION})"
    )