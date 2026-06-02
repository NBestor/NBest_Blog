"""AI summary generation service using DeepSeek / OpenAI-compatible API."""

from openai import OpenAI


SUMMARY_MAX_CHARS = 300


def generateSummary(content: str, api_key: str, base_url: str, model: str) -> dict:
    """Generate a Chinese summary (<= 300 chars) for the given article content.

    Returns:
        dict: { "summary": str, "model": str }

    Raises:
        ValueError: if api_key is empty
        TimeoutError: if API call exceeds 15 seconds
        RuntimeError: on other API errors
    """
    if not api_key:
        raise ValueError("AI_API_KEY is not configured")

    client = OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一个专业的文章编辑。为给定的文章生成一个简洁的中文简介。"
                    "必须严格遵守以下规则："
                    "1. 简介不超过300个字符，超出视为不合格；"
                    "2. 直接描述文章的核心内容和观点；"
                    "3. 不要使用'本文介绍了'、'这篇文章讲述了'等开头语；"
                    "4. 语言精炼，避免冗余修辞。"
                ),
            },
            {"role": "user", "content": content},
        ],
        max_tokens=250,
        temperature=0.3,
        timeout=15,
    )

    summary = response.choices[0].message.content.strip()
    return {
        "summary": summary[:SUMMARY_MAX_CHARS],
        "model": model,
    }