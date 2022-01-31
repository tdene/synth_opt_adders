#!/bin/python3

def lg(x):
    """Returns the base-2 logarithm of x, rounded up"""
    return x.bit_length()-1

def sub_brackets(x):
    """Reformats 'a[0]' to 'a_0'"""
    return x.replace('[','_').replace(']','')

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
