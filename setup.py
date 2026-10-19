from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = [
        line.strip()
        for line in f.read().splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="MEDICAL-AI-CHATBOT",
    version="0.1",
    author="M.Anas-Shaikh",
    packages=find_packages(),
    install_requires=requirements,
)