#!/usr/bin/python
#coding:utf-8

import sys
from modules.node import node

def jaccard(node1,node2):
    l = len(node1.props)
    count = 0.0
    ins = 0.0
    for i in range(l):
        if(node1.props[i] is 1 & node2.props[i] is 1):
            count += 1
            ins += 1
        elif(node1.props[i] is 0 & node2.props[i] is 0):
            continue
        else:
            count += 1
    return ins/count

def clustering(nodes,sid1,sid2,traced):
    group1 = []
    group2 = []
    seed1 = nodes[sid1]
    seed2 = nodes[sid2]
    traced.append(sid1)
    traced.append(sid2)
    for n in nodes:
        if(n == seed1 or n == seed2):
            continue
        else:
            j1 = jaccard(seed1,n)
            j2 = jaccard(seed2,n)
            if j1 >= j2:
                group1.append([n,j1])
            else:
                group2.append([n,j2])

    group1.append([seed1,1])
    group2.append([seed2,1])
    core1 = findCore(group1)
    core2 = findCore(group2)
    if core1 not in traced or core2 not in traced:
        clustering(nodes,core1,core2,traced)
    else:
        getResult(group1,0)
        getResult(group2,1)

def findCore(group):
    for i in range(len(group)):
        for j in range(len(group)):
            if group[i][1] > group[j][1]:
                tmp = group[i]
                group[i] = group[j]
                group[j] = tmp
    return group[len(group)/2][0].id

def getResult(group,gid):
    result = []
    for n in group:
        result.append(n[0])
    for i in range(len(result)):
        for j in range(len(result)):
            if result[i].id < result[j].id:
                tmp = result[i]
                result[i] = result[j]
                result[j] = tmp

    f = open('cluster'+str(gid+1)+'.csv','w')
    for r in result:
        f.write(str(r.id+1))
        f.write('\n')

nodes = []
file = open('house-votes-84.data','r')
lineCount = 0
while True:
    line = file.readline()
    if not line: break
    line = line.replace("\n", "")
    props = line.split(',');
    n = node(lineCount)
    props.pop(0)
    for p in props:
        if(p == 'y'):
            n.props.append(1)
        elif(p == 'n'):
            n.props.append(0)
        else:
            n.props.append(2)
    nodes.append(n)
    lineCount += 1
file.close()

traced = []
clustering(nodes,0,1,traced)
