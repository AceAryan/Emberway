# 0001 — Event bus for cross-system communication

**Status:** Accepted

## Context
Gameplay objects (player, enemies, pickups) need to notify game-flow systems (GameManager, UI, audio, save system) without those systems being wired together in the Inspector or referencing each other's types.

## Decision
Use a static generic `EventBus<T>` keyed by struct event types. Within a single GameObject, use C# events or direct references instead.

## Consequences
- Publishers and subscribers are fully decoupled. New listeners can be added without touching publishers.
- Struct payloads avoid allocations per publish.
- Flow is less visible than direct calls, so each event's publisher and subscribers are tracked in [Event Bus](../Systems/EventBus.md).
- Subscribers must manage their own subscription lifetime (`OnEnable` / `OnDisable`).

## Alternatives considered
- **UnityEvents / Inspector wiring:** visible in the editor, but couples scenes and breaks across scene loads.
- **ScriptableObject event channels:** designer-friendly. Can be adopted later for designer-facing events if needed.
