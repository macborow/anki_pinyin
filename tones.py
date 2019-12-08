# -*- coding: utf-8 -*-
import re

def replace_numbers_with_tones(text):
    """
    Replace syllables ending with numbers (e.g. shu1) with pinyin tone marks.
    ARGS:
        text (str) - input string
    RETURNS:
        str
    """
    vowels = "AaEeIiOoUuVv"
    tones = "ĀÁǍÀāáǎàĒÉĚÈēéěèĪÍǏÌīíǐìŌÓǑÒōóǒòŪÚǓÙūúǔùǕǗǙǛǖǘǚǜ"
    mainvowel_group_index = 1  # make sure the index is correct as group names cannot be used with span() method
    tone_char_regex = re.compile("[^{vowels}]*(?P<mainvowel>[{vowels}])([{vowels}]*)[^{vowels}]*(?P<tonenumber>[1-4])".format(vowels=vowels))
    pos = 0
    chunks = []
    while True:
        match = tone_char_regex.search(text, pos=pos)
        if not match:
            chunks.append(text[pos:])
            break
        replace_index = match.start(mainvowel_group_index)
        next_pos = match.end()
        vowel_index = vowels.index(match.groupdict().get("mainvowel"))
        vowel_with_tone_index = vowel_index * 4 + int(match.groupdict().get("tonenumber")) - 1
        vowel_with_tone = tones[vowel_with_tone_index]
        chunks.append(text[pos:replace_index] + vowel_with_tone + text[replace_index + 1 : next_pos - 1])
        pos = next_pos
    return "".join(chunks)
