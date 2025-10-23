from setuptools import setup, find_packages

setup(
    name="coffee_sales_pipeline",
    version="0.1",
    packages=find_packages(where="coffee_sales_pipeline/src"),
    package_dir={"": "coffee_sales_pipeline/src"},
)
