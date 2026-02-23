# Marimo Notebooks

A collection of interactive marimo notebooks deployed to GitHub Pages using WebAssembly.

## 📁 Repository Structure

```
.
├── apps/              # Readonly apps (interactive but code not editable)
├── notebooks/         # Editable notebooks (users can modify code)
├── .github/
│   └── workflows/
│       └── deploy-dla.yml
└── README.md
```

## 🚀 Adding New Notebooks

### For Readonly Apps (Recommended for Demos)

1. Add your marimo notebook (`.py` file) to the `apps/` directory
2. Commit and push to `main` branch
3. GitHub Actions will automatically build and deploy

```bash
# Example
cp my_notebook.py apps/
git add apps/my_notebook.py
git commit -m "Add new notebook"
git push
```

### For Editable Notebooks

1. Add your marimo notebook to the `notebooks/` directory
2. Commit and push to `main` branch

```bash
cp my_notebook.py notebooks/
git add notebooks/my_notebook.py
git commit -m "Add editable notebook"
git push
```

## GitHub Pages Setup

Before the workflow can deploy, you need to configure GitHub Pages:

1. Push this repository to GitHub
2. Go to your repository Settings → Pages
3. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
4. The workflow will automatically run on the next push

## 🛠️ Local Development

### Running Notebooks Locally

```bash
# Interactive mode (edit in browser)
uv run marimo edit apps/dla_vibed_01.py

# Run as app (readonly)
uv run marimo run apps/dla_vibed_01.py

# Run as script (for testing)
uv run apps/dla_vibed_01.py
```

### Testing Export Locally

```bash
# Export readonly app
uvx marimo export html-wasm apps/dla_vibed_01.py -o test_dist --mode run

# Export editable notebook
uvx marimo export html-wasm notebooks/my_notebook.py -o test_dist --mode edit

# Serve locally to test
cd test_dist
python -m http.server 8000
# Visit http://localhost:8000
```

## Notebook Requirements

All notebooks should include PEP 723 dependencies at the top:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "anywidget",
#     # ... other dependencies
# ]
# ///
```

## 🔍 How It Works

1. **GitHub Actions Trigger**: Workflow runs on pushes to `main` that modify `apps/` or `notebooks/`
2. **Build Process**: 
   - Exports each notebook in `apps/` as readonly WASM HTML
   - Exports each notebook in `notebooks/` as editable WASM HTML
   - Creates an index page listing all notebooks
3. **Deploy**: Publishes to GitHub Pages
4. **Result**: Fully interactive Python notebooks running in the browser via WebAssembly

## 📚 Resources

- [marimo Documentation](https://docs.marimo.io)
- [marimo WASM Export Guide](https://docs.marimo.io/guides/exporting/#export-to-wasm-powered-html)
- [marimo GitHub Pages Guide](https://marimo.io/blog/wasm-github-pages)
- [anywidget Documentation](https://anywidget.dev)

## 🤝 Contributing

Feel free to add your own notebooks! Just follow the structure above and push to `main`.
