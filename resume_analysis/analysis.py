"""
Gap analysis logic: compare resume text with job listing and identify missing skills/requirements.
"""
import re
from collections import defaultdict


def extract_keywords(text):
    """Extract potential skills/requirements as lowercase words and phrases."""
    if not text:
        return set()
    text = text.lower()
    # Remove common punctuation, keep hyphens for phrases like "problem-solving"
    text = re.sub(r'[^\w\s\-]', ' ', text)
    # Split on whitespace
    words = set(w.strip() for w in text.split() if len(w.strip()) > 1)
    # Also consider 2–3 word phrases that might be skills (e.g. "machine learning")
    words_and_phrases = set(words)
    tokens = [t for t in text.split() if len(t) > 1]
    for i in range(len(tokens) - 1):
        bigram = f"{tokens[i]} {tokens[i+1]}"
        if len(bigram) > 4:
            words_and_phrases.add(bigram)
    for i in range(len(tokens) - 2):
        trigram = f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}"
        if len(trigram) > 6:
            words_and_phrases.add(trigram)
    return words_and_phrases


def extract_requirements_sentences(job_text):
    """Heuristic: lines/sentences that look like requirements (contain 'required', 'must', etc.)."""
    if not job_text:
        return []
    lines = []
    for raw in job_text.split('\n'):
        line = raw.strip()
        if not line:
            continue
        lower = line.lower()
        if any(kw in lower for kw in ('required', 'preferred', 'must have', 'should have', 'qualifications', 'experience with', 'knowledge of', 'ability to')):
            lines.append(line)
    if not lines:
        # Fallback: treat each non-empty line as a potential requirement
        lines = [l.strip() for l in job_text.split('\n') if l.strip() and len(l.strip()) > 10]
    return lines[:50]


def run_gap_analysis(resume_text, job_listing_text):
    """
    Compare resume and job listing. Return dict with:
    - missing_skills: set of keywords in job but not in resume
    - matching_skills: set of keywords in both
    - missing_requirements: list of requirement-like sentences from job that don't appear in resume
    - summary: short summary stats
    """
    resume_kw = extract_keywords(resume_text)
    job_kw = extract_keywords(job_listing_text)
    job_requirements = extract_requirements_sentences(job_listing_text)

    missing_skills = job_kw - resume_kw
    matching_skills = job_kw & resume_kw

    # Filter missing to likely "skills" (drop very short or generic words)
    stopwords = {
        'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'has', 'are', 'was', 'were',
        'will', 'would', 'could', 'should', 'may', 'can', 'all', 'our', 'you', 'your', 'they',
        'their', 'been', 'being', 'other', 'into', 'only', 'when', 'what', 'which', 'who',
        'about', 'after', 'before', 'between', 'during', 'more', 'most', 'some', 'such',
        'than', 'then', 'there', 'these', 'those', 'where', 'while', 'will', 'just', 'also',
    }
    missing_skills = {s for s in missing_skills if s not in stopwords and len(s) > 2}
    # Limit to most relevant: prefer longer phrases and words
    missing_list = sorted(missing_skills, key=lambda x: (-len(x), x))[:80]
    matching_list = sorted(matching_skills, key=lambda x: (-len(x), x))[:80]

    resume_lower = (resume_text or '').lower()
    missing_requirements = []
    for req in job_requirements:
        # Check if the gist of this requirement appears in resume (simple substring)
        req_lower = req.lower()
        # Require at least one significant word from the requirement to be in resume for "match"
        req_words = set(w for w in re.findall(r'\w+', req_lower) if len(w) > 3)
        overlap = req_words & set(re.findall(r'\w+', resume_lower))
        if len(overlap) < max(1, len(req_words) // 2):
            missing_requirements.append(req)

    return {
        'missing_skills': missing_list,
        'matching_skills': matching_list,
        'missing_requirements': missing_requirements[:25],
        'summary': {
            'total_job_keywords': len(job_kw),
            'matched_count': len(matching_skills),
            'missing_count': len(missing_list),
            'match_percentage': round(100 * len(matching_skills) / len(job_kw), 1) if job_kw else 0,
        },
    }
