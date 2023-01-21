from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-backlinks',
    version='0.9.0',
    description='A MkDocs plugin for adding backlinks to your documentation pages.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='mkdocs',
    url='https://github.com/danodic-dev/mkdocs-backlinks',
    author='Danilo Guimarães',
    author_email='danilo@danodic.dev',
    license='MIT',
    python_requires='>=3.10',
    install_requires=[
        'mkdocs>=1.4.2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-backlinks = backlinks_plugin.plugin:BacklinksPlugin'
        ]
    }
)
