# Bibkey Replacer

A Python script that replaces old citation keys in LaTeX files (`\cite{...}`) using new BibTeX keys.

## ✨ Use Case

When you're converting an Overleaf LaTeX project that uses manually typed or numeric citation keys into one managed by **Zotero** (or any other reference manager), you often want to replace all the citation keys with consistent, human-readable ones. This tool helps you do that — automatically and reliably.

## 💡 Features

- Matches citations by **DOI** (even if only found in the `url` field)
- Matches citations by **normalized title** (handles casing, spacing, and braces)
- Supports citation prefixes like `doi:...`
- Supports `\cite{A, B, C}` with flexible spacing
- Outputs a clean `.tex` file with updated citation keys

## 📂 File Naming Convention

- `main.tex`: Your LaTeX file with old citation keys
- `old.bib`: Original BibTeX file used in Overleaf or manually curated
- `new.bib`: New BibTeX file exported from Zotero (or cleaned manually)

## 🚀 How to Use

1. Rename your files as:
   - `main.tex` → your main LaTeX file
   - `old.bib` → original `.bib` with old citation keys
   - `new.bib` → the Zotero-exported or cleaned `.bib` file

2. Run the script using Python 3:

```bash
python bibkey_replacer.py
