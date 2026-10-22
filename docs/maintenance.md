# Profile maintenance

This profile is intentionally self-contained. All visuals are committed SVG files, no JavaScript runs in the README, and no hosted statistics service is required.

## Requirements

- Python 3.11 or newer
- Internet access only when refreshing public GitHub contribution data

The generators use the Python standard library and require no `pip install` step.

## Regenerate the profile

From the repository root:

```bash
python scripts/generate_profile_assets.py
python scripts/fetch_contributions.py
python scripts/render_contributions.py
python scripts/validate_profile.py
python -m unittest discover -s tests -v
```

`generate_profile_assets.py` owns the static terminal artwork. `fetch_contributions.py` downloads the public contribution-calendar fragment for `MEDSK2028` and refuses to overwrite data when GitHub returns an incomplete calendar. `render_contributions.py` produces the animated 53-week SVG.

## Automation

`.github/workflows/update-contributions.yml` runs daily and can also be dispatched manually. It has only `contents: write` permission, pins the official GitHub actions to full commit SHAs, validates generated files, and commits only the contribution JSON and SVG when they changed.

Repository settings must allow GitHub Actions to create commits:

1. Open **Settings → Actions → General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Save, then run **Update contribution artwork** once from the Actions tab.

If branch protection blocks direct Actions commits, allow the workflow identity to bypass that rule or replace the final push step with a pull-request workflow.

## Security model

- No personal access token, API key, or other secret is read by the generators.
- The fetcher accepts only a valid GitHub username and contacts a fixed `github.com` endpoint.
- The workflow does not execute downloaded content; it parses contribution-calendar attributes and text.
- A minimum-calendar guard prevents transient or malformed responses from replacing known-good data.
- Private project code and repository URLs are deliberately omitted from the public README.
