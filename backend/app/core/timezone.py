"""时区转换工具：将 SQLite CURRENT_TIMESTAMP (UTC) 转为北京时间 (UTC+8)。"""

from datetime import datetime, timedelta, timezone

BEIJING_TZ = timezone(timedelta(hours=8))


def toBeijingTime(utcStr: str | None) -> str | None:
    """将 UTC 时间字符串 "YYYY-MM-DD HH:MM:SS" 转换为北京时间字符串。

    Args:
        utcStr: UTC 时间字符串，格式 "YYYY-MM-DD HH:MM:SS"，可为 None

    Returns:
        北京时间字符串 "YYYY-MM-DD HH:MM:SS"，输入为 None 时返回 None
    """
    if not utcStr:
        return utcStr

    dt = datetime.strptime(utcStr, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    beijing = dt.astimezone(BEIJING_TZ)
    return beijing.strftime("%Y-%m-%d %H:%M:%S")