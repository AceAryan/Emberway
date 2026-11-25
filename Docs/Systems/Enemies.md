# Enemies

`Scripts/Entities/Enemies/Enemy.cs`, `PatrolEnemy.cs`

## Enemy (abstract)

| Field | Default | Purpose |
|---|---|---|
| `_moveSpeed` | 3 | Movement speed |
| `_damage` | 1 | Contact damage (used from Phase 2) |
| `_detectionRange` | 5 | Player detection radius (gizmo shown when selected) |

- Finds the `Player`-tagged object in `Awake`.
- `Update` calls the abstract `UpdateBehavior()` while alive.
- `Die()` destroys the GameObject (death VFX planned).

## PatrolEnemy
- **Patrol:** walks back and forth within `_patrolDistance` of its spawn X position.
- **Chase:** moves toward the player's X position while the player is within detection range.
- Movement is velocity-based (`Rigidbody2D`).

## Adding an archetype
Derive from `Enemy`, implement `UpdateBehavior()`, and add `Rigidbody2D`, `Collider2D` and `HealthComponent`. Tag it `Enemy`. A state-machine-based enemy framework replaces this pattern in Phase 4.
