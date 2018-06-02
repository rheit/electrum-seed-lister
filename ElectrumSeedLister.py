# ElectrumSeedLister
# Copyright 2018 Marisa Heit
#
# Uses code from Electrum to generate a list of possible wallet seeds,
# when you have a seed already but realize it isn't quite right. Works
# best when only one word is wrong.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
 
import sys
import hmac
import unicodedata
import hashlib
import binascii
import os

# The hash of the mnemonic seed must begin with this
SEED_PREFIX      = '01'      # Standard wallet
SEED_PREFIX_2FA  = '101'     # Two-factor authentication
SEED_PREFIX_SW   = '100'     # Segwit wallet

hmac_sha_512 = lambda x, y: hmac.new(x, y, hashlib.sha512).digest()

def normalize_text(seed):
    # normalize
    seed = unicodedata.normalize('NFKD', seed)
    # lower
    seed = seed.lower()
    # remove accents
    seed = u''.join([c for c in seed if not unicodedata.combining(c)])
    # normalize whitespaces
    seed = u' '.join(seed.split())
    # remove whitespaces between CJK
    #seed = u''.join([seed[i] for i in range(len(seed)) if not (seed[i] in string.whitespace and is_CJK(seed[i-1]) and is_CJK(seed[i+1]))])
    return seed

def bh2u(x):
    """
    str with hex representation of a bytes-like object
    >>> x = bytes((1, 2, 10))
    >>> bh2u(x)
    '01020A'
    :param x: bytes
    :rtype: str
    """
    return binascii.hexlify(x).decode('ascii')

def load_wordlist(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read().strip()
    s = unicodedata.normalize('NFKD', s)
    lines = s.split('\n')
    wordlist = []
    for line in lines:
        line = line.split('#')[0]
        line = line.strip(' \r')
        assert ' ' not in line
        if line:
            wordlist.append(line)
    return wordlist

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def main_oneword(argv):
    wordlist = load_wordlist('english.txt')
    blank = 0
    for x in range(1, len(argv)):
        if (argv[x] not in wordlist):
            print('Not in word list:', argv[x])
            if blank > 0:
                blank = -1
            elif blank == 0:
                blank = x
    if blank == 0:
        print("No words found that aren't in the word list")
        return
    elif blank < 0:
        print("Only one word not in the word list should be given")
        return
    for w in wordlist:
        argv[blank] = w
        check_seed(u' '.join(argv[1:]))

def main(argv):
    wordlist = load_wordlist('english.txt')
    blank = []
    for x in range(1, len(argv)):
        if (argv[x] not in wordlist):
            print('Not in word list:', argv[x])
            blank.append(x)
    if not blank:
        print("No words found that aren't in the word list")
    else:
        if len(blank) > 1:
            if query_yes_no("There is more than one missing word. This will likely produce a very large list.\n"\
                "Do you really want to do this?", "no") == 'no':
                return
        try_combos(argv, blank, wordlist)

def try_combos(argv, blank, wordlist):
    for w in wordlist:
        argv[blank[0]] = w
        if len(blank) > 1:
            try_combos(argv, blank[1:], wordlist)
        check_seed(u' '.join(argv[1:]))

def check_seed(seed):
    seed = normalize_text(seed)
    s = bh2u(hmac_sha_512(b"Seed version", seed.encode('utf8')))
    if s.startswith(SEED_PREFIX):
        print('Standard wallet:', seed)
    if s.startswith(SEED_PREFIX_2FA):
        print('2FA wallet:', seed)
    if s.startswith(SEED_PREFIX_SW):
        print('Segwit wallet:', seed)

main(sys.argv)