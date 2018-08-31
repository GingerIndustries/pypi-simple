from os.path     import dirname, join
from pypi_simple import PYPI_SIMPLE_ENDPOINT, DistributionPackage, \
                            parse_project_page

DATA_DIR = join(dirname(__file__), 'data')

def test_empty():
    assert parse_project_page('', PYPI_SIMPLE_ENDPOINT + 'qypi/') == []

def test_parse_qypi():
    with open(join(DATA_DIR, 'qypi.html'), 'rb') as fp:
        assert parse_project_page(
            fp.read(),
            PYPI_SIMPLE_ENDPOINT + 'qypi/',
            from_encoding='utf-8',
        ) == [
            DistributionPackage(
                filename='qypi-0.1.0-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.tar.gz',
                url="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz#sha256=212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.post1-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/f9/3f/6b184713e79da15cd451f0dab91864633175242f4d321df0cacdd2dc8300/qypi-0.1.0.post1-py3-none-any.whl#sha256=5946a4557550479af90278e5418cd2c32a2626936075078a4c7096be52d43078",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.post1.tar.gz',
                url="https://files.pythonhosted.org/packages/0e/49/3056ee68b44c8eab4d4698b52ae4d18c0db92c80abc312894c02c4722621/qypi-0.1.0.post1.tar.gz#sha256=c99eea315455cf9fde722599ab67eeefdff5c184bb3861a7fd82f8a9387c252d",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.2.0-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/96/b8/9c2d0c3d0d95ccdaa04ebff77f8e85e9ca0888f2844b102d32a81ca3c92e/qypi-0.2.0-py3-none-any.whl#sha256=0923d60c5ff6aaf73c4805b5381868ccdf44d1cfe1d1a659d679be821fe38d53",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.2.0.tar.gz',
                url="https://files.pythonhosted.org/packages/f6/6a/1d37c72684c19f28060bd7ed1bfe3bfb8c6b9b1132b0ea67f98c036930da/qypi-0.2.0.tar.gz#sha256=cf24ea8841d0f10a822fd5cf3809c1324e5b1eab34e148b841dae6ad54919c85",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.3.0-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/79/b4/dbdcc76c55d1714f2d51f1da25c2a8a59cd1e35357bcafefb7ef6efd8c78/qypi-0.3.0-py3-none-any.whl#sha256=4dddbfa57d6b0c23a0cc20aa17aa8b17c4b41bcbd57c8d273dad84601e85e2dd",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.3.0.tar.gz',
                url="https://files.pythonhosted.org/packages/46/08/08f54b999c68fb1973824d4ac290a872136e978c6747dca647fc8116c59f/qypi-0.3.0.tar.gz#sha256=d23f45234a2f7431bd331b9fd4dedc0ff8de1361e171f4f47bb83a15b5726ba1",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.4.0-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/b9/29/82545bfa0b65f8ace22e154f0dd26c3543101523ea86df668995abafcf85/qypi-0.4.0-py3-none-any.whl#sha256=f264f87c34b722afdfde2349999697418e404183c80e5180032b3d61202e9a4d",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.4.0.tar.gz',
                url="https://files.pythonhosted.org/packages/4a/77/c4cd613177fcc894408ba731abc9d3392dcdd4cc9d6be8f1899c942686dd/qypi-0.4.0.tar.gz#sha256=884d59dd776e091b610e967729a57dd29fe095125210ef29ec4f874245baf7b6",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.4.1-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/b3/43/ac36d6a00a86ba7dc9c61f3dd448c233aae2c014c6cae111908ca5644112/qypi-0.4.1-py3-none-any.whl#sha256=488a65d6bd8c10f211e098d2d6e4a66df003be12f028b8f6f858ac2863579eb1",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.4.1.tar.gz',
                url="https://files.pythonhosted.org/packages/70/7f/8da79c0732787236a9a3a7787f2abfaf996f96f6ebccfdb533646f70640e/qypi-0.4.1.tar.gz#sha256=5f69adbf25e8369d25c31e41912ed0e6be429beb62faf4fc424aa667c561f657",
                requires_python="~=3.4",
            ),
        ]

def test_parse_qypi_base():
    with open(join(DATA_DIR, 'qypi_base.html'), 'rb') as fp:
        assert parse_project_page(
            fp.read(),
            PYPI_SIMPLE_ENDPOINT + 'qypi/',
            from_encoding='utf-8',
        ) == [
            DistributionPackage(
                filename='qypi-0.1.0-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.tar.gz',
                url="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz#sha256=212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.post1-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/f9/3f/6b184713e79da15cd451f0dab91864633175242f4d321df0cacdd2dc8300/qypi-0.1.0.post1-py3-none-any.whl#sha256=5946a4557550479af90278e5418cd2c32a2626936075078a4c7096be52d43078",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.post1.tar.gz',
                url="https://files.pythonhosted.org/packages/0e/49/3056ee68b44c8eab4d4698b52ae4d18c0db92c80abc312894c02c4722621/qypi-0.1.0.post1.tar.gz#sha256=c99eea315455cf9fde722599ab67eeefdff5c184bb3861a7fd82f8a9387c252d",
                requires_python="~=3.4",
            ),
        ]

def test_parse_qypi_mixed():
    with open(join(DATA_DIR, 'qypi_mixed.html'), 'rb') as fp:
        assert parse_project_page(
            fp.read(),
            PYPI_SIMPLE_ENDPOINT + 'qypi/',
            from_encoding='utf-8',
        ) == [
            DistributionPackage(
                filename='qypi-0.1.0-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.tar.gz',
                url="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz#sha256=212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551",
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.1.0.post1-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/f9/3f/6b184713e79da15cd451f0dab91864633175242f4d321df0cacdd2dc8300/qypi-0.1.0.post1-py3-none-any.whl#sha256=5946a4557550479af90278e5418cd2c32a2626936075078a4c7096be52d43078",
                has_sig=True,
            ),
            DistributionPackage(
                filename='qypi-0.1.0.post1.tar.gz',
                url="https://files.pythonhosted.org/packages/0e/49/3056ee68b44c8eab4d4698b52ae4d18c0db92c80abc312894c02c4722621/qypi-0.1.0.post1.tar.gz#sha256=c99eea315455cf9fde722599ab67eeefdff5c184bb3861a7fd82f8a9387c252d",
                has_sig=True,
                requires_python="~=3.4",
            ),
            DistributionPackage(
                filename='qypi-0.2.0-py3-none-any.whl',
                url="https://files.pythonhosted.org/packages/96/b8/9c2d0c3d0d95ccdaa04ebff77f8e85e9ca0888f2844b102d32a81ca3c92e/qypi-0.2.0-py3-none-any.whl#sha256=0923d60c5ff6aaf73c4805b5381868ccdf44d1cfe1d1a659d679be821fe38d53",
                has_sig=False,
            ),
        ]