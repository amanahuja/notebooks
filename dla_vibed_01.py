import marimo

__generated_with = "0.20.2"
app = marimo.App(width="columns")

with app.setup:
    import marimo as mo


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
