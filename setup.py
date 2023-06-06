import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_tool",  # Replace with your own username
    version="1.3.2",
    author="xyl",
    author_email="author@example.com",
    description="我的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xyl198809041/py_tool",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'wheel',
        'cython',
        'xlrd',
        'selenium',
        'pandas',
        'numpy',
        'pyquery',
        'requests',
        'fastapi',
        'pywin32',
        'pygame',
        'baidu-aip',
        'pymongo',
        # 'pymssql<3.0',
        'audioplayer',
        'edge_tts',
        'nest_asyncio'
    ]
)
