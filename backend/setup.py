from setuptools import setup, find_packages

setup(
    name="backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask==2.3.3",
        "pydantic==2.4.2",
        "pydantic-settings==2.0.3",
        "motor>=3.3.1",
        "pymongo>=4.6.1",
        "google-cloud-storage==2.10.0",
        "firebase-admin==6.2.0",
        "python-dotenv==1.0.0",
        "boto3==1.28.44",
    ],
) 