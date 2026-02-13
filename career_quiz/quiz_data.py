"""
Career quiz: questions and career mappings based on likes, dislikes, and personality.
"""
# Each question has id, text, and options that map to career category scores
# Categories: analytical, creative, helping, leading, organizing, technical, outdoor, research

CAREER_CATEGORIES = [
    ('analytical', 'Analytical & Data-Driven', 'Data analysis, finance, accounting, strategy'),
    ('creative', 'Creative & Design', 'Design, writing, arts, marketing, media'),
    ('helping', 'Helping & People-Focused', 'Healthcare, teaching, counseling, social work'),
    ('leading', 'Leading & Influencing', 'Management, sales, entrepreneurship, law'),
    ('organizing', 'Organizing & Detail-Oriented', 'Operations, project management, administration'),
    ('technical', 'Technical & Building', 'Engineering, software, IT, construction'),
    ('outdoor', 'Hands-On & Outdoor', 'Agriculture, trades, environmental, sports'),
    ('research', 'Research & Discovery', 'Science, academia, R&D, journalism'),
]

QUESTIONS = [
    {
        'id': 1,
        'text': 'How do you prefer to spend your free time?',
        'options': [
            ('building', 'Building or fixing things', ['technical', 'organizing']),
            ('reading', 'Reading or learning something new', ['research', 'analytical']),
            ('people', 'Spending time with friends or helping others', ['helping', 'leading']),
            ('creative', 'Creating art, music, or writing', ['creative']),
            ('outdoors', 'Being outdoors or doing physical activity', ['outdoor', 'technical']),
        ],
    },
    {
        'id': 2,
        'text': 'What type of problems do you enjoy solving?',
        'options': [
            ('numbers', 'Numbers, patterns, and logic', ['analytical', 'technical']),
            ('people_problems', 'Helping people overcome challenges', ['helping', 'leading']),
            ('design', 'Design and making things look or work better', ['creative', 'technical']),
            ('systems', 'How things fit together and run smoothly', ['organizing', 'analytical']),
            ('discovery', 'Unknown questions and finding new answers', ['research', 'analytical']),
        ],
    },
    {
        'id': 3,
        'text': 'In a team, you usually:',
        'options': [
            ('lead', 'Take charge and make decisions', ['leading']),
            ('support', 'Support others and make sure everyone is okay', ['helping', 'organizing']),
            ('ideas', 'Come up with ideas and new approaches', ['creative', 'research']),
            ('analyze', 'Analyze data and present findings', ['analytical', 'research']),
            ('build', 'Focus on getting the technical work done', ['technical', 'organizing']),
        ],
    },
    {
        'id': 4,
        'text': 'Which subject in school did you enjoy most (or would you)?',
        'options': [
            ('math_science', 'Math or science', ['analytical', 'technical', 'research']),
            ('english_arts', 'English, art, or music', ['creative', 'helping']),
            ('history_social', 'History or social studies', ['research', 'leading', 'helping']),
            ('shop_pe', 'Shop class, PE, or hands-on activities', ['technical', 'outdoor', 'organizing']),
            ('business', 'Business or economics', ['leading', 'analytical', 'organizing']),
        ],
    },
    {
        'id': 5,
        'text': 'What would you rather avoid in a job?',
        'options': [
            ('no_people', 'Working mostly alone with little contact', ['helping', 'leading']),
            ('no_creativity', 'Repetitive work with no room for new ideas', ['creative', 'research']),
            ('no_structure', 'Unclear goals and disorganization', ['organizing', 'analytical']),
            ('no_impact', 'Work that doesn’t help people or society', ['helping', 'leading']),
            ('no_technical', 'Work that doesn’t use technology or tools', ['technical', 'analytical']),
        ],
    },
    {
        'id': 6,
        'text': 'Your ideal work environment is:',
        'options': [
            ('office_team', 'An office with a collaborative team', ['helping', 'leading', 'organizing']),
            ('quiet_focus', 'Quiet so you can focus deeply', ['analytical', 'research', 'technical']),
            ('flexible_creative', 'Flexible and visually inspiring', ['creative', 'leading']),
            ('field', 'Out in the field or on-site', ['outdoor', 'technical', 'helping']),
            ('lab_studio', 'Lab, studio, or workshop', ['research', 'creative', 'technical']),
        ],
    },
    {
        'id': 7,
        'text': 'What matters most to you in a career?',
        'options': [
            ('security', 'Stability and clear structure', ['organizing', 'analytical']),
            ('impact', 'Making a difference for others', ['helping', 'leading']),
            ('innovation', 'Creating something new or cutting-edge', ['creative', 'research', 'technical']),
            ('success', 'Recognition and advancement', ['leading', 'analytical']),
            ('balance', 'Work-life balance and variety', ['outdoor', 'helping', 'creative']),
        ],
    },
    {
        'id': 8,
        'text': 'When you’re stressed, you tend to:',
        'options': [
            ('organize', 'Make a list and tackle things in order', ['organizing', 'analytical']),
            ('talk', 'Talk it through with someone', ['helping', 'leading']),
            ('create', 'Do something creative or physical', ['creative', 'outdoor']),
            ('research', 'Look up information and plan', ['research', 'analytical']),
            ('fix', 'Focus on fixing the problem step by step', ['technical', 'organizing']),
        ],
    },
]

# Career suggestions per top categories (category key -> list of career titles + short description)
CAREER_SUGGESTIONS = {
    'analytical': [
        ('Data Analyst', 'Interpret data to help organizations make decisions.'),
        ('Financial Analyst', 'Analyze financial data and trends.'),
        ('Accountant', 'Manage and report financial information.'),
        ('Actuary', 'Assess risk using mathematics and statistics.'),
        ('Management Consultant', 'Advise organizations on strategy and operations.'),
    ],
    'creative': [
        ('Graphic Designer', 'Create visual content for brands and media.'),
        ('Content Writer / Copywriter', 'Write for marketing, web, or publications.'),
        ('UX Designer', 'Design user experiences for apps and websites.'),
        ('Marketing Specialist', 'Develop and run campaigns to reach audiences.'),
        ('Video Producer', 'Plan and produce video content.'),
    ],
    'helping': [
        ('Teacher / Educator', 'Teach and support student learning.'),
        ('Nurse', 'Provide patient care and support in healthcare.'),
        ('Social Worker', 'Support individuals and families through challenges.'),
        ('Counselor / Therapist', 'Help people with mental and emotional well-being.'),
        ('Human Resources Specialist', 'Support employees and workplace culture.'),
    ],
    'leading': [
        ('Project Manager', 'Lead projects and teams to deliver results.'),
        ('Sales Representative', 'Connect products and services with customers.'),
        ('Entrepreneur', 'Start and run your own business.'),
        ('Lawyer', 'Advise and represent clients in legal matters.'),
        ('Executive / Manager', 'Lead teams and make strategic decisions.'),
    ],
    'organizing': [
        ('Operations Manager', 'Keep day-to-day processes running smoothly.'),
        ('Executive Assistant', 'Support leaders and manage schedules and tasks.'),
        ('Event Planner', 'Organize and run events.'),
        ('Supply Chain / Logistics', 'Manage the flow of goods and information.'),
        ('Compliance Officer', 'Ensure rules and policies are followed.'),
    ],
    'technical': [
        ('Software Developer', 'Build applications and systems.'),
        ('IT Support / Systems Admin', 'Maintain technology and help users.'),
        ('Mechanical Engineer', 'Design and improve mechanical systems.'),
        ('Civil Engineer', 'Plan and oversee infrastructure projects.'),
        ('Cybersecurity Analyst', 'Protect systems and data from threats.'),
    ],
    'outdoor': [
        ('Environmental Scientist', 'Study and protect the environment.'),
        ('Landscape Architect', 'Design outdoor spaces.'),
        ('Agriculture / Farming', 'Grow food and manage land.'),
        ('Construction / Trades', 'Build and repair structures.'),
        ('Park Ranger / Conservation', 'Manage and protect natural areas.'),
    ],
    'research': [
        ('Research Scientist', 'Conduct experiments and studies.'),
        ('University Professor', 'Teach and do research in academia.'),
        ('Journalist / Reporter', 'Investigate and report on stories.'),
        ('Market Research Analyst', 'Study markets and consumer behavior.'),
        ('Policy Analyst', 'Research and advise on policy.'),
    ],
}


def get_questions():
    return QUESTIONS


def get_career_categories():
    return CAREER_CATEGORIES


def score_quiz(selected_options):
    """
    selected_options: list of option keys chosen (e.g. ['building', 'numbers', ...])
    Returns: list of (category_key, score) sorted by score descending.
    """
    scores = {}
    for q in QUESTIONS:
        for opt_key, _label, categories in q['options']:
            if opt_key in selected_options:
                for cat in categories:
                    scores[cat] = scores.get(cat, 0) + 1
    return sorted(scores.items(), key=lambda x: -x[1])


def get_top_careers(score_tuples, top_n=3):
    """Return career suggestions for the top N categories."""
    suggestions = []
    seen = set()
    for cat_key, _score in score_tuples[:top_n]:
        for title, desc in CAREER_SUGGESTIONS.get(cat_key, [])[:3]:
            if title not in seen:
                seen.add(title)
                suggestions.append({'title': title, 'description': desc, 'category': cat_key})
    return suggestions[:10]
