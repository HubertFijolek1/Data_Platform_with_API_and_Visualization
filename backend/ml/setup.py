from setuptools import find_packages, setup

setup(
    name="ml",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "tensorflow==2.15.0",
        "scikit-learn",
        "pandas",
        "textblob",
        "torch",
    ],
)
