# campus_access# Campus Access-Card Manager

## Overview

The Campus Access-Card Manager is a Python command-line application for
managing campus access-card requests.

It allows users to create requests, view individual requests, approve
requests, issue cards, return cards, list requests, save data to a JSON
file, and reload previously saved requests.

The application validates user input and prevents invalid workflow
transitions.

## Features

- Create access-card requests.
- View a request using its unique ID.
- Approve requests with an approver's name.
- Issue cards only after approval.
- Return cards only after issuance.
- List all requests.
- Save requests to a JSON file.
- Reload and validate saved requests.
- Reject invalid input and unsupported workflow transitions.
- Generate sequential request IDs, such as A001 and A002.

## Requirements

- Python 3.12 or a compatible Python 3 version.
- A terminal or command-line interface.

The application uses Python's standard library and does not require
additional packages for its current functionality.

## Project Structure

```text
campus_access/
├── campus_access/
│   ├── __init__.py
│   ├── errors.py
│   ├── work.py
│   ├── storage.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_work.py
│   ├── test_storage.py
│   ├── test_cli.py
│   └── test_errors.py
├── data/
│   └── .gitkeep
├── docs/
│   ├── ai-learning-log.md
│   └── design-decisions.md
├── .gitignore
├── main.py
└── README.md