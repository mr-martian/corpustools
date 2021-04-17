#!/usr/bin/env python3

from typing import List

class Reading:
    def __init__(self, lemh: str, tags: List[str], lemq: str):
        self.lemh = lemh
        self.tags = tags
        self.lemq = lemq
    def surface(self):
        return self.lemh + ''.join('<%s>' % t for t in self.tags) + self.lemq

class LU:
    def __init__(self, readings: List[List[Reading]], wblank: str, mode: str):
        self.readings = readings
        self.wblank = wblank # TODO: split into pieces?
        self.mode = mode
    def __getattribute__(self, key):
        if key == 'lemma':
            return self.readings[0].surface()
        elif key == 'anaphora':
            return self.readings[-1]
        elif key == 'readings':
            # TODO: tagger with no surface
            return self.readings[1:]
        elif key == 'surface':
            return self.readings[0]
        elif key == 'translations':
            if self.mode == 'anaphora':
                return self.readings[1:-1]
            else:
                return self.readings[1:]
        else:
            return self.__dict__[key]

class Blank:
    def __init__(self, content: str):
        self.content = content

def parse(s: str, mode: str):
    tokens = []
    i = 0
    def readblank():
        nonlocal i, s, tokens
        last = i
        block = False
        while i < len(s):
            if s[i] == '\\':
                i += 1
            elif block and s[i] == ']':
                block = False
            elif s[i] == '^' and not block:
                tokens.append(Blank(s[last:i]))
                return
            elif s[i] == '[':
                if i+1 < len(s) and s[i+1] == '[':
                    tokens.append(Blank(s[last:i]))
                    return
                else:
                    block = True
            else:
                pass
            i += 1
        tokens.append(Blank(s[last:]))
    def readlu():
        nonlocal i, s, tokens, mode
        wblank = ''
        last = i
        if s[i] == '[':
            while i < len(s):
                if s[i] == '\\':
                    i += 1
                elif s[i] == ']' and i+1 < len(s) and s[i+1] == ']':
                    wblank = s[last:i+2]
                    i += 2
                    break
                i += 1
        if s[i] != '^':
            raise Exception('not really sure what to do here')
        i += 1
        last = i
        readings = []
        cur = []
        while i < len(s):
            if s[i] == '/' or s[i] == '$':
                readings.append(cur)
                cur = ['']
                i += 1
                if s[i-1] == '$':
                    break
            elif s[i] == '+':
                i += 1
            else:
                lemh = ''
                tags = []
                lemq = ''
                last = i
                while i < len(s):
                    if s[i] == '\\':
                        i += 1
                    elif s[i] == '<':
                        lemh = s[last:i]
                        break
                    i += 1
                while s[i] == '<':
                    i += 1
                    last = i
                    while i < len(s):
                        if s[i] == '>':
                            tags.append(s[last:i])
                            i += 1
                            break
                        i += 1
                last = i
                while s[i] not in '+/$':
                    if s[i] == '\\':
                        i += 1
                    i += 1
                lemq = s[last:i]
                cur.append(Reading(lemh, tags, lemq))
        tokens.append(LU(readings, wblank, mode))
    while i < len(s):
        readblank()
        if i < len(s):
            readlu()
    return tokens
