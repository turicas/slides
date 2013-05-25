#!/usr/bin/env python
# coding: utf-8

'''Create a `dict` and adds key-value pairs to it, while saves information
about the size of the `dict` (the size does not include key and value sizes)
'''

import sys


def dict_size(size, step, filename):
    dictionary = {}
    with open(filename, 'w') as fobj:
        for counter in range(1, size + 1):
            dictionary[counter] = True
            dict_size = sys.getsizeof(dictionary)
            fobj.write('{}\t{}\n'.format(counter, dict_size))
            if counter % step == 0:
                sys.stdout.write('\r{:09d}/{:09d}'.format(counter, size))
                sys.stdout.flush()
        dict_size = sys.getsizeof(dictionary)
        fobj.write('{}\t{}\n'.format(counter, dict_size))
        sys.stdout.write('\r{:09d}/{:09d}'.format(counter, size))
        sys.stdout.flush()
        print('')


if __name__ == '__main__':
    dict_size(size=2 ** 23, step=2 ** 10, filename='dict_size.dat')
