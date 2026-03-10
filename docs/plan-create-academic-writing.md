# Create Tab: Academic Writing Layout and Options (updated)

## Overview

Reframe the Create section as a unified "academic writing" hub: update the home layout and copy, add document-type choice (resume, cover letter, admissions essay) to gap analysis and to AI generate, reword the template card, and show a dynamic templates hero title by doc_type. Nav dropdown stays as-is.

---

## 1. Create home: academic writing hub

**File:** `templates/resume/home.html`

- **Hero:** Broaden messaging to academic writing (resumes, cover letters, admissions essays). Keep badge and primary CTA to templates.
- **Card 1 – AI-generated:** Single card "AI-generated documents" (or similar) with copy for resume, cover letter, or admissions essay; link to generate page (doc-type selector there).
- **Card 2 – Templates:** Title e.g. "Create from a template"; description: resume, cover letter, or admissions essay by major; CTA "Browse templates →"; link to `resume_templates`.
- **Card 3 – Gap analysis:** Title e.g. "Resume, cover letter & essay gap analysis"; copy: paste your document and (job posting or essay prompt); link to `resume_ai_tools`.

---

## 2. Gap analysis: document type (resume | cover letter | admissions essay)

**Backend –** `resume/views.py`

- `ai_tailor_resume_view`: Read `document_type` from body (`resume` | `cover_letter` | `admissions_essay`), default `resume`. Pass into `_ai_gap_analysis`.
- `_ai_gap_analysis(resume, job_or_prompt, document_type='resume')`:  
  - For **resume** / **cover_letter**: second input is "job description"; prompt compares document to job posting (existing for resume; add cover_letter variant).  
  - For **admissions_essay**: second input is "prompt / rubric"; prompt compares essay to the prompt/rubric and returns same JSON shape (match_score, summary, strengths, missing_keywords, suggestions) framed for essay fit.

**Frontend –** `templates/resume/ai_tools.html`

- Document type selector: **Resume** | **Cover letter** | **Admissions essay**.
- When Admissions essay is selected: right column label/placeholder becomes "Essay prompt / rubric" (instead of "Job description"). Left column "Your admissions essay". Headings and button text update accordingly.
- Pass selected `document_type` into `ResumeAI.analyzeGap(resume, jobOrPrompt, documentType)`.

**Frontend –** `static/js/resume-ai.js`

- `analyzeGap(resume, job, documentType)`: send `document_type: documentType || 'resume'` in request body.

---

## 3. AI-generated: resume, cover letter, and admissions essay

**Frontend –** `templates/resume/generate.html`

- Doc-type selector at top: **Resume** | **Cover letter** | **Admissions essay**. Form fields shared where possible; optional short hints per type.
- Submit sends `document_type: 'resume' | 'cover_letter' | 'admissions_essay'` with existing fields.
- Support `?type=cover_letter` and `?type=admissions_essay` so cards/links can deep-link.

**Backend –** `resume/views.py`

- `resume_generate_pdf_view`: Accept `document_type`; allow `resume` (default), `cover_letter`, `admissions_essay`. Same required fields for all for v1.
- `_generate_pdf_impl`: Branch on `document_type`:
  - **Resume:** Existing prompt and HTML/PDF.
  - **Cover letter:** New helper (e.g. `_generate_cover_letter_pdf_impl`) — letter prompt and letter HTML, same PDF pipeline.
  - **Admissions essay:** New helper (e.g. `_generate_admissions_essay_pdf_impl`) — essay prompt (e.g. prompt/rubric, word count), essay HTML (readable essay layout), same PDF pipeline.

No new URLs; same `resume_generate` and `resume_generate_pdf`.

---

## 4. Templates hero title by doc_type

**File:** `templates/resume/templates.html`

- Hero title is currently hardcoded "Resume Templates". Make it dynamic from `doc_type`:
  - `resume` → "Resume Templates"
  - `cover_letter` → "Cover Letter Templates"
  - `admissions_essay` → "Admissions Essay Templates"
- Use existing `doc_type` passed from `resume_templates_view` (already in context for sidebar). No URL or view changes.

---

## 5. Nav dropdown

**No change.** Nav already points to Resume home, Cover letters, Admissions essays; keep as-is.

---

## 6. Summary of file changes

| Area | Files |
|------|--------|
| Create home | `templates/resume/home.html` |
| Gap analysis (doc type + admissions essay) | `templates/resume/ai_tools.html`, `resume/views.py` (`ai_tailor_resume_view`, `_ai_gap_analysis`), `static/js/resume-ai.js` |
| AI-generated (resume + cover letter + admissions essay) | `templates/resume/generate.html`, `resume/views.py` (`resume_generate_pdf_view`, `_generate_pdf_impl` + cover letter and admissions essay helpers) |
| Templates hero by doc_type | `templates/resume/templates.html` |

---

## 7. Flow (all doc types)

- **Create home** → AI-generated card → **Generate page** (choose Resume / Cover letter / Admissions essay) → same form → API branches on `document_type` → PDF.
- **Create home** → Templates card → **Templates page** (hero title and sidebar by doc_type: Resume / Cover letters / Admissions essays).
- **Create home** → Gap analysis card → **AI tools page** (choose Resume / Cover letter / Admissions essay) → paste document + job or prompt → API uses `document_type` in prompt → same result shape.
