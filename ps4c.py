# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        valid_words  = self.valid_words
        return valid_words
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        dictionary = {}        
        letters = string.ascii_uppercase + string.ascii_lowercase 
        for i in letters:
            dictionary[i] = i
       
        index = 0
        for i in vowels_permutation:
            if i != VOWELS_LOWER[index]:
                dictionary[VOWELS_LOWER[index]] = i
                dictionary[VOWELS_UPPER[index]] = i.upper()

            #if i != VOWELS_UPPER[index] and i in VOWELS_UPPER:
                #dictionary[VOWELS_UPPER[index]] = i
            index += 1
        return dictionary

            
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        shifted_message = ''
        for i in self.message_text:
            if i in transpose_dict:
                shifted_message += transpose_dict[i]
            else:
                shifted_message += i
        return shifted_message

#text = SubMessage('Hello World!')
#print (text.build_transpose_dict('eaiuo'))
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
    
        permutation = get_permutations(VOWELS_LOWER)
        decrypted_message = ''
        word = ''
        valid_words  = 0
        num_real_words  = []    

        for vowel in permutation:
            dictionary_transpose = self.build_transpose_dict(vowel)
            decrypted_message = self.apply_transpose(dictionary_transpose)

            for i in decrypted_message:
                if i in string.ascii_letters:
                    word += i

                if i not in string.ascii_letters or len(word) == len(decrypted_message): 
                    if is_word(load_words(WORDLIST_FILENAME),word) == True:
                        valid_words += 1
                    word = ''
                    
            num_real_words.append(valid_words)
            valid_words = 0
            
        highest_valid_words = max(num_real_words)

        for i in range(0,len(num_real_words)):

            if num_real_words[i] == highest_valid_words and highest_valid_words > 1:
                correct_permuation = permutation[i]
                valid_dictionary = self.build_transpose_dict(correct_permuation)
                return self.apply_transpose(valid_dictionary)

            if highest_valid_words <= 1:
                return self.message_text
        
        

   

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eAiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "HAllu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
    print('---------')
    message2 = SubMessage('How are you?')
    permutation2 = 'oiuea'
    enc_dict2 = message.build_transpose_dict(permutation2)
    print("Original message:", message2.get_message_text(), "Permutation:", permutation2)
    print("Expected encryption:", "Hew ori yea?")
    print("Actual encryption:", message2.apply_transpose(enc_dict2))
    enc_message2 = EncryptedSubMessage(message2.apply_transpose(enc_dict2))
    print("Decrypted message:", enc_message2.decrypt_message())

