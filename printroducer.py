#!/usr/bin/env python

"""
This creates pairs of easy-to-type 128-bit shared secrets which you can print
on paper and use for authenticating with SMP or PANDA.

usage:
cat /usr/share/dict/words | python printroducer.py > printroductions.html
"""

import sys, re, math, random

BITS = 128
REJECT = re.compile('[^a-zA-Z]')

stderr = sys.stderr.write
choice = random.SystemRandom().choice

def printroducer(howmany=50):
    howmany=int(howmany)
    words = set()
    for line in sys.stdin.readlines():
        for word in line.split():
            if not REJECT.search( word ):
                words.add( word )
    words = list(words)
    word_count = len(words)
    bpw = math.log(word_count, 2)
    words_needed = int( math.ceil( BITS / bpw ) )
    stderr( "Loaded %s words; %s words * %.3f bits per word = %s bits\n" % (word_count, words_needed, bpw, BITS) )
    print """<html><style>
div {
    margin:0.5em; padding:0;
    page-break-inside: avoid;
}
pre {
    font-size:10px;
    float:left; width:45%;
    white-space: pre-wrap;
    text-align:center;
    margin:1em 0; padding:1em;
    border:1px solid black;
    border-left:0;
}
pre:first-child {
    border-right: 1px dashed black;
    border-left:1px solid black;
    clear:all;
}
</style>
"""
    for i in range(howmany):
        secret = " ".join( choice(words) for j in range(words_needed) )
        print "<div><pre>%s</pre><pre>%s</pre></div>" % (secret, secret)

if __name__ == "__main__": printroducer(*sys.argv[1:])
