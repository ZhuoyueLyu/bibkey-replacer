# Bibkey Replacer

A Python script that replaces old citation keys in LaTeX files (`\cite{...}`) using new BibTeX keys.

## ✨ Use Case

When you're converting an Overleaf LaTeX project that uses manually typed or numeric citation keys into one managed by **Zotero** (or other reference manager), you often want to replace all the citation keys with Zotero's default, human-readable keys (e.g., `smith_article_2020`). This tool helps you do that.

## 📌 Example: Before & After

```latex
% BEFORE:
Recent works have explored hand tracking~\cite{10293847,
    johnsonDeepGestures2021,
    doi:10.5555/abc.def.12345 ,
    smith2020interaction ,
    8574930}
    in AR and VR environments.

% AFTER:
Recent works have explored hand tracking~\cite{wang_handtrack_2023,
    johnson_deepgestures_2021,
    zhou_vrlearn_2020,
    smith_objmanip_2020,
    kim_hciinput_2022}
    in AR and VR environments.
```
> **Note**: All citation keys shown above are **fictional** and used only for illustration.

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
