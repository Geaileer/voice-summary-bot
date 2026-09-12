"""
Finite-state machine states for the bot.

The whole app has exactly three states per user, kept in aiogram's
built-in in-memory FSM storage - no database is needed for this MVP
(see app/bot.py, MemoryStorage).
"""

from aiogram.fsm.state import State, StatesGroup


class BotStates(StatesGroup):
    choosing_language = State()   # right after /start, before a language is picked
    collecting_voices = State()   # language picked, waiting for 1-10 voice messages
    processing = State()          # "Done" was pressed, transcription/summarization in progress
