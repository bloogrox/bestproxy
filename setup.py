from distutils.core import setup

setup(
    name='bestproxy',
    version='0.1.0',
    author='Aslan',
    author_email='bloogrox@gmail.com',
    packages=['bestproxy'],
    url='https://github.com/bloogrox/bestproxy.git',
    description='Python client for BestProxy.ru API',
    install_requires=[
        "requests",
    ],
    dependency_links=[
        "git+https://github.com/bloogrox/http_build_query.git#egg=http_build_query"
    ],
)
