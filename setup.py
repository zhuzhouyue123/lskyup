from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="LskyProUploader",
    author="JoeZhu",
    version="0.0.2",
    author_email="zhuzhouyue2005@outlook.com",
    description="A tool enables you to upload your img to your Lsky Server",
    packages=find_packages(),
    install_requires=requirements,
    license="GPLv3+",
    entry_points={
        "console_scripts": ["lskyup = LskyProUploader.main:cli"]
    },
)
