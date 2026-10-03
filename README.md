# Saeed Gholami Shahbandi's website

Personal website at <https://saeed.im/>, built with [Zensical](https://zensical.org/). The modern theme, indigo
navigation tabs, and Markdown-first structure follow
[KEEPER's build-caisr-keeper-site branch](https://github.com/caisr-hh/keeper/tree/build-caisr-keeper-site) (reference
commit `e1be1d4`).

## Edit content

Each page is an ordinary Markdown file in `docs/`: `index.md`, `about.md`, `research.md`, `photography.md` and
`license.md`. Navigation and site settings live in `zensical.toml`; the small heading adjustments are in
`docs/stylesheets/extra.css`. `overrides/` preserves the personal metadata and a helpful 404 page.

Use relative Markdown links between pages, such as `[Research](research.md)`. Zensical creates clean URLs such as
`/research/`. The retired `/contact/` and `/publications/` URLs redirect to the homepage Profiles section via
`docs/contact/index.html` and `docs/publications/index.html`. The retired `/reading/` URL redirects to the homepage
interests section via `docs/reading/index.html`. Put downloadable files in `docs/assets/`.

## Preview and check

### Prepare photographs

The gallery uses committed WebP copies in `docs/assets/photography/thumbnails/` and `docs/assets/photography/display/`.
Full-resolution JPEGs stay local in `docs/assets/photography/` and are ignored by Git. Keep a separate backup of those
originals; they are not included when cloning this repository.

To create or refresh the web copies after adding `.jpg` originals:

```sh
.venv/bin/python -m pip install -r requirements-images.txt
.venv/bin/python scripts/prepare_photos.py
```

The script preserves orientation and converts embedded color profiles to sRGB, exports 640-pixel thumbnails and
2200-pixel display images without upscaling, and leaves the originals unchanged. Normal site builds use the committed
web copies and do not need Pillow or the originals.

Edit `docs/photography.md` to change captions, reorder photographs, or move them between sections. To add a photograph,
generate its two WebP sizes, then copy an existing `<figure>` block into the appropriate `photo-gallery` section. Set
`src` to its thumbnail and `data-src` to its display copy; keep paths relative to `docs/`, starting with `assets/`.
Update the descriptive `alt` text, caption, and thumbnail dimensions. The `on-glb` class enables Zensical's native
lightbox; `data-gallery="photography"` lets visitors move between all photos in the overlay. Without JavaScript, the
same links open the display images directly.

`make check` verifies that every display image appears exactly once, with a lazy-loaded thumbnail, description,
dimensions, and a working lightbox link. Commit both WebP directories along with the page changes. GitHub Actions
publishes those committed copies; the local originals remain outside version control.

### Build the website

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
