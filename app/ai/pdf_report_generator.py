from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

import pandas as pd

from app.database.db import get_engine

engine = get_engine()


def generate_executive_report():

    reports_df = pd.read_sql(
        """
        SELECT *
        FROM ai_audit_reports
        ORDER BY created_at DESC
        LIMIT 20;
        """,
        engine
    )

    doc = SimpleDocTemplate(
        "reports/executive_audit_report.pdf",
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "ThemisFin AI — Executive Audit Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    for _, row in reports_df.iterrows():

        heading = Paragraph(
            f"""
            <b>
            {row['anomaly_type']}
            </b>
            """,
            styles["Heading2"]
        )

        elements.append(heading)

        content = Paragraph(
            row["generated_report"],
            styles["BodyText"]
        )

        elements.append(content)

        elements.append(Spacer(1, 20))

    doc.build(elements)

    print(
        "Executive audit PDF generated."
    )


if __name__ == "__main__":

    generate_executive_report()