"""AI summary / polish / comment generation service."""

from openai import OpenAI


SUMMARY_MAX_CHARS = 300
CONTENT_MAX_CHARS = 50000

STYLE_PROMPTS = {
    "formal": (
        "你是一位正式的公告撰写专家。请用严谨、正式的语气，"
        "写一段 300 字符以内的正式公告式简介。"
        "直接描述文章核心内容和观点，不要使用'本文介绍了'等开头语。"
    ),
    "marketing": (
        "你是一位营销文案专家。请用夸张、吸引眼球的营销风格，"
        "写一段 300 字符以内的简介。"
        "可以使用感叹号、问号等吸引注意力的方式，但要基于文章实际内容。"
    ),
    "academic": (
        "你是一位学术编辑。请用学术论文摘要的风格，精炼专业，"
        "写一段 300 字符以内的简介。"
        "使用专业术语，客观描述文章内容。"
    ),
    "casual": (
        "请用轻松娱乐的口吻，像朋友聊天一样，"
        "写一段 300 字符以内的简介。"
        "语气自然随意，可以适当口语化。"
    ),
    "humorous": (
        "请用幽默搞笑的风格，可以玩梗，"
        "写一段 300 字符以内的简介。"
        "既要搞笑又要准确传达文章主要内容。"
    ),
}

POLISH_PROMPTS = {
    "formatting": (
        "你是一位排版专家。请仅优化以下文章的排版（段落空行、标题层级），"
        "**严禁修改原文任何一个字，严禁增删任何内容**。"
        "只调整 Markdown 格式，不改文字。"
    ),
    "typo": (
        "你是一位文字校对专家。请仅修正以下文章中的错别字和重复词句，"
        "不要改变原意，不要添加新内容。保持原文风格不变。"
    ),
    "academic": (
        "请用学术规范的语言润色以下文章，保持原意不变。"
        "使语言更加严谨、专业，符合学术写作规范。"
    ),
    "youth_lit": (
        "请用青春文学的风格润色以下文章，文艺清新。"
        "保持原意不变，但让语言更加优美、有画面感。"
    ),
}

NIUBAO_SYSTEM_PROMPT = (
    "你是牛宝，一个温暖、幽默的好朋友。"
    "请根据以下内容，发表一段或安慰、或建议、或鼓励的评论，"
    "控制在 200 字符以内，语气自然像朋友聊天。"
    "不要使用'本文'、'作者'等距离感的词，直接用'你'来称呼。"
)


def _callAI(api_key: str, base_url: str, model: str, systemPrompt: str, userContent: str,
            maxTokens: int = 250, temperature: float = 0.3, timeout: int = 30) -> str:
    """Call AI API with given system + user messages and return response text."""
    if not api_key:
        raise ValueError("AI_API_KEY is not configured")

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userContent},
        ],
        max_tokens=maxTokens,
        temperature=temperature,
        timeout=timeout,
    )
    return response.choices[0].message.content.strip()


def generateSummary(content: str, api_key: str, base_url: str, model: str,
                    style: str = "formal", customPrompt: str | None = None) -> dict:
    """Generate a Chinese summary (<= 300 chars) with given style."""
    if style == "custom" and customPrompt:
        systemPrompt = customPrompt
    else:
        systemPrompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["formal"])

    summary = _callAI(api_key, base_url, model, systemPrompt, content[:CONTENT_MAX_CHARS])
    return {
        "summary": summary[:SUMMARY_MAX_CHARS],
        "model": model,
    }


def polishContent(content: str, api_key: str, base_url: str, model: str,
                  style: str = "formatting", customPrompt: str | None = None) -> dict:
    """Polish article content with given style."""
    if style == "custom" and customPrompt:
        systemPrompt = customPrompt
    else:
        systemPrompt = POLISH_PROMPTS.get(style, POLISH_PROMPTS["formatting"])

    polished = _callAI(api_key, base_url, model, systemPrompt, content[:CONTENT_MAX_CHARS],
                       maxTokens=4096, temperature=0.3, timeout=60)
    return {
        "polished": polished,
        "model": model,
    }


def generateComment(content: str, api_key: str, base_url: str, model: str) -> dict:
    """Generate a comment from Niubao about the given content."""
    comment = _callAI(api_key, base_url, model, NIUBAO_SYSTEM_PROMPT,
                      content[:CONTENT_MAX_CHARS], maxTokens=200, temperature=0.8)
    return {
        "comment": comment,
        "model": model,
    }