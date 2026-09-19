# 📚 Bangalore Home Schooling: ICSE Curriculum Portal

[![Deploy to GitHub Pages](https://github.com/karthik-r-bdump/bangalore-home-schooling/actions/workflows/deploy.yml/badge.svg)](https://github.com/karthik-r-bdump/bangalore-home-schooling/actions/workflows/deploy.yml)
[![Built with Docusaurus](https://img.shields.io/badge/built%20with-Docusaurus%20v3-green.svg)](https://docusaurus.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An open-source, community-driven curriculum repository and educational portal for homeschooling families, independent learners, and educators following the **ICSE (Indian Certificate of Secondary Education / CISCE)** curriculum in **Bangalore, Karnataka**, and across India.

🌐 **Website**: [https://karthik-r-bdump.github.io/bangalore-home-schooling/](https://karthik-r-bdump.github.io/bangalore-home-schooling/)

---

## 🌟 Key Highlights

- 🧒 **Pre-KG to Class 10**: Fully organized structure covering all stages of schooling.
  - **🌱 Foundation Stage (Pre-KG, LKG, UKG)**: Phonics, Early Numeracy, Sensory Play, and Fine Motor Skills.
  - **🎒 Primary Stage (Classes 1 to 5)**: Foundational English, Mathematics, Environmental Studies (EVS), General Science, Social Studies, Second Languages, and Computer Studies.
  - **🔬 Middle School Stage (Classes 6 to 8)**: Physics, Chemistry, Biology, History & Civics, Geography, Algebra & Geometry, and Coding.
  - **🎓 Secondary Stage (Classes 9 & 10 - ICSE Board)**: Board exam preparation, 10-year question banks, specimen paper breakdowns, Java / BlueJ Computer Applications, and marking schemes.
- 📐 **Math & Science Formula Support**: Integrated with LaTeX via KaTeX (`$inline$` and `$$block$$` formulas).
- 📝 **Structured Question Banks**: Objective MCQs, 2-mark definitions/reasons, 3-mark conceptual questions, and 5-mark structured numericals with transparent step marking.
- 🏡 **Bangalore Homeschooling Guide**: Legal aspects under the Right to Education (RTE) Act, daily routines, curriculum planning, recommended textbooks (Selina, Morning Star, Frank), and local Bangalore educational visits (VITM, Planetarium, Lalbagh).
- 🚀 **GitHub Actions Deployment**: Automatic static site generation and deployment to GitHub Pages on push to `main`.

---

## 📂 Repository Structure

```text
bangalore-home-schooling/
├── .agents/                        # Agent instructions, rules, and skills
│   ├── rules/
│   │   └── curriculum-standards.md # ICSE content and mark allocation guidelines
│   └── skills/
│       └── icse-content-creator/   # Custom skill to generate ICSE notes & worksheets
├── .github/
│   └── workflows/
│       └── deploy.yml              # Automated GitHub Pages CI/CD workflow
├── docs/                           # Curriculum content and notes
│   ├── intro.md                    # Main introductory portal
│   ├── homeschooling-guide/        # Legal, planning, rubrics, and recommended books
│   ├── foundation/                 # Pre-KG, LKG, UKG
│   ├── primary/                    # Classes 1 through 5
│   ├── middle-school/              # Classes 6 through 8
│   └── secondary/                  # Classes 9 & 10 (ICSE Board)
├── src/                            # Custom React components & pages
│   ├── components/                 # HomepageFeatures, StageCards
│   ├── css/custom.css              # Custom styling & theme
│   └── pages/index.tsx             # Interactive landing page
├── static/                         # Static assets (images, worksheets, PDFs)
├── docusaurus.config.ts            # Docusaurus configuration
├── sidebars.ts                     # Sidebar hierarchy configuration
└── package.json                    # Dependencies & scripts
```

---

## 🛠️ Getting Started Locally

### Prerequisites
- **Node.js**: v20.0 or later
- **npm**: v10.0 or later

### Installation
```bash
# Clone the repository
git clone https://github.com/karthik-r-bdump/bangalore-home-schooling.git
cd bangalore-home-schooling

# Install dependencies
npm install
```

### Running Locally
```bash
npm start
```
This runs the development server at `http://localhost:3000/bangalore-home-schooling/`. Most changes reflect live without needing to restart.

### Production Build & Verification
```bash
npm run build
npm run serve
```
This bundles the site into static files in `build/` and verifies that there are no broken links or missing assets.

---

## 🤝 Contributing

We welcome contributions from parents, teachers, educators, and students!
- Add chapter summaries, mind maps, and diagrams
- Add questions with step-by-step marking schemes
- Share printable practice worksheets and answer keys
- Improve Bangalore-specific homeschooling resources

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
Educational materials and notes are shared freely to empower home learners everywhere.
