import sys
import re
import string

# read word list into array
words = open("basic.words").readlines()
# chomp newline
words = map(lambda x: x.strip(), words)

# index word list into hash
hash = {}
for word in words : hash[word] = True

# read text file (supplied as '< text' )
text  = sys.stdin.read()

# strip out punctuation, lowercase all text
words = re.sub("[^a-zA-Z-]"," ",text).lower().split()

# def find_fixes(word):
#     suggestions = set()
#     possibilities = fixes(word)
#     for edit in possibilities[:]:
#         possibilities.extend(fixes(edit))
#     for fix in possibilities:
#         if fix in hash.keys():
#             suggestions.add(fix)
#     return suggestions

def fixes(word):
    # find all possible 'words' that are one edit away from word
    letters = string.lowercase
    # all possible splits of word
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    # check for deleted letters
    deletions = [L + R[1:] for L, R in splits if R]
    # check for transposed letters
    transpositions = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    # checked for replaced letters
    replacements   = [L + x + R[1:] for L, R in splits if R for x in letters]
    # check for insertions
    insertions    = [L + x + R for L, R in splits for x in letters]
    # return the set of all fixes that are in words
    return set(deletions + transpositions + replacements + insertions).intersection(hash.keys())
    # possibilities = set(deletions + transpositions + replacements + insertions)
    # return list(possibilities)

def lookup_word(word):
    if not hash.has_key(word):
#        suggestions = find_fixes(word)
        suggestions = fixes(word)
        return False, list(suggestions)
    return True, []


def testing():
    
    test_cases = {
        'cat' : (True, []),
        'dog' : (True, []),
        'dogs' : (True, []),
        'alligator' : (False, []),
        'dwg' : (False, ['dog']),
        'daag' : (False, [])
        }
    
    for word, expected_output in test_cases.iteritems():
        output = lookup_word(word)
        if output != expected_output:
            print "TEST FAILED: " + ','.join([str(x) for x in output]) + " != " + ','.join([str(x) for x in expected_output])
        else:
            print "TEST PASSED"
            


def print_results(word, suggestions):
    if suggestions:
        print word + ' (did you mean: ' + ', '.join(suggestions) + ')'
    else:
        print word + ' (no suggestions)'
        
            
testing()



for word in words:
    found = False
    suggestions = []
    (found, suggestions) = lookup_word(word)
    if not found:
        if word.endswith('s'):
            new_word = word[:-1]
            (found, suggestions) = lookup_word(new_word)
    print_results(word, suggestions)
            

