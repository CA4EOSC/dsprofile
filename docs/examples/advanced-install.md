# Advanced Installation

## Unit Tests

The optional test suite may be installed and run with:

```bash
$ python -m pip install .[test]
$ pytest --cov=dsprofile tests
```

## Documentation

The documentation for `dsprofile` can be installed and built locally with:

```bash
$ python -m pip install .[docs]
$ mkdocs serve
```

The documentation site will then be available in a browser at
`http://127.0.0.1:8000/`.

