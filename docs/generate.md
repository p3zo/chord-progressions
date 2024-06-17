# Generate

## Constraints

```markdown
pct_notes_common: int, default 0

    The percent of pitch classes held in common between adjacent chords.
    Higher values help the generator create more coherent progressions.

note_range_low: int, default 60

    The lowest midi note number that the generator is allowed to use.

note_range_high: int, default 108

    The highest midi note number that the generator is allowed to use.

allowed_chord_types: list, default []

    The list of chord types that the generator is allowed to use.
    See the list of type templates in the [type_templates module](./type_templates.py].
```

Note that if you set the generator parameters to be overly restrictive, the generator will not be able to find a
progression that meets the constraints. 
