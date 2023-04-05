# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    n_1 = []
    list_index = 0
    next_letter_index = 0

    if len(sequence) == 1:
        n_1.append(sequence)
        return n_1
    
    
    else:
        n_1  = get_permutations(sequence[0:len(sequence)-1])
        next_letter_index =  len(n_1[0])
     
        while list_index != len(n_1):
            letter = n_1[0]
            
            for i in range(0,len(letter) + 1):           
                new_letter = letter[0:i] + sequence[next_letter_index] + letter[i:]
                n_1.append(new_letter)
                list_index += 1 
            del n_1[0]

        return ( n_1 )
            
        


#print(get_permutations('aeiou'))



if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    example_input = 'yup'
    print('Input:', example_input)
    print('Expected Output:', ['yup', 'ypu', 'uyp', 'upy', 'puy', 'pyu' ])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'ter'
    print('Input:', example_input)
    print('Expected Output:', ['ter', 'tre', 'etr', 'ert', 'ret', 'rte'])
    print('Actual Output:', get_permutations(example_input))

