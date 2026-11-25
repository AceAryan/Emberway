# 0003 — Single source of truth for death

**Status:** Accepted (Phase 0)

## Context
`PlayerDiedEvent` was published from three places: `HealthComponent` (tag check), `PlayerStateMachine` (Dead state) and `GameManager` (GameOver state). Meanwhile, entities were never destroyed at 0 HP because `HealthComponent` did not call `Entity.Die()`. If `GameManager` had subscribed to the event, `GameOver` → publish → `GameOver` would have created a feedback loop.

## Decision
- `HealthComponent` raises a local `Died` event and has no knowledge of its owner.
- `Entity` subscribes and calls the virtual `Die()`.
- `PlayerController.Die()` is the **only** publisher of `PlayerDiedEvent`.
- `GameManager` only consumes `PlayerDiedEvent`.

## Consequences
- Every death is handled exactly once, by the owning entity's `Die()` override.
- `HealthComponent` is reusable for any object, with no tag dependencies.
- Rule going forward: state machines react to events and do not re-broadcast them.
