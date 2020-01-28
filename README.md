# Wagtail Regulations

[![Build Status](https://travis-ci.org/cfpb/wagtail-regulations.svg?branch=master)](https://travis-ci.org/cfpb/wagtail-regulations)
[![Coverage Status](https://coveralls.io/repos/github/cfpb/wagtail-regulations/badge.svg?branch=master)](https://coveralls.io/github/cfpb/wagtail-regulations?branch=master)

Building blocks for interactive regulations in Wagtail.

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Getting help](#getting-help)
- [Getting involved](#getting-involved)
- [Licensing](#licensing)
- [Credits and references](#credits-and-references)

## Dependencies

- Django 1.11+ (including Django 2.0+)
- Wagtail 1.13+ (including Wagtail 2.0+)
- Python 2.7+, 3.6+

## Installation


## Usage


### Components


#### Regulation pages

Regulation pages are routable Wagtail pages that live in the Wagtail page 
tree and serve the regulation content.


#### Regulation content

Regulation content is stored in Markdown outside of the Wagtail page tree.


#### Regulation search

Regulation content is indexed and searchable using Haystack.


#### Regulation API

The API provides access to the regulation pages and their content so that a 
frontend can consume it.


#### Frontend

The frontend serves the regulation content and search to end users.


### Putting it all together



## Getting help

Please add issues to the [issue tracker](https://github.com/cfpb/wagtail-regulations/issues).

## Getting involved

General instructions on _how_ to contribute can be found in [CONTRIBUTING](CONTRIBUTING.md).

## Licensing
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

## Credits and references

1. Forked from [cfgov-refresh](https://github.com/cfpb/cfgov-refresh)
