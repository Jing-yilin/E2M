import logging

logger = logging.getLogger(__name__)


def estimate_char_to_token(chars: str) -> int:
    return len(chars) // 2


def estimate_token_to_char(tokens: int) -> int:
    return tokens * 2


def clean_to_markdown(content: str):
    # todo: add more rules or use a parser
    if content.startswith("```markdown") and content.endswith("```"):
        content = content[11:-3]
    elif content.startswith("```") and content.endswith("```"):
        content = content[3:-3]
    elif content.startswith("```markdown") and not content.endswith("```"):
        logger.warning("Markdown code block not closed")
        content = content[11:]
    elif content.startswith("```") and not content.endswith("```"):
        logger.warning("Markdown code block not closed")
        content = content[3:]

    return content
