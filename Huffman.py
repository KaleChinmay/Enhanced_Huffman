'''
Author : Chinmay Kale
ID : ck1239
Version : 1
Revision : 1
'''

import heapq
import math
import time


#Node class for building Huffman tree.
class Node:
    __slots__ = 'value','count','left','right' 
    def __init__(self,value,count=1):
        self.left = None
        self.right = None
        self.value = value
        self.count = count

    def __lt__(self, node):
        return (self.count < node.count)

    def __gt__(self, node):
        return (self.count > node.count)
    
    def __str__(self):
        return self.value+' : '+str(self.count)


#Get Input from text
def get_text():
    with open('text.txt','r') as input_file:
        input_text = input_file.read()
        #print(input_text)
        return input_text


#Get frequency of characters in input text
def get_frequency(input_text):
    char_dict = {}
    for char in input_text:
        if char not in char_dict.keys():
            char_dict[char] = 1
        else:
            char_dict[char] += 1
    #print_dict(char_dict)
    return char_dict


#Print a Dictionary
def print_dict(input_dict):
    for key in input_dict.keys():
        print('Key : ',key,', Value : ',input_dict[key])


def huffman(char_dict,encoding_dict):
    priority_queue = []
    heapq.heapify(priority_queue)
    for key in char_dict.keys():
        node = Node(key,char_dict[key])
        heapq.heappush(priority_queue, node)

    while len(priority_queue)>1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        new_node = Node('Intermediate',node1.count+node2.count)
        new_node.left = node1
        new_node.right = node2
        heapq.heappush(priority_queue, new_node)

    huffman_code_traversal(priority_queue[0],encoding_dict)
    

#Traverse helper function
def huffman_code_traversal(root,encoding_dict):
    inorder(root,'',encoding_dict)


#Traverse huffman tree to get Huffman code for every character
def inorder(node,code,encoding_dict):
    if node.left==None and node.right == None:
        encoding_dict[node.value] = code
        return
    inorder(node.left, code+'0',encoding_dict)
    inorder(node.right, code+'1',encoding_dict)


#Encode the text file
def encode(input_text, encoding_dict):
    encoded_text = ''
    for char in input_text:
        if char not in encoding_dict.keys():
            print('Char not available in encoding_dict: ')
            return
        encoded_text += encoding_dict[char]
    encoded_text_len = len(encoded_text)
    input_text_len = len(input_text)*8
    compression_ratio = input_text_len/encoded_text_len
    '''
    print('Length of encoded text is :',encoded_text_len)
    print('Length of input text is :',input_text_len)
    print('Compression ratio',round(compression_ratio,2))
    '''
    return encoded_text, encoded_text_len


#Decode the text file
def decode(encoded_text, encoding_dict):
    decoded_text = ''
    while encoded_text != '':
        for key in encoding_dict.keys():
            if encoded_text.startswith(encoding_dict[key]):
                decoded_text += key
                encoded_text = encoded_text.replace(encoding_dict[key],'',1)
    return decoded_text


#Traditional Huffman code.
def traditional_huffman(input_text):
    char_dict = get_frequency(input_text)
    encoding_dict = {}
    huffman(char_dict, encoding_dict)
    #print_dict(encoding_dict)
    encoded_text, encoded_text_len = encode(input_text, encoding_dict)
    decoded_text = decode(encoded_text, encoding_dict)
    input_text_len = len(input_text)*8
    compression_ratio = input_text_len/encoded_text_len
    print('Length of encoded text is :',encoded_text_len)
    print('Length of input text is :',input_text_len)
    print('Compression ratio',round(compression_ratio,2))
    if input_text == decoded_text:
        print('Decoded text is correct!!')
    else:
        print('Decoded text doesnt match the input text')


#Create different blocks of input text.
def enblock(input_text):
    block_count = 10
    #thresh_hold = 2000
    input_text_block = []
    input_length = len(input_text)
    print('Characters : ',input_length)
    print('Total input length : ',input_length*8)
    #block_count = math.ceil(input_length/thresh_hold)
    thresh_hold = math.ceil(input_length/block_count) 
    print('block_count : ',block_count)
    i = 0
    while i < block_count:
        base_index = i*thresh_hold
        if i==block_count-1:
            input_text_block.append(input_text[base_index:])
        else:
            input_text_block.append(input_text[base_index : base_index+thresh_hold])
        #print(input_text_block[i])
        i = i+1
    return input_text_block
    

#Modified Huffman code
def block_huffman(input_text):
    total_encoded_text_len = 0
    input_text_block = enblock(input_text)
    input_text_block_length = len(input_text_block)
    for i in range(input_text_block_length):
        encoding_dict = {}
        #print('------->')
        #print('Block : ',i+1)
        char_dict = get_frequency(input_text_block[i])
        huffman(char_dict, encoding_dict)
        encoded_text, encoded_text_len = encode(input_text_block[i], encoding_dict)
        total_encoded_text_len += encoded_text_len
        decoded_text = decode(encoded_text, encoding_dict)
        input_text_block_len = len(input_text_block[i])*8
        '''
        if input_text_block[i] == decoded_text:
            print('Decoded text is correct!!')
        else:
            print(input_text_block[i],' : ',decoded_text)
            print('Decoded text doesnt match the input text')
        '''
        #print('<-------')

    input_text_len = len(input_text)*8
    print('total_encoded_text_len : ',total_encoded_text_len)
    print('Total Length of input text is :',input_text_len)
    compression_ratio = input_text_len/total_encoded_text_len
    print('Total Compression ratio',round(compression_ratio,2))        


#Main Function.
def main():
    input_text = get_text()
    start = time.time()

    print('Traditional Huffman Code stats: ')
    traditional_huffman(input_text)
    end = time.time()
    exec_time = round(end - start, 2)
    print('Traditional Huffman Code : ', exec_time)

    start = time.time()
    print('\nImproved Huffman Code(Block Huffman) stats: ')
    block_huffman(input_text)
    end = time.time()
    exec_time = round(end - start, 2)
    print('Improved Huffman Code : ', exec_time)

if __name__=='__main__':
    main()
