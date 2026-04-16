"""
Seed the 6 personality archetypes, majors, and career mappings.
Run: python manage.py seed_careers
"""
from django.core.management.base import BaseCommand

from apps.careers.models import Job, Major, PersonalityType

ARCHETYPES = [
    {
        "key": "systems_thinker",
        "name": "Structured Systems Thinker",
        "icon": "\u2699\ufe0f",
        "traits": [
            "methodical",
            "detail-oriented",
            "process-driven",
            "reliability-focused",
        ],
        "description": (
            "You naturally break down complex systems into structured parts. "
            "You perform best in environments where clarity, optimization, "
            "and repeatable processes matter."
        ),
        "identity_statement": (
            "You are a Structured Systems Thinker \u2014 someone who sees the world "
            "as interconnected systems and instinctively organizes them for "
            "maximum efficiency."
        ),
        "behavioral_explanation": (
            "Your thinking style is linear and hierarchical. You naturally "
            "identify bottlenecks, create frameworks, and prefer working "
            "within well-defined parameters. When faced with ambiguity, "
            "your first instinct is to impose structure."
        ),
        "why_this_fits": (
            "Your quiz responses consistently favored structured approaches "
            "to problem-solving, organized environments, and optimization-focused "
            "activities. This pattern indicates a strong preference for systems "
            "thinking over improvisation."
        ),
        "strengths": (
            "Exceptional at creating order from chaos, designing efficient "
            "workflows, and maintaining high standards of quality and consistency."
        ),
        "growth_areas": (
            "May find highly unstructured or rapidly-changing environments "
            "challenging. Could benefit from practicing comfort with ambiguity "
            "and open-ended exploration."
        ),
        "career_direction": (
            "You thrive in roles that reward precision, optimization, and "
            "systematic thinking \u2014 such as engineering, operations, IT "
            "infrastructure, or project management."
        ),
    },
    {
        "key": "analytical_solver",
        "name": "Analytical Problem Solver",
        "icon": "\U0001f9e0",
        "traits": [
            "data-driven",
            "logical",
            "research-oriented",
            "pattern-recognition",
        ],
        "description": (
            "You approach problems with deep analysis and logical reasoning. "
            "You\u2019re drawn to understanding root causes and using evidence "
            "to guide decisions."
        ),
        "identity_statement": (
            "You are an Analytical Problem Solver \u2014 someone who is happiest "
            "when dissecting complex problems and finding evidence-based solutions."
        ),
        "behavioral_explanation": (
            "Your thinking style is investigative and methodical. You naturally "
            "look for patterns in data, question assumptions, and prefer decisions "
            "grounded in evidence rather than intuition. You enjoy the process "
            "of deep research."
        ),
        "why_this_fits": (
            "Your responses favored logic and data reasoning, deep understanding "
            "of concepts, quiet focused environments, and research-oriented "
            "activities. This pattern reflects a strong analytical orientation."
        ),
        "strengths": (
            "Excellent at research, critical thinking, spotting patterns, "
            "and making sound decisions based on evidence and data."
        ),
        "growth_areas": (
            "May over-analyze decisions or prefer perfection over progress. "
            "Could benefit from practicing faster decision-making and comfort "
            "with incomplete information."
        ),
        "career_direction": (
            "You excel in roles requiring deep analysis and research \u2014 "
            "data science, research, economics, finance, or academic work."
        ),
    },
    {
        "key": "creative_builder",
        "name": "Creative Builder",
        "icon": "\U0001f3a8",
        "traits": [
            "hands-on",
            "innovative",
            "design-oriented",
            "prototyping",
        ],
        "description": (
            "You learn by building and creating. You\u2019re happiest when "
            "you can take an idea and turn it into something tangible, "
            "whether digital or physical."
        ),
        "identity_statement": (
            "You are a Creative Builder \u2014 someone who thinks through making "
            "and whose best ideas emerge from hands-on experimentation."
        ),
        "behavioral_explanation": (
            "Your thinking style is divergent and experimental. You naturally "
            "gravitate toward building prototypes, testing ideas, and refining "
            "through iteration. You\u2019re more energized by creating than "
            "by planning."
        ),
        "why_this_fits": (
            "Your responses consistently favored building and testing, "
            "hands-on learning, flexible environments, and design-oriented "
            "activities. This reflects a strong creative-builder orientation."
        ),
        "strengths": (
            "Excellent at rapid prototyping, creative problem-solving, "
            "visual thinking, and turning abstract ideas into concrete output."
        ),
        "growth_areas": (
            "May struggle with extended planning phases or highly rigid "
            "processes. Could benefit from developing patience for structured "
            "requirements gathering before building."
        ),
        "career_direction": (
            "You thrive in roles where you can build and design \u2014 "
            "UX/UI design, frontend engineering, product design, architecture, "
            "or creative technology roles."
        ),
    },
    {
        "key": "people_strategist",
        "name": "People-Oriented Strategist",
        "icon": "\U0001f91d",
        "traits": [
            "empathetic",
            "collaborative",
            "communicative",
            "leadership-oriented",
        ],
        "description": (
            "You naturally read group dynamics, coordinate people, and "
            "communicate effectively. You\u2019re drawn to roles where "
            "human connection drives outcomes."
        ),
        "identity_statement": (
            "You are a People-Oriented Strategist \u2014 someone who leads "
            "through connection, coordination, and understanding what "
            "motivates others."
        ),
        "behavioral_explanation": (
            "Your thinking style is relational and collaborative. You "
            "naturally consider how decisions affect people, seek input "
            "from others, and prefer environments where teamwork and "
            "communication are central."
        ),
        "why_this_fits": (
            "Your responses consistently favored discussion-based approaches, "
            "collaborative environments, helping and influencing others, "
            "and people-centered activities."
        ),
        "strengths": (
            "Excellent at communication, team leadership, conflict resolution, "
            "mentoring, and building consensus across stakeholders."
        ),
        "growth_areas": (
            "May over-prioritize harmony at the expense of efficiency. "
            "Could benefit from developing comfort with data-driven "
            "decision-making independent of group input."
        ),
        "career_direction": (
            "You excel in roles centered on people \u2014 management, "
            "human resources, marketing, counseling, education, or "
            "product management."
        ),
    },
    {
        "key": "explorer",
        "name": "Explorer / Adaptive Thinker",
        "icon": "\U0001f9ed",
        "traits": [
            "curious",
            "adaptable",
            "entrepreneurial",
            "variety-seeking",
        ],
        "description": (
            "You thrive in new and changing environments. You\u2019re energized "
            "by variety, exploration, and figuring things out as you go."
        ),
        "identity_statement": (
            "You are an Explorer \u2014 someone who is energized by novelty, "
            "adapts quickly, and prefers charting your own course."
        ),
        "behavioral_explanation": (
            "Your thinking style is adaptive and opportunity-driven. You "
            "naturally scan for new possibilities, are comfortable with "
            "uncertainty, and prefer autonomy over rigid structure."
        ),
        "why_this_fits": (
            "Your responses favored experimentation, asking others for "
            "diverse perspectives, flexible approaches, and social or "
            "collaborative activities over solitary focused work."
        ),
        "strengths": (
            "Excellent at adapting to change, finding opportunities, "
            "connecting disparate ideas, and thriving in ambiguity."
        ),
        "growth_areas": (
            "May have difficulty with long-term focus on a single path "
            "or highly routine work. Could benefit from building structured "
            "follow-through habits."
        ),
        "career_direction": (
            "You thrive in roles with variety and autonomy \u2014 "
            "entrepreneurship, consulting, communications, sales, "
            "or startup environments."
        ),
    },
    {
        "key": "impact_visionary",
        "name": "Impact-Driven Visionary",
        "icon": "\U0001f31f",
        "traits": [
            "purpose-driven",
            "big-picture",
            "socially-motivated",
            "leadership-focused",
        ],
        "description": (
            "You\u2019re motivated by making a meaningful difference. "
            "You think in terms of impact, systems change, and the "
            "bigger picture."
        ),
        "identity_statement": (
            "You are an Impact-Driven Visionary \u2014 someone who measures "
            "success by the difference you make and the change you drive."
        ),
        "behavioral_explanation": (
            "Your thinking style is purpose-oriented and strategic. You "
            "naturally think about the \u201cwhy\u201d behind decisions, are drawn "
            "to causes larger than yourself, and prefer work that aligns "
            "with your values."
        ),
        "why_this_fits": (
            "Your responses favored helping and influencing others, "
            "impact-driven motivation, collaborative environments, "
            "and activities focused on societal or organizational change."
        ),
        "strengths": (
            "Excellent at inspiring others, thinking strategically about "
            "long-term impact, and connecting work to meaningful purpose."
        ),
        "growth_areas": (
            "May struggle with purely technical or process-driven work "
            "that lacks a visible human impact. Could benefit from "
            "building patience for incremental progress."
        ),
        "career_direction": (
            "You excel in roles with purpose and influence \u2014 "
            "public policy, nonprofit leadership, social work, "
            "education administration, or mission-driven organizations."
        ),
    },
]

MAJORS = [
    ("computer_science", "Computer Science", "Software engineering, systems design, and computation."),
    ("information_systems", "Information Systems", "Technology management, databases, and enterprise systems."),
    ("engineering", "Engineering", "Mechanical, civil, electrical, and industrial engineering."),
    ("data_science", "Data Science", "Statistics, machine learning, and data-driven decision making."),
    ("mathematics", "Mathematics", "Pure and applied math, modeling, and quantitative analysis."),
    ("economics", "Economics", "Market analysis, policy, and quantitative reasoning."),
    ("design", "Design", "UX/UI design, graphic design, and visual communication."),
    ("cs_frontend", "Computer Science (Frontend)", "Web development, interactive systems, and UI engineering."),
    ("architecture", "Architecture", "Building design, spatial planning, and structural aesthetics."),
    ("business", "Business Administration", "Management, strategy, operations, and organizational leadership."),
    ("marketing", "Marketing", "Brand strategy, consumer behavior, and communications."),
    ("psychology", "Psychology", "Human behavior, cognition, and interpersonal dynamics."),
    ("entrepreneurship", "Entrepreneurship", "Venture creation, innovation, and business development."),
    ("communications", "Communications", "Media, public relations, and organizational communication."),
    ("political_science", "Political Science", "Government, policy analysis, and civic systems."),
    ("sociology", "Sociology", "Social structures, inequality, and community dynamics."),
    ("public_policy", "Public Policy", "Policy design, implementation, and evaluation."),
    ("education", "Education", "Teaching, curriculum design, and educational leadership."),
]

MAJOR_ARCHETYPE_MAP = {
    "systems_thinker": ["computer_science", "information_systems", "engineering"],
    "analytical_solver": ["data_science", "mathematics", "economics"],
    "creative_builder": ["design", "cs_frontend", "architecture"],
    "people_strategist": ["business", "marketing", "psychology"],
    "explorer": ["entrepreneurship", "communications", "business"],
    "impact_visionary": ["political_science", "sociology", "public_policy", "education"],
}

CAREERS = [
    ("Software Engineer", "Design, build, and maintain software systems and applications.", "systems_thinker", ["computer_science", "engineering"]),
    ("Systems Analyst", "Evaluate and improve organizational IT systems and workflows.", "systems_thinker", ["information_systems", "computer_science"]),
    ("DevOps Engineer", "Automate infrastructure, deployments, and system reliability.", "systems_thinker", ["computer_science", "engineering"]),
    ("Project Manager", "Plan, coordinate, and deliver complex technical projects.", "systems_thinker", ["business", "engineering"]),
    ("Operations Manager", "Optimize organizational processes and team performance.", "systems_thinker", ["business", "engineering"]),
    ("Data Analyst", "Interpret data to uncover trends and inform business decisions.", "analytical_solver", ["data_science", "economics"]),
    ("Research Scientist", "Design experiments and advance knowledge in a specialized field.", "analytical_solver", ["data_science", "mathematics"]),
    ("Economist", "Analyze markets, policy impacts, and economic systems.", "analytical_solver", ["economics", "mathematics"]),
    ("Financial Analyst", "Evaluate investments, budgets, and financial performance.", "analytical_solver", ["economics", "business"]),
    ("Actuary", "Assess risk using mathematical and statistical models.", "analytical_solver", ["mathematics", "economics"]),
    ("UX/UI Designer", "Design intuitive, user-centered digital experiences.", "creative_builder", ["design", "cs_frontend"]),
    ("Product Designer", "Shape product vision through prototyping and user research.", "creative_builder", ["design", "cs_frontend"]),
    ("Frontend Engineer", "Build interactive, performant web and mobile interfaces.", "creative_builder", ["cs_frontend", "computer_science"]),
    ("Architect", "Design buildings and spaces that balance form, function, and safety.", "creative_builder", ["architecture", "engineering"]),
    ("Creative Technologist", "Blend technology and design to build novel experiences.", "creative_builder", ["design", "computer_science"]),
    ("Product Manager", "Define product strategy and coordinate cross-functional teams.", "people_strategist", ["business", "psychology"]),
    ("Marketing Manager", "Lead brand strategy, campaigns, and market positioning.", "people_strategist", ["marketing", "communications"]),
    ("HR Business Partner", "Align people strategy with organizational goals.", "people_strategist", ["psychology", "business"]),
    ("Counselor / Therapist", "Support individuals in navigating personal and career challenges.", "people_strategist", ["psychology", "education"]),
    ("Management Consultant", "Advise organizations on strategy, operations, and change.", "people_strategist", ["business", "economics"]),
    ("Startup Founder", "Launch and grow new ventures from concept to market.", "explorer", ["entrepreneurship", "business"]),
    ("Sales Strategist", "Develop and execute strategies to drive revenue growth.", "explorer", ["business", "communications"]),
    ("Business Development Manager", "Identify partnerships and growth opportunities.", "explorer", ["business", "entrepreneurship"]),
    ("Communications Specialist", "Craft messaging and manage organizational narratives.", "explorer", ["communications", "marketing"]),
    ("Innovation Consultant", "Help organizations adopt new methods and technologies.", "explorer", ["entrepreneurship", "business"]),
    ("Policy Analyst", "Research and advise on legislation and public programs.", "impact_visionary", ["public_policy", "political_science"]),
    ("Nonprofit Director", "Lead mission-driven organizations and manage programs.", "impact_visionary", ["public_policy", "sociology"]),
    ("Social Worker", "Support individuals and communities through systemic challenges.", "impact_visionary", ["sociology", "psychology"]),
    ("Education Administrator", "Lead schools or educational programs and drive outcomes.", "impact_visionary", ["education", "public_policy"]),
    ("Community Organizer", "Mobilize people and resources for civic and social change.", "impact_visionary", ["sociology", "political_science"]),
]

CAREER_LEARN_MORE = {
    "Software Engineer": "Software engineers design, build, and maintain software systems. You might work across the stack on web, mobile, or infrastructure. Strong problem-solving and collaboration are key.",
    "Systems Analyst": "Systems analysts evaluate IT systems and recommend improvements. You work between business teams and technical staff to optimize workflows and technology use.",
    "DevOps Engineer": "DevOps engineers automate deployment pipelines, manage cloud infrastructure, and ensure system reliability. Strong scripting and systems knowledge are essential.",
    "Project Manager": "Project managers plan, track, and deliver projects on time and within budget. PMP certification is common. Used across tech, construction, and consulting.",
    "Operations Manager": "Operations managers oversee daily processes, supply chain, and team coordination. The role focuses on efficiency, quality, and continuous improvement.",
    "Data Analyst": "Data analysts collect, clean, and interpret data to help organizations make better decisions. SQL, Python, and visualization tools are standard.",
    "Research Scientist": "Research scientists design and run experiments, analyze results, and publish findings. A PhD is common for academic roles; industry roles may accept a master's.",
    "Economist": "Economists analyze economic data, model trends, and advise on policy or business strategy. Roles exist in government, finance, consulting, and academia.",
    "Financial Analyst": "Financial analysts evaluate investments, budgets, and financial performance. You might work in corporate finance, banking, or investment management.",
    "Actuary": "Actuaries use math and statistics to assess risk in insurance, finance, and pensions. Professional exams (SOA or CAS) are required for credentialing.",
    "UX/UI Designer": "UX/UI designers research user needs, create wireframes and prototypes, and test designs. A strong portfolio is essential. Backgrounds in design or psychology are common.",
    "Product Designer": "Product designers shape products from concept to launch through user research, prototyping, and close collaboration with engineering and business teams.",
    "Frontend Engineer": "Frontend engineers build the interactive layer of web and mobile applications. JavaScript/TypeScript, React, and CSS are core skills.",
    "Architect": "Architects design buildings and spaces balancing aesthetics, safety, and function. Licensure is required. The work blends creativity with technical and regulatory knowledge.",
    "Creative Technologist": "Creative technologists blend art and engineering to build novel interactive experiences. Roles exist in agencies, tech companies, and R&D labs.",
    "Product Manager": "Product managers define what to build and why, working across design, engineering, and business. Strong communication and analytical skills are essential.",
    "Marketing Manager": "Marketing managers lead campaigns, brand strategy, and market positioning. You blend creativity with data to drive awareness and growth.",
    "HR Business Partner": "HRBPs align people strategy with business objectives. You advise leaders on talent, culture, organizational design, and employee development.",
    "Counselor / Therapist": "Counselors and therapists help individuals with mental health, career, or life challenges. Licensure (LPC, LCSW) and a master's degree are required.",
    "Management Consultant": "Consultants advise organizations on strategy, operations, and change management. The work is project-based, analytical, and often involves travel.",
    "Startup Founder": "Founders launch and grow new ventures. You wear many hats \u2014 product, sales, hiring \u2014 and operate with high autonomy and risk tolerance.",
    "Sales Strategist": "Sales strategists develop go-to-market plans and revenue strategies. Strong communication, negotiation, and market knowledge are key.",
    "Business Development Manager": "BD managers identify partnerships, markets, and growth opportunities. You blend relationship-building with strategic thinking.",
    "Communications Specialist": "Communications specialists craft messaging for internal and external audiences. PR, content strategy, and media relations are common focus areas.",
    "Innovation Consultant": "Innovation consultants help organizations adopt new methods, technologies, and business models. Roles exist in consulting firms and corporate strategy teams.",
    "Policy Analyst": "Policy analysts research legislation, evaluate programs, and advise on public policy. Strong research and writing skills are essential.",
    "Nonprofit Director": "Nonprofit directors lead mission-driven organizations, managing programs, fundraising, and stakeholder relationships.",
    "Social Worker": "Social workers support individuals and communities through systemic challenges \u2014 housing, health, education, and crisis intervention. MSW and licensure are standard.",
    "Education Administrator": "Education administrators lead schools or programs, manage budgets, and drive academic outcomes. An EdD or EdS is common for senior roles.",
    "Community Organizer": "Community organizers mobilize people and resources for civic and social change. Strong communication, empathy, and strategic thinking are key.",
}


class Command(BaseCommand):
    help = "Seed 6 personality archetypes, majors, and career mappings."

    def handle(self, *args, **options):
        self._seed_archetypes()
        self._seed_majors()
        self._link_majors_to_archetypes()
        self._seed_jobs()
        self._cleanup_old_archetypes()
        self.stdout.write(self.style.SUCCESS("Career data seeded successfully."))

    def _seed_archetypes(self):
        for data in ARCHETYPES:
            PersonalityType.objects.update_or_create(
                key=data["key"],
                defaults={
                    "name": data["name"],
                    "icon": data["icon"],
                    "description": data["description"],
                    "traits": data["traits"],
                    "identity_statement": data["identity_statement"],
                    "behavioral_explanation": data["behavioral_explanation"],
                    "why_this_fits": data["why_this_fits"],
                    "strengths": data["strengths"],
                    "growth_areas": data["growth_areas"],
                    "career_direction": data["career_direction"],
                },
            )
        self.stdout.write(f"  {len(ARCHETYPES)} personality archetypes")

    def _seed_majors(self):
        for key, name, description in MAJORS:
            Major.objects.update_or_create(
                key=key,
                defaults={"name": name, "description": description},
            )
        self.stdout.write(f"  {len(MAJORS)} majors")

    def _link_majors_to_archetypes(self):
        for arch_key, major_keys in MAJOR_ARCHETYPE_MAP.items():
            archetype = PersonalityType.objects.filter(key=arch_key).first()
            if archetype:
                for mk in major_keys:
                    major = Major.objects.filter(key=mk).first()
                    if major:
                        major.personality_types.add(archetype)

    def _seed_jobs(self):
        for title, description, arch_key, major_keys in CAREERS:
            archetype = PersonalityType.objects.filter(key=arch_key).first()
            learn_more = CAREER_LEARN_MORE.get(title, "")
            job, _ = Job.objects.update_or_create(
                title=title,
                defaults={
                    "description": description,
                    "learn_more": learn_more,
                    "primary_archetype": archetype,
                },
            )
            majors = Major.objects.filter(key__in=major_keys)
            job.majors.set(majors)
        self.stdout.write(f"  {len(CAREERS)} careers")

    def _cleanup_old_archetypes(self):
        valid_keys = [a["key"] for a in ARCHETYPES]
        deleted, _ = PersonalityType.objects.exclude(key__in=valid_keys).delete()
        if deleted:
            self.stdout.write(f"  Removed {deleted} old archetype(s)")
