# Profile maintenance

This profile is self-contained: artwork is committed as SVG, animations run inside the SVG files, and the README executes no JavaScript. The only network operation is the scheduled refresh of GitHub's public contribution calendar.

## Requirements

- Python 3.11 or newer
- Internet access when refreshing public GitHub activity

All scripts use the Python standard library. No `pip install` step is required.

## Regenerate everything

From the repository root:

```bash
python scripts/generate_profile_assets.py
python scripts/fetch_contributions.py
python scripts/render_activity.py
python scripts/validate_profile.py
python -m unittest discover -s tests -v
```

The static generator owns the hero, private-safe project showcase, terminal, capabilities, neural globe, centered radar/current-focus panel, and footer. The activity scripts own `data/contributions.json`, `assets/activity.svg`, and `assets/activity-mobile.svg`, including the full-year grid and decorative looping Python snake.

## Automation

`.github/workflows/update-activity.yml` refreshes the public calendar daily at 05:17 UTC and can be dispatched manually. It uses only official GitHub actions pinned to full commit SHAs and has only `contents: write` permission.

After committing and pushing this redesign, confirm repository settings allow the workflow to commit:

1. Open **Settings → Actions → General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Run **Update public activity artwork** once from the Actions tab.

If branch protection blocks bot commits, allow this workflow to bypass the relevant rule or convert the final step into a pull-request workflow.

## Content integrity

- Featured software descriptions are derived from current private repository documentation.
- The MPLS lab reflects information explicitly supplied for the profile.
- SOC, SIEM, Wazuh, and security-monitoring content is presented as a capability/practice area, not a fabricated repository.
- The security radar and system-status lights are explicitly labeled decorative.
- Public contribution artwork is based only on GitHub's public calendar and is never inflated.
- The Python snake is a decorative SVG motion layer. It never writes, fills, or changes contribution cells.
- Project cards expose README-level summaries only; private source and repository URLs remain undisclosed, with email used for detail requests.
- Private source URLs, credentials, customer data, and unverifiable metrics are not exposed.
- Third-party statistics widgets are intentionally avoided to prevent outages, rate limits, and broken images.
