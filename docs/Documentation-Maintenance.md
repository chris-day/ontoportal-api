# Documentation maintenance

The source pages live in `docs/`. Navigation and site settings live in `zensical.toml`. The old `mkdocs.yml` is retained only as a rollback reference. The GitHub Wiki checkout is an input to the migration; `docs/` is the maintained copy going forward. Changes to the remote wiki are outside this repository's documentation workflow.

## Local setup

Use the repository's existing `.venv` and a compatible Python (the migration was validated with 3.14). From the repository root:

```bash
python3.14 -m venv .venv  # only if .venv does not already exist
.venv/bin/python -m pip install -r requirements-docs.txt
.venv/bin/python -m pip install -e .
.venv/bin/zensical serve
```

Build and validate with:

```bash
.venv/bin/zensical build --clean --strict
.venv/bin/python scripts/check_docs.py
.venv/bin/python -m pip check
```

The local preview is served at `http://localhost:8000/` by default. The configured production base URL is `https://chris-day.github.io/ontoportal-api/`, established from the existing GitHub Pages workflow and a successful HTTP response. A successful local build does not publish the site.

To refresh the pinned dependency closures, upgrade the relevant packages in the existing `.venv`, regenerate both lock files, and verify them:

```bash
.venv/bin/python -m pip install --upgrade zensical playwright pip setuptools wheel
.venv/bin/python scripts/update_docs_lock.py
.venv/bin/python -m pip install -r requirements-docs.txt -r requirements-docs-browser.txt
.venv/bin/python -m pip check
.venv/bin/zensical build --clean --strict
.venv/bin/python scripts/check_docs.py
.venv/bin/python -m pytest -q
```

The lock generator follows installed package metadata to pin the full documentation and browser dependency closures. Review its diff and run the browser checker before accepting a lock update. CI installs these files in its own checkout environment.

## Privacy and services

The site has no analytics, advertisements, comments, external fonts, or active embeds. Search and theme assets are served locally. Zensical's native consent form stores a preference in browser local storage. The optional GitHub content category starts unchecked. **Accept** saves the currently selected categories; **Reject** clears optional consent. The footer link reopens settings so a choice can be changed. The repository link is an ordinary link and makes a request to GitHub only when opened. The GitHub Pages host receives the normal requests needed to serve the site. Consent controls by themselves do not establish legal compliance for a specific deployment.

Do not add third-party scripts, diagrams with CDN runtime dependencies, or remote embeds without reviewing their requests and consent behavior. The source set currently has no Mermaid diagrams or other live embeds. The old network graph plugin was not migrated: its topology view was ancillary and Zensical does not support that plugin. Search remains available. The old revision-date and minify plugins were also omitted; source revision history remains on GitHub and output optimization can be added after a measured need. The old custom Mermaid fence is unnecessary for the current pages.

## Publishing and rollback

The existing Pages deployment workflow builds on pushes to `main` and manual dispatch. Pull requests run build checks only. Publishing still requires the usual repository action or workflow trigger; editing these files does not publish anything. The deployment branch, environment, and Pages settings remain under repository-owner control.

For rollback, restore the pre-migration `mkdocs.yml` and `.github/workflows/docs.yml` from Git revision `5cc0932529992e2c6d86499761ed91dcec8da5ff`, then rebuild with the older MkDocs dependency list recorded in that workflow. The original wiki remains intact in its separate repository.
