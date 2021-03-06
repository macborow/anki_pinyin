
from aqt.editor import Editor
from anki.hooks import addHook

from . import tones
from . import tokens

def colour_tones(text):
    """
    Returns HTML with syllables marked with colours according to the tone number:
        - 1st tone: blue
        - 2nd tone: red
        - 3rd tone: green
        - 4th tone/neutral: no colour (black)
    ARGS:
        test (str) - pinyin text
    RETURNS:
        str
    """
    colour_codes = {
        0: "#000000",
        1: "#0000ff",
        2: "#ff0000",
        3: "#00aa00",
        4: "#000000"
    }
    result = []
    current_tone = -1
    for token in tokens.tokenize(text):
        if token.tone != current_tone:
            if current_tone != -1:
                result.append('</font>')
            if token.tone in colour_codes:
                result.append('<font color="{}">'.format(colour_codes[token.tone]))
        result.append(token.text)
        current_tone = token.tone
    result.append('</font>')
    return ''.join(result)


def addon_replace_tones(self):
    field = self.currentField
    text = self.note.fields[field]
    self.note.fields[field] = colour_tones(tones.replace_numbers_with_tones(text))
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
