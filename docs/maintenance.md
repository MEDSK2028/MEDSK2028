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

The static generator owns the hero, eight-project private-safe showcase, terminal, capabilities, neural globe, centered radar/current-focus panel, and footer. The public, low-detail project pages live under `case-studies/`; original repositories remain private, and product iterations are grouped into one brief. The activity renderer owns `assets/activity.svg` and `assets/activity-mobile.svg` and renders the owner-provided authenticated snapshot in `data/contribution-snapshot-2026.json`; the scheduled fetcher separately refreshes the anonymous public audit in `data/contributions.json`.

## Automation

`.github/workflows/update-activity.yml` refreshes the anonymous public audit daily at 05:17 UTC, regenerates the owner-snapshot artwork, and can be dispatched manually. GitHub's anonymous endpoint currently omits the private contribution levels visible in the owner's authenticated screenshot, so the immutable snapshot is intentionally not overwritten. The workflow uses only official GitHub actions pinned to full commit SHAs and has only `contents: write` permission.

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
- The displayed 487-contribution calendar is reconstructed from the authenticated GitHub screenshot supplied by the profile owner; its 42 active-day levels and six-day longest streak match that snapshot.
- Anonymous API/public-HTML data remains stored separately in `data/contributions.json` and is never presented as the complete private-inclusive history.
- Snapshot intensities use the profile's violet-to-cyan palette rather than GitHub green. No path-following animation is rendered over the contribution cells.
- Project cards expose README-level summaries only; private source and repository URLs remain undisclosed, with email used for detail requests.
- Public case-study briefs disclose only the problem space, high-level scope, and selected technologies. Source code, internal architecture, schemas, endpoints, credentials, private data, and implementation details stay private.
- Empty placeholder repositories and duplicate product iterations are not presented as separate achievements.
- Private source URLs, credentials, customer data, and unverifiable metrics are not exposed.
- Third-party statistics widgets are intentionally avoided to prevent outages, rate limits, and broken images.
