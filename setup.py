from setuptools import setup, find_packages

setup(
    name="linkedin_auto_jobs_applier",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.10.0",
        "webdriver-manager>=4.0.2",
        "click>=8.1.3",
        "google-generativeai>=0.3.1",
        "python-dotenv>=1.0.0",
        "pyyaml",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'linkedin-applier=main:main',
        ],
    },
)
