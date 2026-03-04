"""
Resume & Writing app views.

Sections:
  - Page views: home, templates (resume/cover letter/admissions essay), tips, AI tools, generate
  - API: template HTML, cover letter HTML, PDF generation
  - AI API: Gemini-backed endpoints for gap analysis, enhancement, review, etc.
"""
import io
import json
import logging
import os
import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from .resume_data import RESUME_TEMPLATES, RESUME_TIPS, COVER_LETTER_TEMPLATES
from .models import SavedDocument


# ---------------------------------------------------------------------------
# Page views
# ---------------------------------------------------------------------------

def resume_home_view(request):
    majors = [
        {'key': k, 'label': v['label'], 'icon': v['icon'], 'image': v.get('image'), 'focus': v['focus']}
        for k, v in RESUME_TEMPLATES.items()
    ]
    return render(request, 'resume/home.html', {
        'majors': majors,
    })


def resume_templates_view(request, doc_type=None):
    majors = [
        {'key': k, 'label': v['label'], 'icon': v['icon'], 'image': v.get('image'), 'focus': v['focus']}
        for k, v in RESUME_TEMPLATES.items()
    ]
    doc_type = doc_type or 'resume'
    return render(request, 'resume/templates.html', {
        'majors': majors,
        'doc_type': doc_type,
        'tips': RESUME_TIPS,
    })


def resume_template_detail_view(request, major_key):
    template_data = RESUME_TEMPLATES.get(major_key)
    if not template_data:
        raise Http404("Resume template not found for this major.")
    load_id = request.GET.get('load')
    return render(request, 'resume/template_detail.html', {
        'major_key': major_key,
        'template': template_data,
        'user_is_authenticated': request.user.is_authenticated,
        'load_id': load_id,
    })


def resume_tips_view(request):
    return render(request, 'resume/tips.html', {
        'tips': RESUME_TIPS,
    })


def resume_ai_tools_view(request):
    return render(request, 'resume/ai_tools.html')


def resume_generate_view(request):
    """AI Resume Generator form page."""
    return render(request, 'resume/generate.html')


@login_required
def my_saved_view(request):
    """List current user's saved documents."""
    documents = SavedDocument.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'resume/my_saved.html', {'documents': documents})


@login_required
@require_POST
def save_document_view(request):
    """Create or update a saved document. Expects JSON: title, major_key, doc_type, content; optional id for update."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    title = (data.get('title') or '').strip() or 'Untitled'
    major_key = (data.get('major_key') or '').strip() or None
    doc_type = data.get('doc_type', 'resume')
    if doc_type not in dict(SavedDocument.DOC_TYPE_CHOICES):
        doc_type = 'resume'
    content = data.get('content', '')
    doc_id = data.get('id')
    if doc_id is not None:
        try:
            doc = SavedDocument.objects.get(pk=doc_id, user=request.user)
            doc.title = title
            doc.major_key = major_key
            doc.doc_type = doc_type
            doc.content = content
            doc.save()
        except SavedDocument.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)
    else:
        doc = SavedDocument.objects.create(
            user=request.user,
            title=title,
            major_key=major_key,
            doc_type=doc_type,
            content=content,
        )
    return JsonResponse({
        'id': doc.id,
        'title': doc.title,
        'major_key': doc.major_key or '',
        'doc_type': doc.doc_type,
        'updated_at': doc.updated_at.isoformat(),
    })


@login_required
@require_GET
def load_document_view(request, pk):
    """Return a saved document's content (and metadata) for the current user."""
    try:
        doc = SavedDocument.objects.get(pk=pk, user=request.user)
    except SavedDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)
    return JsonResponse({
        'content': doc.content,
        'title': doc.title,
        'major_key': doc.major_key or '',
        'doc_type': doc.doc_type,
    })


# ---------------------------------------------------------------------------
# API: template/cover-letter HTML, PDF generation
# ---------------------------------------------------------------------------

def resume_template_html_view(request, major_key):
    """Return template HTML for a major (for inline loading on templates page)."""
    template_data = RESUME_TEMPLATES.get(major_key)
    if not template_data:
        return JsonResponse({'error': 'Template not found.'}, status=404)
    html = _build_resume_template_html(template_data, major_key)
    return JsonResponse({'html': html, 'label': template_data['label']})


def resume_cover_letter_html_view(request, major_key):
    """Return cover letter HTML for a major (for inline loading on cover letters page)."""
    cover_data = COVER_LETTER_TEMPLATES.get(major_key)
    resume_data = RESUME_TEMPLATES.get(major_key)
    if not cover_data and not resume_data:
        return JsonResponse({'error': 'Cover letter template not found.'}, status=404)
    html = _build_cover_letter_html(cover_data or resume_data, major_key)
    label = (cover_data or resume_data)['label']
    return JsonResponse({'html': html, 'label': f'{label} Cover Letter'})


def _build_resume_template_html(template, major_key=None):
    """Build resume-paper HTML as H1/H2/P flow for single Quill editor (Word-like)."""
    label = template['label']
    focus = template.get('focus', '').lower()
    sections = template.get('sections', [])
    sample_bullets = template.get('sample_bullets', [])

    def section_content(section):
        if section == 'Summary':
            return f'<p>Results-driven {label} student with experience in {focus}. Passionate about making an impact through practical skills and a strong work ethic. Seeking an entry-level position to apply classroom knowledge in a professional setting.</p>'
        if section in ('Education', 'Education & Training'):
            return f'<p><strong>Bachelor of Science in {label}</strong><br>Your University · Expected May 2026<br>GPA: 3.X/4.0 · Relevant Coursework: [Add your courses]</p>'
        if section in ('Technical Skills', 'Skills', 'Tools & Software', 'Skills & Tools', 'Skills & Equipment'):
            return '<p>Add your relevant skills, tools, and software here. Separate technical skills from soft skills for clarity.</p>'
        if section in ('Certifications', 'Certifications & Licenses', 'Licenses & Certifications'):
            return '<p>List relevant certifications, licenses, and professional training. Include dates earned and issuing organization.</p>'
        if section in ('Portfolio', 'Portfolio & Projects'):
            return '<p>Link to your online portfolio (e.g., Behance, Dribbble, GitHub, personal website). List 2–3 key projects with brief descriptions of your role and impact.</p>'
        # Experience sections
        bullets = ''.join(f'<li>{b}</li>' for b in sample_bullets)
        return f'<ul>{bullets}</ul>'

    contact_placeholder = (
        'email@example.com · (555) 123-4567 · City, State · linkedin.com/in/yourname · github.com/yourname'
        if major_key == 'computer_science'
        else 'email@example.com · (555) 123-4567 · City, State · linkedin.com/in/yourname'
    )

    parts = [
        '<h1>Your Name</h1>',
        f'<p>{contact_placeholder}</p>',
    ]
    for s in sections:
        parts.append(f'<h2>{s}</h2>')
        parts.append(section_content(s))
    return ''.join(parts)


def _build_cover_letter_html(template, major_key=None):
    """Build cover letter HTML as H2/P flow for single Quill editor (Word-like)."""
    label = template.get('label', 'Student')
    sample = template.get('sample_letter', '')
    if sample:
        return f'<h2>Cover Letter</h2>{sample}'
    # Fallback for majors without custom sample
    contact = (
        'email@example.com · (555) 123-4567 · City, State · linkedin.com/in/yourname · github.com/yourname'
        if major_key == 'computer_science'
        else 'email@example.com · (555) 123-4567 · City, State · linkedin.com/in/yourname'
    )
    generic = (
        f'<p>Your Name<br>{contact}</p>'
        '<p>February 18, 2026</p>'
        '<p>Hiring Manager<br>Company Name<br>123 Business Ave<br>City, State 12345</p>'
        '<p>Dear Hiring Manager,</p>'
        f'<p>I am writing to express my interest in the [Position Title] opportunity at [Company Name]. '
        f'As a {label} student at [Your University], I am eager to contribute to your team and grow '
        'as a professional.</p>'
        '<p>[Replace with 1–2 paragraphs that highlight your qualifications, experience, and interest in the role. '
        'Use specific examples and tailor to the job description.]</p>'
        '<p>I would welcome the opportunity to discuss how my background aligns with your needs. Thank you for '
        'considering my application.</p>'
        '<p>Sincerely,<br>Your Name</p>'
    )
    return f'<h2>Cover Letter</h2>{generic}'


@csrf_exempt
@require_POST
def resume_pdf_view(request):
    """Generate a PDF from the resume HTML content. Uses WeasyPrint for selectable text and proper formatting."""
    try:
        body = json.loads(request.body)
        html_content = body.get('html', '').strip()
        filename = body.get('filename', 'resume.pdf')
        if not html_content:
            return JsonResponse({'error': 'No HTML content provided.'}, status=400)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    html_content = _prepare_resume_html(html_content)
    full_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@page {{ size: letter; margin: 0.5in; }}
body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333; line-height: 1.5; margin: 0; padding: 0; }}
.resume-name {{ font-size: 18pt; font-weight: bold; color: #1F2A44; margin-bottom: 4pt; text-align: center; }}
.resume-contact {{ font-size: 10pt; color: #5A6478; text-align: center; margin-bottom: 12pt; padding-bottom: 8pt; border-bottom: 2pt solid #1F2A44; }}
.resume-section {{ margin-bottom: 10pt; }}
.resume-section-title {{ font-size: 11pt; font-weight: bold; color: #1F2A44; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1pt solid #333; padding-bottom: 4pt; margin-bottom: 6pt; }}
.resume-content {{ font-size: 10pt; color: #444; }}
.resume-content ul {{ margin: 4pt 0; padding-left: 20pt; }}
.resume-content li {{ margin-bottom: 4pt; }}
.resume-content strong {{ font-weight: bold; }}
</style>
</head>
<body>
{html_content}
</body>
</html>'''

    full_html = _html_safe_for_weasyprint(full_html)
    pdf_bytes, pdf_err = _html_to_pdf(full_html)
    if pdf_err:
        status = 503 if 'not available' in pdf_err else 500
        return JsonResponse({'error': pdf_err}, status=status)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Length'] = str(len(pdf_bytes))
    safe_name = re.sub(r'[^\w\-\.]', '_', filename)
    if not safe_name.lower().endswith('.pdf'):
        safe_name += '.pdf'
    response['Content-Disposition'] = f'attachment; filename="{safe_name}"'
    return response


def _prepare_resume_html(html):
    """Convert resume-paper HTML structure to xhtml2pdf-friendly format."""
    cleaned = html.replace('class="rp-header"', 'style="text-align:center; border-bottom:2px solid #1F2A44; padding-bottom:8pt; margin-bottom:12pt;"')
    cleaned = cleaned.replace('class="rp-name"', 'class="resume-name" style="font-size:18pt; font-weight:bold; text-align:center;"')
    cleaned = cleaned.replace('class="rp-contact"', 'class="resume-contact" style="font-size:10pt; text-align:center;"')
    cleaned = cleaned.replace('class="rp-section"', 'class="resume-section" style="margin-bottom:12pt;"')
    cleaned = cleaned.replace('class="rp-section-title"', 'class="resume-section-title" style="font-size:11pt; font-weight:bold; text-transform:uppercase; border-bottom:1px solid #ccc; padding-bottom:4pt; margin-bottom:6pt;"')
    cleaned = cleaned.replace('class="rp-content"', 'class="resume-content" style="font-size:10pt;"')
    cleaned = cleaned.replace('contenteditable="true"', '')
    # H1/H2 from single Quill editor (Word-like structure)
    cleaned = re.sub(
        r'<h1(?=\s|>)',
        '<h1 style="font-size:18pt; font-weight:bold; text-align:center; margin:0 0 4pt; color:#1F2A44;"',
        cleaned
    )
    cleaned = re.sub(
        r'<h2(?=\s|>)',
        '<h2 style="font-size:11pt; font-weight:bold; text-transform:uppercase; letter-spacing:0.05em; border-bottom:1px solid #ccc; padding-bottom:4pt; margin:12pt 0 6pt; color:#1F2A44;"',
        cleaned
    )
    return cleaned


def _html_safe_for_weasyprint(html_string):
    """Ensure HTML is valid UTF-8 and strip characters that can break WeasyPrint."""
    if not isinstance(html_string, str):
        html_string = str(html_string, 'utf-8', errors='replace')
    # Replace problematic control chars and ensure valid Unicode
    html_string = html_string.encode('utf-8', errors='replace').decode('utf-8')
    # Remove null bytes and other control characters that can corrupt PDF
    html_string = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', html_string)
    return html_string


def _html_to_pdf(full_html):
    """
    Convert HTML string to PDF bytes. Tries WeasyPrint first; on Windows WeasyPrint
    often fails (GTK/Pango not installed), so falls back to xhtml2pdf (pure Python).
    Returns (pdf_bytes, None) on success, or (None, error_message) on failure.
    """
    # Try WeasyPrint first (better quality where available, e.g. Linux/Mac)
    try:
        from weasyprint import HTML
        result = io.BytesIO()
        HTML(string=full_html).write_pdf(result)
        pdf_bytes = result.getvalue()
        if pdf_bytes:
            return pdf_bytes, None
    except Exception as e:
        err_msg = str(e).lower()
        # WeasyPrint often fails: missing GTK/Pango, or not installed (pycairo/cairo), or ImportError
        if (
            'libgobject' in err_msg or 'gobject' in err_msg or 'find_library' in err_msg
            or 'load library' in err_msg or 'weasyprint' in err_msg or 'no module named' in err_msg
        ):
            pass  # fall through to xhtml2pdf
        else:
            return None, f'PDF generation failed: {e}'

    # Fallback: xhtml2pdf (pure Python, works on Windows without extra deps)
    try:
        from xhtml2pdf import pisa
        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(full_html, dest=result, encoding='utf-8')
        if pisa_status.err:
            return None, 'PDF generation failed (xhtml2pdf reported errors).'
        pdf_bytes = result.getvalue()
        if not pdf_bytes:
            return None, 'PDF generation produced an empty file.'
        return pdf_bytes, None
    except ImportError:
        return None, 'PDF generation not available. Install xhtml2pdf: pip install xhtml2pdf'
    except Exception as e:
        return None, f'PDF generation failed: {e}'


# --------------- AI API endpoints ---------------
# API key stays in backend only (.env). Auto-detects AI Studio vs Vertex (Google Cloud) key.
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
_force_vertex_ai = None  # Set to True after first "API keys are not supported" so we use Vertex


def _get_gemini_key():
    return (
        os.environ.get('GEMINI_API_KEY')
        or os.environ.get('YOUR_GEMINI_API_KEY')
        or os.environ.get('GOOGLE_API_KEY', '')
    )


def _use_vertex_ai():
    if _force_vertex_ai is not None:
        return _force_vertex_ai
    v = os.environ.get('GEMINI_USE_VERTEX_AI', '').lower()
    return v in ('true', '1', 'yes')


def _gemini_client(use_vertex=False):
    """Return a genai Client: AI Studio (api_key) or Vertex AI (vertexai=True, api_key)."""
    try:
        from google import genai
    except ImportError:
        logger.warning("google-genai not installed; AI features disabled. pip install google-genai")
        return None
    key = _get_gemini_key()
    if not key or key == 'your-gemini-api-key-here':
        return None
    if use_vertex:
        return genai.Client(vertexai=True, api_key=key)
    return genai.Client(api_key=key)


def _do_generate(client, prompt):
    """One attempt with given client. Returns (text, None) or (None, error_msg)."""
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={'temperature': 0.7, 'max_output_tokens': 1024},
        )
        text = getattr(response, 'text', None)
        if not text and response.candidates and response.candidates[0].content.parts:
            text = response.candidates[0].content.parts[0].text
        if not text:
            return None, 'Empty response from model'
        return text, None
    except Exception as e:
        return None, str(e)


def _call_gemini(prompt):
    """Call the Gemini API. Tries AI Studio first; if key needs Vertex, retries with Vertex and remembers."""
    global _force_vertex_ai
    key = _get_gemini_key()
    if not key or key == 'your-gemini-api-key-here':
        return None, 'Gemini API key not configured. Add GEMINI_API_KEY in your .env file.'

    client = _gemini_client(use_vertex=_use_vertex_ai())
    if client is None:
        return None, 'Gemini API key not configured. Add GEMINI_API_KEY in your .env file.'

    text, err = _do_generate(client, prompt)
    if err and ('API keys are not supported' in err or 'OAuth2' in err or 'assert a principal' in err):
        _force_vertex_ai = True
        client_vertex = _gemini_client(use_vertex=True)
        text, err = _do_generate(client_vertex, prompt)
    if err:
        return None, err
    return text, None


def ai_status_view(request):
    """Check if the AI backend is available."""
    key = _get_gemini_key()
    configured = bool(key and key != 'your-gemini-api-key-here')
    return JsonResponse({'available': configured})


@csrf_exempt
@require_POST
def ai_extract_pdf_view(request):
    """Extract text from an uploaded PDF file."""
    pdf_file = request.FILES.get('file') or request.FILES.get('pdf')
    if not pdf_file:
        return JsonResponse({'error': 'No PDF file provided.'}, status=400)
    if not pdf_file.name.lower().endswith('.pdf'):
        return JsonResponse({'error': 'File must be a PDF.'}, status=400)
    if pdf_file.size > 10 * 1024 * 1024:  # 10 MB max
        return JsonResponse({'error': 'PDF must be under 10 MB.'}, status=400)
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_file)
        text_parts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
        text = '\n\n'.join(text_parts).strip()
        if not text:
            return JsonResponse({'error': 'Could not extract text from this PDF. It may be image-based or scanned.'}, status=400)
        return JsonResponse({'text': text})
    except Exception as e:
        return JsonResponse({'error': f'Failed to extract text: {str(e)}'}, status=400)


@csrf_exempt
@require_POST
def ai_generate_content_view(request):
    """Generate content from a prompt/task for FutureBot inline use."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    prompt_text = body.get('prompt', '').strip()
    task = body.get('task', '').strip()

    if not prompt_text and not task:
        return JsonResponse({'error': 'Please provide a prompt or task.'}, status=400)

    combined = f'{task}. {prompt_text}' if task and prompt_text else (prompt_text or task)

    task_prompts = {
        'Idea Brainstorm': 'You are a creative writing coach. Generate 5–7 bullet-point ideas based on the user\'s topic. Be concise and actionable. Return ONLY the bullet points.',
        'Paragraph Generator': 'You are an expert writer. Write a well-structured paragraph based on the user\'s request. Be professional and clear. Return ONLY the paragraph.',
        'Case Study': 'You are a professional writer. Write a brief case study or example based on the user\'s topic. Be specific and compelling. Return ONLY the content.',
        'Business Proposal': 'You are a business writing expert. Draft a section for a business proposal based on the user\'s request. Be professional and persuasive. Return ONLY the content.',
        'Resume Summary': 'You are an expert resume writer. Write a 2–3 sentence professional summary based on the user\'s background/goals. Return ONLY the summary.',
        'Cover Letter': 'You are an expert cover letter writer. Draft a paragraph for a cover letter based on the user\'s request. Return ONLY the paragraph.',
    }

    base_instruction = task_prompts.get(task, 'You are a helpful writing assistant. Generate clear, professional content based on the user\'s request. Return ONLY the generated content, no labels or explanation.')

    prompt = f'{base_instruction}\n\nUser request: {combined}'

    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip()})


@csrf_exempt
@require_POST
def ai_enhance_bullet_view(request):
    """Enhance a resume bullet point."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    bullet = body.get('bullet', '').strip()
    major = body.get('major', 'college')
    if not bullet:
        return JsonResponse({'error': 'Please provide a bullet point.'}, status=400)

    prompt = (
        f'You are an expert resume writer for {major} students. '
        'Rewrite this resume bullet point to be more impactful. Use a strong action verb, '
        'add specificity, and quantify results where possible. Keep it to ONE concise bullet point (one sentence). '
        'Return ONLY the improved bullet point, no explanation or extra text.\n\n'
        f'Original: {bullet}'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip().lstrip('-•* ')})


@csrf_exempt
@require_POST
def ai_generate_summary_view(request):
    """Generate a professional resume summary."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    major = body.get('major', 'your field')
    role = body.get('role', '')
    level = body.get('level', 'entry-level')
    skills = body.get('skills', '')

    prompt = (
        f'You are an expert resume writer. Write a professional resume summary (2-3 sentences) for a '
        f'{level} {major} student'
        + (f' targeting a {role} role' if role else '') + '. '
        + (f'Key skills: {skills}. ' if skills else '')
        + 'Make it confident, specific, and tailored. Return ONLY the summary paragraph, no labels or explanation.'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip()})


@csrf_exempt
@require_POST
def ai_suggest_skills_view(request):
    """Suggest skills based on major and target role."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    major = body.get('major', 'your field')
    role = body.get('role', '')

    prompt = (
        f'You are a career advisor for {major} students. '
        + (f'The student is targeting a {role} role. ' if role else '')
        + 'List 12-15 relevant skills they should include on their resume, separated into '
        '"Technical Skills" and "Soft Skills" categories. Format as two short lists. '
        'Return ONLY the skill lists, no extra explanation. Use bullet points.'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip()})


@csrf_exempt
@require_POST
def ai_tailor_resume_view(request):
    """Tailor resume content to a job description, or run gap analysis (compare resume to job posting)."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    resume = body.get('resume', '').strip()
    job = body.get('job', '').strip()
    mode = body.get('mode', '')

    if not resume or not job:
        return JsonResponse({'error': 'Please provide both resume content and a job description.'}, status=400)

    if mode == 'gap_analysis':
        return _ai_gap_analysis(resume, job)
    return _ai_tailor_resume(resume, job)


def _ai_gap_analysis(resume, job):
    """Compare resume to job posting; return match score, strengths, missing keywords, and suggestions."""
    prompt = (
        'You are an expert resume consultant and hiring manager. Analyze how well the following resume matches '
        'the job description. Return your analysis as a JSON object with EXACTLY this structure (no markdown, no code fences, ONLY raw JSON):\n'
        '{\n'
        '  "match_score": <number 0-100 representing overall match percentage>,\n'
        '  "summary": "<1-2 sentence overview of how well the resume matches>",\n'
        '  "strengths": ["<strength 1>", "<strength 2>", ...],\n'
        '  "missing_keywords": ["<keyword 1>", "<keyword 2>", ...],\n'
        '  "suggestions": ["<actionable suggestion 1>", "<actionable suggestion 2>", ...]\n'
        '}\n\n'
        'Rules:\n'
        '- match_score should reflect realistic alignment (most students score 30-70)\n'
        '- strengths: 2-4 things the resume already does well for this role\n'
        '- missing_keywords: 4-8 specific skills, tools, or keywords from the job posting missing from the resume\n'
        '- suggestions: 3-5 specific, actionable things the student could add or change to improve their match\n'
        '- Return ONLY the JSON object, nothing else\n\n'
        f'--- RESUME ---\n{resume}\n\n--- JOB DESCRIPTION ---\n{job}'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    # Parse JSON response
    cleaned = text.strip().replace('```json', '').replace('```', '').strip()
    try:
        parsed = json.loads(cleaned)
        match_score = parsed.get('match_score', 50)
        if not isinstance(match_score, (int, float)):
            match_score = 50
        match_score = max(0, min(100, int(match_score)))
        result = {
            'match_score': match_score,
            'summary': parsed.get('summary', 'Analysis complete.'),
            'strengths': parsed.get('strengths', []) if isinstance(parsed.get('strengths'), list) else [],
            'missing_keywords': parsed.get('missing_keywords', []) if isinstance(parsed.get('missing_keywords'), list) else [],
            'suggestions': parsed.get('suggestions', []) if isinstance(parsed.get('suggestions'), list) else [],
        }
        return JsonResponse({'result': result})
    except json.JSONDecodeError:
        return JsonResponse({
            'result': {
                'match_score': 50,
                'summary': cleaned[:500] if cleaned else 'Analysis complete.',
                'strengths': [],
                'missing_keywords': [],
                'suggestions': [cleaned] if cleaned else ['Could not parse structured analysis.']
            }
        })


def _ai_tailor_resume(resume, job):
    """Rewrite resume content to better match the job description."""
    prompt = (
        'You are an expert resume consultant. A student has the following resume content and wants to tailor it '
        'to a specific job posting. Rewrite their resume content to better match the job description by:\n'
        '1. Incorporating relevant keywords from the job posting\n'
        '2. Reordering bullet points to highlight the most relevant experience\n'
        '3. Strengthening bullet points with action verbs and quantified results\n'
        '4. Keeping the same overall structure\n\n'
        'Return ONLY the improved resume content, formatted with clear section headers and bullet points. '
        'Do not include any explanation or commentary.\n\n'
        f'--- RESUME CONTENT ---\n{resume}\n\n'
        f'--- JOB DESCRIPTION ---\n{job}'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip()})


@csrf_exempt
@require_POST
def ai_review_resume_view(request):
    """Full resume review: score, verdict, strengths, improvements, missing."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    resume_text = body.get('resume', '').strip()
    major = body.get('major', 'college')
    if not resume_text or len(resume_text) < 30:
        return JsonResponse({'error': 'Please provide resume content (at least 30 characters).'}, status=400)

    prompt = (
        f'You are an expert resume reviewer and career counselor for {major} students. '
        'Review the following resume and provide detailed, actionable feedback. '
        'Return your review as a JSON object with EXACTLY this structure (no markdown, no code fences, ONLY raw JSON):\n'
        '{\n'
        '  "score": <number 0-100 representing overall resume quality>,\n'
        '  "verdict": "<one short phrase like \'Strong foundation, needs polish\'>",\n'
        '  "strengths": ["<strength 1>", "<strength 2>", ...],\n'
        '  "improvements": [\n'
        '    {"area": "<section or aspect>", "issue": "<what\'s wrong>", "fix": "<specific suggestion>"},\n'
        '    ...\n'
        '  ],\n'
        '  "missing": ["<thing they should add 1>", ...]\n'
        '}\n\n'
        'Rules: score 40-75 typical; 2-3 strengths; 3-5 improvements; 2-4 missing. '
        'Return ONLY the JSON object, nothing else.\n\n'
        f'--- RESUME ---\n{resume_text}'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)

    cleaned = text.strip().replace('```json', '').replace('```', '').strip()
    try:
        parsed = json.loads(cleaned)
        score = parsed.get('score', 50)
        if not isinstance(score, (int, float)):
            score = 50
        score = max(0, min(100, int(score)))
        result = {
            'score': score,
            'verdict': parsed.get('verdict') or 'Review complete',
            'strengths': parsed.get('strengths') if isinstance(parsed.get('strengths'), list) else [],
            'improvements': parsed.get('improvements') if isinstance(parsed.get('improvements'), list) else [],
            'missing': parsed.get('missing') if isinstance(parsed.get('missing'), list) else [],
        }
        return JsonResponse({'result': result})
    except json.JSONDecodeError:
        return JsonResponse({
            'result': {
                'score': 50,
                'verdict': 'Review complete',
                'strengths': [],
                'improvements': [{'area': 'General', 'issue': 'Could not parse feedback', 'fix': cleaned[:300]}],
                'missing': [],
            }
        })


@csrf_exempt
@require_POST
def ai_enhance_resume_view(request):
    """Enhance resume content: improve wording, add bold/formatting to key terms."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    html_content = body.get('html', '').strip()
    major = body.get('major', 'your field')
    if not html_content or len(html_content) < 50:
        return JsonResponse({'error': 'Please provide resume content to enhance.'}, status=400)

    prompt = (
        f'You are an expert resume writer for {major} students. Enhance the following resume HTML. '
        'Improve wording to be more impactful, add <strong> to key achievements and skills, '
        'and apply <em> where appropriate for emphasis. Keep the exact same HTML structure '
        '(same div classes: rp-name, rp-contact, rp-section, rp-section-title, rp-content, ul, li). '
        'Return ONLY the enhanced HTML with no explanation. Preserve all section titles and layout.\n\n'
        f'--- RESUME HTML ---\n{html_content}'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'html': text.strip()})


def _call_gemini_long(prompt, max_tokens=2048):
    """Call Gemini with higher token limit for longer outputs (e.g. full resume)."""
    global _force_vertex_ai
    key = _get_gemini_key()
    if not key or key == 'your-gemini-api-key-here':
        return None, 'Gemini API key not configured. Add GEMINI_API_KEY in your .env file.'

    client = _gemini_client(use_vertex=_use_vertex_ai())
    if client is None:
        return None, 'Gemini API key not configured.'

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={'temperature': 0.5, 'max_output_tokens': max_tokens},
        )
        text = getattr(response, 'text', None)
        if not text and response.candidates and response.candidates[0].content.parts:
            text = response.candidates[0].content.parts[0].text
        if not text:
            return None, 'Empty response from model'
        return text, None
    except Exception as e:
        err = str(e)
        if 'API keys are not supported' in err or 'OAuth2' in err or 'assert a principal' in err:
            _force_vertex_ai = True
            client_vertex = _gemini_client(use_vertex=True)
            try:
                response = client_vertex.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config={'temperature': 0.5, 'max_output_tokens': max_tokens},
                )
                text = getattr(response, 'text', None)
                if not text and response.candidates and response.candidates[0].content.parts:
                    text = response.candidates[0].content.parts[0].text
                if not text:
                    return None, 'Empty response from model'
                return text, None
            except Exception as e2:
                return None, str(e2)
        return None, err


@csrf_exempt
@require_POST
def resume_generate_pdf_view(request):
    """Generate a resume from form answers via AI, return PDF."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    name = (body.get('name') or '').strip()
    email = (body.get('email') or '').strip()
    phone = (body.get('phone') or '').strip()
    job_title = (body.get('job_title') or '').strip()
    if not name or not email or not phone or not job_title:
        return JsonResponse({'error': 'Please fill in name, email, phone, and job title.'}, status=400)

    try:
        return _generate_pdf_impl(body, name, email, phone, job_title)
    except Exception as e:
        logger.exception('resume_generate_pdf failed')
        return JsonResponse({'error': str(e)}, status=500)


def _generate_pdf_impl(body, name, email, phone, job_title):
    """Generate resume PDF; returns HttpResponse or raises."""
    prompt = (
        'You are an expert resume writer. Generate a professional, one-page resume as HTML. '
        'Use EXACTLY this structure - no extra wrapper, only the content below. '
        'Return ONLY the HTML, no explanation or markdown.\n\n'
        'Structure:\n'
        '<div class="rp-header">\n'
        '  <div class="rp-name">FULL NAME</div>\n'
        '  <div class="rp-contact">email | phone | location | linkedin [| github for tech roles]</div>\n'
        '</div>\n'
        '<div class="rp-section">\n'
        '  <div class="rp-section-title">SUMMARY</div>\n'
        '  <div class="rp-content">2-3 sentence summary tailored to the target role</div>\n'
        '</div>\n'
        '<div class="rp-section">\n'
        '  <div class="rp-section-title">EDUCATION</div>\n'
        '  <div class="rp-content">degree, school, date, GPA if provided</div>\n'
        '</div>\n'
        '<div class="rp-section">\n'
        '  <div class="rp-section-title">EXPERIENCE</div>\n'
        '  <div class="rp-content"><ul><li>bullet 1</li><li>bullet 2</li>...</ul></div>\n'
        '</div>\n'
        '<div class="rp-section">\n'
        '  <div class="rp-section-title">SKILLS</div>\n'
        '  <div class="rp-content">skills listed</div>\n'
        '</div>\n'
        '(Add PROJECTS or CERTIFICATIONS sections only if the user provided that info.)\n\n'
        'Rules: Use <strong> for emphasis. Bullets in <ul><li>. Keep it one page. Match keywords from the job.\n\n'
        f'--- USER INFO ---\n'
        f'Name: {name}\nEmail: {email}\nPhone: {phone}\n'
        f'Location: {body.get("location", "")}\nLinkedIn: {body.get("linkedin", "")}\nGitHub: {body.get("github", "")}\n'
        f'Target job: {job_title}\nCompany/industry: {body.get("company", "")}\n'
        f'Keywords to include: {body.get("keywords", "")}\n'
        f'Education: {body.get("degree", "")} at {body.get("school", "")}, grad: {body.get("graduation", "")}, GPA: {body.get("gpa", "")}\n'
        f'Experience: {body.get("experience", "")}\n'
        f'Skills: {body.get("skills", "")}\n'
        f'Projects/extracurriculars: {body.get("projects", "")}\n'
        f'Certifications: {body.get("certifications", "")}\n'
        f'Their summary (use or improve): {body.get("summary", "")}'
    )

    text, err = _call_gemini_long(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)

    html_content = text.strip()
    # Remove markdown code blocks if present
    if html_content.startswith('```'):
        html_content = re.sub(r'^```\w*\n?', '', html_content)
        html_content = re.sub(r'\n?```\s*$', '', html_content)
    html_content = html_content.strip()

    html_content = _prepare_resume_html(html_content)
    full_html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@page { size: letter; margin: 0.5in; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333; line-height: 1.5; margin: 0; padding: 0; }
.resume-name { font-size: 18pt; font-weight: bold; color: #1F2A44; margin-bottom: 4pt; text-align: center; }
.resume-contact { font-size: 10pt; color: #5A6478; text-align: center; margin-bottom: 12pt; padding-bottom: 8pt; border-bottom: 2pt solid #1F2A44; }
.resume-section { margin-bottom: 10pt; }
.resume-section-title { font-size: 11pt; font-weight: bold; color: #1F2A44; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1pt solid #333; padding-bottom: 4pt; margin-bottom: 6pt; }
.resume-content { font-size: 10pt; color: #444; }
.resume-content ul { margin: 4pt 0; padding-left: 20pt; }
.resume-content li { margin-bottom: 4pt; }
.resume-content strong { font-weight: bold; }
</style>
</head>
<body>
''' + html_content + '''
</body>
</html>'''

    pdf_bytes, pdf_err = _html_to_pdf(full_html)
    if pdf_err:
        status = 503 if 'not available' in pdf_err else 500
        return JsonResponse({'error': pdf_err}, status=status)

    safe_name = re.sub(r'[^\w\-\.]', '_', name or 'resume')
    filename = f'{safe_name}-resume.pdf'
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Length'] = str(len(pdf_bytes))
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
