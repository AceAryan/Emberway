# Roadmap

Status: ✅ done · 🔨 in progress · ⬜ planned

| Phase | Focus | Key deliverables | Status |
|---|---|---|---|
| 0 | Foundation | Bug fixes, single death flow, event bus hardening, assembly definitions, EditMode tests, documentation | 🔨 |
| 1 | Movement feel | Coyote time, jump buffering, variable jump height, dash, Cinemachine camera | ⬜ |
| 2 | Combat core | Attack combo, hurt state with knockback and i-frames, enemy contact damage, health UI | ⬜ |
| 3 | Deflect & posture | Parry window, posture/stagger meter, perfect-parry rewards, hit-stop | ⬜ |
| 4 | Enemy AI | Enemy FSM framework, telegraphed attacks, 3+ archetypes | ⬜ |
| 5 | World | Tilemap rooms, room transitions, save points, save/load, death & respawn | ⬜ |
| 6 | Progression | Ability-gated areas, skill tree, currency, ScriptableObject-driven data | ⬜ |
| 7 | Bosses | Boss framework (phases, attack patterns), first boss | ⬜ |
| 8 | Presentation | Menus, pause, world map, audio, VFX and game feel | ⬜ |
| 9 | Narrative | Dialogue and cutscene system | ⬜ |
| 10 | Release | Polish, performance, build pipeline | ⬜ |

## Phase 0 — Foundation

- [x] Death flow: `HealthComponent.Died` → `Entity.Die()` (virtual) → single `PlayerDiedEvent` publisher
- [x] `GameManager` reacts to `PlayerDiedEvent` instead of re-publishing it; Boot no longer transitions re-entrantly
- [x] `EventBus` snapshot iteration, per-handler exception isolation, clear on play-mode start
- [x] `Emberway` runtime assembly and `Emberway.Tests.EditMode` test assembly; `HealthComponent` tests
- [ ] Attack hitbox placed on the facing side
- [ ] Patrol enemy direction derived from position (no jitter); physics in `FixedUpdate`
- [ ] Attack cooldown / overlapping attack coroutines
- [ ] `PlayerState.Jumping` reachable
- [ ] Remove per-frame logging
