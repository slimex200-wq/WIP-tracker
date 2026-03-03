# Global Claude Code Configuration
# Place this file at: ~/.claude/CLAUDE.md

---

## Communication
- Respond in Korean
- Be concise and direct — no filler phrases
- When uncertain, ask before acting

---

## Core Philosophy
- Incremental progress over big bangs — small changes that compile and pass tests
- Clear intent over clever code — boring and obvious beats clever
- Pragmatic over dogmatic — adapt to project reality
- Study existing patterns before implementing anything new

---

## Workflow: Always Plan Before Coding
1. Understand existing code patterns first
2. Break complex work into 3–5 stages
3. Show the plan and wait for approval before writing code
4. Implement one stage at a time
5. Run tests after each change

If stuck after 3 attempts:
- Stop and document what failed
- Propose alternative approaches
- Ask for guidance — never spin in circles

---

## Code Quality Rules

**Every commit must:**
- Compile successfully
- Pass all existing tests
- Include tests for new functionality
- Follow project formatting/linting standards

**NEVER:**
- Use `--no-verify` to bypass commit hooks
- Disable or skip tests instead of fixing them
- Commit broken or untested code
- Make assumptions — verify with existing code

**ALWAYS:**
- Commit working code incrementally
- Handle errors with descriptive messages (never silently swallow exceptions)
- Prefer composition over inheritance
- Use dependency injection to enable testability

---

## Before Making Changes
- List all files that will be affected
- Confirm before deleting or overwriting anything
- Do not refactor code that wasn't requested
- Do not introduce new dependencies without strong justification

---

## Git
- Write clear commit messages explaining *why*, not just *what*
- Never commit directly to `main` or `master`
- Follow conventional commits format if the project uses it

---

## Testing
- Write tests before implementation when possible (TDD)
- Test behavior, not implementation details
- One assertion per test when possible
- Use descriptive test names that explain the scenario
- Tests must be deterministic — no random or time-dependent behavior

---

## Decision Framework
When multiple valid approaches exist, choose based on:
1. **Testability** — Can I easily test this?
2. **Readability** — Will someone understand this in 6 months?
3. **Consistency** — Does this match project patterns?
4. **Simplicity** — Is this the simplest solution that works?
5. **Reversibility** — How hard to change later?
