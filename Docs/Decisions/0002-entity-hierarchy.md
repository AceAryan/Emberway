# 0002 — Inheritance for entities, composition for capabilities

**Status:** Accepted

## Context
Players, enemies and destructibles share behavior (taking damage, dying) but differ in control logic. Pure inheritance leads to deep hierarchies, and pure composition spreads simple logic across many components.

## Decision
A shallow `Entity` → `Enemy` / `PlayerController` hierarchy defines identity and overridable lifecycle (`Die`). Reusable capabilities (health, and later posture, knockback, hurtboxes) are separate components the entity coordinates.

## Consequences
- New enemy types require a single subclass implementing `UpdateBehavior()`.
- Capabilities are testable in isolation (see `HealthComponentTests`).
- The hierarchy should stay shallow (≤ 3 levels). Shared behavior that only some subclasses need belongs in a component.
