# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Emberway — a 2D action-metroidvania: the player is a teenage girl escorting a rescued red baby dragon (an evolving companion that grants abilities) home across biomes; see `Docs/Story.md`. The user's original story draft is in the Obsidian vault (`story idea.md`). Art is produced by Claude (pixel art, generator scripts kept in the repo); the user gives direction. Unity **6000.3.15f1** (Unity 6.3 LTS), 2D URP, new Input System, Aseprite art via `com.unity.2d.aseprite`.

## Commands

There is no CLI build/lint pipeline; work happens in the Unity Editor. The only scene is `Assets/_Project/Scenes/SampleScene.unity`.

Tests use the Unity Test Framework. Runtime code compiles into the `Emberway` assembly (`Assets/_Project/Scripts/Emberway.asmdef`, references `Unity.InputSystem`; add new package assemblies there when needed). EditMode tests live in `Assets/_Project/Tests/EditMode` (`Emberway.Tests.EditMode.asmdef`). Headless run (Editor must be closed, and Unity Hub must be running and signed in or licensing fails with exit 198):

```
"C:\Program Files\Unity\Hub\Editor\6000.3.15f1\Editor\Unity.exe" -batchmode -projectPath . -runTests -testPlatform EditMode -testResults results.xml -logFile unity.log
```
Add `-testFilter <TestName>` for a single test. `Awake` does not run for components added in EditMode tests, so components expose explicit initializers (e.g. `HealthComponent.ResetHealth()`).

## Collaboration workflow (important)

The user is building this as a learning project in **guided mode**: Claude writes specs, notes and infrastructure code; the user writes gameplay logic marked `// TODO (you): Phase N Task M`, then asks Claude to "review task N". Do not implement `TODO (you)` tasks unless the user asks you to. When reviewing, fill the note's *Review* section and log bugs in the Bug Journal.

Every change is documented in two places, with different styles:
- `Docs/` (in repo): professional, concise technical docs (Roadmap, Architecture, Changelog, Systems/, Decisions/ ADRs). Keep Roadmap checkboxes and Changelog current.
- Obsidian vault `D:\Notes\Obsidian\10 Projects\Emberway\`: detailed learning notes for the user. Structure: `00 Emberway Hub.md`, `Phase N - <Name>/NN <Topic>.md`, `Concepts/`, `Bug Journal.md`. Notes use `tags: [ai-edited, emberway, ...]` frontmatter, Mermaid diagrams, `> [!hint]-` collapsible hints for YOUR TURN tasks, and end with `#flashcards` cards in `Question::Answer` format (Spaced Repetition plugin). Don't overwrite the user's own `Emberway notes.md`.

The game is in the Nine Sols-like genre (deflect/parry combat, metroidvania world, bosses, skill tree) but story, characters and art are the user's own.

## Architecture

All game code lives in `Assets/_Project/Scripts/`, global namespace (no namespaces used).

- **EventBus** (`Core/EventBus.cs`): static generic `EventBus<T> where T : struct`. Event types are plain structs declared in `Core/GameBus.cs`. Handlers are static lists — subscribers must `Unsubscribe` in `OnDisable`/`OnDestroy` or they leak across scene loads / play sessions.
- **GameManager** (`Core/GameManager.cs`): `DontDestroyOnLoad` singleton with a `GameState` FSM (`TransitionTo` → `OnExit`/`OnEnter`). Pausing is done via `Time.timeScale`.
- **Entity hierarchy**: `Entity` (abstract, requires a sibling `HealthComponent`) → `PlayerController`, and → `Enemy` (abstract; subclasses implement `UpdateBehavior()`) → `PatrolEnemy`. Damage goes through `Entity.TakeDamage` → `HealthComponent`. Death: `HealthComponent.Died` event → `Entity` (subscribed in `Awake`) → virtual `Die()`. `PlayerController.Die()` is the sole publisher of `PlayerDiedEvent`; `GameManager` only consumes it. Overrides of `Awake`/`OnDestroy` must call base.
- **Player**: `PlayerController` handles physics movement (Rigidbody2D velocity in `FixedUpdate`), ground check via `OverlapCircle` on a `GroundCheck` child, sprite facing by flipping `transform.localScale.x`, and drives the Animator. `PlayerStateMachine` is a separate component that reads `PlayerController`'s public state properties (`IsMoving`, `IsFalling`, `IsGrounded`, …); it does not drive animation.
- **Input**: `PlayerInput` component with *Send Messages* behavior using `Assets/InputSystem_Actions.inputactions`, so input arrives via `OnMove`/`OnJump`/`OnAttack(InputValue)` methods — renaming them breaks input silently.
- **Combat**: `AttackHitbox` is a trigger collider on a child GameObject of Player, toggled active by `PlayerController.AttackRoutine` for `_attackDuration`; it damages colliders tagged `Enemy`.

Conventions relied on by code: tags `Player` and `Enemy`; Animator parameters `Speed` (float), `IsGrounded` (bool), `Attack` (trigger); private serialized fields use `_camelCase`.

## Git

Commit messages follow Conventional Commits (`feat:`, `test:`, `docs:`), small one-feature commits.
