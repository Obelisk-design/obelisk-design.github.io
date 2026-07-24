---
title: "Claude SDK for Python"
description: "The Claude SDK for Python provides access to the Claude API from Python applications."
pubDate: 2026-07-24
tags: ["AI", "Claude Code"]
url: https://github.com/anthropics/anthropic-sdk-python
source: github.com
heroImage: ../../assets/blog-placeholder-1.jpg
---

# Claude SDK for Python

[![PyPI version](https://camo.githubusercontent.com/235acf1b166b8c9131d9ed3a734ac97201303a6b6c97096d2aad3424d98609b8/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f616e7468726f7069632e737667)](https://pypi.org/project/anthropic/)

The Claude SDK for Python provides access to the [Claude API](https://docs.anthropic.com/en/api/) from Python applications.

## Documentation

Full documentation is available at **[platform.claude.com/docs/en/api/sdks/python](https://platform.claude.com/docs/en/api/sdks/python)**.

## Installation

```
pip install anthropic
```

## Getting started

```
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],

    model="claude-opus-4-6",
)

print(message.content)
```

## Requirements

Python 3.9+

## Contributing

See [CONTRIBUTING.md](/anthropics/anthropic-sdk-python/blob/main/CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](/anthropics/anthropic-sdk-python/blob/main/LICENSE) file for details.
