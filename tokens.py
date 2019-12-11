import re

import tones

class Token:
    __slots__ = ['text', 'tone']
    def __init__(self, text, tone):
        self.text = text
        self.tone = tone

    def __str__(self):
        return "<{} tone={}>".format(repr(self.text), self.tone)

    def __repr__(self):
        return str(self)


def tokenize(text):
    """
    Split given text into syllables. This is an approximation as it can match syllables that "do not exist",
    i.e. the function assumes that the text contains valid pinyin content.
    YIELDS:
        Token - individual tokens. Text not matched to any syllable is marked as tone 0 (neutral).
    """
    vowels = "aeiouü"
    tones_list = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ"
    initials = ['', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'w']
    neutral_finals = ['a', 'o', 'e', 'ai', 'ei', 'ao', 'ou', 'an', 'en', 'ang', 'eng', 'er',
                      'i', 'ia', 'io', 'ie', 'iao', 'iu', 'ian', 'in', 'iang', 'ing',
                      'u', 'ua', 'ue', 'uo', 'uai', 'ui', 'uan', 'un', 'uang', 'ong',
                      'ü', 'üe', 'üan', 'ün', 'iong']

    tone_regex = re.compile("[{}]".format(tones_list))
    def get_tone_number(syllable):
        """
        Detect tone number. 0 - neutral
        RETURNS:
            int
        """
        tone_number = 0
        match = tone_regex.search(syllable)
        if match:
            tone_number = tones_list.index(match.group(0)) % 4 + 1
        return tone_number

    finals = []
    # create all permutations of syllables and tones - this will produce some invalid combinations but that's fine
    for final in neutral_finals:
        index = tones.get_index_of_tone_vowel(final)
        assert index > -1
        tones_start = vowels.index(final[index]) * 4
        finals.append(final)  # neutral tone
        for tone_index in range(tones_start, tones_start + 4):
            tmp_final = final[:index] + tones_list[tone_index] + final[index + 1:]
            finals.append(tmp_final)
    permutations = ['{}{}'.format(initial, final) for initial in initials for final in finals]
    permutations.sort(key=lambda x: -len(x))  # check for longest match first
    unmatched = []
    while text:
        for syllable in permutations:
            if text.startswith(syllable):
                if unmatched:
                    yield Token(''.join(unmatched), 0)
                    unmatched = []
                yield Token(syllable, get_tone_number(syllable))
                text = text[len(syllable):]
                continue
        unmatched.append(text[0])
        text = text[1:]
    if unmatched:
        yield Token(''.join(unmatched), 0)

