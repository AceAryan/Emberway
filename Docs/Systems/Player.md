# Player

`Scripts/Entities/Player/PlayerController.cs`, `PlayerStateMachine.cs`, `Scripts/Systems/AttackHitbox.cs`

## Components on the Player GameObject
`Rigidbody2D`, `Collider2D`, `Animator`, `PlayerInput`, `HealthComponent`, `PlayerController`, `PlayerStateMachine`. Children: `GroundCheck`, `AttackHitbox` (trigger collider, inactive by default).

## Input
`PlayerInput` uses **Send Messages** with `Assets/InputSystem_Actions.inputactions`. Actions map to methods by name:

| Action | Method |
|---|---|
| Move | `OnMove(InputValue)` → caches horizontal input |
| Jump | `OnJump(InputValue)` → sets vertical velocity if grounded |
| Attack | `OnAttack(InputValue)` → `Attack` animator trigger + hitbox coroutine |

## Movement
- Horizontal velocity is set in `FixedUpdate` from cached input.
- Ground detection: `Physics2D.OverlapCircle` at `GroundCheck` (radius 0.1) against the `Ground` layer, evaluated in `Update`.
- Facing: `transform.localScale.x = ±1`. Children (including `AttackHitbox`) mirror with the parent.

## State machine
`PlayerStateMachine` derives `PlayerState` from controller queries (`IsMoving`, `IsJumping`, `IsFalling`, `IsGrounded`). It is observational in Phase 0. Animation is driven separately by Animator parameters.

| State | Exits |
|---|---|
| Idle | → Running (moving), → Jumping (rising), → Falling |
| Running | → Idle (not moving), → Jumping (rising), → Falling |
| Jumping | → Falling |
| Falling | → Idle / Running (grounded) |
| Hurt, Dead | Reserved (Phase 2) |

## Attack
`AttackRoutine` activates the hitbox for `_attackDuration` seconds. `AttackHitbox.OnTriggerEnter2D` damages colliders tagged `Enemy` through `Entity.TakeDamage`.

## Death
`Die()` is overridden to publish `PlayerDiedEvent`. The player GameObject is not destroyed.
