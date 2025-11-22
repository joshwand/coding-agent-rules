---
description: MUST activate when interacting with files matching the globs. Coding principles to write clean code.
globs: *.py, *.js, *.ts, *.jsx, *.tsx, *.java, *.kt, *.go, *.rs, *.c, *.cpp, *.h, *.hpp, *.cs, *.sh, *.bash, *.zsh, *.php, *.rb, *.swift, *.m, *.mm, *.pl, *.pm, *.lua, *.sql, *.html, *.css, *.scss, *.sass, *.less
alwaysApply: false
---
# Coding Principles

**Priority**: High  
**Instruction**: MUST follow all of the principles below

## NoSideEffects

** Definition**: When applying changes, do not delete existing code, comments, commented-out code, etc. unless it is directly related to the code being changed.

## CDAbsPathBeforeRun

Before running any command, cd into the *absolute path* to the required working directory first, e.g. `cd ~/code/projectdir/subdir && run_command_from_here`

## DRY

**Definition**: Every piece of knowledge must have a single, unambiguous, authoritative representation within a system

### Key Points
- Eliminate code duplication through abstraction
- Centralize business logic in single sources
- Improve maintainability through code reuse

### Consequences
- Risk: Change propagation errors
- Risk: Inconsistent behavior

### Solution
- Abstract shared logic
- Centralize business rules

### Implementation Methods
- Parameterization
- Inheritance patterns
- Configuration centralization

## SingleResponsibility

**Definition**: Each code entity should have single responsibility and consistent meaning

### Key Points
- Functions/classes should do one thing well
- Avoid multi-purpose variables
- Prevent context-dependent behavior

## KISS

**Definition**: Prioritize simplicity in design and implementation
### Benefits
- Reduced implementation time
- Lower defect probability
- Enhanced maintainability

### Metrics
- Cyclomatic complexity < 5

### Implementation
- Do the simplest thing that could possibly work
- Avoid speculative generality

## CognitiveClarity

**Definition**: Code should be immediately understandable

**Sub-principle: DontMakeMeThink**:
- Definition: Minimize cognitive load through immediate understandability
- Metrics:
  - Time-to-understand < 30 seconds
  - Zero surprise factor

### Implementation
- Meaningful naming conventions
- Predictable patterns
- Minimal mental mapping requirements

## YAGNI

**Definition**: Implement features only when actually needed
### Original Justification
- Save time by avoiding unneeded code
- Prevent guesswork pollution

## OptimizationDiscipline

**Definition**: Delay performance tuning until proven necessary

**Quote**: "Premature optimization is the root of all evil" - Donald Knuth

### Guidelines
- Profile before optimizing
- Focus on critical 3%

### Statistics
- Critical section percentage: 3%
- Non-critical optimization attempts: 97%

## BoyScout

**Definition**: Continuous incremental improvement of code quality

### Practice
- Opportunistic refactoring
- Technical debt reduction
- Immediate cleanup of discovered issues
- Approval from User is Required
- Track Technical Debt

### Quality Metrics
- Code health index ≥ 0.8

**Degradation Rate**: 5% (Allowed monthly decline)

### Rationale
- Counteracts natural code quality decay
- Reduces technical debt compound interest

## MaintainerFocus

**Definition**: Code for long-term maintainability

### Considerations
- Assume unfamiliar maintainers
- Document non-obvious decisions
- Anticipate future modification needs

**Quote**: "Always code as if the person who ends up maintaining your code is a violent psychopath who knows where you live" - Martin Golding

### Practice
- Assume zero domain knowledge in maintainers

### Time Factor
- Assume 6-month knowledge decay
- Code becomes foreign after 1 year

## LeastAstonishment

**Definition**: Meet user expectations through predictable behavior
### Implementation
- Consistent naming
- Standard patterns
- Minimal side effects

### Violation Examples
- Unexpected side effects in getter methods
- Non-standard exception throwing patterns
### Convention Rules
- Follow language idioms
- Maintain consistent error handling

## VerifyEarlyAndOften

**Definition**: Verify code correctness early and often
### Key Points
- Test early and often
- Code and verify incrementally
- Use unit tests
- Use integration tests
- Run the tests often
- You are not done until all the tests pass.
### Implementation
- Limit the scope of changes at one time
- Strive to avoid large leaps in complexity at any step
- Write unit tests for all functions
- Use integration tests for system-level validation
- Use separate AI integration tests to verify prompts/responses, using the real model.
### Violation Examples
- No unit tests for critical functions
- Lack of integration tests
- Failure to run tests after making changes to source or test code
- Failure to ensure passing tests
- AI integration tests that only use mock responses
### Convention Rules
- Use test-driven development
- Implement automated testing

## NoGiantLeaps

**Definition**: Don't try to make big changes all at once; take incremental steps that can be tested along the way.
### Key Points
- Break down large tasks into smaller, manageable steps
- Test each step before proceeding
- Ensure each step adds value and is reversible
- Avoid introducing unnecessary complexity
### Violation Examples
- Attempting a large refactor without incremental testing
## NoSyntheticData

**Definition**: If you encounter a problem when working with data, NEVER fall back to some fake or simplified data. You can do this in a test in order to debug the issue, but NEVER use fake data in non-test code.
### Violation Examples
- Using fake data in non-test code
- Using simplified data in non-test code

## AskUserForStrategyChoices

**Definition**: If you have a choice of strategies, ask the user for their preference; don't make assumptions about the best strategy.
### Violation Examples
- "Here a number of approaches [...] Let's do option 3 because it's the best one"
- "We could either: a) b) or c) [...] Let's implement b) as it seems more practical

## AskUserBeforeChangingRequirements

**Definition**: If you encounter a problem, ask the user for help before giving up on the given task and doing something simpler or easier.

### Violation Examples
- "I couldn't get this to work, so let's just [do something simpler or easier]"
- "I couldn't get this to work, so let's just [do the thing the user already told us not to do], since it's easier and more straightforward"

## NoPlaceholdersWithoutApproval

**Definition**: If you are implementing a feature, implement it fully and correctly. Do not put placeholders or partial implementations in the code.

### Requirements
- If you are implementing a feature, implement it fully and correctly. Do not put placeholders or partial implementations in the code.
- If you are not sure about the implementation, ask the user for help.
- If you are not sure about the requirements, ask the user for clarification.
- If something is too big or complex, break it down into smaller, manageable steps, document the plan, and inform the user about it.

### Violation Examples
- Leaving a placeholder implementation in the code
- Having a TODO comment in the code without a real implementation
- Having a method with an empty body and just 'pass' as the implementation
- "Insert real implementation here"
- "Later we will add the real implementation"
- "This is a placeholder implementation"

## NoMagicValues

**Definition**: Do not embed important scalar values in the code. Instead, define constants for them, or even better, use a configuration file.

### Violation Examples
- Using an int or float directly in the code
- Using a regular expression directly in the code
- Using an absolute path directly in the code
- Using a URL string directly in the code

## NoVictoryWithoutVerification

Alias: .v

**Definition**: When you have completed a task, do not say you are done, nor mark any tasks as done, until you and the user have confirmed the task was completed correctly. 

### Instead:
- Whenever possible, verify the task with automated tests. If automated tests are not possible, or you have been instructed not to use them, direct the user on how to verify the task as appropriate, e.g. via manual testing scenarios, reviewing automated tests reports, etc.  
- Don't return control to the user until you have verified the task was completed correctly, or you have asked the user for verification, or you need to ask a question or an important decision needs to be made.


## ProveItToMe

alias: .pi

**Definition**: If you have completed a task, prove it to the user by showing them the result in the form of a complete list of passing test cases, screenshots, etc.

## ItsNotDoneUntilItCompletelyWorks

alias: .nd, .ndy, .ynd

**Definition**: Do not mark a task as done until the *functionality* is completely working. No partial victories are acceptable.

### Violation Examples
- "______ is still broken but I've fixed the primary issue"
- "We've validated _____; the test failures are unrelated"
- "The API call is working!" (but the UI is still broken or unknown)
- "The data is being sent correctly!" (but the processing on either end is still broken or unknown)

## KeepItProfessional

**Definition**: 

### Standards

- Use emoji only when it's helpful visually to distinguish between different types of messages.
- No emoji in docs.
- No emoji in code comments.
- No emoji in bullet lists.
- No emoji in logs unless it's for readability.
- No ALL CAPS in responses.
- No excessive exclamation marks.


### Violation Examples
- "MISSION ACCOMPLISHED!"
- "features: - 🧰 scalable \n - 🔒 secure"
- "Success! 🎉"


## ImNotAbsolutelyRight

aliases: .nyr, .inar, .ynar

** Definition**: Never say anything like "that's absolutely correct!" or "that's absolutely right" or "I see the issue" 

### Violation Examples
- "You're absolutely right!"
- "That's absolutely correct!"
- "That's absolutely right"
- "That's a great idea!"
- "That's a great insight!"
- "That's a great observation!"
- "That's a great suggestion!"
- "That's a great catch!"
- "I see the issue" (this should be reserved for when you've found the root cause of the issue)

## NoChangelogComments

**Definition**: Do not include comments that indicate what you changed

### Violation Examples
- "This now __________"
- "Removed the call to ____"

## NoShortcuts

**Definition**: Do not fall back to shortcuts or quick fixes. Always do the right thing. If there's no other option, ask the user for help.

### Violation Examples
- "We'll do ____ for now"
- "The tests didn't work, let me create a standalone test"

## NoLazyPatternMatching

**Definition**: You must not fall back to pattern matching or heuristics. Always try to do the real version of the thing you are trying to do. If there's no other option, you must ask the user for help, do not proceed without their explicit approval.

### Violation Examples

```
def _fallback_button_detection(page):

  # Look for common button patterns
  common_patterns = [
      ('submit_button', ['button[type="submit"]', 'button:has-text("Submit")', '.submit-button']),
      ('next_button', ['button:has-text("Next")', 'button:has-text("Continue")', '.next-button']),
      ('login_button', ['button:has-text("Login")', 'button:has-text("Sign in")', '.login-button']),
  ]
  for action_name, selectors in common_patterns:
      for selector in selectors:
          button = page.locator(selector)
          if button.is_visible():
              return action_name
    return None
```