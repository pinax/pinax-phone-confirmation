# Pinax Phone Confirmation
    
[![](https://img.shields.io/pypi/v/pinax-phone-confirmation.svg)](https://pypi.python.org/pypi/pinax-phone-confirmation/)

[![](https://img.shields.io/github/contributors/pinax/pinax-phone-confirmation.svg)](https://github.com/pinax/pinax-phone-confirmation/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-phone-confirmation.svg)](https://github.com/pinax/pinax-phone-confirmation/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-phone-confirmation.svg)](https://github.com/pinax/pinax-phone-confirmation/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Overview](#overview)
* [Documentation](#documentation)
  * [Installation](#installation)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## pinax-phone-confirmation

### Overview

`pinax-phone-confirmation` is an app to provide phone confirmation via Twilio.


## Documentation

### Installation

To install pinax-phone-confirmation:

```shell
    $ pip install django-phoneconfirmation
```

Add `phoneconfirmation` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "phoneconfirmation",
    ]
```


## Change Log

### 0.2

* Move documentation into README
* Update LICENSE, .gitignore, MANIFEST.in, Makefile, setup.py

### 0.1

* Initial release


## Contribute

For an overview on how contributing to Pinax works read this [blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/)
and watch the included video, or read our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section.
For concrete contribution ideas, please see our
[Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our [Pinax Slack team](http://slack.pinaxproject.com)
and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course
also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our blog post on [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project
has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/).
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject)
and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-2019 James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).


