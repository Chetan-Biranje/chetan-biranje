# Chetan Biranje — Animated GitHub README

## Install in your GitHub profile

1. Open the repository named exactly `Chetan-Biranje` (the profile README repository).
2. Back it up or download a copy before replacing files.
3. Copy the contents of this ZIP into that repository, preserving folder paths.
4. Review the three featured-project cards and replace their placeholder labels and links with real repositories.
5. Commit and push the files.
6. In GitHub, open Settings → Actions → General. Ensure Actions are enabled and workflow permissions allow read/write access to repository contents.
7. Open Actions → Refresh animated profile README → Run workflow.

The scheduled refresh runs daily at 01:17 UTC. It uses the repository-provided `GITHUB_TOKEN`; no personal access token is required.

## Local preview

```bash
pip install -r requirements.txt
STATIC=1 python scripts/render_readme_cards.py
```

## Important

- `assets/portrait.jpg` is derived from the photo you supplied and is converted to ASCII by the renderer.
- GitHub contribution data is populated when the workflow runs successfully.
- The three featured-project cards are placeholders because the exact repositories to feature have not been confirmed.
- This package does not modify your live GitHub repository. You must upload/commit it yourself.
