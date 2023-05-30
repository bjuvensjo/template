This project can be used to create and use them from terminal (or scripts).

See section tool.poetry.scripts in pyproject.toml for which templates currently are supported.

## Installation

Install with pipx:

    # Alt 1
    pipx install git+https://github.com/bjuvensjo/template.git@main
    
    # Alt 2 
    # The commands will use the code of your cloned repo.
    # Run in the directory of the clone of this repo:
    pipx install -f -e .
