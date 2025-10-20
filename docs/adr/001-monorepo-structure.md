# ADR 001: Monorepo Structure

**Status:** Accepted  
**Date:** 2025-10-20  
**Deciders:** Engineering Team

## Context

The TLS AI/AR production system consists of multiple services, shared libraries, and infrastructure components. We need to decide on a repository structure that facilitates:
- Code sharing between services
- Consistent versioning
- Atomic changes across services
- Clear separation of concerns
- Easy developer onboarding

## Decision

We will use a **monorepo structure** with the following organization:

```
TLS-Concept-production-2.0/
├── apps/           # Microservices and applications
├── packages/       # Shared libraries and utilities
├── docs/           # Documentation and policies
├── tests/          # Test suites
└── infra/          # Infrastructure as code
```

### Rationale

**Advantages:**
1. **Shared Code Management**: Event contracts, models, and utilities can be shared across services without package publishing overhead
2. **Atomic Changes**: Cross-service changes can be committed and tested together
3. **Consistent Tooling**: Single CI/CD pipeline, linting, and testing configuration
4. **Simplified Dependencies**: Direct imports between packages without version management complexity
5. **Better Discoverability**: All code is in one place, making it easier for developers to understand the system

**Disadvantages:**
1. **Build Complexity**: Need to manage which services to build/deploy
2. **Repository Size**: Could grow large over time
3. **Access Control**: Cannot easily restrict access to specific services

### Alternatives Considered

1. **Multi-repo (Microservices per repo)**
   - Rejected: Would require publishing shared packages, versioning complexity, and difficulty making atomic cross-service changes

2. **Multi-repo with shared packages repo**
   - Rejected: Still requires package publishing and version management overhead

## Consequences

**Positive:**
- Faster development with shared code
- Easier refactoring across services
- Simplified dependency management
- Single source of truth for models and contracts

**Negative:**
- Need tooling to determine what changed and what to deploy
- CI/CD must be efficient to avoid long build times
- Git history includes all services

## Implementation

- Use Python's `sys.path` manipulation for local package imports
- Implement selective CI/CD based on changed paths
- Use shared requirements.txt for common dependencies
- Structure apps as independently runnable services
