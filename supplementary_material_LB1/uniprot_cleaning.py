#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import argv
file1=open(argv[1], "r")
file2=open(argv[2],"r")
file3=open(argv[3], "w")
lst=[]
lst2=[]
for line in file1:
    lst.append(line)
for line2 in file2:
    lst2.append(line2)
for i in lst:
    if i not in lst2:
        file3.write(i)

