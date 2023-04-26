from setuptools import setup

setup(
    name='django-system-settings',
    version='1.0.0',
    description='Django app for database persistent system settings',
    long_description_content_type='text/x-rst',
    author='Michal Kašpar',
    author_email='info@coex.cz',
    license='MIT',
    url='https://github.com/COEXCZ/django-system-settings',
    packages=["system_settings"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ],
    install_requires=[
        "django>=3.2",
        "pydantic>=1.0"
    ],
)
