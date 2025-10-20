# ADR 002: Policy-Based Access Control

**Status:** Accepted  
**Date:** 2025-10-20  
**Deciders:** Engineering Team

## Context

The system needs to control when vehicles can be started, unlocked, or driven based on:
- SOP completion status
- QA inspection results
- Defect presence
- User certifications
- Customer priority (hot units)

The access control logic must be:
- Easy to modify without code changes
- Auditable and traceable
- Testable in isolation
- Expressive enough for complex rules

## Decision

We will implement a **declarative rules engine** using YAML-based policy definitions.

### Policy Format

```yaml
version: v1
name: Vehicle Access Control Policy
rules:
  - id: grant-start-after-qa
    priority: 100
    conditions:
      all:
        - field: vehicle.status
          operator: "=="
          value: install_done
        - field: qa.status
          operator: "=="
          value: green
    actions:
      - type: grant
        scope: start
        ttl_seconds: 1800
        reason: "Install+QA green"
```

### Rules Engine

The engine evaluates policies against context (vehicle state, QA results, defects, user info) and returns grant/deny decisions with reasons.

**Features:**
- Priority-based rule ordering
- Support for AND (`all`) and OR (`any`) conditions
- Nested field access (e.g., `vehicle.install.progress.percent`)
- Multiple comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`, `in`, `not_in`)
- Deny takes precedence over grant

## Rationale

**Why policy-based instead of hardcoded:**
1. **Flexibility**: Rules can be modified without code deployment
2. **Auditability**: All access decisions are based on versioned policies
3. **Testability**: Policies can be tested independently with various contexts
4. **Maintainability**: Non-developers can understand and propose rule changes
5. **Compliance**: Easy to demonstrate access control logic to auditors

**Why YAML over alternatives:**
- Human-readable and writable
- Well-supported tooling
- Version control friendly
- No executable code (safer)

### Alternatives Considered

1. **Hardcoded Logic in API**
   - Rejected: Difficult to modify, test, and audit

2. **Database-Stored Rules (UI-Configured)**
   - Rejected for V1: Adds complexity, need version control for policies anyway

3. **Python-Based DSL**
   - Rejected: Requires programming knowledge, harder to audit

4. **External Policy Engine (OPA/Cedar)**
   - Considered for future: V1 custom implementation is simpler and sufficient

## Consequences

**Positive:**
- Clear separation between policy and implementation
- Easy to add new rules without code changes
- Policies are version-controlled with code
- Can simulate policy changes before deployment
- Support for hot-reloading policies

**Negative:**
- Need to implement custom evaluation engine
- Limited expressiveness compared to full programming language
- Performance consideration for complex policies (mitigated by caching)

## Implementation

1. **Rules Engine Package**: `packages/rules-engine/`
2. **Policy Storage**: `docs/policies/*.yaml`
3. **Evaluation**: On each access request, load policy and evaluate against context
4. **Caching**: Cache compiled policies, invalidate on file change
5. **Testing**: Unit tests for engine, integration tests for policies

## Future Enhancements

- Policy validation on commit via CI/CD
- Policy simulation tool
- Multiple policies per scope
- Time-based rules (e.g., grant access only during business hours)
- Rate limiting and quota rules
