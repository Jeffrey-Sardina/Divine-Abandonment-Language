from phonetics import onsets, codas, vowels
import random
import sys

def gen_syllable(illegal_onsets=set(), illegal_vowels = set(), illegal_codas=set(),
        has_onset=True, has_coda=True):
    # generate syllable
    onset = random.choice(list(onsets["all"] - illegal_onsets)) if has_onset else ""
    vowel = random.choice(list(vowels["all"] - illegal_vowels))
    coda = random.choice(list(codas["all"] - illegal_codas)) if has_coda else ""

    # determine syllable structure
    structure = ""
    if has_onset and onset in onsets["singles"]:
        structure += "C"
    elif has_onset and onset in onsets["clusters"]:
        structure += "CC"
    structure += "V"
    if has_coda and coda in codas["singles"]:
        structure += "C"
    elif has_coda and coda in codas["clusters"]:
        structure += "CC"

    onset = onset.strip()
    vowel = vowel.strip()
    coda = coda.strip()
    return onset, vowel, coda, structure

def gen_word(num_syllables, onset_rate, coda_rate):
    word = ""
    word_structure = ""
    illegal_onsets=set()
    last_coda = ""
    for i in range(num_syllables):
        """
        No onset clusters allowed mid-word
        (except in compoun words, which this should not generate)

        Don't create coda if this is not the only sylable
        """
        is_first_syllable = i == 0
        is_last_syllable = i == num_syllables - 1
        is_only_syllable = num_syllables == 1

        if not is_first_syllable:
            illegal_onsets |= onsets["clusters"]
        
        if is_last_syllable or not is_only_syllable:
            has_coda = False
        else:
            has_coda = random.random() < coda_rate

        if last_coda == "" or is_first_syllable:
            has_onset = True
        else:
            has_onset = random.random() < onset_rate

        # generate syllable
        onset, vowel, coda, structure = gen_syllable(illegal_onsets=illegal_onsets,
            has_onset=has_onset, has_coda=has_coda)
        syllable = onset + vowel + coda

        word += syllable
        if is_first_syllable:
            word_structure += structure
        else:
            word_structure += f"-{structure}"

        last_coda = coda

    return word, word_structure

def gen_words(n, length, onset_rate, coda_rate):
    words = set()
    for _ in range(n):
        word, structure = gen_word(length, onset_rate, coda_rate)
        words.add((word, structure))
    return words

def write_words(out_file, words, append=True):
    mode = "a" if append else "w"
    with open(out_file, mode) as out:
        for word, structure in words:
            print(word, structure, sep="\t", file=out)

def main(num_iterations, length):
    onset_rate = len(onsets) / (len(onsets) + len(vowels))
    coda_rate = len(codas) / (len(codas) + len(vowels))
    words = gen_words(num_iterations, length, onset_rate, coda_rate)
    write_words("generated_words." + str(length) + ".tsv", words, append=False)
    print("Generated", len(words), "words of length", str(length), ":)))")
    if length >= 3:
        print("Note: generating words of length 3 or greater is likely a linguistically poor choice; try manually evolving words instead")
        print("Sincerely, you")

def gather_input():
    # check input for errors
    err = None
    try:
        num_iterations = int(sys.argv[1])
        length = int(sys.argv[2])
    except:
        err = True
    if len(sys.argv) > 3:
        err = True

    # if there are errors, specify correct program use
    if err:
        print("Usage: python gen_words.py <number of words> <word length>")
        print("Note that fewer words than requested may be returned, as chance repeats sometimes occur")
        exit(0)
    
    # reutnr data needed for the rest of the program
    return num_iterations, length

if __name__ == "__main__":
    num_iterations, length = gather_input()
    main(num_iterations, length)
