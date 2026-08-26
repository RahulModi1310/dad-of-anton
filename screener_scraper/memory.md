# Agent Instructions

## Code Style

- DO NOT add comments unless explicitly asked
- DO NOT add type hints unless already present in the file
- Follow existing code conventions in the file you're editing
- Use `snake_case` for functions and variables
- Use `UPPER_SNAKE_CASE` for constants

## File Operations

- NEVER create files unless explicitly asked
- ALWAYS read a file before editing it
- PREFER editing existing files over creating new ones
- Use relative paths when possible

## Git Operations

- NEVER commit unless explicitly asked
- NEVER push unless explicitly asked
- NEVER run `git add`, `git commit`, or `git push` without explicit user permission
- ALWAYS check `git status` before committing
- Remove `__pycache__/` and `output/` from staging before committing

## Communication

- Be concise — no preamble or postamble
- Answer in fewer than 4 lines unless asked for detail
- Show code changes in +/- diff format when discussing changes
- Ask clarifying questions before implementing if requirements are ambiguous

## Error Handling

- If a tool fails, explain why before retrying
- Don't assume URLs unless provided by user
- Don't guess library availability — check first

## Windows-Specific

- Use `cmd /c` for chained commands (PowerShell doesn't support `&&`)
- Path separators: forward slashes in Python, backslashes in cmd
- Test scripts before declaring them working

## Planning Mode

- When in plan mode, DO NOT make any edits
- Present changes in diff format for approval
- Ask clarifying questions before proceeding
- Wait for explicit "go" or "yes" before implementing
