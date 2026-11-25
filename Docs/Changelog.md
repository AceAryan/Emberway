# Changelog

## Phase 0 — Foundation (in progress)

### Changed
- `HealthComponent` exposes a `Died` event and `ResetHealth()`. It no longer checks the `Player` tag or publishes global events. Negative damage and heal amounts are ignored.
- `Entity` subscribes to `HealthComponent.Died` and calls the virtual `Die()`, so enemies are now destroyed at 0 HP.
- `PlayerController.Die()` publishes `PlayerDiedEvent` (sole publisher) without destroying the player.
- `GameManager` subscribes to `PlayerDiedEvent` → `GameOver`. `GameOver` no longer publishes `PlayerDiedEvent`, which removes a potential infinite loop. Boot → MainMenu is no longer triggered from inside `OnEnter`. Same-state transitions are ignored.
- `PlayerStateMachine` no longer publishes `PlayerDiedEvent`.
- `EventBus.Publish` iterates a snapshot and isolates handler exceptions. All buses are cleared at play-mode start (`EventBusRegistry`).

### Added
- `Emberway.asmdef` runtime assembly.
- `Emberway.Tests.EditMode` assembly with `HealthComponentTests`.
- `Docs/` technical documentation.

## Pre-Phase 0
- Initial prototype: player movement, jump, attack hitbox, patrol enemy, EventBus, GameManager FSM, HealthComponent.
