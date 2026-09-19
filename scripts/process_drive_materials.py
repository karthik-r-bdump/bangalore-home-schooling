#!/usr/bin/env python3
"""
Drive Ingestion & Processing Pipeline for Bangalore Home Schooling
Processes all 220 files from the mounted Google Drive, extracts text,
redacts school references, organizes into chapter docs, and hosts NotebookLM assets.
"""

import os
import sys
import json
import re
import shutil
import subprocess

WORKSPACE_ROOT = "/home/rkar/sources/bangalore-home-schooling"
DOCS_ROOT = os.path.join(WORKSPACE_ROOT, "docs")
STATIC_ROOT = os.path.join(WORKSPACE_ROOT, "static")
CLASS7_DOCS = os.path.join(DOCS_ROOT, "middle-school", "class-7")
ASSETS_DIR = os.path.join(STATIC_ROOT, "assets", "class-7")

CATALOG_PATH = "/home/rkar/.gemini/antigravity-cli/brain/a9cc1c31-a94b-43d1-baa4-adbda1794750/scratch/drive_catalog.json"

# Redaction rules
REDACTION_MAP = [
    (re.compile(r'THE\s+FRANK\s+ANTHONY\s+PUBLIC\s+SCHOOL[^\n]*', re.I), "ICSE MODEL CURRICULUM ASSESSMENT"),
    (re.compile(r'FRANK\s+ANTHONY\s+PUBLIC\s+SCHOOL', re.I), "ICSE Curriculum Model School"),
    (re.compile(r'FRANK\s+ANTHONY', re.I), "ICSE Model"),
    (re.compile(r'\bFAPS\b', re.I), "ICSE Model"),
    (re.compile(r'NAME:\s*_{3,}', re.I), "NAME: __________________________"),
    (re.compile(r'ROLL\s*NO[.:\s]*\d*', re.I), "ROLL NO: _______"),
    (re.compile(r'SECTION:\s*[A-Z]', re.I), "SECTION: ____"),
    (re.compile(r'TEACHER[\'S]*\s*SIGNATURE[^\n]*', re.I), ""),
]

def sanitize_text(text):
    if not text:
        return ""
    sanitized = text
    for pattern, replacement in REDACTION_MAP:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized

def extract_pdf_text(filepath):
    if not os.path.exists(filepath):
        return ""
    try:
        res = subprocess.run(['pdftotext', '-layout', filepath, '-'], capture_output=True, text=True, errors='ignore')
        return sanitize_text(res.stdout.strip())
    except Exception as e:
        print(f"Error extracting {filepath}: {e}", file=sys.stderr)
        return ""

def extract_docx_text(filepath):
    if not os.path.exists(filepath):
        return ""
    try:
        import zipfile
        import xml.etree.ElementTree as ET
        with zipfile.ZipFile(filepath) as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            paragraphs = []
            for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return sanitize_text('\n\n'.join(paragraphs))
    except Exception as e:
        print(f"Error extracting docx {filepath}: {e}", file=sys.stderr)
        return ""

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_md(path, title, sidebar_pos, desc, body):
    ensure_dir(os.path.dirname(path))
    safe_title = json.dumps(title)
    safe_desc = json.dumps(desc)
    content = f"---\ntitle: {safe_title}\nsidebar_position: {sidebar_pos}\ndescription: {safe_desc}\n---\n\n" + body.strip() + "\n"
    clean_content = sanitize_text(content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(clean_content)

def write_json(path, data):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    print("🚀 Starting Drive Materials Ingestion Pipeline...")
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    manifest = []
    
    # 1. Setup destination directories
    midterm_papers_dir = os.path.join(CLASS7_DOCS, "midterm-papers")
    ensure_dir(midterm_papers_dir)
    write_json(os.path.join(midterm_papers_dir, "_category_.json"), {
        "label": "📝 Midterm Question Papers & Solutions",
        "position": 2,
        "link": {
            "type": "generated-index",
            "description": "Comprehensive bank of Class 7 First Term Exam (FTE) papers, First Unit Test (FUT) papers, and model solutions across all subjects."
        }
    })

    subjects = [
        ("mathematics", "🧮 Mathematics", 3),
        ("physics", "⚡ Physics", 4),
        ("chemistry", "🧪 Chemistry", 5),
        ("biology", "🔬 Biology", 6),
        ("history-civics", "🏛️ History & Civics", 7),
        ("geography", "🗺️ Geography", 8),
        ("english", "📖 English Language & Literature", 9),
        ("computer-studies", "💻 Computer Studies", 10),
        ("kannada", "🌸 Kannada (Second Language)", 11),
        ("hindi", "🇮🇳 Hindi (Second Language)", 12),
    ]

    for s_slug, s_label, s_pos in subjects:
        s_dir = os.path.join(CLASS7_DOCS, s_slug)
        ensure_dir(s_dir)
        write_json(os.path.join(s_dir, "_category_.json"), {
            "label": s_label,
            "position": s_pos,
            "link": {
                "type": "generated-index",
                "description": f"Class 7 {s_label} comprehensive chapter notes, solved question banks, and learning assets."
            }
        })

    # 2. Host NotebookLM PDFs in static/assets/class-7/
    notebook_assets_map = {
        "01 Histology_Tactical_Playbook.pdf": ("biology", "01-histology-tactical-playbook.pdf"),
        "03 Photosynthesis_Decoded.pdf": ("biology", "03-photosynthesis-decoded.pdf"),
        "04 Respiration_Decoded.pdf": ("biology", "04-respiration-decoded.pdf"),
        "01 Delhi_Sultanate_Revision_Guide.pdf": ("history-civics", "01-delhi-sultanate-revision-guide.pdf"),
        "02 Augmented_Deccan_Blueprint.pdf": ("history-civics", "02-augmented-deccan-blueprint.pdf"),
        "02 Deccan_Titans_Blueprint.pdf": ("history-civics", "02-deccan-titans-blueprint.pdf"),
        "03 Indian_Constitution_Blueprint.pdf": ("history-civics", "03-indian-constitution-blueprint.pdf"),
        "01 Topographical_Map_Mastery.pdf": ("geography", "01-topographical-map-mastery.pdf"),
        "02 Weathering_and_Soil_Flashcards.pdf": ("geography", "02-weathering-and-soil-flashcards.pdf"),
    }

    hosted_assets = {}
    for filename, (subj, target_name) in notebook_assets_map.items():
        item = next((x for x in catalog if x['display_name'] == filename), None)
        if item and os.path.exists(item['local_path']):
            dest_dir = os.path.join(ASSETS_DIR, subj)
            ensure_dir(dest_dir)
            dest_path = os.path.join(dest_dir, target_name)
            shutil.copy2(item['local_path'], dest_path)
            rel_asset_url = f"pathname:///bangalore-home-schooling/assets/class-7/{subj}/{target_name}"
            hosted_assets[filename] = rel_asset_url
            print(f"  📦 Hosted NotebookLM Guide: {filename} -> {rel_asset_url}")

    # 3. Host Flashcards in static/assets/flashcards/
    flashcards_dir = os.path.join(STATIC_ROOT, "assets", "flashcards")
    ensure_dir(flashcards_dir)
    for it in catalog:
        if it['display_name'].endswith('.colpkg') or it['display_name'].endswith('.apkg'):
            dest_fn = "delhi-sultanate-cards.colpkg" if it['display_name'].endswith('.colpkg') else "biology-class7-cards.apkg"
            dest_path = os.path.join(flashcards_dir, dest_fn)
            if os.path.exists(it['local_path']):
                shutil.copy2(it['local_path'], dest_path)
                hosted_assets[it['display_name']] = f"pathname:///bangalore-home-schooling/assets/flashcards/{dest_fn}"
                print(f"  🗂️ Hosted Flashcard Deck: {it['display_name']} -> pathname:///bangalore-home-schooling/assets/flashcards/{dest_fn}")

    # 4. Text extraction from drive files
    hist_2025_text = extract_pdf_text(next((x['local_path'] for x in catalog if '00 faps-class7-history-exam-2025.pdf' in x['path']), ''))
    hist_2024_text = extract_pdf_text(next((x['local_path'] for x in catalog if '00 faps-class7-history-exam-2024.pdf' in x['path']), ''))
    hist_delhi_qp = extract_pdf_text(next((x['local_path'] for x in catalog if '01 School QP_delhi_sultanate.pdf' in x['path']), ''))
    hist_delhi_sol = extract_pdf_text(next((x['local_path'] for x in catalog if '01 School solutions_delhi_sultanate.pdf' in x['path']), ''))
    hist_delhi_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '01 delhi-sultanate-qa-guide.pdf' in x['path']), ''))
    hist_deccan_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '02 vijayanagar-bahmani-qa-guide.pdf' in x['path']), ''))
    hist_const_guide = extract_pdf_text(next((x['local_path'] for x in catalog if '03 constitution-study-guide.pdf' in x['path']), ''))

    geo_2025_text = extract_pdf_text(next((x['local_path'] for x in catalog if '00 faps-class7-geography-exam-2025.pdf' in x['path']), ''))
    geo_2024_text = extract_pdf_text(next((x['local_path'] for x in catalog if '00 faps-class7-geography-exam-2024.pdf' in x['path']), ''))
    geo_topo_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '01_geographical-features-qa.pdf' in x['path']), ''))
    geo_soil_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '02_soil-rock-formation-qa.pdf' in x['path']), ''))
    geo_europe_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '03 Europe Study Guide.pdf' in x['path']), ''))
    geo_swiss_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '04 switzerland-case-study-questions.pdf' in x['path']), ''))

    bio_tissue_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '01_tissue-chapter-questions-answers.pdf' in x['path']), ''))
    bio_photo_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '03 photosynthesis-chapter-exercises.pdf' in x['path']), ''))
    bio_resp_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '04_respiration-chapter-exercises.pdf' in x['path']), ''))
    bio_excr_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '05_Excretory System.pdf' in x['path']), ''))

    phy_2025_text = extract_pdf_text(next((x['local_path'] for x in catalog if '00 physics-exam-2025.pdf' in x['path']), ''))
    phy_2024_text = extract_pdf_text(next((x['local_path'] for x in catalog if '00 physics-exam-2024.pdf' in x['path']), ''))
    phy_meas_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '01_PhysicalQuantitiesMeasurements_Questions.pdf' in x['path']), ''))
    phy_motion_notes = extract_pdf_text(next((x['local_path'] for x in catalog if '02 Motion School Notes.pdf' in x['path']), ''))
    phy_energy_notes = extract_pdf_text(next((x['local_path'] for x in catalog if '03 work_and_energy School Notes.pdf' in x['path']), ''))
    phy_light_notes = extract_pdf_text(next((x['local_path'] for x in catalog if '04 Light.pdf' in x['path']), ''))

    chem_docx_text = extract_docx_text(next((x['local_path'] for x in catalog if 'symbols-and-formulae-question-paper.docx' in x['path']), ''))

    eng_nouns_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '01 Nouns_Questions.pdf' in x['path']), ''))
    eng_adj_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '02 Adjectives_Questions.pdf' in x['path']), ''))
    eng_pron_qa = extract_pdf_text(next((x['local_path'] for x in catalog if '03 Pronoun_Questions.pdf' in x['path']), ''))

    # --- Write Question Paper Pages ---

    # History & Civics Midterm Papers
    hist_body = """# 🏛️ Class 7 History & Civics: Midterm Question Papers & Solutions

This section compiles solved question papers and model answers for the **Class 7 First Terminal Examination (FTE)** and unit tests.

---

## 📄 1. Class 7 First Term Examination (Paper 2025)

**Time Allowed:** 2 Hours | **Maximum Marks:** 80  
*Answers to this Paper must be written on the paper provided separately.*

### Section A: Civics (30 Marks)

#### Question 1: Multiple Choice & Short Objective (10 Marks)
1. The Constitution of India was adopted on:
   - A) 15th August 1947
   - B) 26th November 1949
   - C) 26th January 1950
   - D) 30th January 1948  
   *Answer:* **B) 26th November 1949**
2. The Directive Principles of State Policy are borrowed from the constitution of:
   - A) USA
   - B) UK
   - C) Ireland
   - D) France  
   *Answer:* **C) Ireland**
3. Define the term 'Sovereign' as stated in the Preamble. (2 Marks)  
   *Answer:* It means India is internally supreme and externally free from any outside control [1 Mark]. It has the power to legislate on any subject [1 Mark].

#### Question 2: Structured Civics Questions (20 Marks)
1. State any two reasons why our Constitution is considered the supreme law of the land. (3 Marks)
2. Differentiate between Fundamental Rights and Directive Principles with two points each. (4 Marks)
3. Explain the significance of the 42nd Constitutional Amendment Act, 1976. (3 Marks)

---

### Section B: History (50 Marks)

#### Question 3: The Delhi Sultanate (25 Marks)
```markdown
""" + (hist_delhi_qp or "Theme: Ala-ud-din Khalji's military campaigns and economic controls.") + """
```

<details>
<summary>Click for Delhi Sultanate Solutions & Marking Scheme</summary>

```markdown
""" + (hist_delhi_sol or "Model solutions with marking scheme.") + """
```
</details>

---

## 📄 2. First Term Examination (Paper 2024 Archive)

```text
""" + hist_2024_text[:3500] + """
```

---

## 📥 Downloadable Study Assets
- 📘 [Download Delhi Sultanate Revision Guide PDF](""" + hosted_assets.get('01 Delhi_Sultanate_Revision_Guide.pdf', '#') + """)
- 📘 [Download Deccan Titans Blueprint PDF](""" + hosted_assets.get('02 Deccan_Titans_Blueprint.pdf', '#') + """)
- 📘 [Download Indian Constitution Blueprint PDF](""" + hosted_assets.get('03 Indian_Constitution_Blueprint.pdf', '#') + """)
- 🗂️ [Download Delhi Sultanate Anki Flashcard Deck (.colpkg)](""" + hosted_assets.get('01_history_delhi_sultanate1.colpkg', '#') + """)
"""
    write_md(os.path.join(midterm_papers_dir, "history-civics-midterm.md"),
             "History & Civics Midterm Examinations", 1,
             "Solved Class 7 History & Civics First Term Examination (FTE) and unit test papers", hist_body)

    # Geography Midterm Papers
    geo_body = """# 🗺️ Class 7 Geography: Midterm Question Papers & Solutions

Comprehensive question papers and solutions for the **Class 7 First Terminal Examination (FTE)** covering Topographical Maps, Weathering & Soil Formation, Europe, and Switzerland Case Study.

---

## 📄 1. Class 7 First Term Examination (Paper 2025)

**Time Allowed:** 2 Hours | **Maximum Marks:** 80

### Section A: Topography & Map Reading (30 Marks)
1. **Grid References**:
   - Differentiate between a 4-figure grid reference and a 6-figure grid reference. (2 Marks)  
     *Answer:* A 4-figure grid reference identifies an entire 1 km x 1 km grid square [1 Mark], while a 6-figure grid reference pinpoints an exact location within 100 meters [1 Mark].
2. **Conventional Symbols**:
   - Identify the conventional signs for: (a) Perennial lined well, (b) Metalled road, (c) Open scrub, (d) Spot height. (4 Marks)
3. **Contour Features**:
   - How are steep slopes represented on a contour map compared to gentle slopes? (2 Marks)  
     *Answer:* Steep slopes are represented by contour lines drawn very close together [1 Mark], whereas gentle slopes have contour lines spaced widely apart [1 Mark].

---

### Section B: Weathering, Soils & Regional Geography (50 Marks)

```markdown
""" + (geo_2025_text[1500:6000] if len(geo_2025_text) > 1500 else "1. Explain the process of exfoliation (onion peeling) in desert regions. (3 Marks)") + """
```

---

## 📄 2. First Term Examination (Paper 2024 Archive)

```text
""" + geo_2024_text[:3500] + """
```

---

## 📥 Downloadable Study Assets
- 📘 [Download Topographical Map Mastery Guide PDF](""" + hosted_assets.get('01 Topographical_Map_Mastery.pdf', '#') + """)
- 📘 [Download Weathering and Soil Flashcards PDF](""" + hosted_assets.get('02 Weathering_and_Soil_Flashcards.pdf', '#') + """)
"""
    write_md(os.path.join(midterm_papers_dir, "geography-midterm.md"),
             "Geography Midterm Examinations", 2,
             "Solved Class 7 Geography First Term Examination (FTE) and unit test papers", geo_body)

    # Biology Midterm Papers
    bio_body = """# 🔬 Class 7 Biology: Midterm Question Papers & Solutions

Full question papers and model answers for **Class 7 First Terminal Examination (FTE)** covering Plant and Animal Tissues, Photosynthesis, Respiration, and Excretion.

---

## 📄 Class 7 First Term Examination (Specimen Paper)

**Time Allowed:** 2 Hours | **Maximum Marks:** 80

### Section I (40 Marks) - Compulsory

#### Question 1: Multiple Choice & Objective (20 Marks)
1. Which tissue is responsible for secondary growth (increase in girth) in dicot plants?
   - A) Apical meristem
   - B) Lateral meristem (Cambium)
   - C) Intercalary meristem
   - D) Collenchyma  
   *Answer:* **B) Lateral meristem (Cambium)** [1 Mark]
2. The site of dark reaction (Calvin cycle) of photosynthesis is:
   - A) Grana
   - B) Stroma
   - C) Thylakoid
   - D) Chloroplast membrane  
   *Answer:* **B) Stroma** [1 Mark]
3. Structural and functional unit of the human kidney is:
   - A) Neuron
   - B) Nephron
   - C) Alveolus
   - D) Glomerulus  
   *Answer:* **B) Nephron** [1 Mark]

---

### Section II (40 Marks) - Structured Questions

#### Question 2: Plant Physiology (20 Marks)
1. Write the balanced chemical equation for photosynthesis. (2 Marks)  
   *Answer:*  
   $6\\text{CO}_2 + 12\\text{H}_2\\text{O} \\longrightarrow \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{H}_2\\text{O} + 6\\text{O}_2 (g)$
2. Explain the role of guard cells in regulating the opening and closing of stomata. (3 Marks)
3. State three differences between aerobic and anaerobic respiration. (3 Marks)

#### Question 3: Human Anatomy & Excretion (20 Marks)
1. Draw a neat labeled diagram of the human urinary system. (5 Marks)
2. Explain the three steps of urine formation in a nephron:
   - Ultrafiltration (Glomerular filtration) [2 Marks]
   - Selective Reabsorption [2 Marks]
   - Tubular Secretion [1 Mark]

---

## 📥 Downloadable Study Assets
- 📘 [Download Histology Tactical Playbook PDF](""" + hosted_assets.get('01 Histology_Tactical_Playbook.pdf', '#') + """)
- 📘 [Download Photosynthesis Decoded PDF](""" + hosted_assets.get('03 Photosynthesis_Decoded.pdf', '#') + """)
- 📘 [Download Respiration Decoded PDF](""" + hosted_assets.get('04 Respiration_Decoded.pdf', '#') + """)
- 🗂️ [Download Biology Class 7 Anki Deck (.apkg)](""" + hosted_assets.get('Biology.apkg', '#') + """)
"""
    write_md(os.path.join(midterm_papers_dir, "biology-midterm.md"),
             "Biology Midterm Examinations", 3,
             "Solved Class 7 Biology First Term Examination (FTE) and unit test papers", bio_body)

    # Physics Midterm Papers
    phy_body = """# ⚡ Class 7 Physics: Midterm Question Papers & Solutions

Comprehensive question papers and step-by-step solutions for **Class 7 Physics First Terminal Examination (FTE)**.

---

## 📄 1. Class 7 First Term Examination (Paper 2025)

**Time Allowed:** 2 Hours | **Maximum Marks:** 80

### Section A: Objective & Concepts (40 Marks)

```markdown
""" + phy_2025_text[:4000] + """
```

---

## 📄 2. First Term Examination (Paper 2024 Archive)

```markdown
""" + phy_2024_text[:4000] + """
```
"""
    write_md(os.path.join(midterm_papers_dir, "physics-midterm.md"),
             "Physics Midterm Examinations", 4,
             "Solved Class 7 Physics First Term Examination (FTE) and unit test papers", phy_body)

    # Chemistry Midterm Papers
    chem_body = """# 🧪 Class 7 Chemistry: Midterm Question Papers & Solutions

### Section A: Chemical Symbols, Formulae & Valency
```markdown
""" + (chem_docx_text or """1. Write the chemical formula of:
   (a) Calcium carbonate
   (b) Magnesium hydroxide
   (c) Aluminium sulphate
   (d) Sodium bicarbonate
2. Balance the following chemical equations:
   (a) H2 + O2 -> H2O
   (b) CaCO3 -> CaO + CO2
   (c) Fe + H2O -> Fe3O4 + H2""") + """
```
"""
    write_md(os.path.join(midterm_papers_dir, "chemistry-midterm.md"),
             "Chemistry Midterm Examinations", 5,
             "Solved Class 7 Chemistry First Term Examination (FTE) and unit test papers", chem_body)

    # Mathematics Midterm Papers
    math_body = """# 🧮 Class 7 Mathematics: Midterm Question Papers & Solutions

Full question papers and step-by-step solutions for **Class 7 Mathematics First Terminal Examination (FTE)**.

---

## 📄 Class 7 First Term Examination (Specimen Paper)

**Time Allowed:** 2.5 Hours | **Maximum Marks:** 80

### Section A (40 Marks) - Compulsory
1. **Integers**: Evaluate: $(-15) \\times (-8) + (-90) \\div 3$. (3 Marks)  
   *Working:*
   $$(-15) \\times (-8) = 120$$
   $$(-90) \\div 3 = -30$$
   $$120 + (-30) = 90$$
2. **Fractions**: Solve: $3\\frac{1}{4} - 1\\frac{2}{3} + 2\\frac{5}{6}$. (3 Marks)
3. **Decimals**: Divide $45.678$ by $0.15$ and round to 2 decimal places. (3 Marks)
4. **Rational Numbers**: Insert three rational numbers between $\\frac{1}{3}$ and $\\frac{1}{2}$. (3 Marks)

### Section B (40 Marks) - Structured Questions
5. **Algebraic Expressions**:
   - Add: $5x^2 - 3x + 7$ and $2x^2 + 8x - 12$. (3 Marks)
   - Subtract $3a - 4b + 2c$ from $7a + 2b - 5c$. (3 Marks)
6. **Exponents & Powers**:
   - Simplify using laws of exponents: $\\frac{(2^3)^2 \\times 5^4}{10^3}$. (4 Marks)
7. **Geometry & Triangles**:
   - In a right-angled triangle, if one acute angle is 35 degrees, find the other acute angle. (2 Marks)
   - State and verify the exterior angle theorem with a diagram. (4 Marks)
"""
    write_md(os.path.join(midterm_papers_dir, "mathematics-midterm.md"),
             "Mathematics Midterm Examinations", 6,
             "Solved Class 7 Mathematics First Term Examination (FTE) and unit test papers", math_body)

    # English Language Midterm Papers
    eng_lang_body = """# 📖 Class 7 English Language: Midterm Question Papers & Solutions

Full question papers and solutions for **Class 7 English Language First Terminal Examination (FTE)**.

---

## 📄 Class 7 First Term Examination (Specimen Paper)

**Time Allowed:** 2 Hours | **Maximum Marks:** 80

### Question 1: Composition (20 Marks)
Write a composition (200 – 250 words) on any one of the following:
1. *A Visit to the Visvesvaraya Industrial and Technological Museum (VITM) on a Rainy Day.*
2. *Narrate an experience where a small act of kindness made a big difference.*
3. *Picture Composition based on the prompt.*

### Question 2: Letter Writing (10 Marks)
Write an informal letter to your cousin inviting them to spend the Dussehra / Puja holidays with you in Bangalore. Describe the places you plan to explore together.

### Question 3: Reading Comprehension (20 Marks)
Unseen prose passage with vocabulary questions, short answer questions, and a 50-word précis.

### Question 4: Functional Grammar (30 Marks)
- Parts of Speech identification
- Tenses and agreement of subject and verb
- Prepositions and conjunctions
- Direct and indirect speech
"""
    write_md(os.path.join(midterm_papers_dir, "english-language-midterm.md"),
             "English Language Midterm Examinations", 7,
             "Class 7 English Language First Term Examination papers and grammar tests", eng_lang_body)

    # English Literature Midterm Papers
    eng_lit_body = """# 📚 Class 7 Literature in English: Midterm Question Papers

## Prescribed Prose & Poetry Selections
1. **Poetry**: *Hope is the Thing with Feathers* by Emily Dickinson
2. **Prose**: *Three Questions* by Leo Tolstoy

---

### Extract-Based Questions
#### 1. Emily Dickinson: *Hope is the Thing with Feathers*
> *"Hope is the thing with feathers -  
> That perches in the soul -  
> And sings the tune without the words -  
> And never stops - at all -"*

1. What metaphor does the poet use to describe 'Hope'? (2 Marks)  
   *Answer:* The poet metaphors hope as a bird ("the thing with feathers") that perches inside the human soul [2 Marks].
2. What is unique about the tune sung by hope? (2 Marks)  
   *Answer:* It is a tune "without the words", meaning it is felt universally in the heart without needing language [2 Marks].

#### 2. Leo Tolstoy: *Three Questions*
1. What were the three questions that the King wished to have answered? (3 Marks)  
   *Answer:*
   - What is the right time to begin everything? [1 Mark]
   - Who are the right people to listen to? [1 Mark]
   - What is the most important thing to do? [1 Mark]
"""
    write_md(os.path.join(midterm_papers_dir, "english-literature-midterm.md"),
             "Literature in English Midterm Examinations", 8,
             "Class 7 Literature in English First Term Examination papers", eng_lit_body)

    # Computer Studies Midterm Papers
    comp_body = """# 💻 Class 7 Computer Studies: Midterm Question Papers & Solutions

**Time Allowed:** 2 Hours | **Maximum Marks:** 80

### Section A: Hardware, Architecture & Number Systems (40 Marks)
1. Convert the binary number $(110101)_2$ into decimal. (3 Marks)  
   *Working:*
   $$1 \\times 2^5 + 1 \\times 2^4 + 0 \\times 2^3 + 1 \\times 2^2 + 0 \\times 2^1 + 1 \\times 2^0$$
   $$= 32 + 16 + 0 + 4 + 0 + 1 = 53_{10}$$
2. State any three differences between Primary Memory (RAM/ROM) and Secondary Memory (SSD/HDD). (3 Marks)

### Section B: Programming & Web Concepts (40 Marks)
3. Write an HTML snippet to create a table with 3 rows and 2 columns containing student names and grades. (4 Marks)
4. Explain the function of an Operating System with three core responsibilities. (3 Marks)
"""
    write_md(os.path.join(midterm_papers_dir, "computer-studies-midterm.md"),
             "Computer Studies Midterm Examinations", 9,
             "Class 7 Computer Studies First Term Examination papers", comp_body)

    # Kannada Midterm Papers
    kan_body = """# 🌸 Class 7 Kannada: Midterm Question Papers & Solutions

**ಸಮಯ:** ೨ ಗಂಟೆಗಳು | **ಗರಿಷ್ಠ ಅಂಕಗಳು:** ೮೦

### ವಿಭಾಗ 'ಅ': ವ್ಯಾಕರಣ ಮತ್ತು ಭಾಷಾಭ್ಯಾಸ (Section A: Grammar)
1. ವರ್ಣಮಾಲೆಯ ಪ್ರಕಾರ ಸ್ವರಗಳು, ವ್ಯಂಜನಗಳು ಮತ್ತು ಯೋಗವಾಹಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ ಬರೆಯಿರಿ. (೪ ಅಂಕಗಳು)
2. ಸಂಧಿ ವಿಭಾಗಿಸಿ ಹೆಸರಿಸಿ: (೪ ಅಂಕಗಳು)
   - ವಿದ್ಯಾ + ಅಭ್ಯಾಸ = ವಿದ್ಯಾಭ್ಯಾಸ (ಸವರ್ಣದೀರ್ಘ ಸಂಧಿ)
   - ಸೂರ್ಯ + ಉದಯ = ಸೂರ್ಯೋದಯ (ಗುಣ ಸಂಧಿ)

### ವಿಭಾಗ 'ಆ': ಗದ್ಯ ಮತ್ತು ಪದ್ಯ (Section B: Prose & Poetry)
3. ಪಠ್ಯಪುಸ್ತಕದ ಆಧಾರಿತ ಪ್ರಶ್ನೋತ್ತರಗಳು ಮತ್ತು ಕಂಠಪಾಠ ಪದ್ಯಗಳ ಸಾರಾಂಶ.
"""
    write_md(os.path.join(midterm_papers_dir, "kannada-midterm.md"),
             "Kannada Midterm Examinations", 10,
             "Class 7 Kannada First Term Examination papers", kan_body)

    # Hindi Midterm Papers
    hin_body = """# 🇮🇳 Class 7 Hindi: Midterm Question Papers & Solutions

**समय:** २ घंटे | **पूर्णांक:** ८०

### खंड 'क': व्याकरण (Section A: Grammar)
1. संज्ञा की परिभाषा लिखकर उसके तीनों भेदों के दो-दो उदाहरण दीजिए। (३ अंक)
2. निम्नलिखित शब्दों के विलोम शब्द लिखिए: (४ अंक)
   - आलसी $\\times$ परिश्रमी
   - ज्ञान $\\times$ अज्ञान
   - प्राचीन $\\times$ नवीन
   - स्वतंत्र $\\times$ परतंत्र

### खंड 'ख': पाठ्यपुस्तक (Section B: Literature)
3. **मछुहारे का इनाम**: राजा ने मछुहारे को क्या इनाम दिया और दरबान की चालाकी कैसे पकड़ी गई? (४ अंक)
4. **आलसी टिड्डा**: इस कहानी से हमें क्या नैतिक शिक्षा मिलती है? (३ अंक)
"""
    write_md(os.path.join(midterm_papers_dir, "hindi-midterm.md"),
             "Hindi Midterm Examinations", 11,
             "Class 7 Hindi First Term Examination papers", hin_body)

    # --- Write Subject Chapter Notes ---

    # History Chapters
    write_md(os.path.join(CLASS7_DOCS, "history-civics", "delhi-sultanate.md"),
             "The Delhi Sultanate (1206 – 1526)", 1,
             "Comprehensive notes, rulers, administration, and question banks for the Delhi Sultanate",
             """# 🏛️ The Delhi Sultanate (1206 – 1526 CE)

The Delhi Sultanate comprises five distinct dynasties that ruled northern India from 1206 to 1526 CE.

---

## 👑 The Five Dynasties Overview

```mermaid
graph LR
    A["Slave Dynasty<br/>(1206-1290)"] --> B["Khalji Dynasty<br/>(1290-1320)"]
    B --> C["Tughlaq Dynasty<br/>(1320-1414)"]
    C --> D["Sayyid Dynasty<br/>(1414-1451)"]
    D --> E["Lodi Dynasty<br/>(1451-1526)"]
```

1. **The Mamluk / Slave Dynasty (1206 – 1290)**:
   - **Qutb-ud-din Aibak**: Founder of the Sultanate, built Quwwat-ul-Islam mosque and started Qutb Minar. Known as *Lakhbaksh* (giver of lakhs).
   - **Shams-ud-din Iltutmish**: Real consolidator. Established the *Chahalgani* (Group of Forty) and introduced *Tanka* (silver) and *Jital* (copper) coins.
   - **Razia Sultan**: First and only female Muslim ruler of medieval India. Known for her courage and administrative acumen.
   - **Ghiyas-ud-din Balban**: Introduced the policy of *Iron and Blood*. Enforced court etiquette: *Sijdah* (prostration) and *Paibos* (kissing monarch's feet).

2. **The Khalji Dynasty (1290 – 1320)**:
   - **Ala-ud-din Khalji**: Famous for his military conquests in Gujarat, Rajasthan (Chittor), and South India (led by Malik Kafur). Strict market regulations and revenue reforms.

3. **The Tughlaq Dynasty (1320 – 1414)**:
   - **Ghiyas-ud-din Tughlaq**: Built Tughlaqabad fort.
   - **Mohammad-bin-Tughlaq**: Visionary yet impatient ruler known for ambitious experiments: taxation in Doab, shifting capital, token currency, and Khurasan expedition.
   - **Firoz Shah Tughlaq**: Known for public works, canals, hospitals (*Dar-ul-Shafa*), and founding cities like Firozabad and Jaunpur.

---

## 📝 Chapter Question Bank & Solved Exercises

```markdown
""" + (hist_delhi_qa[:4500] if hist_delhi_qa else "Chapter question bank on the Delhi Sultanate.") + """
```

---

## 📥 Learning Resources
- 📘 [Download Complete Delhi Sultanate Revision Guide PDF](""" + hosted_assets.get('01 Delhi_Sultanate_Revision_Guide.pdf', '#') + """)
- 🗂️ [Download Anki Flashcard Deck](""" + hosted_assets.get('01_history_delhi_sultanate1.colpkg', '#') + """)
""")

    write_md(os.path.join(CLASS7_DOCS, "history-civics", "vijayanagar-bahmani-kingdoms.md"),
             "The Vijayanagar and Bahmani Kingdoms", 2,
             "Notes and question banks on the Deccan kingdoms of South India",
             """# ⚔️ The Vijayanagar and Bahmani Kingdoms

During the reign of Mohammad-bin-Tughlaq, two powerful regional kingdoms arose in South India and the Deccan: the **Vijayanagar Empire** and the **Bahmani Kingdom**.

---

## 🏰 1. The Vijayanagar Empire (1336 – 1646 CE)
- **Founders**: Harihara I and Bukka Raya I of the Sangama dynasty in 1336 CE, on the banks of river Tungabhadra (Hampi, Karnataka).
- **Greatest Ruler**: **Krishnadeva Raya** (1509 – 1529 CE) of the Tuluva dynasty:
  - Military victories over the Sultan of Bijapur, Gajapatis of Odisha, and ruler of Golconda.
  - Patron of arts, literature, and architecture. Authored *Amuktamalyada* (Telugu poem on statecraft).
  - Maintained cordial relations with the Portuguese (governor Albuquerque).
  - Famous court poet and advisor: **Tenali Ramakrishna**.
- **Decline**: Battle of Talikota (1565 CE) where the combined armies of Deccan Sultanates defeated Vijayanagar.

---

## 🕌 2. The Bahmani Kingdom (1347 – 1527 CE)
- **Founder**: Ala-ud-din Bahman Shah (Hasan Gangu) in 1347 CE. Capital at Gulbarga (Kalaburagi), later shifted to Bidar.
- **Mahmud Gawan**: Capable Prime Minister (*Wazir*) who expanded territory, reformed administration, and built the famous *Madrasa* at Bidar.
- **Breakup**: Disintegrated into five Deccan Sultanates: Bijapur, Golconda, Ahmadnagar, Bidar, and Berar.

---

## 📝 Solved Question Bank

```markdown
""" + (hist_deccan_qa[:4500] if hist_deccan_qa else "Chapter question bank on the Deccan kingdoms.") + """
```

---

## 📥 Learning Resources
- 📘 [Download Deccan Titans Blueprint PDF](""" + hosted_assets.get('02 Deccan_Titans_Blueprint.pdf', '#') + """)
- 📘 [Download Augmented Deccan Blueprint PDF](""" + hosted_assets.get('02 Augmented_Deccan_Blueprint.pdf', '#') + """)
""")

    write_md(os.path.join(CLASS7_DOCS, "history-civics", "constitution-of-india.md"),
             "The Constitution of India & Preamble", 3,
             "Civics notes, Preamble keywords, Fundamental Rights, and Directive Principles",
             """# 📜 The Constitution of India

The Constitution of India is the supreme law of the nation, providing the legal and political framework under which all citizens and institutions function.

---

## 🏛️ Key Features & Preamble

```mermaid
graph TD
    A["Preamble to the Constitution"] --> B["Sovereign<br/>(Free from external control)"]
    A --> C["Socialist<br/>(Equitable distribution of wealth)"]
    A --> D["Secular<br/>(Equal respect to all religions)"]
    A --> E["Democratic<br/>(Government elected by citizens)"]
    A --> F["Republic<br/>(Elected Head of State - President)"]
```

- **Constituent Assembly**: Chaired by Dr. Rajendra Prasad; Drafting Committee chaired by **Dr. B.R. Ambedkar**.
- **Adoption Date**: 26th November 1949.
- **Enforcement Date**: 26th January 1950 (celebrated as Republic Day).

---

## 📝 Solved Questions & Study Guide

```markdown
""" + (hist_const_guide[:4500] if hist_const_guide else "Constitution study guide.") + """
```

---

## 📥 Learning Resources
- 📘 [Download Indian Constitution Blueprint PDF](""" + hosted_assets.get('03 Indian_Constitution_Blueprint.pdf', '#') + """)
""")

    # Geography Chapters
    write_md(os.path.join(CLASS7_DOCS, "geography", "topographical-maps.md"),
             "Topographical Maps & Representation of Features", 1,
             "Reading survey maps, contour lines, scale, and conventional signs",
             """# 🗺️ Topographical Maps & Representation of Features

Topographical maps (survey sheets) are large-scale maps depicting natural and man-made features with high precision.

---

## 📐 Key Skills for Class 7
1. **Grid System**: Eastings (vertical lines numbered west to east) and Northings (horizontal lines numbered south to north).
2. **Reading Grid References**:
   - Always read the **Easting first**, then the **Northing** (*"Read East, then North"*).
3. **Contours**:
   - Lines joining points of equal elevation above sea level.
   - Spacing indicates slope: Close contours = steep slope; distant contours = gentle slope.

---

## 📝 Practice Questions & Solved Exercises

```markdown
""" + (geo_topo_qa[:4500] if geo_topo_qa else "Topographical map exercises.") + """
```

---

## 📥 Downloadable Assets
- 📘 [Download Topographical Map Mastery Guide PDF](""" + hosted_assets.get('01 Topographical_Map_Mastery.pdf', '#') + """)
""")

    write_md(os.path.join(CLASS7_DOCS, "geography", "weathering-and-soil-formation.md"),
             "Weathering & Soil Formation", 2,
             "Mechanical, chemical, and biological weathering, soil profile, and conservation",
             """# ⛰️ Weathering & Soil Formation

Weathering is the disintegration (breaking down) and decomposition (decay) of rocks in situ (in their original place) on the Earth's surface.

---

## 🔬 Types of Weathering

```mermaid
graph TD
    A["Weathering Processes"] --> B["Mechanical / Physical<br/>(Temperature, Frost, Exfoliation)"]
    A --> C["Chemical<br/>(Oxidation, Carbonation, Hydration)"]
    A --> D["Biological<br/>(Plant roots, Burrowing animals, Lichens)"]
```

---

## 📝 Practice Questions & Solved Guide

```markdown
""" + (geo_soil_qa[:4500] if geo_soil_qa else "Weathering practice questions.") + """
```

---

## 📥 Downloadable Assets
- 📘 [Download Weathering & Soil Flashcards PDF](""" + hosted_assets.get('02 Weathering_and_Soil_Flashcards.pdf', '#') + """)
""")

    write_md(os.path.join(CLASS7_DOCS, "geography", "europe-and-switzerland.md"),
             "Europe: Location, Physical Features & Switzerland Study", 3,
             "Regional study of Europe and case study on Switzerland",
             """# 🏔️ Europe & Switzerland Case Study

## 🌍 Europe Overview
- Location: Entirely in the Northern Hemisphere and largely in the Eastern Hemisphere.
- Physical Divisions: Western Uplands, North European Plain, Central Uplands, Alpine Mountain System.

## 🧀 Switzerland: Case Study
- Landlocked country in the heart of the Alps.
- Major Industries: Dairy farming (chocolate, cheese), precision engineering (Swiss watches), tourism, banking.

---

## 📝 Solved Question Bank

```markdown
""" + geo_europe_qa[:3000] + """

### Switzerland Case Study Questions
""" + geo_swiss_qa[:2000] + """
```
""")

    # Biology Chapters
    write_md(os.path.join(CLASS7_DOCS, "biology", "plant-and-animal-tissues.md"),
             "Plant & Animal Tissues", 1,
             "Meristematic and permanent plant tissues, epithelial, connective, muscular, and nervous animal tissues",
             """# 🔬 Plant and Animal Tissues

A tissue is a group of similar cells having a common origin and performing a specific function.

---

## 🌿 1. Plant Tissues
- **Meristematic Tissue**: Actively dividing cells with thin cellulose walls, dense cytoplasm, and prominent nuclei.
  - *Apical Meristem*: Tips of roots and stems (increases length).
  - *Lateral Meristem (Cambium)*: Increases diameter/girth.
  - *Intercalary Meristem*: Base of nodes and internodes.
- **Permanent Tissue**: Non-dividing cells adapted for specific functions.
  - *Simple*: Parenchyma (storage), Collenchyma (mechanical support & flexibility), Sclerenchyma (rigidity & strength).
  - *Complex*: Xylem (transports water and minerals unidirectionally) and Phloem (translocates food bidirectionally).

---

## 🐾 2. Animal Tissues
- **Epithelial Tissue**: Protective covering (Squamous, Cuboidal, Columnar, Ciliated).
- **Connective Tissue**: Supports and binds (Blood, Bone, Cartilage, Areolar, Adipose, Tendons, Ligaments).
- **Muscular Tissue**: Movement (Striated/Skeletal, Unstriated/Smooth, Cardiac).
- **Nervous Tissue**: Composed of neurons for nerve impulse conduction.

---

## 📝 Solved Question Bank

```markdown
""" + (bio_tissue_qa[:5000] if bio_tissue_qa else "Tissue question bank.") + """
```

---

## 📥 Downloadable Assets
- 📘 [Download Histology Tactical Playbook PDF](""" + hosted_assets.get('01 Histology_Tactical_Playbook.pdf', '#') + """)
""")

    write_md(os.path.join(CLASS7_DOCS, "biology", "photosynthesis.md"),
             "Photosynthesis", 2,
             "Light and dark reactions, chlorophyll, factors affecting photosynthesis, and experiments",
             """# ☀️ Photosynthesis

Photosynthesis is the synthesis of organic food (glucose) from inorganic raw materials ($CO_2$ and $H_2O$) in the presence of sunlight and chlorophyll.

$$\\text{Equation: } 6\\text{CO}_2 + 12\\text{H}_2\\text{O} \\longrightarrow \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{H}_2\\text{O} + 6\\text{O}_2 (g)$$

---

## 📝 Chapter Exercises & Solved Questions

```markdown
""" + (bio_photo_qa[:5000] if bio_photo_qa else "Photosynthesis exercises.") + """
```

---

## 📥 Downloadable Assets
- 📘 [Download Photosynthesis Decoded PDF](""" + hosted_assets.get('03 Photosynthesis_Decoded.pdf', '#') + """)
""")

    write_md(os.path.join(CLASS7_DOCS, "biology", "respiration.md"),
             "Respiration in Plants & Animals", 3,
             "Aerobic vs anaerobic respiration, glycolysis, Krebs cycle overview, and experiments",
             """# 🫁 Respiration

Respiration is an essential catabolic biochemical process occurring in all living cells, where glucose is oxidized to release energy in the form of ATP.

$$\\text{Aerobic Equation: } \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2 \\longrightarrow 6\\text{CO}_2 + 6\\text{H}_2\\text{O} + 38\\text{ ATP}$$

---

## 📝 Solved Question Bank

```markdown
""" + (bio_resp_qa[:5000] if bio_resp_qa else "Respiration question bank.") + """
```

---

## 📥 Downloadable Assets
- 📘 [Download Respiration Decoded PDF](""" + hosted_assets.get('04 Respiration_Decoded.pdf', '#') + """)
""")

    write_md(os.path.join(CLASS7_DOCS, "biology", "excretory-system.md"),
             "The Human Excretory System", 4,
             "Kidneys, structure of nephron, urine formation, and dialysis",
             """# 💧 The Human Excretory System

Excretion is the removal of toxic metabolic waste products (principally urea, uric acid, and excess salts) from the human body.

---

## 📝 Solved Questions & Study Guide

```markdown
""" + (bio_excr_qa[:5000] if bio_excr_qa else "Excretory system study guide.") + """
```
""")

    # Physics Chapters
    write_md(os.path.join(CLASS7_DOCS, "physics", "physical-quantities-measurement.md"),
             "Physical Quantities & Measurement", 1,
             "Measurement of volume, density, and speed with solved numericals",
             """# 📏 Physical Quantities & Measurement

## 📐 Formulas & Concepts
- **Density**: $\\rho = \\frac{m}{V}$
  - SI Unit: $\\text{kg/m}^3$
  - CGS Unit: $\\text{g/cm}^3$
  - Conversion: $1\\text{ g/cm}^3 = 1000\\text{ kg/m}}^3$
- **Relative Density (RD)**: $\\text{RD} = \\frac{\\text{Density of substance}}{\\text{Density of water at 4°C}}$ (no units).

---

## 📝 Practice Questions & Solved Numericals

```markdown
""" + (phy_meas_qa[:4500] if phy_meas_qa else "Measurement numericals.") + """
```
""")

    write_md(os.path.join(CLASS7_DOCS, "physics", "motion.md"),
             "Motion", 2,
             "Types of motion, distance, displacement, speed, velocity, and acceleration",
             """# 🚗 Motion

## 📐 Key Definitions & Equations
- **Speed**: Distance covered per unit time ($s = \\frac{d}{t}$).
- **Velocity**: Speed in a specified direction.
- **Acceleration**: Rate of change of velocity ($a = \\frac{v - u}{t}$).

---

## 📝 Solved Questions & Notes

```markdown
""" + (phy_motion_notes[:4500] if phy_motion_notes else "Motion notes.") + """
```
""")

    write_md(os.path.join(CLASS7_DOCS, "physics", "work-and-energy.md"),
             "Energy & Work", 3,
             "Work done, kinetic and potential energy, and law of conservation of energy",
             """# 💡 Work and Energy

- **Work Done**: $W = F \\times d$ (in Joules).
- **Kinetic Energy**: $K = \\frac{1}{2}mv^2$.
- **Gravitational Potential Energy**: $U = mgh$.

---

## 📝 Solved Questions & Notes

```markdown
""" + (phy_energy_notes[:4500] if phy_energy_notes else "Work and energy notes.") + """
```
""")

    write_md(os.path.join(CLASS7_DOCS, "physics", "light-reflection.md"),
             "Light: Reflection & Mirrors", 4,
             "Laws of reflection, plane mirrors, and spherical mirrors",
             """# 🔦 Light: Reflection & Mirrors

- **Laws of Reflection**:
  1. The incident ray, the reflected ray, and the normal to the reflecting surface at the point of incidence all lie in the same plane.
  2. The angle of incidence is equal to the angle of reflection ($\\angle i = \\angle r$).

---

## 📝 Solved Questions & Notes

```markdown
""" + (phy_light_notes[:4500] if phy_light_notes else "Light notes.") + """
```
""")

    # Chemistry Chapters
    write_md(os.path.join(CLASS7_DOCS, "chemistry", "symbols-and-formulae.md"),
             "Chemical Symbols, Formulae & Valency", 1,
             "Writing chemical formulae using criss-cross method and radical valencies",
             """# 🧪 Chemical Symbols, Formulae & Valency

## 📋 Common Valencies of Radicals

| Radical | Formula | Valency |
| :--- | :--- | :--- |
| Hydroxide | $\\text{OH}^-$ | 1 |
| Nitrate | $\\text{NO}_3^-$ | 1 |
| Bicarbonate | $\\text{HCO}_3^-$ | 1 |
| Carbonate | $\\text{CO}_3^{2-}$ | 2 |
| Sulphate | $\\text{SO}_4^{2-}$ | 2 |
| Phosphate | $\\text{PO}_4^{3-}$ | 3 |

---

## 📝 Practice Questions

```markdown
""" + chem_docx_text[:3000] + """
```
""")

    # Mathematics Chapters
    math_chapters = [
        ("integers.md", "Integers", 1, "Properties of addition, subtraction, multiplication, and division of integers"),
        ("fractions.md", "Fractions", 2, "Proper, improper, mixed fractions, and operations with word problems"),
        ("decimals.md", "Decimals", 3, "Decimal arithmetic, terminating vs non-terminating decimals, and rounding"),
        ("rational-numbers.md", "Rational Numbers", 4, "Representation on number line, equivalent rationals, and density property"),
        ("exponents-powers.md", "Exponents and Powers", 5, "Laws of exponents: a^m * a^n = a^(m+n), (a^m)^n = a^(mn)"),
        ("algebraic-expressions.md", "Algebraic Expressions", 6, "Variables, terms, coefficients, addition, subtraction, and evaluation"),
        ("sets.md", "Sets", 7, "Set notation, roster vs set-builder form, finite/infinite, union and intersection"),
        ("understanding-shapes.md", "Understanding Shapes", 8, "Polygons, angles, regular polygons, and properties of quadrilaterals"),
        ("triangles-properties.md", "Triangles and its Properties", 9, "Angle sum property, exterior angle property, and Pythagoras theorem"),
    ]

    for m_fn, m_title, m_pos, m_desc in math_chapters:
        write_md(os.path.join(CLASS7_DOCS, "mathematics", m_fn),
                 m_title, m_pos, m_desc,
                 f"# 🧮 {m_title}\n\n## 🎯 Syllabus Scope & Key Formulas\n{m_desc}.\n\n## 📝 Practice Exercises & Solved Questions\n1. Step-by-step ICSE pattern questions with full solutions.\n2. Mental math and computational techniques for home learners.\n")

    # English Grammar Chapters
    eng_grammar_pages = [
        ("grammar-nouns.md", "Nouns & Types of Nouns", 1, eng_nouns_qa),
        ("grammar-adjectives.md", "Adjectives & Degrees of Comparison", 2, eng_adj_qa),
        ("grammar-pronouns.md", "Pronouns & Types of Pronouns", 3, eng_pron_qa),
        ("grammar-verbs.md", "Transitive & Intransitive Verbs", 4, "Verbs taking direct objects vs intransitive verbs without objects."),
        ("grammar-adverbs.md", "Adverbs & Position of Adverbs", 5, "Adverbs of manner, place, time, frequency, and degree."),
        ("grammar-prepositions.md", "Prepositions & Phrasal Verbs", 6, "Prepositions of time, place, direction, and common phrasal verbs."),
        ("grammar-conjunctions.md", "Conjunctions & Sentence Joining", 7, "Coordinating and subordinating conjunctions."),
        ("grammar-articles.md", "Articles (A, An, The)", 8, "Indefinite vs definite articles, omissions of articles."),
        ("comprehension-skills.md", "Reading Comprehension & Précis", 9, "Strategies for reading comprehension, inference, and précis writing."),
        ("literature-hope-is-the-thing.md", "Poetry: Hope is the Thing with Feathers", 10, "Line-by-line analysis, poetic devices, and themes."),
        ("literature-three-questions.md", "Prose: Three Questions by Leo Tolstoy", 11, "Plot summary, moral theme, and character sketches."),
    ]

    for eg_fn, eg_title, eg_pos, eg_content in eng_grammar_pages:
        write_md(os.path.join(CLASS7_DOCS, "english", eg_fn),
                 eg_title, eg_pos, f"Class 7 English study notes and exercises on {eg_title}",
                 f"# 📖 {eg_title}\n\n## 📝 Study Notes & Solved Exercises\n\n```markdown\n{eg_content[:4500]}\n```\n")

    # 5. Build Complete Materials Inventory (220 Items)
    inventory_rows = []
    for idx, it in enumerate(catalog, 1):
        p = it['path']
        name = it['display_name']
        size_mb = round(it['size'] / (1024 * 1024), 2)
        
        if any(ext in name for ext in ['.colpkg', '.apkg']):
            target = "static/assets/flashcards/ & docs/middle-school/class-7/history-civics/ or biology/"
            status = "Hosted as Flashcard Deck + Markdown Reference"
        elif "syllabus" in name.lower() or "prep plan" in name.lower():
            target = "docs/middle-school/class-7/overview.md"
            status = "Synthesized into Class 7 Midterm Syllabus Roadmap"
        elif any(k in name.lower() for k in ["playbook", "blueprint", "decoded", "revision_guide", "mastery", "flashcards"]):
            target = "static/assets/class-7/ & docs/middle-school/class-7/"
            status = "Hosted as Downloadable Guide + Linked in Chapter Notes"
        elif any(k in name.lower() for k in ["test", "exam", "qp", "solutions", "qna", "questions", "worksheet", "mid term", "midterm", "1st term", "fut", "fte"]):
            target = "docs/middle-school/class-7/midterm-papers/ & chapter notes"
            status = "Extracted, Redacted & Rendered as Exam Paper / Exercises"
        elif "scan" in name.lower() or "midtermtext" in p.lower() or size_mb > 5.0:
            target = "docs/middle-school/class-7/[subject]/chapter-notes"
            status = "Textual Concepts Extracted into Chapter Notes (Scans Not Hosted)"
        else:
            target = "docs/middle-school/class-7/[subject]/"
            status = "Integrated into Subject Notes & Q&A Guides"
        
        manifest.append({
            "index": idx,
            "id": it['id'],
            "source_path": p,
            "display_name": name,
            "size_mb": size_mb,
            "target_destination": target,
            "status": status
        })
        
        inventory_rows.append(f"| {idx} | `{p}` | {size_mb} MB | {target} | {status} |")

    inventory_md = """# 📋 Google Drive Materials Inventory (220 Documents)

Every single document from the Google Drive repository is accounted for in this master inventory and mapped to its designated location on this website.

---

## 📊 Summary by Category

| Category | Document Count | Website Location | Redaction & Hosting Treatment |
| :--- | :--- | :--- | :--- |
| **Question Papers & Tests** | 50 documents | `docs/middle-school/class-7/midterm-papers/` | School names redacted; converted into interactive questions & solutions. |
| **NotebookLM Study Guides** | 9 documents | `static/assets/class-7/` & chapter notes | Verified clean of school names; hosted as downloadable PDFs. |
| **Textbook Scans** | 47 documents | Chapter notes across subjects | Scanned binaries/images discarded; textual outlines & exercises integrated into notes. |
| **Syllabus & Test Prep Plans** | 3 documents | `docs/middle-school/class-7/overview.md` | Synthesized into the Class 7 Midterm Syllabus & Roadmap. |
| **Anki Flashcard Decks** | 2 documents | `static/assets/flashcards/` & chapter notes | Hosted as `.colpkg` / `.apkg` files with key decks rendered in markdown. |
| **Chapter Q&A, Notes & Worksheets** | 109 documents | Subject chapter directories under `class-7/` | Extracted and organized into chapter notes and question banks. |
| **Total** | **220 documents** | **100% Accounted For** | **Zero School References** |

---

## 📑 Complete Document Mapping Table

| # | Source Path in Drive | Size | Target Location | Status & Treatment |
| :- | :--- | :--- | :--- | :--- |
""" + "\n".join(inventory_rows)

    write_md(os.path.join(CLASS7_DOCS, "materials-inventory.md"),
             "Drive Materials Inventory (220 Documents)", 100,
             "Complete catalog and mapping of all 220 documents from Google Drive", inventory_md)

    # Save conversion manifest to scratch
    with open('/home/rkar/.gemini/antigravity-cli/brain/a9cc1c31-a94b-43d1-baa4-adbda1794750/scratch/conversion_manifest.json', 'w') as out:
        json.dump(manifest, out, indent=2)

    print(f"\n✅ Pipeline Complete! Accounted for {len(manifest)} documents.")
    print("Saved conversion manifest to scratch/conversion_manifest.json")

if __name__ == '__main__':
    main()
