from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.node import Node


# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------
# Reference: https://iq.opengenus.org/autocomplete-with-ternary-search-tree/


class TernarySearchTreeDictionary:
    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        self.ternaryTree = Node()
        for word_frequency in words_frequencies:
            self.add_word_frequency(word_frequency)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        cur_node = self.ternaryTree
        word_len = len(word)
        i = 0
        while i < word_len and cur_node != None:
            letter = word[i]
            if letter < cur_node.letter:
                cur_node = cur_node.left
            elif letter == cur_node.letter:
                i += 1
                if i < word_len:
                    cur_node = cur_node.middle
            else:
                cur_node = cur_node.right

        if i < word_len or cur_node == None or cur_node.end_word == False:
            return 0

        return cur_node.frequency

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary if it isn't there yet
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TODO: Implement
        cur_node = self.ternaryTree
        word_len = len(word_frequency.word)
        i = 0
        while i < word_len:
            letter = word_frequency.word[i]
            if cur_node.letter == None:
                cur_node.letter = letter
            if letter < cur_node.letter:
                if cur_node.left == None:
                    cur_node.left = Node()
                cur_node = cur_node.left
            elif letter == cur_node.letter:
                if i == word_len - 1:
                    break
                if cur_node.middle == None:
                    cur_node.middle = Node()
                cur_node = cur_node.middle
                i += 1
            elif letter > cur_node.letter:
                if cur_node.right == None:
                    cur_node.right = Node()
                cur_node = cur_node.right
        if cur_node.end_word == False:
            cur_node.end_word = True
            cur_node.frequency = word_frequency.frequency
            return True
        return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # First, perform a search on the word, if doesn't exist return False
        if self.search(word) == 0:
            return False

        cur_node = self.ternaryTree

        node_list = []
        word_len = len(word)
        i = 0
        while i < word_len and cur_node != None:
            letter = word[i]
            if letter < cur_node.letter:
                cur_node = cur_node.left
            elif letter == cur_node.letter:
                node_list.append(cur_node)
                i += 1
                if i < word_len:
                    cur_node = cur_node.middle
            else:
                cur_node = cur_node.right

        # Reverse node list
        node_list = node_list[::-1]

        # Start resetting value or removing nodes
        for i in range(len(node_list)):
            node = node_list[i]
            if i == 0:
                node.end_word = 0
            if node.middle == None and node.left == None and node.right == None:
                node = None
        return True

    def autocomplete(self, word: str) -> [str]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        cur_node = self.ternaryTree
        word_len = len(word)
        i = 0
        while i < word_len and cur_node != None:
            letter = word[i]
            if letter < cur_node.letter:
                cur_node = cur_node.left
            elif letter == cur_node.letter:
                i += 1
                if i < word_len:
                    cur_node = cur_node.middle
            else:
                cur_node = cur_node.right

        # Word not found
        if i < word_len or cur_node == None:
            return []

        word_list = []
        word_list.append([cur_node, word, cur_node.frequency, cur_node.end_word])

        # Iterate through remaining nodes in tree
        i = 0
        while i != len(word_list):
            cur_node = word_list[i][0]
            cur_word = word_list[i][1]
            for dir in {cur_node.left, cur_node.middle, cur_node.right}:
                list_item = None
                if dir != None:
                    if dir == cur_node.left or dir == cur_node.right:
                        list_item = [
                            dir,
                            cur_word[:-1] + dir.letter,
                            dir.frequency,
                            dir.end_word,
                        ]
                        if i > 0 and list_item not in word_list:
                            word_list.append(list_item)
                    else:
                        list_item = [
                            dir,
                            cur_word + dir.letter,
                            dir.frequency,
                            dir.end_word,
                        ]
                        word_list.append(list_item)
            i += 1

        # Remove words that don't exist
        temp_word_list = []
        for data in word_list:
            frequency, end_word = data[2], data[3]
            if frequency != None and end_word == True:
                temp_word_list.append(data)
        word_list = temp_word_list

        for i in range(len(word_list)):
            word_list[i] = word_list[i][1:]

        # Sort by frequency
        if word_list != []:
            word_list.sort(key=lambda x: x[1], reverse=True)
            word_list = word_list[:3]
            for i in range(len(word_list)):
                word_list[i] = WordFrequency(word_list[i][0], word_list[i][1])

        return word_list
