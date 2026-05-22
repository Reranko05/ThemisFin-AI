import os

import google.generativeai as genai
from dotenv import load_dotenv

from app.ai.rag_pipeline import (
    retrieve_policy_context
)

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.0-flash-lite"
)


def generate_audit_finding(anomaly):

    query = f"""
    {anomaly['anomaly_type']}
    involving transaction amount
    {anomaly['amount']}
    """

    retrieved_docs = retrieve_policy_context(
        query
    )

    policy_context = "\n".join([
        doc.page_content
        for doc in retrieved_docs
    ])

    prompt = f"""
    You are an enterprise financial auditor.

    Transaction anomaly:
    {anomaly}

    Relevant compliance policy:
    {policy_context}

    Generate:
    1. Audit finding
    2. Risk explanation
    3. Recommended remediation

    Use professional audit language.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print(f"Gemini API failed: {e}")

        fallback_report = f"""
        AUDIT FINDING

        Transaction {anomaly['transaction_id']}
        triggered a {anomaly['anomaly_type']}
        anomaly involving amount
        {anomaly['amount']}.

        POLICY CONTEXT

        The transaction potentially violates
        enterprise approval and compliance
        controls related to authorization,
        operational monitoring, and risk
        governance.

        RISK ASSESSMENT

        This activity may indicate elevated
        operational risk exposure and requires
        additional compliance review.

        RECOMMENDED REMEDIATION

        - Perform secondary approval validation
        - Review transaction authorization chain
        - Escalate for audit investigation
        - Validate policy compliance alignment
        """

        return fallback_report