import re


# =========================================================
# SKILL WEIGHTS
# =========================================================

SKILL_WEIGHTS = {
    "python": 20,
    "fastapi": 15,
    "rest api": 10,
    "sql": 10,
    "postgresql": 10,
    "sqlalchemy": 10,
    "git": 5,
    "github": 5,
    "docker": 5,
    "aws": 3,
    "kubernetes": 2,
}


# =========================================================
# SKILL ALIASES
# Handles normal spelling + common OCR variations
# =========================================================

SKILL_ALIASES = {
    "python": [
        "python",
        "python3",
        "python 3",
    ],

    "fastapi": [
        "fastapi",
        "fast api",
    ],

    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest-api",
        "restful-api",
        "rest api development",
        "restful api development",
        "rest apis development",
        "restful apis development",
    ],

    "sql": [
        "sql",
        "structured query language",
    ],

    "postgresql": [
        "postgresql",
        "postgres",
        "postgre sql",
        "postgre-sql",
    ],

    "sqlalchemy": [
        "sqlalchemy",
        "sql alchemy",
        "sql-alchemy",
    ],

    "git": [
        "git",
        "git version control",
        "version control with git",
    ],

    "github": [
        "github",
        "git hub",
        "git-hub",
    ],

    "docker": [
        "docker",
        "docker container",
        "docker containers",
        "containerization",
    ],

    "aws": [
        "aws",
        "amazon web services",
        "amazon web service",
    ],

    "kubernetes": [
        "kubernetes",
        "k8s",
    ],
}


# =========================================================
# OCR NORMALIZATION
# =========================================================

OCR_REPLACEMENTS = {
    # API OCR mistakes
    "apl": "api",
    "apls": "apis",
    "a pl": "api",
    "a pls": "apis",
    "a p l": "api",
    "a p l s": "apis",

    # Common OCR mistakes
    "fast api": "fastapi",
    "sql alchemy": "sqlalchemy",
    "git hub": "github",
    "postgre sql": "postgresql",
}


def normalize_text(text: str) -> str:
    """
    Normalize text before ATS matching.

    Handles:
    - lowercase
    - OCR errors
    - hyphens/slashes
    - repeated spaces
    """

    if not text:
        return ""

    text = text.lower()

    # OCR corrections
    for wrong, correct in OCR_REPLACEMENTS.items():
        text = text.replace(wrong, correct)

    # Keep important words separated
    text = re.sub(r"[-_/]", " ", text)

    # Normalize common punctuation
    text = re.sub(r"[|•·]", " ", text)

    # Remove excessive punctuation
    text = re.sub(r"[^\w\s+#.]", " ", text)

    # Re-apply OCR replacements after punctuation cleanup
    for wrong, correct in OCR_REPLACEMENTS.items():
        text = text.replace(wrong, correct)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# KEYWORD MATCHING
# =========================================================

def contains_keyword(text: str, keyword: str) -> bool:
    """
    Safely checks whether a keyword exists in text.
    """

    text = normalize_text(text)
    keyword = normalize_text(keyword)

    if not text or not keyword:
        return False

    pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

    return bool(re.search(pattern, text))


# =========================================================
# SKILL EXTRACTION
# =========================================================

def extract_skills(text: str) -> set[str]:
    """
    Extract canonical skills from resume/job description.
    """

    text = normalize_text(text)

    found_skills = set()

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            normalized_alias = normalize_text(alias)

            if contains_keyword(text, normalized_alias):
                found_skills.add(canonical_skill)
                break

    return found_skills


# =========================================================
# KEYWORD GROUPS
# =========================================================

KEYWORD_GROUPS = {

    "backend": [
        "backend",
        "back end",
        "server side",
        "server-side",
        "backend development",
    ],

    "api": [
        "api",
        "apis",
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
    ],

    "database": [
        "database",
        "databases",
        "db",
        "postgresql",
        "sql",
    ],

    "authentication": [
        "authentication",
        "authorization",
        "jwt",
        "oauth",
        "login",
        "security",
    ],

    "testing": [
        "testing",
        "unit testing",
        "pytest",
        "test cases",
        "api testing",
    ],

    "cloud": [
        "cloud",
        "aws",
        "azure",
        "gcp",
        "google cloud",
    ],

    "deployment": [
        "deployment",
        "deploy",
        "ci/cd",
        "cicd",
        "docker",
        "containerization",
    ],

    "version_control": [
        "git",
        "github",
        "gitlab",
        "version control",
    ],

    "nlp": [
        "nlp",
        "natural language processing",
        "text processing",
    ],

    "machine_learning": [
        "machine learning",
        "machine-learning",
        "ml",
        "artificial intelligence",
    ],
}


# =========================================================
# KEYWORD SCORE
# =========================================================

def calculate_keyword_score(
    resume_text: str,
    job_description: str
) -> dict:

    resume_text = normalize_text(resume_text)
    job_description = normalize_text(job_description)

    matched_groups = []
    missing_groups = []

    for group, keywords in KEYWORD_GROUPS.items():

        job_requires_group = any(
            contains_keyword(job_description, keyword)
            for keyword in keywords
        )

        if not job_requires_group:
            continue

        resume_has_group = any(
            contains_keyword(resume_text, keyword)
            for keyword in keywords
        )

        if resume_has_group:
            matched_groups.append(group)
        else:
            missing_groups.append(group)

    total = len(matched_groups) + len(missing_groups)

    if total > 0:
        score = round(
            (len(matched_groups) / total) * 100
        )
    else:
        score = 100

    return {
        "keyword_score": score,
        "matched_keywords": sorted(matched_groups),
        "missing_keywords": sorted(missing_groups),
    }


# =========================================================
# ROLE MATCHING
# =========================================================

ROLE_KEYWORDS = {

    "backend developer": [
        "backend developer",
        "backend engineer",
        "back end developer",
        "back end engineer",
        "back-end developer",
        "back-end engineer",
        "backend development",
    ],

    "software developer": [
        "software developer",
        "software engineer",
        "software development",
    ],

    "python developer": [
        "python developer",
        "python engineer",
        "python development",
    ],

    "full stack developer": [
        "full stack",
        "full-stack",
        "full stack developer",
        "full-stack developer",
    ],

    "data analyst": [
        "data analyst",
        "data analysis",
        "data analytics",
    ],

    "machine learning": [
        "machine learning engineer",
        "machine learning",
        "ml engineer",
        "ml developer",
    ],

    "ai engineer": [
        "ai engineer",
        "artificial intelligence engineer",
        "ai development",
    ],
}


ROLE_SKILL_SIGNALS = {

    "backend developer": [
        "python",
        "fastapi",
        "flask",
        "django",
        "rest api",
        "sql",
        "postgresql",
        "sqlalchemy",
        "backend",
    ],

    "python developer": [
        "python",
        "fastapi",
        "flask",
        "django",
        "python development",
    ],

    "software developer": [
        "python",
        "c++",
        "java",
        "javascript",
        "software development",
        "programming",
    ],

    "full stack developer": [
        "frontend",
        "backend",
        "react",
        "javascript",
        "html",
        "css",
        "api",
    ],

    "data analyst": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "excel",
        "data analysis",
    ],

    "machine learning": [
        "machine learning",
        "ml",
        "tensorflow",
        "pytorch",
        "scikit learn",
        "sklearn",
        "python",
        "model",
    ],

    "ai engineer": [
        "artificial intelligence",
        "ai",
        "machine learning",
        "python",
        "nlp",
        "deep learning",
    ],
}


def calculate_role_match(
    resume_text: str,
    job_description: str
) -> dict:

    resume_text = normalize_text(resume_text)
    job_description = normalize_text(job_description)

    detected_roles = []

    for role, keywords in ROLE_KEYWORDS.items():

        if any(
            contains_keyword(job_description, keyword)
            for keyword in keywords
        ):
            detected_roles.append(role)

    if not detected_roles:

        return {
            "role_match_score": 100,
            "target_roles": [],
            "matched_roles": [],
        }

    matched_roles = []

    for role in detected_roles:

        # Exact role title
        exact_role_match = any(
            contains_keyword(resume_text, keyword)
            for keyword in ROLE_KEYWORDS[role]
        )

        if exact_role_match:
            matched_roles.append(role)
            continue

        # Skill-based role matching
        signals = ROLE_SKILL_SIGNALS.get(role, [])

        matched_signals = sum(
            1
            for signal in signals
            if contains_keyword(resume_text, signal)
        )

        # If resume contains enough relevant skills,
        # consider the role matched even if exact title
        # isn't present.
        if matched_signals >= 2:
            matched_roles.append(role)

    score = round(
        (len(matched_roles) / len(detected_roles)) * 100
    )

    return {
        "role_match_score": score,
        "target_roles": sorted(detected_roles),
        "matched_roles": sorted(matched_roles),
    }


# =========================================================
# EDUCATION MATCHING
# =========================================================

EDUCATION_KEYWORDS = [

    "b.tech",
    "btech",
    "b.e",
    "be degree",
    "bachelor",
    "bachelor degree",
    "computer science",
    "computer science engineering",
    "information technology",
    "artificial intelligence",
    "engineering degree",
    "undergraduate",
]


def calculate_education_score(
    resume_text: str,
    job_description: str
) -> dict:

    resume_text = normalize_text(resume_text)
    job_description = normalize_text(job_description)

    education_required = any(
        contains_keyword(job_description, keyword)
        for keyword in EDUCATION_KEYWORDS
    )

    if not education_required:

        return {
            "education_score": 100,
            "education_required": False,
        }

    education_found = any(
        contains_keyword(resume_text, keyword)
        for keyword in EDUCATION_KEYWORDS
    )

    return {
        "education_score": 100 if education_found else 0,
        "education_required": True,
    }


# =========================================================
# RESUME QUALITY
# =========================================================

QUALITY_SECTIONS = [

    "summary",
    "objective",
    "technical skills",
    "skills",
    "experience",
    "education",
    "projects",
    "certifications",
    "achievements",
]


def calculate_resume_quality(
    resume_text: str
) -> dict:

    resume_text = normalize_text(resume_text)

    found_sections = []

    for section in QUALITY_SECTIONS:

        if contains_keyword(resume_text, section):
            found_sections.append(section)

    score = round(
        (len(found_sections) / len(QUALITY_SECTIONS)) * 100
    )

    return {
        "resume_quality_score": score,
        "sections_found": sorted(found_sections),
    }


# =========================================================
# MAIN ATS CALCULATOR
# =========================================================

def calculate_ats_score(
    resume_text: str,
    job_description: str
) -> dict:

    # Normalize inputs
    resume_text_normalized = normalize_text(resume_text)
    job_description_normalized = normalize_text(job_description)

    # ---------------------------------------------
    # SKILLS
    # ---------------------------------------------

    resume_skills = extract_skills(
        resume_text_normalized
    )

    job_skills = extract_skills(
        job_description_normalized
    )

    matched_skills = resume_skills.intersection(
        job_skills
    )

    missing_skills = job_skills - resume_skills

    total_weight = sum(
        SKILL_WEIGHTS.get(skill, 0)
        for skill in job_skills
    )

    matched_weight = sum(
        SKILL_WEIGHTS.get(skill, 0)
        for skill in matched_skills
    )

    if total_weight > 0:

        skill_score = round(
            (matched_weight / total_weight) * 100
        )

    else:

        skill_score = 100

    # ---------------------------------------------
    # KEYWORDS
    # ---------------------------------------------

    keyword_result = calculate_keyword_score(
        resume_text_normalized,
        job_description_normalized
    )

    # ---------------------------------------------
    # ROLE
    # ---------------------------------------------

    role_result = calculate_role_match(
        resume_text_normalized,
        job_description_normalized
    )

    # ---------------------------------------------
    # EDUCATION
    # ---------------------------------------------

    education_result = calculate_education_score(
        resume_text_normalized,
        job_description_normalized
    )

    # ---------------------------------------------
    # RESUME QUALITY
    # ---------------------------------------------

    quality_result = calculate_resume_quality(
        resume_text_normalized
    )

    # ---------------------------------------------
    # FINAL ATS SCORE
    # ---------------------------------------------

    final_score = round(

        (
            skill_score * 0.50
            + keyword_result["keyword_score"] * 0.20
            + role_result["role_match_score"] * 0.15
            + education_result["education_score"] * 0.10
            + quality_result["resume_quality_score"] * 0.05
        )

    )

    final_score = max(
        0,
        min(100, final_score)
    )

    # ---------------------------------------------
    # RESULT
    # ---------------------------------------------

    return {

        "ats_score": final_score,

        "matched_skills": sorted(
            matched_skills
        ),

        "missing_skills": sorted(
            missing_skills
        ),

        "skills_found_in_resume": sorted(
            resume_skills
        ),

        "skills_required_by_job": sorted(
            job_skills
        ),

        "score_breakdown": {

            "skill_match": skill_score,

            "keyword_match":
                keyword_result["keyword_score"],

            "role_match":
                role_result["role_match_score"],

            "education_match":
                education_result["education_score"],

            "resume_quality":
                quality_result["resume_quality_score"],
        },

        "matched_keywords":
            keyword_result["matched_keywords"],

        "missing_keywords":
            keyword_result["missing_keywords"],

        "target_roles":
            role_result["target_roles"],

        "matched_roles":
            role_result["matched_roles"],

        "education_required":
            education_result["education_required"],

        "resume_sections_found":
            quality_result["sections_found"],
    }