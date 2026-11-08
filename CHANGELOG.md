# Changelog

All notable changes to this project are documented here, in the style of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.3] - 2026-11-08

### Added
- Two worked examples in SKILL.md ("Should I add an MCP server for this?" and "The agent said it saved the file, but it isn't there.").
- This changelog.
- Standing efficiency policy section in docs/ENGINEERING-RESOURCES.md (dated 2026-10-29).

### Changed
- README version, document register and package list updated; the architecture diagrams link moved under "Use the skill".

### Removed
- Leftover push instructions, folder `.gitignore` and `.github` templates from the historical architecture reference, including a personal local file path.
- Links to a private repository in `docs/ARCHITECTURE-OPTIONS.md`, replaced with plain text.

### Notes
- Version 0.1.3 was rechecked on the neutral and educational prompts on 2026-11-08, with no measurable change from 0.1.2 (see the README's baseline comparison).

## [Documentation addendum] - 2026-10-15

### Added
- `docs/ENGINEERING-RESOURCES.md`: engineering backlog, evaluation/tracing contracts and future capability policy.
- `docs/ARCHITECTURE-OPTIONS.md`: architecture diagrams and implementation options.
- Links to tested optional extension prototypes.

### Notes
- Documentation only; skill version 0.1.2 and historical evaluation results unchanged.

## [0.1.2] - 2026-09-27

### Changed
- Activation boundary: added one sentence so answers stay in scope when the skill does not apply (fixes over-application on educational questions such as "What is RAG?").

### Added
- Baseline with/without-skill results and 0.1.2 rechecks in the README.

## [0.1.1] - 2026-09-12 to 2026-09-20

### Added
- Initial release of the skill, `.gitignore` and project record (2026-09-12).
- Evaluation documentation through Gate 4: the 18-case suite, and Gate 2, Gate 3 and Gate 4 records and results PDF (2026-09-20).

### Changed
- Refined the skill's discovery description (2026-09-20).
