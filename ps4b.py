# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):

    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
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
        copy = self.valid_words
        return copy

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        dictionary = {}        
        letters = string.ascii_uppercase + string.ascii_lowercase 
        for i in letters:
            dictionary[i] = i
        dict_list = list(dictionary)
        index = 0
 
        for letter in dictionary:
            if index + shift >= 52:
                dictionary[letter] = dict_list[(index + shift) -52]
                index +=1
            else:
                dictionary[letter] = dict_list[index + shift]
                index +=1

        return dictionary

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_dictionary  = Message.build_shift_dict(self,shift)
        shifted_message = ''
        for i in self.message_text:
            if i in shifted_dictionary and i in string.ascii_lowercase:
                shifted_message += shifted_dictionary[i].lower()                      # Assigns dictionary keys shifted value to shifted message.

            if i in shifted_dictionary and i in string.ascii_uppercase:
                shifted_message += shifted_dictionary[i].upper()

            if i not in shifted_dictionary:
                shifted_message += i
        #print(shifted_dictionary)
        return shifted_message

#text = Message('Hello, World!')
#print(text.apply_shift(4) )

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self,text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        dictionary = self.encryption_dict
        return dictionary

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

#text = PlaintextMessage('hello',2)
#print(text.shift,text.message_text_encrypted)
#print(text.get_encryption_dict())
#text.change_shift(24)
#print(text.shift,text.message_text_encrypted)
#print(text.get_encryption_dict())


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self,text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        real_words  = 0
        decrypted_message = ''
        word  = ''
        list_of_real_words = []

        for i in range(0,27):
            decrypted_message = self.apply_shift(26 - i)
            #print(decrypted_message)
            word = ''
            for j in decrypted_message:
                if j in string.ascii_letters:
                    word += j
                if j not in string.ascii_letters or len(word) == len(decrypted_message): ## meaning if j == '' , ! etc or we reach end of string
                    #print(word)
                    if is_word(load_words(WORDLIST_FILENAME),word) == True:
                        #print('word=',word)
                        real_words += 1
                    word = ''
            list_of_real_words.append(real_words)
            real_words = 0

        for i in range(0,len(list_of_real_words)):
            if list_of_real_words[i] == max(list_of_real_words):
                return (26-i,self.apply_shift(26-i))

#text = PlaintextMessage('hello',2)
#new_text = text.get_message_text_encrypted()
#print(new_text)
#print(get_story_string())
#print('--------')
#cipher = CiphertextMessage(new_text)
#print('cipher',cipher.decrypt_message())


if __name__ == '__main__':

#    Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print('-----')
 
#   Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    print('-------')
    

    #TODO: WRITE YOUR TEST CASES HERE

    text2 = PlaintextMessage('Today',3)
    print('Expected Output: Wrgdb')
    print('Actual output:', text2.get_message_text_encrypted())
    print('-------')

    ciphertext2 = CiphertextMessage('Wrgdb')
    print('Expected Output:', (23, 'Today'))
    print('Actual Output:', ciphertext2.decrypt_message())

    #TODO: best shift value and unencrypted story 
    
    story = CiphertextMessage(get_story_string())
    print((story.decrypt_message()))
    
