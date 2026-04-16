"""
Quiz scoring engine and behavior-based result interpretation.

All business logic lives here, not in views.

Scoring (multi-weight):
  For each answer, iterate the choice's weights dict and add
  weight_value * question.weight to each archetype's cumulative score.

Interpretation:
  Results are derived from score distribution and answer patterns —
  never from hardcoded personality paragraphs.
"""
from collections import defaultdict

from apps.careers.models import Job, Major, PersonalityType
from apps.quiz.constants import QUIZ_QUESTION_COUNT
from apps.quiz.models import Choice, Question


# ---------------------------------------------------------------------------
# Question theme mapping — used to generate behavioral observations.
# ---------------------------------------------------------------------------
QUESTION_THEMES = {
    1: {"dimension": "task approach", "context": "starting new work"},
    2: {"dimension": "collaboration style", "context": "group dynamics"},
    3: {"dimension": "flow state", "context": "peak engagement"},
    4: {"dimension": "learning preference", "context": "acquiring knowledge"},
    5: {"dimension": "self-identity", "context": "self-perception"},
    6: {"dimension": "uncertainty response", "context": "handling ambiguity"},
    7: {"dimension": "environment fit", "context": "ideal conditions"},
    8: {"dimension": "perceptual focus", "context": "noticing patterns"},
    9: {"dimension": "core motivation", "context": "internal drive"},
    10: {"dimension": "unstructured time", "context": "free-choice behavior"},
}

COGNITIVE_PROFILES = {
    "systems_thinker": {
        "label": "Systems",
        "style": "structured and process-oriented",
        "verb": "organize, optimize, and systematize",
        "preference": "clarity, order, and repeatable processes",
        "strength_phrase": "creating structure from complexity",
        "approach": "step-by-step planning and methodical execution",
    },
    "analytical_solver": {
        "label": "Analytical",
        "style": "logic-driven and precision-focused",
        "verb": "analyze, investigate, and reason through evidence",
        "preference": "depth, accuracy, and evidence-based decisions",
        "strength_phrase": "deep analysis and pattern recognition",
        "approach": "research-first thinking and careful evaluation",
    },
    "creative_builder": {
        "label": "Creative",
        "style": "idea-first and experimentally driven",
        "verb": "build, design, and iterate on ideas",
        "preference": "flexibility, hands-on work, and creative freedom",
        "strength_phrase": "turning abstract ideas into tangible output",
        "approach": "rapid prototyping and learning through making",
    },
    "people_strategist": {
        "label": "People",
        "style": "relationally aware and collaboration-driven",
        "verb": "connect, coordinate, and motivate others",
        "preference": "teamwork, communication, and human connection",
        "strength_phrase": "reading group dynamics and building consensus",
        "approach": "discussion-based decision-making and empathetic leadership",
    },
    "explorer": {
        "label": "Explorer",
        "style": "novelty-seeking and highly adaptable",
        "verb": "explore, experiment, and chart new paths",
        "preference": "variety, autonomy, and unconventional approaches",
        "strength_phrase": "adapting to change and finding unexpected opportunities",
        "approach": "flexible exploration and independent problem-solving",
    },
    "impact_visionary": {
        "label": "Visionary",
        "style": "future-oriented and meaning-driven",
        "verb": "inspire, advocate, and drive purposeful change",
        "preference": "purpose, impact, and values-aligned work",
        "strength_phrase": "connecting work to a larger mission",
        "approach": "big-picture thinking and cause-driven strategy",
    },
}

BEHAVIOR_TEMPLATES = {
    ("task approach", "systems_thinker"): "You approach new tasks by creating a plan before taking action",
    ("task approach", "analytical_solver"): "You approach new tasks by gathering information and understanding the context first",
    ("task approach", "creative_builder"): "You approach new tasks by jumping in and building something immediately",
    ("task approach", "people_strategist"): "You approach new tasks by seeking collaboration and shared direction",
    ("task approach", "explorer"): "You approach new tasks by looking for an original or unexpected angle",
    ("task approach", "impact_visionary"): "You approach new tasks by considering the broader impact of the work",

    ("collaboration style", "systems_thinker"): "In group settings, you naturally take on the role of organizer and planner",
    ("collaboration style", "analytical_solver"): "In group settings, you focus on accuracy and quality control",
    ("collaboration style", "creative_builder"): "In group settings, you gravitate toward the hands-on creative work",
    ("collaboration style", "people_strategist"): "In group settings, you focus on keeping people aligned and motivated",
    ("collaboration style", "explorer"): "In group settings, you push the group to consider unconventional approaches",
    ("collaboration style", "impact_visionary"): "In group settings, you connect the work to a larger purpose",

    ("flow state", "systems_thinker"): "You feel most engaged when things are running smoothly because of your organization",
    ("flow state", "analytical_solver"): "You feel most engaged when you're deep in a complex problem",
    ("flow state", "creative_builder"): "You feel most engaged when you're actively making or building something",
    ("flow state", "people_strategist"): "You feel most engaged when you're connecting with or helping others",
    ("flow state", "explorer"): "You feel most engaged when you're exploring something entirely new",
    ("flow state", "impact_visionary"): "You feel most engaged when working on something that could drive real change",

    ("learning preference", "systems_thinker"): "You learn best through structured, step-by-step processes",
    ("learning preference", "analytical_solver"): "You learn best by understanding the underlying logic before applying it",
    ("learning preference", "creative_builder"): "You learn best through hands-on experimentation and trial",
    ("learning preference", "people_strategist"): "You learn best through discussion, examples, and group interaction",
    ("learning preference", "explorer"): "You learn best by finding your own path and experimenting independently",
    ("learning preference", "impact_visionary"): "You learn best when the material connects to real-world purpose",

    ("self-identity", "systems_thinker"): "You see yourself as someone who values organization and efficiency",
    ("self-identity", "analytical_solver"): "You see yourself as someone who likes understanding how things work beneath the surface",
    ("self-identity", "creative_builder"): "You see yourself as someone who would rather create than follow rules",
    ("self-identity", "people_strategist"): "You see yourself as someone others come to for support and advice",
    ("self-identity", "explorer"): "You see yourself as someone who needs variety and resists repetition",
    ("self-identity", "impact_visionary"): "You see yourself as someone driven by fairness and making things better",

    ("uncertainty response", "systems_thinker"): "When uncertain, your instinct is to create structure and organize your thoughts",
    ("uncertainty response", "analytical_solver"): "When uncertain, you turn to research and information gathering",
    ("uncertainty response", "creative_builder"): "When uncertain, you try different approaches to see what works",
    ("uncertainty response", "people_strategist"): "When uncertain, you seek input from people you trust",
    ("uncertainty response", "explorer"): "When uncertain, you step back and reframe the problem from a new angle",
    ("uncertainty response", "impact_visionary"): "When uncertain, you evaluate whether the issue aligns with what matters most",

    ("environment fit", "systems_thinker"): "You thrive in structured environments with clear expectations",
    ("environment fit", "analytical_solver"): "You thrive in quiet, focused environments with room for deep thinking",
    ("environment fit", "creative_builder"): "You thrive in flexible environments where you can experiment freely",
    ("environment fit", "people_strategist"): "You thrive in collaborative environments built around teamwork",
    ("environment fit", "explorer"): "You thrive in fast-moving environments where no two days look the same",
    ("environment fit", "impact_visionary"): "You thrive in purpose-driven environments where the work feels meaningful",

    ("perceptual focus", "systems_thinker"): "You naturally notice inefficiencies and things that could be better organized",
    ("perceptual focus", "analytical_solver"): "You naturally notice inconsistencies and things that don't add up",
    ("perceptual focus", "creative_builder"): "You naturally notice design, aesthetics, and visual details",
    ("perceptual focus", "people_strategist"): "You naturally notice social dynamics and how people are feeling",
    ("perceptual focus", "explorer"): "You naturally notice anything new or unexpected in your surroundings",
    ("perceptual focus", "impact_visionary"): "You naturally notice whether environments feel inclusive and fair",

    ("core motivation", "systems_thinker"): "You're driven by mastery and making things run well",
    ("core motivation", "analytical_solver"): "You're driven by solving complex problems that stretch your thinking",
    ("core motivation", "creative_builder"): "You're driven by bringing new ideas to life",
    ("core motivation", "people_strategist"): "You're driven by helping people and building meaningful relationships",
    ("core motivation", "explorer"): "You're driven by discovery and keeping life interesting",
    ("core motivation", "impact_visionary"): "You're driven by making a tangible difference in your community",

    ("unstructured time", "systems_thinker"): "Given free time, you gravitate toward organizing, planning, or optimizing",
    ("unstructured time", "analytical_solver"): "Given free time, you gravitate toward deep research and learning",
    ("unstructured time", "creative_builder"): "Given free time, you gravitate toward personal projects and creative work",
    ("unstructured time", "people_strategist"): "Given free time, you gravitate toward spending time with people",
    ("unstructured time", "explorer"): "Given free time, you gravitate toward new experiences and exploration",
    ("unstructured time", "impact_visionary"): "Given free time, you gravitate toward causes and purposeful activities",
}

RECOMMENDATION_REASONS = {
    "systems_thinker": "your consistent preference for structured, process-oriented approaches",
    "analytical_solver": "your pattern of choosing logic-driven, research-first methods",
    "creative_builder": "your repeated preference for hands-on building and design-oriented work",
    "people_strategist": "your strong pull toward collaboration, communication, and people-centered approaches",
    "explorer": "your consistent choice of flexible, novelty-seeking, and independent paths",
    "impact_visionary": "your orientation toward purpose, impact, and values-driven decisions",
}


def canonical_questions():
    """Return the fixed 10-question deck, ordered by `order`."""
    return list(
        Question.objects.order_by("order")
        .prefetch_related("choices")[:QUIZ_QUESTION_COUNT]
    )


def _dominant_archetype(weights):
    """Return the archetype key with the highest weight in a choice."""
    if not weights:
        return None
    return max(weights, key=weights.get)


def calculate_quiz_result(ordered_choice_keys):
    """
    Multi-weight scoring: for each answer, add
    choice.weights[arch] * question.weight for every archetype.
    """
    if len(ordered_choice_keys) != QUIZ_QUESTION_COUNT:
        return None

    questions = canonical_questions()
    if len(questions) != QUIZ_QUESTION_COUNT:
        return None

    scores = defaultdict(float)
    answer_history = []

    for i, key in enumerate(ordered_choice_keys):
        choice = (
            Choice.objects
            .filter(question=questions[i], key=key)
            .first()
        )
        if not choice:
            return None

        weights = choice.weights or {}
        if not weights:
            return None

        q_weight = questions[i].weight
        for arch_key, arch_weight in weights.items():
            if arch_weight:
                scores[arch_key] += arch_weight * q_weight

        answer_history.append({
            "question_order": questions[i].order,
            "archetype_chosen": _dominant_archetype(weights),
            "weight": q_weight,
        })

    ranked = sorted(scores.items(), key=lambda x: -x[1])

    primary = _lookup_type(ranked[0][0]) if ranked else None
    secondary = _lookup_type(ranked[1][0]) if len(ranked) > 1 else None

    return {
        "primary_type": primary,
        "secondary_type": secondary,
        "scores": dict(scores),
        "ranked": ranked,
        "answer_history": answer_history,
    }


def _lookup_type(key):
    return PersonalityType.objects.filter(key=key).first()


# ---------------------------------------------------------------------------
# Result interpretation engine (unchanged structure, same 4-layer output)
# ---------------------------------------------------------------------------

def _build_identity_summary(primary, secondary, scores, total_possible):
    p_key = primary.key
    s_key = secondary.key if secondary else None
    p_profile = COGNITIVE_PROFILES.get(p_key, {})
    s_profile = COGNITIVE_PROFILES.get(s_key, {}) if s_key else {}

    p_label = p_profile.get("label", primary.name)
    s_label = s_profile.get("label", secondary.name if secondary else "")

    p_score = scores.get(p_key, 0)
    s_score = scores.get(s_key, 0) if s_key else 0

    if s_key and s_score > 0:
        gap = p_score - s_score
        if gap <= 1.5:
            blend = (
                f"You are a {p_label}-{s_label} blend \u2014 "
                f"equally drawn to {p_profile.get('preference', '')} "
                f"and {s_profile.get('preference', '')}."
            )
        else:
            blend = (
                f"You are primarily a {p_label} thinker with strong "
                f"{s_label} tendencies, meaning you naturally "
                f"{p_profile.get('verb', 'think')} while also valuing "
                f"{s_profile.get('preference', '')}."
            )
    else:
        blend = (
            f"You are a clear {p_label} thinker who consistently "
            f"gravitates toward {p_profile.get('preference', '')}."
        )

    return blend


def _build_behavior_breakdown(answer_history, scores, ranked):
    observations = []
    archetype_counts = defaultdict(int)
    for ans in answer_history:
        if ans["archetype_chosen"]:
            archetype_counts[ans["archetype_chosen"]] += 1

    primary_key = ranked[0][0] if ranked else None
    secondary_key = ranked[1][0] if len(ranked) > 1 else None

    high_weight_answers = sorted(
        answer_history, key=lambda a: -a["weight"]
    )

    seen_dimensions = set()
    for ans in high_weight_answers:
        theme = QUESTION_THEMES.get(ans["question_order"])
        if not theme:
            continue
        dim = theme["dimension"]
        if dim in seen_dimensions:
            continue

        arch = ans["archetype_chosen"]
        template = BEHAVIOR_TEMPLATES.get((dim, arch))
        if not template:
            continue

        if arch == primary_key or arch == secondary_key:
            seen_dimensions.add(dim)
            observations.append(template)

        if len(observations) >= 5:
            break

    if primary_key and archetype_counts.get(primary_key, 0) >= 4:
        p_profile = COGNITIVE_PROFILES.get(primary_key, {})
        consistency_note = (
            f"Across multiple question types, you consistently chose "
            f"{p_profile.get('style', 'similar')} approaches \u2014 "
            f"this was not a single-area pattern but a broad cognitive tendency"
        )
        if consistency_note not in observations:
            observations.append(consistency_note)

    if len(ranked) >= 3 and ranked[0][1] - ranked[2][1] <= 2.0:
        observations.append(
            "Your scores were relatively balanced across several thinking "
            "styles, suggesting cognitive flexibility rather than a single "
            "dominant mode"
        )

    return observations[:6]


def _build_thinking_profile(primary, secondary, scores, ranked):
    p_key = primary.key
    p_profile = COGNITIVE_PROFILES.get(p_key, {})

    parts = [
        f"Your thinking style is {p_profile.get('style', 'distinctive')}. "
        f"You tend to {p_profile.get('verb', 'approach problems')} as your "
        f"default mode of operating.",
    ]

    parts.append(
        f"Your natural strength is {p_profile.get('strength_phrase', 'problem-solving')}, "
        f"and you are most effective when your environment supports "
        f"{p_profile.get('preference', 'your preferred approach')}."
    )

    if secondary:
        s_key = secondary.key
        s_profile = COGNITIVE_PROFILES.get(s_key, {})
        s_score = scores.get(s_key, 0)
        p_score = scores.get(p_key, 0)

        if p_score > 0 and s_score / p_score >= 0.6:
            parts.append(
                f"Your secondary {s_profile.get('label', '')} orientation "
                f"means you also draw on {s_profile.get('approach', 'alternative methods')} "
                f"\u2014 this combination makes you particularly effective at "
                f"bridging {p_profile.get('label', 'one')} and "
                f"{s_profile.get('label', 'another')} perspectives."
            )
        else:
            parts.append(
                f"While your {s_profile.get('label', 'secondary')} side "
                f"is present, it plays a supporting role \u2014 surfacing mainly "
                f"when your primary approach encounters its limits."
            )

    lowest = ranked[-1] if ranked else None
    if lowest:
        low_profile = COGNITIVE_PROFILES.get(lowest[0], {})
        parts.append(
            f"You are least drawn to {low_profile.get('style', 'certain')} "
            f"approaches, which may feel unnatural but can be a useful "
            f"complement when developed intentionally."
        )

    return " ".join(parts)


def _build_pathway_majors(primary, secondary):
    primary_reason = RECOMMENDATION_REASONS.get(
        primary.key, "your assessment results"
    )

    majors = list(
        Major.objects.filter(personality_types=primary).distinct()[:4]
    )

    if secondary and len(majors) < 4:
        secondary_majors = (
            Major.objects.filter(personality_types=secondary)
            .exclude(pk__in=[m.pk for m in majors])
            .distinct()[:2]
        )
        majors.extend(secondary_majors)

    secondary_reason = RECOMMENDATION_REASONS.get(
        secondary.key if secondary else "", ""
    )

    result = []
    primary_pks = set(
        Major.objects.filter(personality_types=primary)
        .values_list("pk", flat=True)
    )
    for m in majors:
        if m.pk in primary_pks:
            reason = f"Aligns with {primary_reason}."
        else:
            reason = f"Complements your secondary tendency toward {secondary_reason}." if secondary_reason else ""
        result.append({
            "name": m.name,
            "description": m.description,
            "reason": reason,
        })

    return result


def _build_pathway_careers(primary, secondary):
    primary_reason = RECOMMENDATION_REASONS.get(
        primary.key, "your assessment results"
    )

    careers = list(
        Job.objects.filter(primary_archetype=primary)
        .select_related("primary_archetype")[:4]
    )

    if secondary and len(careers) < 6:
        secondary_careers = (
            Job.objects.filter(primary_archetype=secondary)
            .exclude(pk__in=[c.pk for c in careers])
            .select_related("primary_archetype")[:2]
        )
        careers.extend(secondary_careers)

    secondary_reason = RECOMMENDATION_REASONS.get(
        secondary.key if secondary else "", ""
    )

    result = []
    for c in careers:
        if c.primary_archetype and c.primary_archetype.key == primary.key:
            reason = f"Directly matches {primary_reason}."
        else:
            reason = f"Draws on your secondary tendency toward {secondary_reason}." if secondary_reason else ""
        result.append({
            "title": c.title,
            "description": c.description,
            "learn_more": c.learn_more,
            "reason": reason,
        })

    return result


def build_results_payload(result_dict):
    """
    Build the complete 4-layer results response from scoring output.
    """
    primary = result_dict["primary_type"]
    secondary = result_dict["secondary_type"]
    scores = result_dict["scores"]
    ranked = result_dict["ranked"]
    answer_history = result_dict.get("answer_history", [])

    total_possible = QUIZ_QUESTION_COUNT * 2.0

    primary_data = _serialize_archetype(primary) if primary else None
    secondary_data = _serialize_archetype(secondary) if secondary else None

    scores_list = [
        {"archetype": key, "score": round(score, 1)}
        for key, score in ranked
    ]

    identity_summary = ""
    behavior_breakdown = []
    thinking_profile = ""
    majors_data = []
    careers_data = []

    if primary:
        identity_summary = _build_identity_summary(
            primary, secondary, scores, total_possible
        )
        behavior_breakdown = _build_behavior_breakdown(
            answer_history, scores, ranked
        )
        thinking_profile = _build_thinking_profile(
            primary, secondary, scores, ranked
        )
        majors_data = _build_pathway_majors(primary, secondary)
        careers_data = _build_pathway_careers(primary, secondary)

    return {
        "personality": {
            "primary": primary_data,
            "secondary": secondary_data,
        },
        "scores": scores_list,
        "identity_summary": identity_summary,
        "behavior_breakdown": behavior_breakdown,
        "thinking_profile": thinking_profile,
        "suggested_majors": majors_data,
        "careers": careers_data,
    }


def _serialize_archetype(pt):
    if not pt:
        return None
    return {
        "key": pt.key,
        "name": pt.name,
        "description": pt.description,
        "icon": pt.icon,
        "traits": pt.traits,
    }
