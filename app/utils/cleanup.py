"""
Clears the temporary, in-memory session state after a batch of voice
messages has been processed.

Note on "temporary files": this project never writes voice audio to
disk (see app/services/audio.py) - files are downloaded straight into
memory and transcribed immediately, so there is no on-disk cleanup to
perform. The only temporary state that exists is the FSM's in-memory
list of voice references for the current batch, which is what this
function clears, while keeping the user's chosen interface language.
"""

from aiogram.fsm.context import FSMContext


async def clear_voice_session(state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    await state.set_data({"lang": lang, "voices": []})
