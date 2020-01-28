# Wagtail-Regulations

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

Wagtail Regulations provides the building blocks to create and serve 
interactive US federal regulations on existing Wagtail sites. 
It is intended to integrate into sites that may have their base templates, 
design language and components, and Wagtail base pages. It also provides 
everything needed to stand-up a new interactive regulations site using the 
US Web Design System.

The basic components are as follows:

#### Regulation content

Wagtail Regulations includes Django models that represent regulations, their 
effective versions, subparts, and sections. 

Regulation content is stored in `Section` objects in  Markdown outside of the 
Wagtail page tree.

#### Regulation pages

Regulation pages are routable Wagtail pages that live in the Wagtail page 
tree and serve the regulation content from the 
[regulation content](#regulation-content). Regulation pages can be used two 
ways:

1. By inheriting from the abstract `wagtailregulations.RegulationPage` model 
   directly.
2. By creating a new page model using any `Page` subclass and 
   `RegulationPageMixin`.


#### Regulation search

Regulation content is indexed and searchable using Haystack.


#### Regulation API

The API provides access to the regulation pages and their content so that a 
frontend can consume it.


#### Frontend

The frontend serves the regulation content and search to end users.


#### eCFR Parser



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
