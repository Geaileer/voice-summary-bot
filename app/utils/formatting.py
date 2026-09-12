"""
Turns (summary, key_points, transcript) into one or more Telegram
messages, never exceeding Telegram's 4096-character message limit and
never cutting text mid-word (spec section 16).
"""

from __future__ import annotations

from app.utils.texts import t

# Telegram's hard limit is 4096 characters; we split well below that to
# leave headroom for headers/emoji and to keep individual messages easy to read.
_SAFE_CHUNK_SIZE = 3500


def _split_text(text: str, chunk_size: int = _SAFE_CHUNK_SIZE) -> list[str]:
    """Split text into ordered chunks, preferring line breaks, then spaces."""
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > chunk_size:
        split_at = remaining.rfind("\n", 0, chunk_size)
        if split_at <= 0:
            split_at = remaining.rfind(" ", 0, chunk_size)
        if split_at <= 0:
            split_at = chunk_size
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


def format_result_messages(lang: str, summary: str, key_points: list[str], transcript: str) -> list[str]:
    """Build the ordered list of Telegram messages for the final result."""
    messages: list[str] = []

    summary_block = f"{t(lang, 'result_summary_header')}\n{summary}"
    if key_points:
        bullets = "\n".join(f"• {point}" for point in key_points)
        summary_block += f"\n\n{t(lang, 'result_keypoints_header')}\n{bullets}"
    messages.extend(_split_text(summary_block))

    transcript_block = f"{t(lang, 'result_transcript_header')}\n{transcript}"
    messages.extend(_split_text(transcript_block))

    return messages
