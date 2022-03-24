from curses import endwin
from dataclasses import asdict
from distutils.command.build_scripts import first_line_re
from itertools import chain
from locale import currency
from operator import truediv
from re import search
from sys import intern
from dictionary import node
from dictionary import word_frequency
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.node import Node


# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


class TernarySearchTreeDictionary(BaseDictionary):

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """

        self.ternaryTree = None

        for word in words_frequencies:
            curNode = self.ternaryTree # Reset starting position of ternary tree
            
            for i in range(len(word.word)):
                char = word.word[i]

                if i == 0: # First char
                    if curNode == None:
                        self.ternaryTree = Node(char)
                        curNode = self.ternaryTree
                    # Find valid start point 
                    validStart = False
                    while not validStart:
                        if curNode.letter == char:
                            validStart = True
                        elif char < curNode.letter:
                            if curNode.left == None:
                                curNode.left = Node(char)
                                validStart = True
                            elif curNode.left.letter == char:
                                validStart = True
                            curNode = curNode.left

                        elif char > curNode.letter:
                            if curNode.right == None:
                                curNode.right = Node(char)
                                validStart = True
                            elif curNode.right.letter == char:
                                validStart = True
                            curNode = curNode.right
                else: # If not first char
                    validNode = False
                    while not validNode:
                        if curNode.middle == None: # If node beneath is empty, set node
                            curNode.middle = Node(char)
                            curNode = curNode.middle
                            validNode = True
                        elif curNode.middle.letter == char: # If node beneath matches current char, update node
                            curNode = curNode.middle
                            validNode = True
                        elif char <= curNode.letter: # If char is smaller than value of node
                            if curNode.middle.left == None:
                                curNode.middle.left = Node(char)
                                curNode = curNode.middle.left
                                validNode = True
                            elif curNode.middle.left.letter == char:
                                curNode = curNode.middle.left
                                validNode = True
                            else:
                                validNode = True # TODO: Add functionality if left child is full
                        elif char > curNode.letter: # If char is greater than value of node 
                            if curNode.middle.right == None:
                                curNode.middle.right = Node(char)
                                curNode = curNode.middle.right
                                validNode = True
                            elif curNode.middle.right.letter == char:
                                curNode = curNode.middle.right
                                validNode = True
                            else:
                                validNode = True # TODO: Add functionality if right child is full

                    if i == len(word.word) - 1:
                        curNode.frequency = word.frequency
                        curNode.end_word = True


        # import gc

        # for obj in gc.get_objects():
        #     if isinstance(obj, Node):
        #         print("Letter: {} Score: {}".format(obj.letter, obj.frequency))
        #         if obj.left != None:
        #             print("left: " + obj.left.letter)
        #         if obj.middle != None:
        #             print("middle: " + obj.middle.letter)
        #         if obj.right != None:
        #             print("right: " + obj.right.letter)

        #         print()

        l = ['cute', 'ant', 'cut', 'cuts', 'apple', 'cub', 'fathom', 'apologetic']

        for i in l:
            print(i + ": " + str(self.search(i)))

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
                
        curNode = self.ternaryTree
        for i in range(len(word)):
            found = False
            char = word[i]
            while not found:
                if i == 0: # If first char
                    if char == curNode.letter: # If letter found
                        found = True
                    elif char < curNode.letter: # If letter less than cur node
                        if curNode.left == None: # If letter not found
                            return 0
                        else: # Update node loc
                            curNode = curNode.left
                    elif char > curNode.letter: # If letter more than cur node
                        if curNode.right == None: # If letter not found
                            return 0
                        else: # Update node loc
                            curNode = curNode.right
                else:
                    if curNode.middle == None: # If next letter not found
                        return 0
                    elif char == curNode.middle.letter: # Update node loc
                        curNode, found = curNode.middle, True
                    elif char < curNode.letter: # If less than node
                        if curNode.middle.left == None:
                            return 0
                        elif curNode.middle.left.letter != char:
                            return 0
                        elif curNode.middle.left.letter == char:
                            curNode, found = curNode.middle.left, True
                    elif char > curNode.letter: # If more than mid node
                        if curNode.middle.right == None:
                            return 0
                        elif curNode.middle.right.letter != char:
                            return 0
                        elif curNode.middle.right.letter == char:
                            curNode, found = curNode.middle.right, True

        return curNode.frequency


    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """

        # Search for word and see if it exists
        if self.search(word_frequency.word) == 0:
            curNode = self.ternaryTree # Reset starting position of ternary tree
            
            for i in range(len(word_frequency.word)):
                char = word_frequency.word[i]

                if i == 0: # First char
                    if curNode == None:
                        self.ternaryTree = Node(char)
                        curNode = self.ternaryTree
                    # Find valid start point 
                    validStart = False
                    while not validStart:
                        if curNode.letter == char:
                            validStart = True
                        elif char < curNode.letter:
                            if curNode.left == None:
                                curNode.left = Node(char)
                                validStart = True
                            elif curNode.left.letter == char:
                                validStart = True
                            curNode = curNode.left

                        elif char > curNode.letter:
                            if curNode.right == None:
                                curNode.right = Node(char)
                                validStart = True
                            elif curNode.right.letter == char:
                                validStart = True
                            curNode = curNode.right
                else: # If not first char
                    validNode = False
                    while not validNode:
                        if curNode.middle == None: # If node beneath is empty, set node
                            curNode.middle = Node(char)
                            curNode = curNode.middle
                            validNode = True
                        elif curNode.middle.letter == char: # If node beneath matches current char, update node
                            curNode = curNode.middle
                            validNode = True
                        elif char <= curNode.letter: # If char is smaller than value of node
                            if curNode.middle.left == None:
                                curNode.middle.left = Node(char)
                                curNode = curNode.middle.left
                                validNode = True
                            elif curNode.middle.left.letter == char:
                                curNode = curNode.middle.left
                                validNode = True
                            else:
                                validNode = True # TODO: Add functionality if left child is full
                        elif char > curNode.letter: # If char is greater than value of node 
                            if curNode.middle.right == None:
                                curNode.middle.right = Node(char)
                                curNode = curNode.middle.right
                                validNode = True
                            elif curNode.middle.right.letter == char:
                                curNode = curNode.middle.right
                                validNode = True
                            else:
                                validNode = True # TODO: Add functionality if right child is full

                    if i == len(word_frequency.word) - 1:
                        curNode.frequency = word_frequency.frequency
                        curNode.end_word = True
            return True
        else:
            return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # TO BE IMPLEMENTED
        # place holder for return


        return False

    def autocomplete(self, word: str) -> [str]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return []
