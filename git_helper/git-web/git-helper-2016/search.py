from __future__ import print_function

import sys
sys.path.append('.')
sys.path.append('..')

try:
    get_input = raw_input
except NameError:
    get_input = input

import stackexchange
so = stackexchange.Site(stackexchange.StackOverflow, app_key='OxiOwQCYQn8W1qr31PnIng((', impose_throttling=True)


so.impose_throttling = True
so.throttle_stop = False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        term = get_input('Please provide a search term:')
    else:
        term = ' '.join(sys.argv[1:])
    print('Searching for %s...' % term,)
    sys.stdout.flush()

    qs = so.search(intitle=term)

    print('\r--- questions with "%s" in title ---' % (term))

    print(type(qs))
    for q in qs:
        print('%8d %s' % (q.id, q.title))
