# Event Bus

`Assets/_Project/Scripts/Core/EventBus.cs`, events in `Core/GameBus.cs`

## Purpose
Global, type-safe publish/subscribe for communication between systems that should not reference each other directly. Each event struct type `T` has its own independent handler list.

## API

| Member | Description |
|---|---|
| `EventBus<T>.Subscribe(Action<T>)` | Registers a handler. Duplicate registrations are ignored. |
| `EventBus<T>.Unsubscribe(Action<T>)` | Removes a handler. |
| `EventBus<T>.Publish(T)` | Invokes all handlers synchronously. |
| `EventBus<T>.Clear()` | Removes all handlers for `T`. |

## Behavior
- **Snapshot iteration:** handlers may subscribe or unsubscribe during `Publish`. Changes take effect on the next publish.
- **Exception isolation:** an exception in one handler is logged and does not prevent other handlers from running.
- **Play-mode reset:** every `EventBus<T>` registers with `EventBusRegistry`, which clears all buses at `RuntimeInitializeLoadType.SubsystemRegistration`. This keeps behavior correct when domain reload is disabled.

## Usage

```csharp
private void OnEnable()  => EventBus<PlayerDiedEvent>.Subscribe(OnPlayerDied);
private void OnDisable() => EventBus<PlayerDiedEvent>.Unsubscribe(OnPlayerDied);
private void OnPlayerDied(PlayerDiedEvent e) { /* ... */ }
```

Subscribers **must** unsubscribe in `OnDisable` / `OnDestroy`. Handlers are held by a static list and would otherwise reference destroyed objects.

## Events

| Event | Payload | Publisher | Subscribers |
|---|---|---|---|
| `PlayerDiedEvent` | — | `PlayerController.Die()` | `GameManager` |
| `CheckpointReachedEvent` | `CheckpointIndex` | *(Phase 5)* | — |
| `GameCompletedEvent` | — | `GameManager` (GameCompleted) | — |
| `CollectiblePickedUpEvent` | `CollectibleID` | *(Phase 6)* | — |

## Guidelines
- Each event has exactly one conceptual publisher.
- Do not publish an event from a handler of the same event.
- Use direct references or C# events for communication within a single GameObject.
