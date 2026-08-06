"""Which authored field feeds which channel.

A studio does not write one sentence and blast it everywhere. It writes NATIVE copy per
surface: a 280-character post is not an email subject, an email is not a podcast
description, and a 9:16 short is not a ten-minute YouTube outline. This module is the map
between what a Creative Lead authors and what each channel actually publishes.

    CHANNEL          <- AUTHORED FIELD
    x, linkedin, ... <- days.<Day>.social[n]      native short-form posts
    youtube          <- days.<Day>.short          9:16 vertical script/caption
    youtube_longform <- days.<Day>.longform       long-form title + outline
    podcast          <- days.<Day>.podcast        episode title + description
    blog             <- weeks.<n>.blog            the week's article
    email            <- days.<Day>.email_subject + email_body
    sms              <- days.<Day>.sms            <=160 chars, hard limit
    nextdoor         <- days.<Day>.social[0]      manual delivery, still authored

WHY THERE IS NO SILENT FALLBACK
An earlier version used the week's tagline as the body for EVERY channel. Everything
"worked" — payloads built, validation passed, the mock accepted them — and the output was
fifteen identical posts. Nothing failed, so nothing got fixed.

`resolve()` returns None when a channel has no authored content, and the completeness gate
turns that into a visible failure. An unauthored channel should be loud, because the
alternative is shipping filler under a client's name.
"""
from __future__ import annotations

from .calendar import Week

# Channels that publish native short-form social copy, drawn from `social[]`.
SOCIAL_CHANNELS = {
    "x", "linkedin", "instagram", "facebook", "threads", "bluesky", "pinterest",
    "tiktok", "nextdoor",
}

# Hard platform limits. Exceeding one is a silent truncation at the platform.
LIMITS = {"sms": 160, "x": 280, "bluesky": 300}


def _days_in_order(wd: Week) -> list[tuple[str, dict]]:
    out = []
    for day, slot in (wd.days or {}).items():
        if isinstance(slot, dict):
            out.append((str(day), slot))
    return out


def resolve(wd: Week, channel: str) -> tuple[str, str] | None:
    """Return (body, source_field) for a channel, or None if nothing is authored.

    Deliberately returns None rather than inventing text. The caller decides whether an
    unauthored channel is a warning or a failure; this function never papers over it.
    """
    ch = str(channel)

    if ch == "blog":
        if wd.blog:
            return wd.blog, "blog"
        return None

    if ch == "email":
        for day, slot in _days_in_order(wd):
            subject = slot.get("email_subject") or slot.get("email")
            if subject:
                return str(subject), f"days.{day}.email_subject"
        return None

    if ch == "sms":
        for day, slot in _days_in_order(wd):
            if slot.get("sms"):
                return str(slot["sms"]), f"days.{day}.sms"
        return None

    if ch == "youtube":
        for day, slot in _days_in_order(wd):
            if slot.get("short"):
                return str(slot["short"]), f"days.{day}.short"
        return None

    if ch == "youtube_longform":
        for day, slot in _days_in_order(wd):
            if slot.get("longform"):
                return str(slot["longform"]), f"days.{day}.longform"
        return None

    if ch == "podcast":
        for day, slot in _days_in_order(wd):
            if slot.get("podcast"):
                return str(slot["podcast"]), f"days.{day}.podcast"
        return None

    if ch in SOCIAL_CHANNELS:
        picks = resolve_many(wd, ch, 1)
        return picks[0] if picks else None

    return None


def social_pool(wd: Week) -> list[tuple[str, str]]:
    """Every authored social post for the week, in day order."""
    posts: list[tuple[str, str]] = []
    for day, slot in _days_in_order(wd):
        raw = slot.get("social")
        if isinstance(raw, str) and raw.strip():
            posts.append((raw, f"days.{day}.social"))
        elif isinstance(raw, (list, tuple)):
            for i, item in enumerate(raw):
                if isinstance(item, str) and item.strip():
                    posts.append((item, f"days.{day}.social[{i}]"))
    return posts


def resolve_many(wd: Week, channel: str, n: int) -> list[tuple[str, str]]:
    """Allocate up to `n` posts to a channel from the week's pool.

    THE BUG THIS REPLACES: the old resolver handed each social channel exactly ONE post
    and discarded the rest. A week authoring 5 posts a day — 35 across the week — shipped
    9 and dropped 26. The work was done, gate-checked, and then quietly never left the
    building. Nothing failed, so nothing surfaced it.

    Channels are offset into the pool by name so two platforms do not open with the same
    sentence, and the pool wraps only if a channel's cadence genuinely exceeds what was
    authored — which the cadence gate reports rather than hiding.
    """
    pool = social_pool(wd)
    if not pool or n <= 0:
        return []
    start = sorted(SOCIAL_CHANNELS).index(channel) if channel in SOCIAL_CHANNELS else 0
    return [pool[(start + i) % len(pool)] for i in range(min(n, len(pool)))]


def unauthored(wd: Week, channels: list[str]) -> list[str]:
    """Channels a brand declares but this week has no content for."""
    return [c for c in channels if resolve(wd, c) is None]


def over_limit(body: str, channel: str) -> int | None:
    """The limit a body exceeds, or None. Checked before anything is sent."""
    limit = LIMITS.get(str(channel))
    return limit if limit and len(body) > limit else None
