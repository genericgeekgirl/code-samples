from collections import Counter, OrderedDict
import sys
import re
import argparse
import json

def main():
    args = parse_args()

    try:
        # check that file exists and can be read from
        with open(args.textfile) as f:
            f.read()
    except IOError as e:
        # print error (without full traceback) and exit
        sys.tracebacklimit = 0
        raise
    else:
        # do the thing
        count_words(args.textfile, args.cutoff, args.json)
        

def count_words(textfile, cutoff=10, json_format=False): 
        counter = get_counter(textfile)

        if json_format:
            print get_json(counter)           
        else:
            print get_top_words(counter, cutoff)
           
            
def get_counter(textfile):
    # words must contain letters, hyphens, and apostrophes
    # words cannot contain numbers or underscores (as opposed to using \w)
    words = re.findall(r"['a-z]+(?:[-']['a-z]+)*", open(textfile).read().lower())
    return Counter(words)


def get_top_words(counter, cutoff=10):
    # when not printing in JSON, print only the most common words
    return '\n'.join('{} - {}'.format(key, value) for key, value in counter.most_common(cutoff))


def get_json(counter):
    # when printing in JSON, print all word counts
    # example showed them unsorted, either alphabetically or numerically,
    # so I ordered them alphabetically
    return json.dumps(OrderedDict(sorted(counter.items())))
    
        
def parse_args():
    # parse positional and optional arguments from command-line
    parser = argparse.ArgumentParser(description="Read in a file and show a list of the most common words in the file.")
    parser.add_argument('textfile', type=str, help="text file to analyze")
    parser.add_argument('--json', const=True, type=bool, nargs='?', help ="display results in JSON format")
    parser.add_argument('-n', action='store', dest='cutoff', default=10, type=int, help ="number of 'most common' words to show (defaults to 10)")
    return parser.parse_args()


if __name__ == "__main__":
    main()
