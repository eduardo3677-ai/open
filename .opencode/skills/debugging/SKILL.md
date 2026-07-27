---
name: debugging
description: Use ONLY when debugging errors, fixing bugs, or troubleshooting issues. Focus on identifying root causes and providing systematic solutions.
---

# Debugging Skill

When debugging issues:

## Analysis Steps
1. **Understand the Problem**
   - Reproduce the issue
   - Identify error messages and stack traces
   - Determine when the issue occurs

2. **Gather Information**
   - Check logs and console output
   - Examine relevant code sections
   - Review recent changes

3. **Form Hypotheses**
   - Identify possible causes
   - Prioritize most likely scenarios
   - Consider edge cases

## Debugging Techniques
- **Binary Search**: Comment out half the code to isolate the issue
- **Logging**: Add strategic console logs to trace execution flow
- **Breakpoints**: Use debugger to inspect state at specific points
- **Unit Tests**: Write tests to reproduce the issue

## Common Issues to Check
- Null/undefined values
- Race conditions
- Memory leaks
- Incorrect data types
- Missing error handling
- Async/await issues
- Configuration problems

## Verification
- Confirm the fix resolves the issue
- Test edge cases
- Ensure no regressions
- Document the root cause and solution

Always provide the root cause analysis, not just symptoms.