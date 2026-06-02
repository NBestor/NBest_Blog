from datetime import date, timedelta
from sqlite3 import Row

from app.db.database import getDatabaseConnection


def parseDate(value: str) -> date:
    return date.fromisoformat(value)


def isLeapYear(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def yearlyDisplayDate(eventDate: date, targetYear: int) -> date:
    if eventDate.month == 2 and eventDate.day == 29 and not isLeapYear(targetYear):
        return date(targetYear, 2, 28)
    return date(targetYear, eventDate.month, eventDate.day)


def formatCalendarEvent(row: Row, displayDate: date | None = None) -> dict[str, str | int | bool | None]:
    eventDate = parseDate(row["event_date"])
    if displayDate is None:
        displayDate = eventDate

    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "title": row["title"],
        "event_date": row["event_date"],
        "display_date": displayDate.isoformat(),
        "event_type": row["event_type"],
        "note": row["note"],
        "is_yearly": bool(row["is_yearly"]),
        "create_time": row["create_time"],
        "update_time": row["update_time"],
    }


def getDisplayDatesInRange(row: Row, startDate: date, endDate: date) -> list[date]:
    eventDate = parseDate(row["event_date"])
    if not row["is_yearly"]:
        return [eventDate] if startDate <= eventDate <= endDate else []

    dates = []
    for year in range(startDate.year, endDate.year + 1):
        displayDate = yearlyDisplayDate(eventDate, year)
        if startDate <= displayDate <= endDate:
            dates.append(displayDate)
    return dates


def listCalendarEvents(userId: int, month: str | None = None) -> list[dict[str, str | int | bool | None]]:
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM calendar_events
            WHERE user_id = ?
            ORDER BY event_date ASC, id ASC
            """,
            (userId,),
        ).fetchall()

    if month is None:
        return [formatCalendarEvent(row) for row in rows]

    year, monthNumber = (int(part) for part in month.split("-", 1))
    startDate = date(year, monthNumber, 1)
    if monthNumber == 12:
        endDate = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        endDate = date(year, monthNumber + 1, 1) - timedelta(days=1)

    items = []
    for row in rows:
        for displayDate in getDisplayDatesInRange(row, startDate, endDate):
            items.append(formatCalendarEvent(row, displayDate))

    return sorted(items, key=lambda item: (str(item["display_date"]), int(item["id"])))


def createCalendarEvent(
    userId: int,
    title: str,
    eventDate: str,
    eventType: str,
    note: str | None,
    isYearly: bool,
) -> dict[str, str | int | bool | None]:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO calendar_events (user_id, title, event_date, event_type, note, is_yearly)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (userId, title, eventDate, eventType, note, int(isYearly)),
        )
        connection.commit()
        row = connection.execute("SELECT * FROM calendar_events WHERE id = ?", (cursor.lastrowid,)).fetchone()

    return formatCalendarEvent(row)


def updateCalendarEvent(
    userId: int,
    eventId: int,
    title: str,
    eventDate: str,
    eventType: str,
    note: str | None,
    isYearly: bool,
) -> dict[str, str | int | bool | None] | None:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            """
            UPDATE calendar_events
            SET title = ?,
                event_date = ?,
                event_type = ?,
                note = ?,
                is_yearly = ?,
                update_time = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (title, eventDate, eventType, note, int(isYearly), eventId, userId),
        )
        if cursor.rowcount == 0:
            return None
        connection.commit()
        row = connection.execute(
            "SELECT * FROM calendar_events WHERE id = ? AND user_id = ?",
            (eventId, userId),
        ).fetchone()

    return formatCalendarEvent(row)


def deleteCalendarEvent(userId: int, eventId: int) -> bool:
    with getDatabaseConnection() as connection:
        cursor = connection.execute(
            "DELETE FROM calendar_events WHERE id = ? AND user_id = ?",
            (eventId, userId),
        )
        connection.commit()
        return cursor.rowcount > 0


def listCalendarReminders(userId: int) -> list[dict[str, str | int | bool | None]]:
    startDate = date.today()
    endDate = startDate + timedelta(days=7)
    with getDatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM calendar_events
            WHERE user_id = ?
            ORDER BY event_date ASC, id ASC
            """,
            (userId,),
        ).fetchall()

    items = []
    for row in rows:
        for displayDate in getDisplayDatesInRange(row, startDate, endDate):
            items.append(formatCalendarEvent(row, displayDate))

    return sorted(items, key=lambda item: (str(item["display_date"]), int(item["id"])))
