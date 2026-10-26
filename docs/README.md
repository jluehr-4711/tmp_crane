# Project documentation index

Project: control a **Crane Sports Power X6 Crosstrainer-Ergometer** (Royalbeach Art.-Nr. 33821,
Aldi Süd 2006) with an ESP32, while keeping the original console swappable.

| Doc | Purpose |
|-----|---------|
| [01-project-overview.md](01-project-overview.md) | Goal, rules, big picture, phases |
| [02-material-inventory.md](02-material-inventory.md) | Every file in `material/` and what it tells us |
| [03-hardware-reference.md](03-hardware-reference.md) | The machine: electrical system, parts, boards, connectors, known/unknown |
| [04-plan.md](04-plan.md) | Phased plan (wiring first, then software), next concrete steps |
| [05-open-questions.md](05-open-questions.md) | Questions for the owner + unknowns to measure |
| [06-photo-guide.md](06-photo-guide.md) | What to photograph before the measurement session, with plain-language locations |
| [sessions/](sessions/) | One log per session, newest last |
| [reference/](reference/) | Extracted manual text (greppable) |
| [img/](img/) | Crops and rendered manual pages used by the docs |

## Conventions

- Every session gets `sessions/YYYY-MM-DD-session-NN.md`: what was done, what was found, what is next.
- Measurements go into `03-hardware-reference.md` (facts) and the session log (how obtained).
- Part numbers in parentheses, e.g. "(91)", refer to the manual's spare-parts list (page 19).
- Unverified statements are marked **[assumption]**. Remove the tag once measured.
- Language: English, with original German terms in quotes where they help find things in the manual.
