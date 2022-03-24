from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED. List-based dictionary implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class ListDictionary(BaseDictionary):

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """

        self.dictList = []
        for i in words_frequencies:
            pair = [i.word, i.frequency]
            self.dictList.append(pair)


    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        for i in self.dictList:
            if i[0] == word.strip():
                return i[1]

        return 0



    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """

        for i in self.dictList:
            if i[0] == word_frequency.word:
                return False
            else:
                pair = [word_frequency.word, word_frequency.frequency]
                self.dictList.append(pair)
                return True




    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        for i in self.dictList:
            if i[0] == word.strip():
                self.dictList.remove(i)
                return True

        return False


    def autocomplete(self, prefix_word: str) -> [str]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """
        shortList = []
        finalList = []
        for i in self.dictList:
            if i[0].startswith(prefix_word):
                shortList.append([i[0], i[1]])

        shortList = sorted(shortList, key=lambda x: x[1], reverse=True)
        shortList = shortList[:3]

        for i in shortList:
            wordItem = WordFrequency(i[0], i[1])
            finalList.append(wordItem)

        return(finalList)
