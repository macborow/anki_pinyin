# -*- coding: utf-8 -*-
import re

def replace_numbers_with_tones(text):
    """
    Replace syllables ending with numbers (e.g. shu1) with pinyin tone marks.
    The tone marks are assigned with the following priority:
     - A and E first
     - O is accented in OU
     - otherwise, the *final* vowel
    ARGS:
        text (str) - input string
    RETURNS:
        str
    """
    vowels = "AaEeIiOoUuVv"
    tones = "ĀÁǍÀāáǎàĒÉĚÈēéěèĪÍǏÌīíǐìŌÓǑÒōóǒòŪÚǓÙūúǔùǕǗǙǛǖǘǚǜ"
    vowel_group_index = 1  # make sure the index is correct as group names cannot be used with span() method
    tone_char_regex = re.compile("[^{vowels}{tones}]*(?P<vowels>[{vowels}]+)[^{vowels}{tones}]*(?P<tonenumber>[1-4])".format(vowels=vowels, tones=tones))
    pos = 0
    chunks = []
    while True:
        match = tone_char_regex.search(text, pos=pos)
        if not match:
            chunks.append(text[pos:])
            break
        next_pos = match.end()

        vowel_group_text = match.groupdict().get("vowels")
        replace_index = match.end(vowel_group_index) - 1
        if 'a' in vowel_group_text:
            replace_index = match.start(vowel_group_index) + vowel_group_text.index('a')
        elif 'e' in vowel_group_text:
            replace_index = match.start(vowel_group_index) + vowel_group_text.index('e')
        elif 'ou' in vowel_group_text:
            replace_index = match.start(vowel_group_index) + vowel_group_text.index('ou')

        print(replace_index, text[replace_index])
        vowel_index = vowels.index(text[replace_index])
        vowel_with_tone_index = vowel_index * 4 + int(match.groupdict().get("tonenumber")) - 1
        vowel_with_tone = tones[vowel_with_tone_index]
        chunks.append(text[pos:replace_index] + vowel_with_tone + text[replace_index + 1 : next_pos - 1])
        pos = next_pos
    return "".join(chunks)
