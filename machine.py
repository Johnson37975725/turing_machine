#!/usr/bin/python
import sys
import json

class Machine:
    def __init__(self, table):
        self.table = table
        self.tape  = ['none' for i in range(1000)]
        self.hdr_pos  = 0
        self.m_config = table['^']

    def print_tape(self, l = 100):
        print ''.join([' ' if self.tape[i] == 'none' else self.tape[i] for i in range(l)])

    def step(self):
        c = self.m_config
        s = self.tape[self.hdr_pos]

        if s in self.table[c].keys():
            b = self.table[c][s]
        elif 'else' in self.table[c].keys():
            b = self.table[c]['else']
        else:
            print 'Error: No corresponding behaviour for ' + s
            exit(1)

        for o in b[0]:
            if o[0] == 'N':
                pass # Not Mowve
            elif o[0] == 'P':
                self.tape[self.hdr_pos] = o[1]
            elif o[0] == 'E':
                self.tape[self.hdr_pos] = 'none'
            elif o[0] == 'R':
                self.hdr_pos = self.hdr_pos + 1
                if self.hdr_pos >= len(self.tape):
                    print 'Error: Out of tape-length on the right side'
                    exit(1)
            elif o[0] == 'L':
                self.hdr_pos = self.hdr_pos - 1
                if self.hdr_pos < 0:
                    print 'Error: Out of tape-length on the left side'
                    exit(1)
            else:
                print 'Error: No corresponding operation for' + o
                exit(1)

        self.m_config = b[1]

        return(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: python ' + sys.argv[0] + " fname steps"
        exit(1)

    with open(sys.argv[1], 'r') as f:
        m = Machine(json.load(f))

    for i in range(int(sys.argv[2])):
        m.step()
        m.print_tape()
