# Saeed Gholami Shahbandi's website

Personal website at <https://saeed.im/>, built with [Zensical](https://zensical.org/). The modern theme, indigo
navigation tabs, and Markdown-first structure follow
[KEEPER's build-caisr-keeper-site branch](https://github.com/caisr-hh/keeper/tree/build-caisr-keeper-site) (reference
commit `e1be1d4`).

## Edit content

Each page is an ordinary Markdown file in `docs/`: `index.md`, `about.md`, `research.md`, `publications.md`,
`photography.md`, `reading.md`, and `license.md`. Navigation and site settings live in `zensical.toml`; the small
heading adjustments are in `docs/stylesheets/extra.css`. `overrides/` preserves the personal metadata and a helpful 404
page.

Use relative Markdown links between pages, such as `[Research](research.md)`. Zensical creates the existing clean URLs,
including `/research/` and `/publications/`. The retired `/contact/` URL redirects to the homepage Profiles section via
`docs/contact/index.html`. Put downloadable files in `docs/assets/`.

## Preview and check

With Python 3.12 or newer, including `venv` and `pip`:

```sh
make create-env
make serve
```

Open <http://127.0.0.1:8001/>. To choose another port, use `make serve PORT=8010`. The tools are pinned in
`requirements.txt`, matching the reference branch. Re-run `make create-env` after changing dependencies. You do not need
to activate the environment: Make uses `.venv/bin/` directly.

```sh
make format
make check
```

Checks cover Markdown formatting and linting, workflow YAML, a strict build, generated local links and anchors, and
preservation of the existing page URLs, domain, favicon, feed, and thesis download. Use `make build` for just the build.
The generated `site/` directory is ignored and should not be committed.

## Publish

The GitHub Actions workflow checks pull requests and pushes to `master`. A successful push to `master` uploads `site/`
and deploys it with the official GitHub Pages actions. It does not publish feature branches.

Before the first deployment, set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. Keep the
custom domain set to `saeed.im`; `docs/CNAME` also preserves it in the output. No DNS change is needed. The root `CNAME`
is retained for repository-level domain configuration.

The migration preserves the existing biographical and publication information; it does not update publication status or
career history. Research images and external profile links remain hosted by their original providers.

## License and credits

See [License and Credits](docs/license.md).
