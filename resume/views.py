import json
import os

from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from google import genai

from .resume_data import RESUME_TEMPLATES, RESUME_TIPS


def resume_home_view(request):
    majors = [
        {'key': k, 'label': v['label'], 'icon': v['icon'], 'focus': v['focus']}
        for k, v in RESUME_TEMPLATES.items()
    ]
    return render(request, 'resume/home.html', {
        'majors': majors,
    })


def resume_templates_view(request):
    majors = [
        {'key': k, 'label': v['label'], 'icon': v['icon'], 'focus': v['focus']}
        for k, v in RESUME_TEMPLATES.items()
    ]
    return render(request, 'resume/templates.html', {
        'majors': majors,
    })


def resume_template_detail_view(request, major_key):
    template_data = RESUME_TEMPLATES.get(major_key)
    if not template_data:
        raise Http404("Resume template not found for this major.")
    return render(request, 'resume/template_detail.html', {
        'major_key': major_key,
        'template': template_data,
    })


def resume_tips_view(request):
    return render(request, 'resume/tips.html', {
        'tips': RESUME_TIPS,
    })


def resume_ai_tools_view(request):
    return render(request, 'resume/ai_tools.html')


# --------------- AI API endpoints ---------------
# API key stays in backend only (.env). Auto-detects AI Studio vs Vertex (Google Cloud) key.
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')
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
