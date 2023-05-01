from setuptools import setup, find_packages

setup(
    name="LskyProUploader",
    author="JoeZhu",
    version="0.0.2",
    author_email="zhuzhouyue2005@outlook.com",
    description="A tool enables you to upload your img to your Lsky Server",
    packages=find_packages(),
    license="GPL-3.0 license",
    install_requires=['Click', 'Requests'],
    entry_points={
        "console_scripts": ["lskyup = LskyProUploader.main:cli"]
    },
    python_requires=">=3"
)
