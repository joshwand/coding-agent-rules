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
- 
### Convention Rules
- Follow language idioms
- Maintain consistent error handling

## VerifyEarlyAndOften

**Definition**: Verify code correctness early and often

### Key Points
- Test early and often
- Implement incrementally
- Use unit tests
- Use integration tests

### Implementation
- Limit the scope of changes at one time
- Strive to avoid large leaps in complexity at any step
- Write unit tests for all functions
- Use integration tests for system-level validation

### Violation Examples
- No unit tests for critical functions
- Lack of integration tests

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

## AskUserBeforeChangingRequirements

**Definition**: If you encounter a problem, ask the user for help before giving up on the given task and doing something simpler or easier.

### Violation Examples
- I couldn't get this to work, so let's just do something simpler or easier 
- I couldn't get this to work, so let's just do the thing the user already told us not to do, since it's easier and more straightforward

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

