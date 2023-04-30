from setuptools import setup, find_packages

setup(
    name="lskyup",
    author="JoeZhu",
    author_email="zhuzhouyue2005@outlook.com",
    description="A tool enables you to upload your img to your Lsky Server",
    packages=find_packages(),
    license="GPL v3",
    install_requires=['Click', 'Requests'],
    entry_points={
        "console_scripts": ["lskyup = main:cli"]
    },
    python_requires=">=3"
)
