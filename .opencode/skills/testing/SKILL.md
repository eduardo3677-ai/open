---
name: testing
description: Use ONLY when writing tests, improving test coverage, or debugging test failures. Focus on writing clean, maintainable tests and ensuring test quality.
---

# Testing Skill

When writing or improving tests:

## Testing Principles
- **Test behavior, not implementation**: Focus on what the code does, not how
- **Arrange, Act, Assert**: Structure tests clearly with these three phases
- **One assertion per test**: Keep tests focused and easy to understand
- **Descriptive test names**: Test names should document expected behavior

## Test Types
- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test how components work together
- **End-to-End Tests**: Test complete user workflows
- **Property-Based Tests**: Test with randomized inputs for edge cases

## Best Practices
- **Mock external dependencies**: Isolate the code being tested
- **Test edge cases**: Boundary conditions, null/undefined, empty inputs
- **Keep tests fast**: Avoid slow operations like network calls
- **Use test factories**: Create reusable test data builders
- **Clean up after tests**: Remove test data and reset state

## Coverage Goals
- **Critical paths**: 100% coverage for business logic
- **Error handling**: Test all error conditions
- **Integration points**: Test API calls, database operations
- **Edge cases**: Test unusual but valid inputs

## Test Patterns
- **Happy Path**: Test expected successful scenarios
- **Error Cases**: Test failure scenarios and error handling
- **Boundary Cases**: Test minimum, maximum, and empty values
- **Integration Tests**: Test interactions between components

## Debugging Test Failures
- Check test isolation (tests shouldn't depend on each other)
- Verify mocks and stubs are configured correctly
- Examine actual vs expected values carefully
- Check timing issues in async tests
- Review environment configuration

Good tests are documentation of expected behavior.