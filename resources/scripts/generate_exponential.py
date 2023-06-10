# -*- coding: utf-8 -*-

import sys
from scipy.stats import expon

def main():
    args = sys.argv

    if len(args) != 2 :
        print('inform exponential distribution parameter')
        return

    if args[1].isnumeric() == False :
        print('exponential distribution parameter must be a number')
        return

    timeInMinutes = expon.rvs(scale=int(args[1]), size=1)[0]
    timeInMilliseconds = timeInMinutes * 60 * 1000

    print("%.0f" % timeInMilliseconds)


if __name__ == "__main__":
    main()

