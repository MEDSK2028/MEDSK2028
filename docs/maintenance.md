# Profile maintenance

This profile is intentionally self-contained. All visuals are committed SVG files, no JavaScript runs in the README, and no hosted statistics service is required.

## Requirements

- Python 3.11 or newer

The generator uses only the Python standard library and requires no `pip install` step.

## Regenerate the profile

From the repository root:

```bash
python scripts/generate_profile_assets.py
python scripts/validate_profile.py
python -m unittest discover -s tests -v
```

`generate_profile_assets.py` owns every terminal visual, including responsive desktop and mobile variants for the hero, selected projects, and engineering footprint.

## Content integrity

- Project summaries must stay grounded in repository documentation or information explicitly supplied for this profile.
- The engineering footprint maps technologies to selected projects; it does not claim contribution counts, years of experience, or performance results.
- Private project code and repository URLs are deliberately omitted from the public README.
- No personal access token, API key, or other secret is required.
