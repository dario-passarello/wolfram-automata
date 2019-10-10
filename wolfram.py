import numpy as np
from PIL import Image
import argparse

'''
Reads from a file with name filename a binary string that represents the initial status
'''
def read_from_file(filename):
    fp = open(filename,'r')
    line = fp.readline()
    print("Input: " + line)
    arr = []
    for c in line:
        if c == '0':
            arr.append(0)
        elif c == '1':
            arr.append(1)
        else:
            print("PARSE ERROR")
    return arr
'''
The transiction function of the elementary cellular automata
'''
def transition_function_n(left,status,right,n):
    return (n >> (left*4 + status*2 + right)) % 2 

'''
Simulates the next step of the automaton from the previous step, with boundary conditions chosen from the user
'''
def update_n(prev, args):
    new = []
    for i in range(0,len(prev)):
        if (i-1 < 0 or i+1 >= len(prev)) and args.b != "c":
            new.append(int(args.b))
        else:
            i_left = (i-1)%len(prev)
            i_right = (i+1)%len(prev) 
            new.append(transition_function_n(prev[i_left], prev[i], prev[i_right],args.rule_number))
    return new

'''
Simulates the automanton starting from starting_condition for a number of steps specified from the user
'''
def simulate(starting_condition,args):
    history = []
    prev = starting_condition
    history.append(prev)
    for k in range(0, args.steps):
        new = update_n(prev, args)
        history.append(new)
        prev = new
    return history
       
'''
Converts a binary matrix in a binary picture and saves that picture in the disk as 'out.bmp'
'''
def convert_bitmap(matrix):
    img = Image.new('1',(len(matrix[0]),len(matrix)))
    pixels = img.load()
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            pixels[i,j] = 1 - matrix[j][i]
    img.save('out.bmp')
    return img

'''
Given two binary n x m matrices h1 and h2, returns an n x m matrix with ones in the positions where h1 and h2 are different
'''
def get_diffs(h1, h2):
    diff = [[0 for item in h1[0]] for j in h1]
    for i in range(0,len(h1)):
        for j in range(0, len(h1[0])):
            if h1[i][j] != h2[i][j]:
                diff[i][j] = 1
    return diff


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="A path to a binary string that represents the initial state of the CA")
    parser.add_argument("rule_number", type=int, help="The Wolfram's rule number (between 0 and 255)")
    parser.add_argument("steps", type=int, help="Number of discrete time steps to simulate")
    parser.add_argument("-b","-boundary", type=str, choices=["c","1","0"], default="c", help="Choose boundary conditions (0,1,c)")
    parser.add_argument("-c","-compare", type=str, help="Show differences with another starting condition")
    parser.add_argument("-cc","-change","-change_central", action="store_true", help="Negate the central bit of the initial state and compare the two evolutions")
    parser.add_argument("-o","-output", type=str, default = "out.bmp", help="Specify output image file")
    parser.add_argument("-s","-show","-show_preview", action="store_true", help="Show preview")
    args = parser.parse_args() 

    out = [[]]
    s1 = read_from_file(args.input_file)
    if args.c is not None or args.cc:
        if args.cc:
            s2 = s1.copy()
            s2[int(len(s2)/2)] = 1 - s2[int(len(s2)/2)]
        else:
            s2 = read_from_file(args.c)
            if len(s1) != len(s2):
                print("ERROR! Can't compare lattices of different lenghts")
                assert(1 == 2)
        h1 = simulate(s1, args)
        h2 = simulate(s2, args)
        out = get_diffs(h1, h2)
    else:
        out = simulate(s1, args)
    img = convert_bitmap(out)
    if args.s:
        img.show()


   
