import json
from django.shortcuts import render, redirect
from .quiz_data import (
    get_questions,
    get_majors,
    get_major_by_key,
    score_quiz,
    get_top_careers,
    get_career_categories,
    get_results_summary_paragraph,
    get_suggested_majors,
    get_explore_summary_paragraph,
)


def quiz_home_view(request):
    """Step 1: Choose short or full quiz. If length in GET, set session and redirect to choose-path."""
    length = request.GET.get('length')
    if length == 'short':
        request.session['quiz_short'] = True
        return redirect('career_quiz_choose_path')
    if length == 'full':
        request.session['quiz_short'] = False
        return redirect('career_quiz_choose_path')
    return render(request, 'career_quiz/quiz_home.html')


def choose_path_view(request):
    """Step 2: Choose path (major vs explore). Requires quiz length to be set."""
    if 'quiz_short' not in request.session:
        return redirect('career_quiz_home')
    return render(request, 'career_quiz/quiz_choose_path.html', {
        'quiz_short': request.session['quiz_short'],
    })


def about_view(request):
    """About FutureFit — company info, mission, what we offer."""
    return render(request, 'career_quiz/quiz_about.html')


def how_it_works_view(request):
    """How the Career Discovery Quiz works — formats, paths, what you get."""
    return render(request, 'career_quiz/quiz_how_it_works.html')


def major_selection_view(request):
    """User picks their major; we store it in session and redirect to the quiz."""
    if request.GET.get('length') == 'short':
        request.session['quiz_short'] = True
    elif request.GET.get('length') == 'full':
        request.session['quiz_short'] = False
    if request.method == 'POST':
        major_key = request.POST.get('major')
        if major_key:
            request.session['quiz_major'] = major_key
            return redirect('career_quiz_take')
    majors = get_majors()
    preselect = request.GET.get('preselect', '')
    quiz_short = request.session.get('quiz_short', False)
    return render(request, 'career_quiz/major_selection.html', {
        'majors': majors,
        'preselect': preselect,
        'quiz_short': quiz_short,
    })


def quiz_view(request):
    """Show the quiz. If no major in session, redirect to major selection."""
    if not request.session.get('quiz_major'):
        return redirect('career_quiz_major')
    quiz_short = request.session.get('quiz_short', False)
    questions = get_questions(short=quiz_short)
    major = get_major_by_key(request.session['quiz_major'])
    return render(request, 'career_quiz/quiz.html', {
        'questions': questions,
        'major': major,
        'quiz_short': quiz_short,
    })


def quiz_results_view(request):
    if request.method != 'POST':
        return render(request, 'career_quiz/quiz_results.html', {
            'suggestions': [],
            'scores': [],
            'scores_json': '[]',
            'major': None,
            'error': True,
        })
    major_key = request.POST.get('major') or request.session.get('quiz_major')
    quiz_short = request.session.get('quiz_short', False)
    num_questions = len(get_questions(short=quiz_short))
    selected = []
    for i in range(1, num_questions + 1):
        key = request.POST.get(f'q{i}')
        if key:
            selected.append(key)
    if len(selected) < num_questions:
        return render(request, 'career_quiz/quiz_results.html', {
            'suggestions': [],
            'scores': [],
            'scores_json': '[]',
            'major': get_major_by_key(major_key) if major_key else None,
            'error': True,
            'message': 'Please answer all questions.',
        })
    score_tuples = score_quiz(selected)
    category_names = {c[0]: (c[1], c[2]) for c in get_career_categories()}
    scores_with_names = [
        (cat, score, category_names.get(cat, (cat, ''))[0], category_names.get(cat, (cat, ''))[1])
        for cat, score in score_tuples
    ]
    suggestions = get_top_careers(score_tuples, major_key=major_key, max_careers=6)
    major_info = get_major_by_key(major_key) if major_key else None
    results_summary = get_results_summary_paragraph(
        scores_with_names, suggestions,
        major_label=major_info['label'] if major_info else None,
    )
    scores_json = json.dumps([{'name': name, 'score': score} for _c, score, name, _d in scores_with_names])
    return render(request, 'career_quiz/quiz_results.html', {
        'suggestions': suggestions,
        'scores': scores_with_names,
        'scores_json': scores_json,
        'results_summary': results_summary,
        'major': major_info,
        'error': False,
        'message': None,
    })


def explore_quiz_view(request):
    """Broad quiz for students who don't know their major—no major selection."""
    if request.GET.get('length') == 'short':
        request.session['quiz_short'] = True
    elif request.GET.get('length') == 'full':
        request.session['quiz_short'] = False
    quiz_short = request.session.get('quiz_short', False)
    questions = get_questions(short=quiz_short)
    return render(request, 'career_quiz/explore_quiz.html', {
        'questions': questions,
        'quiz_short': quiz_short,
    })


def explore_results_view(request):
    """Results for explore quiz: suggested majors, job categories, and sample careers. GET with saved answers re-displays results."""
    quiz_short = request.session.get('quiz_short', False)
    num_questions = len(get_questions(short=quiz_short))
    if request.method == 'GET':
        answers = request.session.get('explore_quiz_answers')
        if not answers or len(answers) < num_questions:
            return redirect('career_quiz_home')
        return _render_explore_results(answers, request)
    selected = []
    for i in range(1, num_questions + 1):
        key = request.POST.get(f'q{i}')
        if key:
            selected.append(key)
    if len(selected) < num_questions:
        return render(request, 'career_quiz/explore_results.html', {
            'suggested_majors': [],
            'scores': [],
            'scores_json': '[]',
            'suggestions': [],
            'explore_summary': None,
            'error': True,
            'message': 'Please answer all questions.',
        })
    request.session['explore_quiz_answers'] = selected
    return _render_explore_results(selected, request)


def _render_explore_results(selected, request):
    """Shared: compute and render explore results from a list of answer option keys."""
    score_tuples = score_quiz(selected)
    category_names = {c[0]: (c[1], c[2]) for c in get_career_categories()}
    scores_with_names = [
        (cat, score, category_names.get(cat, (cat, ''))[0], category_names.get(cat, (cat, ''))[1])
        for cat, score in score_tuples
    ]
    suggested_majors = get_suggested_majors(score_tuples, top_n=6)
    suggestions = get_top_careers(score_tuples, major_key=None, max_careers=6)
    explore_summary = get_explore_summary_paragraph(scores_with_names, suggested_majors)
    scores_json = json.dumps([{'name': name, 'score': score} for _c, score, name, _d in scores_with_names])
    return render(request, 'career_quiz/explore_results.html', {
        'suggested_majors': suggested_majors,
        'scores': scores_with_names,
        'scores_json': scores_json,
        'suggestions': suggestions,
        'explore_summary': explore_summary,
        'error': False,
        'message': None,
    })


def results_for_major_view(request, major_key):
    """
    Show career results for a specific major using the user's saved explore quiz answers.
    No need to retake the quiz—we reuse their explore results and filter by major.
    """
    quiz_short = request.session.get('quiz_short', False)
    num_required = len(get_questions(short=quiz_short))
    answers = request.session.get('explore_quiz_answers')
    if not answers or len(answers) < num_required:
        return redirect('career_quiz_home')
    major_info = get_major_by_key(major_key)
    if not major_info:
        return redirect('career_quiz_home')
    score_tuples = score_quiz(answers)
    category_names = {c[0]: (c[1], c[2]) for c in get_career_categories()}
    scores_with_names = [
        (cat, score, category_names.get(cat, (cat, ''))[0], category_names.get(cat, (cat, ''))[1])
        for cat, score in score_tuples
    ]
    suggestions = get_top_careers(score_tuples, major_key=major_key, max_careers=6)
    results_summary = get_results_summary_paragraph(
        scores_with_names, suggestions,
        major_label=major_info['label'],
    )
    scores_json = json.dumps([{'name': name, 'score': score} for _c, score, name, _d in scores_with_names])
    return render(request, 'career_quiz/quiz_results.html', {
        'suggestions': suggestions,
        'scores': scores_with_names,
        'scores_json': scores_json,
        'results_summary': results_summary,
        'major': major_info,
        'from_explore': True,
        'error': False,
        'message': None,
    })
