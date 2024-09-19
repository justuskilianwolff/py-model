# Python Template
This is a template for a python project using `rye` as a package manager.

## Rye
Rye is a comprehensive project and package management solution for Python. Docs can be found [here](https://rye.astral.sh/). The dependencies are managed via the `pyproject.toml`file.

### Adding and removing dependecies
- Add a [development] dependency: `rye add [--dev] <package_name>`
- Add an optional dependency, e.g., for an interface: `rye add --optional interface streamlit`
- Remove a dependency: `rye remove <package_name>`
  
### Syncing the virtual environment
- Sync virtual environment with last settings (default is to sync normal and dev, but no optional dependencies): `rye sync`
- When you want to change the last settings pass the `--reset`
- `--no-dev` excludes the development dependencies
- To install optional features use the `--feature` flag: `rye sync --features interface`

### Updating
- To self update run: `rye self update`

## Coverage
Check whether your code is properly tested: `coverage .`

## Vulture
Check whether your code is used: `vulture . [--min-confidence <int>]`

## Pylint 
Lint your code: `pylint .`

## Ruff
I acutally don't know if this is much different from `rye fmt`and `rye lint, but I usually use (with the alias `ru`):
- Formatting: `ruff format`
- Linting and fixing: `ruff check --fix`
