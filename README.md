# vydyap.github.io

My portfolio website: **https://vydyap.github.io**

Plain HTML and CSS, with no framework and no build step. It loads fast, works without JavaScript, and
follows the visitor's light or dark setting.

| File | Purpose |
|---|---|
| `index.html` | The whole site: intro, featured projects, more projects, skills, contact |
| `styles.css` | All styling, including dark mode and the layouts for phones and tablets |
| `assets/img/` | Project screenshots, converted to WebP (about 40 KB each) |
| `scripts/check_site.py` | Checks that every linked file exists, every image has alt text and a size, in-page links resolve, and no link uses http |
| `.github/workflows/deploy.yml` | Runs the check on every push, then deploys to GitHub Pages |

Run it locally:

```bash
python -m http.server 8000      # then open http://localhost:8000
python scripts/check_site.py    # the same check CI runs
```

Project facts and numbers on the site come from each project's README and its measured results.
