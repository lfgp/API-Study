from setuptools import find_packages, setup


setup(
    name="api-study",
    version="0.1.0",
    description="Educational content generation with student profiles and prompt comparison.",
    packages=find_packages(exclude=("tests", "venv", "data")),
    include_package_data=True,
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "rich>=13.0.0",
        "flask>=2.3.0",
        "flask-cors>=4.0.0",
        "redis>=5.0.0",
        "diskcache>=5.0.0",
    ],
    python_requires=">=3.10",
)
