# Assumes big.txt is in the same dir.

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('../input/big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] * 10 **(len(word)) / N

def correction(word): 
    "Most probable spelling correction for word."
    
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."    
    
    return (known([word]) or known(similar_edit(word)) or known(double_edit(word)) or known(double_edit2(word)) or known(double_back_edit(word)) or known(double_back_edit2(word)) or known(vowel_edit(word)) or known(edits1(word)) or known(edits2(word)) or [word])
    
    #return (known([word]) or known(edits1(word)) or known(edits2(word)) or known(edits3(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return list(set(w for w in words if w in WORDS))

def vowels(char):
    "Generate all possible vowels if the char is vowel, in other cases return empty list"
    vowels = 'aeiou'
    if (char == 'a' or char == 'u' or char == 'i' or char == 'o' or char == 'e'):
        return vowels
    else:
        return ''
    
def similar_to(char):
    "Generates some similar characters if char satisfies any of conditions"
    if (char == 'c'):
        return 's'
    if (char == 's'):
        return 'c'
    if (char == 'b'):
        return 'p'
    if (char == 'p'):
        return 'b'
    if (char == 'n'):
        return 'm'
    if (char == 'm'):
        return 'n'
    if (char == 'd'):
        return 't'
    if (char == 't'):
        return 'd'
    else:
        return ''
  
def double_back_edit(word):
    "Removing one of the 2 sequently appearing characters in words (if there any)"
    splits = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if len(R)>1 if R[0]==R[1]]
    
    return set(deletes)


def double_back_edit2(word):
    "Removing one of the 2 sequently appearing characters in words (if there any) second time"
    deletes = []
    for e in double_back_edit(word):
        splits = [(e[:i], e[i:])    for i in range(len(e) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if len(R)>1 if R[0]==R[1]]
    
    return set(deletes)
    
def double_edit(word):
    "Doing the same that the function above but on reverse direction (e.g. 'adres' -> 'address'"
    letters = 'bcdeflmnoprstvy'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    inserts    = [L + L[-1] + R               for L, R in splits if L]
    
    return set(inserts)
   
def double_edit2(word):
    "Same as double_back_edit2 but on reverse direction"
    letters = 'bcdeflmnoprstvy'
    for e in double_edit(word):
        splits     = [(e[:i], e[i:])    for i in range(len(e) + 1)]
        inserts    = [L + L[-1] + R               for L, R in splits if L]
    
    return set(inserts)

def vowel_edit(word):
    "Getting set of words where vowels are replaced(common mestake :) )"
    for e in double_edit(word):
        splits     = [(e[:i], e[i:])    for i in range(len(e) + 1)]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in vowels(R[0])]
    
    return set(replaces)
    
def similar_edit(word):
    "Getting set of where chars are replaced by similar ones (if any) (common mictake?)"
    for e in double_edit(word):
        splits     = [(e[:i], e[i:])    for i in range(len(e) + 1)]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in similar_to(R[0])]
    
    return set(replaces)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
  
    
def edits3(word):
    "All edits that are four edits away from 'word'."
    return (e3 for e2 in edits2(word) for e3 in edits2(e2))

# Assumes spell-testset1.txt and spell-testset2.txt are in the same dir.

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    x = 0
    y = 0
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]


#spelltest(Testset(open('../input/spell-testset1.txt'))) # Development set
#spelltest(Testset(open('../input/spell-testset2.txt'))) # Final test set
def test_corpus(filename):
    print("Testing " + filename)
    spelltest(Testset(open('../input/' + filename)))     

test_corpus('spell-testset1.txt') # Development set
test_corpus('spell-testset2.txt') # Final test set

# Supplementary sets
test_corpus('wikipedia.txt')
test_corpus('aspell.txt')



