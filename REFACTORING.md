# Refactoring notes

## Initial design problems

| Problem | Type | Why it made changes harder |
|---|---|---|
| HTTP handling, SQL, business rules, validation, and notifications were in the same file | Cohesion | A change to one responsibility required editing a large file containing unrelated code |
| Route handlers opened SQLite connections and contained queries | Coupling | Changing the database or schema also required changing the HTTP layer |
| The fine rate and fine calculations were repeated | Coupling | A rate change could be applied inconsistently across loans, members, and reports |
| `CURRENT_MEMBER` shared notification state between requests | Coupling | Notifications depended on call order and could use the wrong member during concurrent requests |
| `check(value, kind)` used a string to choose unrelated validation rules | Coupling | Adding or changing one validation rule required modifying a shared control function |
| Routes wrote notification messages directly to `outbox.txt` | Cohesion | Changing the notification mechanism required editing loan behavior |

## Result

| Measure | Before | After |
|---|---:|---:|
| Tests passing | 53 | 53 |
| Lines in the largest application file | 555 | 141 |
| Places where the fine rate appears | 7 | 1 |
| Route handlers containing SQL | 16 | 0 |
| Places that open the database | 17 | 1 |
| Can the fine rule be tested without HTTP or a database? | No | Yes |

The instructor's separate change request was not provided, so the number of places edited for it cannot be measured yet.

## Design questions

1. `fines.py` is the most cohesive module. Its only job is calculating and formatting fines.
2. Route handlers no longer depend directly on SQLite. The HTTP API and database queries can now change independently through the service and repository layers.
3. Services still depend on repository modules, and loan operations depend on book and member data. This coupling represents the library workflow and keeps the small project straightforward without adding a dependency-injection framework.
