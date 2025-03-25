# ✂️📃 PDF Cutter

A Python tool that make it easier to print massive documents on school printers, by splitting them into 30-page chunks.

> 📖 PDF Cutter slices your PDFs for PaperCut

## Download

Cloning the repository or download the source code from this GitHub repository.

On school computers, it's easiest to download [just the `main.py` file](https://github.com/RandomSearch18/pdf-cutter/raw/refs/heads/main/main.py).

## Run

You can run the program with `uv`:

```bash
uv run main.py
```

If you don't have `uv` installed, then you must install the `pypdf` package manually, and then run `main.py`. E.g.

```bash
py -m pip install pypdf
py main.py
```

## Acknowledgements

### Resources used

- [Tim Golden's Python Stuff: Print](https://timgolden.me.uk/python/win32_how_do_i/print.html)
- [Answer: Print to standard printer from Python?](https://stackoverflow.com/a/22550163/11519302)
