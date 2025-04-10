# SilvaViridis.Python.DockerComposeBuilder

Template python project

### Usage

```python
from SilvaViridis.Python.DockerComposeBuilder import DockerComposeGenerator
from SilvaViridis.Python.DockerComposeBuilder.Models import Container, Image, RestartPolicy

adminer = Container(
    container_name = "adminer",
    image = Image(image = "adminer", tag = "5"),
    restart = RestartPolicy.always,
)

yml = DockerComposeGenerator(containers = frozenset([adminer])).generate()

print(yml)
```

```
services:
  adminer:
    container_name: adminer
    image: adminer:5
    restart: always
```

### Setup the Project

1. Install [Python](https://www.python.org/downloads/) and  [PDM](https://pdm-project.org/en/latest/#installation)

2. Execute in your shell

```sh
git clone git@github.com:ruafelianna/SilvaViridis.Python.DockerComposeBuilder.git \
    && cd SilvaViridis.Python.DockerComposeBuilder \
    && chmod u+x scripts/*.sh \
    && ./scripts/setup.sh
```

### Shell Scripts

- `./scripts/clean.sh` - cleans virtual environment and PDM Python version files.
- `./scripts/setup.sh` - does a clean installation of the development environment for this package and runs package build.
- `./scripts/update-gitignore.sh` - downloads fresh versions of Python, VS and VSCode `.gitignore` files and compiles them into one file. The old `.gitignore` file is removed. `curl` is required for this script to work.

### PDM Scripts

- `pdm run clean` - cleans build and test files.
- `pdm run build` - installs dependencies, runs static type checker and tests, builds a package.
- `pdm run test` - runs tests with coverage report.
- `pdm run update_lock` - updates `pdm.lock` file.

### Documentation

| Language | Link |
|:---:|:---:|
| English | [here](docs/en/index.md) |
