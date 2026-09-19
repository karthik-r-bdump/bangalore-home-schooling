# Agent Guidelines: Bangalore Home Schooling (ICSE)

Welcome! This repository hosts an open-source educational portal and curriculum repository for homeschooling families following the **ICSE (Indian Certificate of Secondary Education / CISCE)** syllabus from **Pre-KG to Class 10**.

---

## 🎯 Primary Goals

1. **Curriculum Integrity**: All educational notes, questions, and worksheets must strictly adhere to the Council for the Indian School Certificate Examinations (CISCE) regulations, syllabus, and marking conventions.
2. **School-Agnostic & Anonymization Policy (CRITICAL)**:
   - This portal is completely **school-agnostic**.
   - **NEVER** mention any specific school name (e.g., *The Frank Anthony Public School*, *FAPS*, *Bishop Cotton*, *Greenwood High*, *Bethany*, *NPS*, etc.) anywhere in the repository, documentation, page titles, URLs, frontmatter, or content.
   - **NEVER** host or link raw PDF scans or images that contain school crests, letterheads, watermarks, or teacher/examiner names.
   - All past examination papers, unit tests, and worksheets must be retitled using standardized, generic ICSE naming (e.g., *"ICSE Class 7 Midterm Examination - Paper 1"* or *"Class 7 First Term Exam (FTE) Specimen Paper"*).
   - Before committing any changes, the redaction linter (`npm run lint:redaction`) **MUST** pass with zero violations.
3. **Accessible Explanations**: Concepts should be presented clearly with real-world examples, diagrams, and progressive difficulty suitable for independent and home learners.
4. **Reproducibility & Quality**: All changes must preserve documentation integrity and pass the Docusaurus build (`npm run build`) without broken links.

---

## 📁 Repository Structure

- `docs/`: All curriculum content and homeschooling guides.
  - `homeschooling-guide/`: Practical guidelines for Bangalore/India (legal context, planning, rubrics, books).
  - `foundation/`: Pre-KG, LKG, UKG (ECCE / Play-based learning & phonics).
  - `primary/`: Classes 1 through 5 (Foundational English, Math, EVS/Science, Social Studies, Second Languages).
  - `middle-school/`: Classes 6 through 8 (Physics, Chemistry, Biology, History & Civics, Geography, Math, Coding).
    - `class-7/`: Comprehensive Class 7 curriculum, chapter notes, and centralized midterm question paper bank.
  - `secondary/`: Classes 9 and 10 (ICSE Board Examination preparation, 10-year question banks, Java BlueJ).
- `src/`: Custom React components, homepage, and global styles.
- `static/`: Static assets (images, downloadable PDFs, worksheets).
- `scripts/`: Automation, extraction, and validation tools.
  - `lint_school_names.py`: Redaction validator preventing school-specific references.
- `.github/workflows/deploy.yml`: Automated GitHub Actions deployment to GitHub Pages.

---

## ✍️ Content Standards

### 1. Frontmatter
Every markdown file in `docs/` must start with proper YAML frontmatter:
```markdown
---
title: Chapter or Subject Name
sidebar_position: 1 # integer position in the sidebar
description: Brief summary for SEO and previews
---
```

### 2. Math & Formulas
Use standard LaTeX syntax enabled via `remark-math` and `rehype-katex`:
- Inline formulas: `$E = mc^2$`
- Block formulas:
  ```markdown
  $$
  I = \frac{P \times R \times T}{100}
  $$
  ```

### 3. Callout Admonitions
Use Docusaurus admonitions for tips, warnings, and high-yield notes:
```markdown
:::note ICSE Board Tip
In Physics numericals, 1 mark is allocated for stating the formula, 1 mark for substitution with proper units, and 1 mark for the final answer with units.
:::

:::tip Bangalore Learning Spot
Visit the Visvesvaraya Industrial and Technological Museum (VITM) on Kasturba Road to explore interactive exhibits related to this topic!
:::
```

### 4. Diagrams & Visuals
- Use Mermaid diagrams for flowcharts, cycles, and taxonomic trees:
  ```markdown
  ```mermaid
  graph TD
      A[Sunlight] --> B[Chlorophyll]
      B --> C[Photosynthesis]
  ```
- Store raster images (PNG, JPG) or vector graphics (SVG) in `static/img/` and reference them using relative paths or `/img/...`.
- **Never store images containing school letterheads, logos, or scanned textbook pages.**

---

## 🧪 Verification Commands

Before concluding any work that adds or updates content:
```bash
# 1. Validate redaction (zero school references)
npm run lint:redaction

# 2. Type check and build test
npm run build
```
Never commit changes if either command fails.
