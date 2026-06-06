"""Markdown to HTML renderer using Python markdown library."""
import re
import markdown


def renderMarkdown(content: str) -> str:
    """Convert Markdown content to HTML.

    For LaTeX math blocks ($$...$$) and inline math ($...$),
    wraps them in katex-compatible HTML tags so the frontend
    can run KaTeX auto-render on the final HTML.
    """
    if not content:
        return ""

    # Step 1: Protect math blocks from markdown processing
    math_blocks = []

    def replace_block(m):
        math_blocks.append(m.group(1))
        return f"@@MATH_BLOCK_{len(math_blocks) - 1}@@"

    def replace_inline(m):
        math_blocks.append(m.group(1))
        return f"@@MATH_INLINE_{len(math_blocks) - 1}@@"

    content = re.sub(r"\$\$(.+?)\$\$", replace_block, content, flags=re.DOTALL)
    content = re.sub(r"\$(.+?)\$", replace_inline, content)

    # Step 2: Render Markdown to HTML
    html = markdown.markdown(
        content,
        extensions=["fenced_code", "tables", "codehilite"],
        tab_length=2,
    )

    # Step 3: Restore math blocks as KaTeX-compatible HTML
    for i, block in enumerate(math_blocks):
        html = html.replace(f"@@MATH_BLOCK_{i}@@", f'<div class="math-block">$${block}$$</div>')
        html = html.replace(f"@@MATH_INLINE_{i}@@", f'<span class="math-inline">${block}$</span>')

    return html