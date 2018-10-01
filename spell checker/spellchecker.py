import sys
import re

words = open("basic.words").readlines()
# chomp newline
words = map(lambda x: x.strip(), words)

hash = {}
for word in words : hash[word] = True

text  = sys.stdin.read()

# strip out punctuation, lowercase all text
words = re.sub("[^a-zA-Z'-]"," ",text).lower().split()

for word in words:
   print (hash.has_key(word), word)

