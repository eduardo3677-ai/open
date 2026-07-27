---
name: refactoring
description: Use ONLY when asked to refactor code, improve code structure, or apply design patterns. Focus on making code more maintainable, readable, and efficient.
---

# Refactoring Skill

When refactoring code:

## Refactoring Principles
- **Don't change functionality**: Behavior should remain the same
- **Small steps**: Incremental changes that are easy to verify
- **Test thoroughly**: Ensure tests pass after each change
- **Improve gradually**: Don't try to refactor everything at once

## Common Refactoring Patterns
- **Extract Method**: Break down large functions into smaller, focused ones
- **Rename Variables**: Use descriptive names that reveal intent
- **Remove Duplication**: Apply DRY principle
- **Simplify Conditionals**: Reduce nested if statements
- **Introduce Parameters**: Replace hardcoded values with parameters
- **Encapsulate Collections**: Provide controlled access to data structures

## Code Smells to Address
- Long methods and functions
- Duplicate code
- Large classes/modules
- Long parameter lists
- Feature envy (methods more interested in other classes)
- Data clumps (variables that always appear together)
- Primitive obsession (using basic types instead of objects)

## Structural Improvements
- Apply appropriate design patterns
- Improve separation of concerns
- Reduce coupling between components
- Increase cohesion within modules
- Improve error handling
- Add missing documentation

## Performance Refactoring
- Identify bottlenecks before optimizing
- Consider algorithm improvements first
- Optimize database queries
- Cache expensive operations
- Reduce memory allocations

Always ensure tests exist and pass before and after refactoring.