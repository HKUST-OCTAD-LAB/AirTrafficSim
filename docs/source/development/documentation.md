# Documentation development

This documentation is written using the [Sphinx](https://www.sphinx-doc.org/en/master/index.html) Python library. The theme [Furo](https://pradyunsg.me/furo/) is used and each page is written with an extended MarkDown syntax called [MyST](https://myst-parser.readthedocs.io/en/latest/index.html).

## Installation

To contribute to the development of the documentation, please set up the environment with the following commands. This will install [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and related themes and libraries for this project.

```{code-block} bash
conda activate airtrafficsim
conda install -c conda-forge sphinx myst-parser furo numpydoc
```

## Building and previewing documentation

A GitHub action is set up to automatically build and publish this documentation to the GitHub page. However, you may also want to preview the documentation during development.

First, you can build the documentation locally by executing the following commands.

```{code-block} bash
sphinx-build -b html docs/source/ docs/build/html
```

Then, you may preview the documentation by executing the following commands.

```{code-block} bash
python3 -m http.server 8000
```

This will open a Python server. Navigate to [`http://localhost:8000/docs/build/html`](http://localhost:8000/docs/build/html/) in your browser to preview the website.