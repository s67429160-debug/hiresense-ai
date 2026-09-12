from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

import os


# =========================================================
# REPORT DIRECTORY
# =========================================================

REPORT_DIR = os.path.join(
    "uploads",
    "reports"
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


# =========================================================
# GENERATE ATS REPORT
# =========================================================

def generate_ats_report(
    analysis,
    resume_filename,
    user_name,
    matched_skills,
    missing_skills,
    score_breakdown,
    recommendations=None,
):

    # -----------------------------------------------------
    # PDF FILE PATH
    # -----------------------------------------------------

    file_path = os.path.join(
        REPORT_DIR,
        f"ats_report_{analysis.id}.pdf"
    )

    absolute_path = os.path.abspath(
        file_path
    )

    print("GENERATING PDF:", absolute_path)


    # -----------------------------------------------------
    # PDF DOCUMENT
    # -----------------------------------------------------

    doc = SimpleDocTemplate(
        absolute_path,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )


    # -----------------------------------------------------
    # STYLES
    # -----------------------------------------------------

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=8,
    )


    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=20,
    )


    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        spaceBefore=12,
        spaceAfter=8,
    )


    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
    )


    score_style = ParagraphStyle(
        "ScoreStyle",
        parent=styles["Heading1"],
        fontSize=38,
        leading=42,
        alignment=TA_CENTER,
    )


    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=12,
        textColor=colors.grey,
    )


    # -----------------------------------------------------
    # STORY
    # -----------------------------------------------------

    story = []


    # =====================================================
    # TITLE
    # =====================================================

    story.append(
        Paragraph(
            "HireSense AI",
            title_style
        )
    )


    story.append(
        Paragraph(
            "AI-Powered Resume Analysis Report",
            subtitle_style
        )
    )


    # =====================================================
    # CANDIDATE INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "Candidate Information",
            heading_style
        )
    )


    candidate_data = [
        [
            "Candidate",
            str(user_name)
        ],
        [
            "Resume",
            str(resume_filename)
        ],
        [
            "Analysis ID",
            str(analysis.id)
        ],
        [
            "Analysis Date",
            str(analysis.created_at)
            if analysis.created_at
            else "N/A"
        ],
    ]


    candidate_table = Table(
        candidate_data,
        colWidths=[
            45 * mm,
            125 * mm
        ]
    )


    candidate_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eeeeee")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.lightgrey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )


    story.append(
        candidate_table
    )


    story.append(
        Spacer(1, 15)
    )


    # =====================================================
    # ATS SCORE
    # =====================================================

    story.append(
        Paragraph(
            "Overall ATS Score",
            heading_style
        )
    )


    score_table = Table(
        [
            [
                Paragraph(
                    f"{analysis.ats_score}%",
                    score_style
                )
            ]
        ],
        colWidths=[
            170 * mm
        ],
        rowHeights=[
            35 * mm
        ],
    )


    score_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#f3f3f3")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                colors.HexColor("#dddddd")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
        ])
    )


    story.append(
        score_table
    )


    story.append(
        Spacer(1, 10)
    )


    # =====================================================
    # SCORE BREAKDOWN
    # =====================================================

    story.append(
        Paragraph(
            "Score Breakdown",
            heading_style
        )
    )


    if score_breakdown is None:
        score_breakdown = {}


    breakdown_data = [
        [
            "Category",
            "Score"
        ],
        [
            "Skill Match",
            f"{score_breakdown.get('skill_match', 0)}%"
        ],
        [
            "Keyword Match",
            f"{score_breakdown.get('keyword_match', 0)}%"
        ],
        [
            "Role Match",
            f"{score_breakdown.get('role_match', 0)}%"
        ],
        [
            "Education Match",
            f"{score_breakdown.get('education_match', 0)}%"
        ],
        [
            "Resume Quality",
            f"{score_breakdown.get('resume_quality', 0)}%"
        ],
    ]


    breakdown_table = Table(
        breakdown_data,
        colWidths=[
            125 * mm,
            45 * mm
        ]
    )


    breakdown_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#eeeeee")
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (1, 0),
                (1, -1),
                "CENTER"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.lightgrey
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )


    story.append(
        breakdown_table
    )


    # =====================================================
    # MATCHED SKILLS
    # =====================================================

    story.append(
        Paragraph(
            "Matched Skills",
            heading_style
        )
    )


    if matched_skills:

        matched_text = ", ".join(
            str(skill).strip().title()
            for skill in matched_skills
            if str(skill).strip()
        )


        story.append(
            Paragraph(
                matched_text,
                normal_style
            )
        )

    else:

        story.append(
            Paragraph(
                "No matched skills identified.",
                normal_style
            )
        )


    # =====================================================
    # MISSING SKILLS
    # =====================================================

    story.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )


    if missing_skills:

        missing_text = ", ".join(
            str(skill).strip().title()
            for skill in missing_skills
            if str(skill).strip()
        )


        story.append(
            Paragraph(
                missing_text,
                normal_style
            )
        )

    else:

        story.append(
            Paragraph(
                "No missing skills identified.",
                normal_style
            )
        )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    if recommendations:

        story.append(
            Paragraph(
                "Recommended Improvements",
                heading_style
            )
        )


        recommendation_rows = [
            [
                "Skill",
                "Priority",
                "Reason"
            ]
        ]


        for recommendation in recommendations:

            skill = recommendation.get(
                "skill",
                recommendation.get(
                    "title",
                    "Recommended Skill"
                )
            )


            priority = recommendation.get(
                "priority",
                "Medium"
            )


            reason = recommendation.get(
                "reason",
                recommendation.get(
                    "description",
                    ""
                )
            )


            recommendation_rows.append([
                Paragraph(
                    str(skill),
                    normal_style
                ),
                Paragraph(
                    str(priority),
                    normal_style
                ),
                Paragraph(
                    str(reason),
                    normal_style
                ),
            ])


        recommendation_table = Table(
            recommendation_rows,
            colWidths=[
                40 * mm,
                30 * mm,
                100 * mm
            ],
            repeatRows=1,
        )


        recommendation_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#eeeeee")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
            ])
        )


        story.append(
            recommendation_table
        )


    # =====================================================
    # FOOTER
    # =====================================================

    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "Generated by HireSense AI",
            small_style
        )
    )


    story.append(
        Paragraph(
            "This report is intended for resume improvement and career analysis.",
            small_style
        )
    )


    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)


    # =====================================================
    # VERIFY FILE
    # =====================================================

    if not os.path.exists(absolute_path):

        raise FileNotFoundError(
            f"PDF report was not created: {absolute_path}"
        )


    print(
        "PDF CREATED SUCCESSFULLY:",
        absolute_path
    )


    return absolute_path