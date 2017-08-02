import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word = word.lower()
    fcomp = 0

    for char in word:
        if char == '*':
            continue
        fcomp += SCRABBLE_LETTER_VALUES[char]

    scomp = max(7*len(word)-3*(n-len(word)), 1)
    word_score = fcomp*scomp

    return word_score

# print(get_word_score('jar', 7))
# print(get_word_score('c*ws', 3))

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()

# display_hand({'a':1, 'x':2, 'l':3, 'e':1})

def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy()

    for char in word:
        if char in new_hand.keys():
            new_hand[char] -= 1

    return new_hand

# new_hand = update_hand({'j':2, 'o':1, 'l':1, 'w':1, 'n':2}, 'jolly')
# display_hand(new_hand)

word_list = load_words()

def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    vowels = 'aeiou'
    word = word.lower()
    temp_hand = hand.copy()
    wild_pos = word.find('*')

    if wild_pos != -1:
        for v in vowels:
            try_word = word[:wild_pos] + v + word[wild_pos + 1:]
            if try_word in word_list:
                break
            elif v == 'u' and try_word not in word_list:
                return False

    elif word not in word_list:
        return False
    for char in word:
        if char not in temp_hand.keys() or temp_hand[char] == 0:
            return False
        temp_hand[char] -= 1
    return True

#hand = {'r': 2, 'a': 1, 'p': 1, 't': 2, 'e': 1, '*': 1}
#word = 'rapt*re'

#hand = {'a': 1, 'r': 1, 'e': 1, 'j': 2, 'm': 1, '*': 1}
#word = "e*m"

#hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
#word = "h*ney"

#hand = {'c': 1, 'o': 1, '*': 1, 'w': 1, 's':1, 'z':1, 'y': 2}
#word = "c*wz"

#print(is_valid_word(word, hand, word_list))

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {'*':1}
    n -= 1
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand

#  print(deal_hand(7))

def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    hand_len = 0
    for num in hand.values():
        hand_len += num
    return hand_len

# hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
# print(calculate_handlen(hand))

def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """
    total_score = 0  # Keep track of the total score

    while calculate_handlen(hand) > 0: # As long as there are still letters left in the hand:
        print('Current Hand: ', end="")
        display_hand(hand)  # Display the hand
        word = str(input('Enter word, or "!!" to indicate that you are finished:'))  # Ask user for input

        if word == '!!':  # If the input is two exclamation points:
            print('Total score: ', total_score, 'points')
            return total_score  # End the game (break out of the loop)

        elif word != '!!':  # Otherwise (the input is not two exclamation points):
            current_score = get_word_score(word, calculate_handlen(hand))
            if is_valid_word(word, hand, word_list):  # If the word is valid:
                print(word, 'earned', current_score, 'points.', end=" ")  # Tell the user how many points the word earned,
                total_score += current_score
                print('Total:', total_score, 'points')  # and the updated total score
                hand = update_hand(hand, word)  # update the user's hand by removing the letters of their inputted word
            else:  # Otherwise (the word is not valid):
                print('This is not a valid word. Please enter a valid word.')  # Reject invalid word (print a message)
                hand = update_hand(hand, word)  # update the user's hand by removing the letters of their inputted word

        # Game is over (user entered '!!' or ran out of letters),
        # so tell user the total score

    print('Ran out of letters. Total score: ', total_score, 'points')
    return total_score  # Return the total score as result of function

# hand = {'a': 1, 'c': 1, 'f': 1, 'i': 1, '*':1, 't':1, 'x': 1}

# play_hand(hand, word_list)

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    new_letter = random.choice(VOWELS + CONSONANTS)
    sub_hand = hand.copy()

    while new_letter in sub_hand.keys():
        new_letter = random.choice(VOWELS + CONSONANTS)
    value = sub_hand[letter]
    del sub_hand[letter]
    sub_hand[new_letter] = value

    return sub_hand

# substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    num_hands = int(input('Enter total number of hands: '))
    total_score = 0

    for num in range(num_hands):
        current_score1 = 0
        current_score2 = 0
        hand = deal_hand(HAND_SIZE)
        print('Current hand: ', end='')
        display_hand(hand)
        subs = str(input('Would you like to substitute a letter?'))
        if subs == 'yes' or subs == 'y':
            letter = str(input('Which letter would you like to replace? '))
            hand = substitute_hand(hand, letter)
        current_score1 = play_hand(hand, word_list)

        replay = str(input('Would you like to replay the hand? '))
        if replay == 'yes' or replay == 'y':
            current_score2 = play_hand(hand, word_list)
        total_score = total_score + max(current_score1,current_score2)

    return total_score




# play_game(word_list)
