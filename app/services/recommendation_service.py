RECOMMENDATIONS = {
    "python": {
        "priority": "High",
        "recommendation": "Strengthen Python fundamentals, OOP, error handling, and backend development.",
    },
    "fastapi": {
        "priority": "High",
        "recommendation": "Learn FastAPI routing, dependency injection, authentication, validation, and async APIs.",
    },
    "rest api": {
        "priority": "High",
        "recommendation": "Learn REST API design, HTTP methods, status codes, authentication, and API best practices.",
    },
    "sql": {
        "priority": "High",
        "recommendation": "Practice SQL queries, joins, subqueries, indexes, and database optimization.",
    },
    "postgresql": {
        "priority": "Medium",
        "recommendation": "Learn PostgreSQL schema design, indexes, relationships, transactions, and optimization.",
    },
    "sqlalchemy": {
        "priority": "Medium",
        "recommendation": "Learn SQLAlchemy ORM, models, relationships, queries, and database sessions.",
    },
    "git": {
        "priority": "Medium",
        "recommendation": "Practice Git branching, commits, merging, rebasing, and pull requests.",
    },
    "github": {
        "priority": "Medium",
        "recommendation": "Learn GitHub repositories, pull requests, issues, Actions, and collaborative workflows.",
    },
    "docker": {
        "priority": "High",
        "recommendation": "Learn Docker images, containers, Dockerfiles, volumes, networking, and Docker Compose.",
    },
    "aws": {
        "priority": "High",
        "recommendation": "Learn AWS fundamentals including EC2, S3, IAM, RDS, and deployment basics.",
    },
    "kubernetes": {
        "priority": "Medium",
        "recommendation": "Learn Kubernetes pods, deployments, services, config maps, and container orchestration.",
    },
}


def generate_recommendations(missing_skills: list[str]) -> list[dict]:
    recommendations = []

    for skill in missing_skills:
        recommendation = RECOMMENDATIONS.get(skill)

        if recommendation:
            recommendations.append(
                {
                    "skill": skill,
                    "priority": recommendation["priority"],
                    "recommendation": recommendation["recommendation"],
                }
            )

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    recommendations.sort(
        key=lambda item: priority_order.get(
            item["priority"],
            99,
        )
    )

    return recommendations