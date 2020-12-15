#!/usr/bin/env python
# coding: utf-8

# In[1]:
import re


def research(pattern: str, seq: str) -> re.Match:
    return re.search(re.compile(pattern), seq)


def show(res: re.Match):
    print(f"'{res.group()}' founded between {res.span()} indexes" if res else "Does Not Contain")


# In[2]:
str_instance = '1 Quick Brown Fox Jumps Over 1 Lazy Dog'

# In[3]:
show(research(r'\s*', str_instance))
show(research(r'^[A-Z]+$', str_instance))
show(research(r'[A-Z]\d*', str_instance))
show(research(r'^\d+\.\d+$', str_instance))
show(research(r'F..x', str_instance))
