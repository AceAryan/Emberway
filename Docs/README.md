# Emberway — Technical Documentation

Emberway is a 2D action-platformer with metroidvania structure, built in Unity 6.3 LTS (2D URP). This folder documents the game's architecture, systems and design decisions.

| Document | Contents |
|---|---|
| [Story](Story.md) | Premise, structure, characters, progression |
| [Roadmap](Roadmap.md) | Development phases and status |
| [Architecture](Architecture.md) | System overview, data flow, conventions |
| [Changelog](Changelog.md) | Changes per phase |
| **Systems** | |
| [Event Bus](Systems/EventBus.md) | Global typed publish/subscribe |
| [Game Manager](Systems/GameManager.md) | Top-level game state machine |
| [Entities & Health](Systems/Entities.md) | Entity hierarchy, health and death flow |
| [Player](Systems/Player.md) | Movement, input, state machine, attack |
| [Enemies](Systems/Enemies.md) | Enemy base class and archetypes |
| [Art Pipeline](Systems/ArtPipeline.md) | Code-generated pixel art, specs, asset replacement |
| **Decisions** | |
| [0001 — Event bus for cross-system communication](Decisions/0001-event-bus.md) | |
| [0002 — Inheritance for entities, composition for capabilities](Decisions/0002-entity-hierarchy.md) | |
| [0003 — Single source of truth for death](Decisions/0003-death-flow.md) | |
