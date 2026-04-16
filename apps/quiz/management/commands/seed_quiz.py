"""
Seed exactly 10 weighted quiz questions with 4 multi-weight choices each.

Each choice distributes scoring weight across all 6 archetypes, producing
nuanced blended results rather than single-archetype buckets.

Run: python manage.py seed_quiz
Prerequisite: python manage.py seed_careers
"""
from django.core.management.base import BaseCommand

from apps.careers.models import PersonalityType
from apps.quiz.constants import QUIZ_QUESTION_COUNT
from apps.quiz.models import Choice, Question

# Keys: sy=systems, an=analytical, cr=creative, pe=people, ex=explorer, vi=visionary
W = {
    "sy": "systems_thinker",
    "an": "analytical_solver",
    "cr": "creative_builder",
    "pe": "people_strategist",
    "ex": "explorer",
    "vi": "impact_visionary",
}


def _w(sy=0, an=0, cr=0, pe=0, ex=0, vi=0):
    return {
        W["sy"]: sy, W["an"]: an, W["cr"]: cr,
        W["pe"]: pe, W["ex"]: ex, W["vi"]: vi,
    }


QUESTIONS = [
    # ── Q1  Task approach  (1.5) ──────────────────────────────────────────
    {
        "order": 1,
        "weight": 1.5,
        "text": "You just got a big assignment. What\u2019s your first move?",
        "choices": [
            ("A", "Break it into steps and make a plan",
             _w(sy=1.0, an=0.3)),
            ("B", "Research the topic before doing anything",
             _w(an=1.0, sy=0.2, vi=0.1)),
            ("C", "Start sketching ideas or building a rough draft",
             _w(cr=1.0, ex=0.3)),
            ("D", "Find someone to work on it with",
             _w(pe=1.0, vi=0.2)),
        ],
    },
    # ── Q2  Collaboration style  (1.0) ────────────────────────────────────
    {
        "order": 2,
        "weight": 1.0,
        "text": "In a group project, you usually end up\u2026",
        "choices": [
            ("A", "Keeping the group organized and on schedule",
             _w(sy=1.0, pe=0.2)),
            ("B", "Checking facts and catching mistakes",
             _w(an=1.0, sy=0.2)),
            ("C", "Designing the presentation or building the final product",
             _w(cr=1.0, ex=0.2)),
            ("D", "Making sure everyone feels included and motivated",
             _w(pe=1.0, vi=0.3)),
        ],
    },
    # ── Q3  Flow state  (2.0) ─────────────────────────────────────────────
    {
        "order": 3,
        "weight": 2.0,
        "text": "When do you feel most \u201cin the zone\u201d?",
        "choices": [
            ("A", "When everything is running smoothly because you set it up",
             _w(sy=1.0, an=0.2)),
            ("B", "When you\u2019re deep in a problem that really makes you think",
             _w(an=1.0, ex=0.2)),
            ("C", "When you\u2019re building or creating something new",
             _w(cr=1.0, ex=0.3, vi=0.1)),
            ("D", "When you\u2019re connecting with people or helping someone out",
             _w(pe=0.8, vi=0.5)),
        ],
    },
    # ── Q4  Learning preference  (1.5) ────────────────────────────────────
    {
        "order": 4,
        "weight": 1.5,
        "text": "How do you learn something new best?",
        "choices": [
            ("A", "Follow a clear, step-by-step guide",
             _w(sy=1.0, an=0.2)),
            ("B", "Understand why it works before trying it",
             _w(an=1.0, vi=0.1)),
            ("C", "Jump in and figure it out hands-on",
             _w(cr=0.8, ex=0.5)),
            ("D", "Talk it through with someone or learn in a group",
             _w(pe=1.0, ex=0.1, vi=0.2)),
        ],
    },
    # ── Q5  Self-identity  (1.5) ──────────────────────────────────────────
    {
        "order": 5,
        "weight": 1.5,
        "text": "Which of these sounds most like you?",
        "choices": [
            ("A", "You like things to be organized and running well",
             _w(sy=1.0, an=0.2)),
            ("B", "You\u2019d rather create something than follow a rulebook",
             _w(cr=1.0, ex=0.4)),
            ("C", "You get restless doing the same thing for too long",
             _w(ex=1.0, cr=0.3)),
            ("D", "You care a lot about fairness and making things better",
             _w(vi=1.0, pe=0.4)),
        ],
    },
    # ── Q6  Uncertainty response  (1.0) ───────────────────────────────────
    {
        "order": 6,
        "weight": 1.0,
        "text": "When you\u2019re confused about something, you usually\u2026",
        "choices": [
            ("A", "Make a list or outline to sort it out",
             _w(sy=1.0, an=0.3)),
            ("B", "Look it up and research on your own",
             _w(an=1.0, ex=0.1)),
            ("C", "Try different things until something clicks",
             _w(cr=0.6, ex=0.7)),
            ("D", "Ask someone you trust for their take",
             _w(pe=1.0, vi=0.1)),
        ],
    },
    # ── Q7  Environment fit  (2.0) ────────────────────────────────────────
    {
        "order": 7,
        "weight": 2.0,
        "text": "What kind of environment do you do your best work in?",
        "choices": [
            ("A", "Structured and predictable, with clear expectations",
             _w(sy=1.0, an=0.3)),
            ("B", "Flexible and creative, where you can experiment",
             _w(cr=0.8, ex=0.5)),
            ("C", "Collaborative, where you\u2019re around people you can work with",
             _w(pe=1.0, vi=0.2)),
            ("D", "Fast-moving and varied, where you\u2019re always learning",
             _w(ex=1.0, an=0.2, cr=0.1)),
        ],
    },
    # ── Q8  Perceptual focus  (1.5) ───────────────────────────────────────
    {
        "order": 8,
        "weight": 1.5,
        "text": "When you walk into a room, what do you notice first?",
        "choices": [
            ("A", "What could be organized or set up better",
             _w(sy=1.0, an=0.2)),
            ("B", "The design, colors, or how the space looks",
             _w(cr=1.0, ex=0.1)),
            ("C", "The people \u2014 who\u2019s talking, who looks left out",
             _w(pe=0.8, vi=0.5)),
            ("D", "Something new or unexpected that catches my eye",
             _w(ex=1.0, cr=0.2)),
        ],
    },
    # ── Q9  Core motivation  (1.0) ────────────────────────────────────────
    {
        "order": 9,
        "weight": 1.0,
        "text": "What drives you the most?",
        "choices": [
            ("A", "Getting really good at making things run well",
             _w(sy=0.8, an=0.4)),
            ("B", "Bringing new ideas to life",
             _w(cr=1.0, ex=0.3)),
            ("C", "Helping people and building strong relationships",
             _w(pe=1.0, vi=0.3)),
            ("D", "Making a real difference in my community or the world",
             _w(vi=1.0, pe=0.3, ex=0.1)),
        ],
    },
    # ── Q10  Free time  (2.0) ─────────────────────────────────────────────
    {
        "order": 10,
        "weight": 2.0,
        "text": "If you had a completely free day, you\u2019d most likely\u2026",
        "choices": [
            ("A", "Plan the week ahead or reorganize your space",
             _w(sy=1.0, an=0.1)),
            ("B", "Work on a creative project or personal hobby",
             _w(cr=1.0, ex=0.2)),
            ("C", "Hang out with friends, family, or your community",
             _w(pe=0.9, vi=0.3)),
            ("D", "Explore somewhere new or try something you\u2019ve never done",
             _w(ex=1.0, cr=0.2, vi=0.1)),
        ],
    },
]


class Command(BaseCommand):
    help = f"Seed exactly {QUIZ_QUESTION_COUNT} multi-weight quiz questions (4 choices each)."

    def handle(self, *args, **options):
        if PersonalityType.objects.count() == 0:
            self.stderr.write(
                self.style.ERROR(
                    "No personality types found. Run seed_careers first."
                )
            )
            return

        Question.objects.all().delete()
        self.stdout.write("  Cleared existing questions.")

        for q_data in QUESTIONS[:QUIZ_QUESTION_COUNT]:
            question = Question.objects.create(
                text=q_data["text"],
                order=q_data["order"],
                weight=q_data["weight"],
            )
            for label, text, weights in q_data["choices"]:
                key = f"q{q_data['order']}{label.lower()}"
                Choice.objects.create(
                    question=question,
                    key=key,
                    label=label,
                    text=text,
                    weights=weights,
                )

        count = Question.objects.count()
        choice_count = Choice.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {count} questions with {choice_count} choices "
                f"({choice_count // count} per question)."
            )
        )
        if count != QUIZ_QUESTION_COUNT:
            self.stderr.write(
                self.style.WARNING(
                    f"Expected {QUIZ_QUESTION_COUNT}, got {count}. Check data."
                )
            )
