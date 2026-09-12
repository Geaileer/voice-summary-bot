"""
Exceptions raised by the audio/transcription/summarization services.

Each one maps to a specific, understandable message shown to the user
(see app/services/pipeline.py) instead of a raw stack trace. Full
technical details always go to the logs, never to the chat.
"""


class ProcessingError(Exception):
    """Base class for any error that should produce a user-facing message."""


class DownloadFailed(ProcessingError):
    """A voice message could not be downloaded from Telegram."""


class FileTooLarge(ProcessingError):
    """A voice message is larger than Telegram allows bots to download."""


class RateLimitReached(ProcessingError):
    """The free Groq tier's rate limit was hit."""


class ServiceUnavailable(ProcessingError):
    """Groq's API was unreachable or timed out."""


class TranscriptionFailed(ProcessingError):
    """Speech-to-text failed for a reason other than a rate limit."""


class SummarizationFailed(ProcessingError):
    """Summarization failed, or returned output that couldn't be used."""
