#!/usr/bin/python

def main():
    from collections import OrderedDict
    d = OrderedDict()
    with open(args.stem_count_file) as src:
        for l in src:
            fields = l.strip().split()
            w, stem, freq = fields[0], fields[1], int(fields[2])
            if not w in d:
                d[w] = (stem,freq)
            else:
                d[w] = max([d[w],(stem,freq)],key=lambda x:x[1])
    for w, t in d.iteritems():
        print w, t[0]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('stem_count_file')
    args = parser.parse_args()
    main()
