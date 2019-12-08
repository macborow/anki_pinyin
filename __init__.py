
from aqt.editor import Editor
from anki.hooks import addHook

from . import tones

def addon_replace_tones(self):
    field = self.currentField
    text = self.note.fields[field]
    self.note.fields[field] = tones.replace_numbers_with_tones(text)
    self.note.flush()
    self.loadNote(focusTo=field)

Editor.addon_replace_tones = addon_replace_tones


def setupButtons(buttons, editor):
    buttons.append(editor.addButton(icon=None,  # TODO: replace with .png icon
                                    cmd="tones",
                                    func=addon_replace_tones,
                                    tip="Replace numbers with pinyin tone marks",
                                    keys="Ctrl+0"))
    return buttons

addHook("setupEditorButtons", setupButtons)
