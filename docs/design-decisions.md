# Design Decisions

## 1. Overview

The Campus Access-Card Manager is a Python command-line application
for managing campus access-card requests.

The design separates request management, error handling, JSON storage,
and user interaction into different modules.

This separation makes the code easier to understand, test, and maintain.

## 2. Module Organization

The application uses the following modules:

### `campus_access/work.py`

This module contains the `RequestManager` class and the main request
operations.

It handles request creation, validation, lookup, approval, issuance,
return, listing, and conversion of manager data for storage.

### `campus_access/errors.py`

This module defines the application's custom exceptions:

- `RequestError`
- `DataError`

Separating these exceptions makes it easier for other modules to
report and handle application errors.

### `campus_access/storage.py`

This module handles saving requests to JSON and loading them again.

It validates loaded data through the request manager and translates
storage-related failures into `DataError` exceptions.

### `campus_access/cli.py`

This module provides the numbered command-line menu and connects
user input to the request manager and storage functions.

### `main.py`

This file is the application's entry point.

It starts the command-line interface.

## 3. Request Data Model

Each request is represented as a dictionary containing:

- `id`
- `fellow_id`
- `card_type`
- `status`
- `approved_by`

A dictionary provides a straightforward way to associate each field
with its value.

The request manager stores requests using their IDs as keys, allowing
requests to be looked up by ID.

## 4. Request ID Generation

Request IDs use the letter `A` followed by digits, such as `A001`
and `A002`.

The manager maintains a counter for generating sequential IDs.

The counter is included in the saved data so that loading requests
does not cause the next ID to restart from the beginning.

Loaded request data is checked to ensure that the next ID will not
duplicate an existing request ID.

## 5. Input Validation

Validation is performed before accepting requests or changing their
state.

The application checks that:

- Fellow IDs are nonblank strings.
- Card types belong to the supported set: `visitor`, `student`, or
  `staff`.
- Request IDs have the expected format.
- Referenced requests exist.
- Approver names are nonblank.
- Workflow operations are allowed for the current status.

These checks help prevent invalid input from changing the request data.

## 6. Workflow Design

Requests follow the sequence:

`requested -> approved -> issued -> returned`

Each operation checks the current status before changing it.

Approval records the approver's name. Issuance requires an approved
request with a valid approver. Returning a card requires the request
to be in the issued state.

Invalid transitions raise `RequestError` rather than silently
changing the request.

The returned status is final.

## 7. Error Handling

The application uses two custom exception types.

### `RequestError`

This exception represents invalid request operations, malformed
identifiers, invalid input, and unsupported workflow transitions.

### `DataError`

This exception represents failures when saving or loading data,
including malformed JSON and invalid saved request records.

The CLI catches these expected exceptions and displays an error
message to the user.

## 8. JSON Storage

JSON was selected as the storage format because it is readable and
supported by Python's standard library.

The saved data includes the request records and the next request ID.

Saving uses a temporary file followed by replacement of the target
file. This helps avoid leaving a partially written target file if
writing fails before replacement.

Loading validates the JSON structure and request records. Invalid
data should be reported rather than silently replaced with an empty
request list.

The current application stores data in `data/requests.json`.

## 9. Testing Strategy

The project uses Python's `unittest` framework.

The tests are divided into separate files for workflow behavior,
storage, CLI behavior, and custom exceptions.

The storage tests use temporary directories so that test files do
not need to be kept in the project directory.

The latest recorded full test run passed 37 tests.

Testing includes successful request operations, invalid input,
workflow restrictions, saving, loading, and rejection of invalid
saved data.

## 10. Git and Collaboration

Feature work is developed on a separate branch and submitted through
a Pull Request.

This approach keeps feature changes separate from the main branch
until they are ready to be reviewed and merged.

Pull Requests also provide a place to discuss changes and record
review activity.

## 11. Known Limitations

The application is a local command-line tool using JSON storage. It
does not currently provide a graphical interface or a database-backed
multi-user service.

The test suite covers important expected behaviors and error
conditions, but it may not cover every possible input or failure.

Additional testing and code review can help identify further
improvements.