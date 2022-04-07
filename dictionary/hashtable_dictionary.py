from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED. Hash-table-based dictionary.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class HashTableDictionary(BaseDictionary):

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        self.thisDict = {}
        for i in words_frequencies:
            wordCat = i.word
            freqCat = i.frequency
            self.thisDict.update({wordCat: freqCat})


    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """

        for i in self.thisDict:
            if i == word:
                return(self.thisDict[i])
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        for i in self.thisDict:
            if i == word_frequency.word:
                return False
            else:
                self.thisDict.update({word_frequency.word: word_frequency.frequency})
                return True

        return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        for i in self.thisDict:
            if i == word:
                del self.thisDict[i]
                return True

        return False

    def autocomplete(self, prefix_word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        newDict = {}
        finalList = []
        for i in self.thisDict:
            if i.startswith(prefix_word):
                newDict.update({i: self.thisDict[i]})

        newDict = dict(sorted(newDict.items(), key=lambda item: item[1]))

        for i in list(reversed(list(newDict)))[0:3]:
            wordItem = WordFrequency(i, newDict[i])
            finalList.append(wordItem)

        return(finalList)
