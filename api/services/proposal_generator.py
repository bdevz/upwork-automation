"""
Service for generating and scoring proposals using OpenAI.
"""
import json
from typing import Dict, List

from openai import AsyncOpenAI

from shared.config import settings, ProposalTemplateConfig
from shared.models import Job
from shared.utils import setup_logging

logger = setup_logging("proposal_generator")

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def generate_proposal_content(job: Job) -> str:
    """
    Generates a 3-paragraph proposal for a given job using the OpenAI API.
    """
    prompt = f"""
    Generate a 3-paragraph proposal for the following job posting.

    **Job Title:** {job.title}
    **Job Description:** {job.description}

    **Instructions:**
    1.  **Paragraph 1 (Introduction):** Start with a goal-focused introduction that shows you understand the client's needs.
    2.  **Paragraph 2 (Experience):** Detail your relevant experience. Use metrics to quantify your achievements.
    3.  **Paragraph 3 (Call to Action):** End with a clear call-to-action, suggesting the next steps.
    """

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=ProposalTemplateConfig.MAX_PROPOSAL_LENGTH,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating proposal content: {e}")
        return "Error: Could not generate proposal content."


async def score_proposal_quality(proposal_text: str, job_description: str) -> Dict[str, any]:
    """
    Scores the quality of a proposal against a job description.
    """
    prompt = f"""
    Evaluate the following proposal based on the job description and the quality factors: {', '.join(ProposalTemplateConfig.QUALITY_FACTORS)}.
    Return a JSON object with 'quality_score' (0.0 to 1.0) and 'optimization_suggestions' (a list of strings).

    **Job Description:**
    {job_description}

    **Proposal Text:**
    {proposal_text}
    """
    # This is a placeholder for the actual implementation
    return {"quality_score": 0.85, "optimization_suggestions": ["Consider adding more specific examples of your work."]}

