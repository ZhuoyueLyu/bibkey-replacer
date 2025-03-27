import re
from pathlib import Path

# === File paths ===
tex_path = Path("main.tex")
new_bib_path = Path("new.bib")
old_bib_path = Path("old.bib")

# === Load file contents ===
tex_content = tex_path.read_text()
new_bib_content = new_bib_path.read_text()
old_bib_content = old_bib_path.read_text()

# === Utility functions ===
def normalize_title_strict(title):
    title = re.sub(r"[{}]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.lower().strip()

def strict_extract_bib_field(entry, field):
    pattern = rf'(?<!\w){re.escape(field)}\s*=\s*(\{{(?:[^{{}}]*|(?:\{{[^{{}}]*\}}))*\}}|"(?:[^"]*)")'
    match = re.search(pattern, entry, re.DOTALL)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith('{') and value.endswith('}'):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value.strip()

def extract_cite_keys(text):
    pattern = r"\\cite\{([^}]+)\}"
    matches = re.findall(pattern, text)
    keys = []
    for match in matches:
        keys.extend([k.strip() for k in match.split(",")])
    return set(keys)

def parse_bib_entries(bib_content):
    entries = {}
    pattern = r'@(\w+)\{([^,]+),'
    for match in re.finditer(pattern, bib_content):
        _, key = match.groups()
        start = match.start()
        brace_count = 0
        for i in range(start, len(bib_content)):
            if bib_content[i] == '{':
                brace_count += 1
            elif bib_content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    entries[key] = bib_content[start:i+1]
                    break
    return entries

def replace_cite_keys(text, mapping):
    def replacer(match):
        keys = match.group(1).split(',')
        new_keys = [mapping.get(k.strip(), k.strip()) for k in keys]
        return f"\\cite{{{', '.join(new_keys)}}}"
    return re.sub(r"\\cite\{([^}]+)\}", replacer, text)

# === Parse BibTeX entries ===
new_entries = parse_bib_entries(new_bib_content)
old_entries = parse_bib_entries(old_bib_content)

# === Build DOI and Title Mappings ===
doi_to_key = {}
title_to_key = {}

for key, entry in new_entries.items():
    doi = strict_extract_bib_field(entry, 'doi')
    url = strict_extract_bib_field(entry, 'url')
    title = strict_extract_bib_field(entry, 'title')

    if not doi and url and "10." in url:
        doi_match = re.search(r'10\.\d{4,9}/[\S]+', url)
        if doi_match:
            doi = doi_match.group(0).strip()

    if doi:
        doi_to_key[doi.strip()] = key
    if title:
        normalized_title = normalize_title_strict(title)
        title_to_key[normalized_title] = key

# === Build old-to-new citation key mapping ===
old_to_new_keys = {}
for cite_key in extract_cite_keys(tex_content):
    cleaned_key = cite_key.strip()
    if cleaned_key.startswith("doi:"):
        cleaned_key = cleaned_key.replace("doi:", "", 1).strip()

    if '/' in cleaned_key:
        if cleaned_key in doi_to_key:
            old_to_new_keys[cite_key] = doi_to_key[cleaned_key]
        else:
            for doi, ref_key in doi_to_key.items():
                if cleaned_key == doi.strip():
                    old_to_new_keys[cite_key] = ref_key
                    break
    elif cite_key in old_entries:
        title = strict_extract_bib_field(old_entries[cite_key], 'title')
        if title:
            normalized = normalize_title_strict(title)
            if normalized in title_to_key:
                old_to_new_keys[cite_key] = title_to_key[normalized]

# === Apply replacements ===
updated_tex_content = replace_cite_keys(tex_content, old_to_new_keys)

# === Save output ===
output_path = Path("main_updated.tex")
output_path.write_text(updated_tex_content)
print(f"Updated LaTeX saved to: {output_path}")
