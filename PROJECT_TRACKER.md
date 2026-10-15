# TraceLess Project Tracker

> **Status:** Planning and backlog creation
> **Backend:** Python + FastAPI
> **Last updated:** 2026-10-15

## Goal

Build TraceLess, a privacy-first digital-footprint risk analyzer that turns user-authorized inputs and permitted sources into clear findings, explainable risk levels, and practical remediation guidance.

## Current GitHub tracker

The [MVP tracking issue](https://github.com/Sanjuar/TraceLess/issues/1) is the high-level tracker. Work should be tracked in individual issues below.

### Phase 1: Planning and design

- [ ] [#2 Document system architecture and interaction flow](https://github.com/Sanjuar/TraceLess/issues/2)
- [ ] [#4 Define scan input validation and authorized analysis boundaries](https://github.com/Sanjuar/TraceLess/issues/4)
- [ ] [#5 Design finding schema and explainable risk scoring model](https://github.com/Sanjuar/TraceLess/issues/5)
- [ ] [#13 Review threat model and security edge cases](https://github.com/Sanjuar/TraceLess/issues/13)
- [ ] [#15 Research privacy-safe data-breach exposure checks](https://github.com/Sanjuar/TraceLess/issues/15)

### Phase 2: Backend foundation

- [ ] [#3 Initialize Python project structure and FastAPI application](https://github.com/Sanjuar/TraceLess/issues/3)
- [ ] [#7 Build scan API endpoints with FastAPI](https://github.com/Sanjuar/TraceLess/issues/7)
- [ ] [#6 Implement first analysis module with normalized findings](https://github.com/Sanjuar/TraceLess/issues/6)
- [ ] [#9 Add privacy-first data retention and deletion rules](https://github.com/Sanjuar/TraceLess/issues/9)

### Phase 3: User experience

- [ ] [#8 Build scan report UI and remediation guidance](https://github.com/Sanjuar/TraceLess/issues/8)

### Phase 4: Testing and release

- [ ] [#10 Add automated tests for API, validation, and scoring](https://github.com/Sanjuar/TraceLess/issues/10)
- [ ] [#11 Set up CI checks and secure configuration](https://github.com/Sanjuar/TraceLess/issues/11)
- [ ] [#12 Write README and local developer setup guide](https://github.com/Sanjuar/TraceLess/issues/12)
- [ ] [#14 Prepare MVP end-to-end demo and release checklist](https://github.com/Sanjuar/TraceLess/issues/14)

## Definition of done

- [ ] Acceptance criteria for the issue are satisfied.
- [ ] Tests are added or updated where applicable.
- [ ] Documentation and examples remain current.
- [ ] No secrets or unnecessary personal data are logged or committed.
- [ ] Analysis uses user-submitted or otherwise authorized data and sources.
- [ ] Severity and confidence are explained separately, and limitations are clear.

## Privacy and security principles

- Analyze only user-provided or otherwise authorized data and permitted sources.
- Do not bypass authentication, access controls, or source protections.
- Minimize personal data collected, returned, logged, and retained.
- Do not download, expose, or display stolen credentials.
- Treat breach exposure as a sourced finding, not proof that an account is currently compromised.
- Use synthetic fixtures in tests.

## Architecture reference

Keep the implementation aligned with the [TraceLess Interaction Model and System Architecture in Notion](https://app.notion.com/p/TraceLess-Interaction-Model-System-Architecture-3f92065960bf8110a46df06a13556ebc).

## Issue board

[Open TraceLess GitHub Issues](https://github.com/Sanjuar/TraceLess/issues)
