# Contributing to Bangalore Home Schooling (ICSE)

Thank you for your interest in contributing to the **Bangalore Home Schooling** curriculum portal! This project is built by homeschooling parents, independent educators, and learners to make high-quality ICSE-aligned educational resources freely accessible.

---

## 🌟 Ways You Can Contribute

1. **Chapter Notes & Summaries**: Write concise, concept-first notes for any subject and standard (Pre-KG to Class 10).
2. **ICSE Question Banks**: Add objective MCQs, 2-mark definitions/reasons, 3-mark conceptual questions, and 5-mark structured questions with step-by-step solutions and marking schemes.
3. **Printable Worksheets**: Create practice sheets with solution keys.
4. **Visuals & Assets**: Contribute diagrams, flowcharts, mind maps, or educational activity guides.
5. **Bangalore & Homeschooling Guidance**: Share field trip experiences, library resources, co-op meetups, and practical homeschooling tips.

---

## 🛠️ Step-by-Step Contribution Workflow

### 1. Fork & Clone
```bash
git clone https://github.com/<your-username>/bangalore-home-schooling.git
cd bangalore-home-schooling
git checkout -b add-class-10-physics-calorimetry
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Add or Modify Content
Locate the relevant stage and class in `docs/`:
- Foundation: `docs/foundation/{pre-kg, lkg, ukg}/`
- Primary: `docs/primary/class-{1..5}/`
- Middle School: `docs/middle-school/class-{6..8}/`
- Secondary: `docs/secondary/class-{9, 10}/`
- Homeschooling Guide: `docs/homeschooling-guide/`

Follow the structure specified in [AGENTS.md](AGENTS.md) and [.agents/rules/curriculum-standards.md](.agents/rules/curriculum-standards.md).

### 4. Verify the Build
Before submitting your changes, always verify that the static site builds without broken links:
```bash
npm run build
```

### 5. Submit a Pull Request
Commit your changes with a descriptive message and open a Pull Request against the `main` branch.

---

## 📋 Content Guidelines

- **Spelling**: Use British English spelling (e.g., *colour*, *aluminium*, *sulphate*, *programme*) as required by CISCE.
- **Formulas**: Write mathematical and chemical formulas using LaTeX (`$inline$` or `$$block$$`).
- **Marking Scheme**: When providing question answers for Middle or Secondary school, indicate marks in square brackets (e.g., `[1 Mark]`) for each step.
- **Originality**: Ensure all submitted notes and explanations are original or openly licensed. Do not paste copyrighted textbook text verbatim.
