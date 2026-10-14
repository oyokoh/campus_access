
**Important:** This README records the 37 passing tests you just ran. If the code or test suite changes later, update that statement to match the latest results.

---

## Step 3: Fill in `docs/ai-learning-log.md`

Open `docs/ai-learning-log.md` and paste the following:

```markdown
# AI Learning Log

## 1. Purpose

This document records how AI assistance was used while developing the
Campus Access-Card Manager, what was learned, and how suggested changes
were checked.

AI was used as a learning and debugging assistant. The project code
and test results were checked locally rather than assuming that
suggested code worked correctly.

## 2. Areas Where AI Assistance Was Used

AI assistance was used to help with:

- Understanding Python package and module organization.
- Structuring the request-management workflow.
- Implementing validation for request IDs, fellow IDs, and card types.
- Understanding valid and invalid workflow transitions.
- Implementing JSON save and load operations.
- Writing and correcting unit tests.
- Diagnosing Python indentation errors.
- Understanding Git branches, commits, pushes, and Pull Requests.
- Improving project documentation.

## 3. Learning and Problem Solving

### Python package organization

The project separates its functionality into modules under the
`campus_access` package.

This helped me understand how related code can be organized into
separate files instead of placing the entire application in one file.

### Validation and workflow rules

I learned that validating input before changing a request helps
prevent invalid data and incorrect workflow transitions.

The application uses the following workflow:

`requested -> approved -> issued -> returned`

A card cannot be issued before approval, and a request cannot be
returned before issuance.

### Exceptions

The project uses `RequestError` for invalid request operations and
`DataError` for storage-related failures.

This helped me understand how custom exceptions can communicate
application errors clearly.

### JSON storage

I learned how JSON can be used to save application data between runs.

The storage tests check that request fields are saved, that the next
request ID is preserved, that saved requests can be restored, and
that malformed JSON and invalid saved data are rejected.

### Unit testing

I used Python's `unittest` framework to check expected behavior and
invalid operations.

I learned that tests should check not only successful operations but
also invalid input and error handling.

### Git and collaboration

I learned how to work on a feature branch, push changes to GitHub,
create a Pull Request, and merge approved work into the main branch.

The request-validation feature was merged through Pull Request #1.

## 4. Verification Performed

The following checks were performed during development:

1. Ran the storage tests:

   `python3 -m unittest tests.test_storage -v`

   Result: 9 tests passed.

2. Ran the full test suite:

   `python3 -m unittest discover -s tests -v`

   Result: 37 tests passed.

3. Started the application using:

   `python3 main.py`

   Result: The command-line menu appeared successfully.

4. Selected option 9.

   Result: The application displayed `Goodbye!` and exited.

5. Manually tested reloading saved request data through the CLI.

   Result: A previously saved request could be loaded and viewed.

## 5. Debugging Experience

During development, an indentation error occurred while adding storage
tests.

The error was corrected by reviewing the structure of the test class
and ensuring that statements under `with` blocks were indented correctly.

The storage tests and the full test suite were then run again.

## 6. Limitations and Further Checks

The latest recorded full test run passed all 37 tests. However, passing
tests does not prove that every possible input or failure condition
has been covered.

Further work should include:

- Reviewing the tests against every coursework requirement.
- Checking that all required documentation is complete.
- Reviewing the code with a teammate.
- Confirming that any additional review requirements are satisfied.

## 7. Reflection

Using AI assistance helped me understand errors, improve the
organization of the project, and write tests for expected and
invalid behavior.

I learned that suggested code must be checked by running tests and
examining the results. I also learned the importance of documenting
design choices and using branches and Pull Requests to manage changes.

This log records the assistance and verification performed during
development. It should be updated if additional work or reviews are
completed.