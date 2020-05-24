import random
"""DO NOT RUN THIS PROGRAM! RUN OutputGUI.py INSTEAD!"""


def hangman_states(lives):
    if lives == 6:
        print("     ———————"
              "\n     |     |"
              "\n     0     |"
              "\n    -:-    |"
              "\n    ╱ ╲    |"
              "\n   =========")
    elif lives == 5:
        print("     ———————"
              "\n     |     |"
              "\n     0     |"
              "\n    -:-    |"
              "\n    ╱      |"
              "\n   =========")
    elif lives == 4:
        print("     ———————"
              "\n     |     |"
              "\n     0     |"
              "\n    -:-    |"
              "\n           |"
              "\n   =========")
    elif lives == 3:
        print("     ———————"
              "\n     |     |"
              "\n     0     |"
              "\n    -:     |"
              "\n           |"
              "\n   =========")
    elif lives == 2:
        print("     ———————"
              "\n     |     |"
              "\n     0     |"
              "\n     :     |"
              "\n           |"
              "\n   =========")
    elif lives == 1:
        print("     ———————"
              "\n     |     |"
              "\n     0     |"
              "\n           |"
              "\n           |"
              "\n   =========")
    elif lives == 0:
        print(" ╲    ╱                 ╲    ╱"
              "\n  ╲  ╱                   ╲  ╱"
              "\n   ╲╱                     ╲╱"
              "\n   ╱╲                     ╱╲"
              "\n  ╱  ╲                   ╱  ╲"
              "\n ╱    ╲ ——————————————— ╱    ╲")
    elif lives == 10:
        print("                             0000000000000000000000000"
              "\n                        00000000000000000000000000000000000"
              "\n                    0000000000000000000000000000000000000000000"
              "\n                 0000000000000000000000000000000000000000000000000"
              "\n               00000000000000000000000000000000000000000000000000000"
              "\n             000000000000000000000000000000000000000000000000000000000"
              "\n           0000000000000000000000000000000000000000000000000000000000000"
              "\n         00000000000000000000000000000000000000000000000000000000000000000"
              "\n        0000000000000000000000000000000000000000000000000000000000000000000"
              "\n      00000000000000000000000000000000000000000000000000000000000000000000000"
              "\n     0000000000000000000000000000000000000000000000000000000000000000000000000"
              "\n    000000000000000000000000000000000000000000000000000000000000000000000000000"
              "\n   0000000000000000   000000000000000000000000000000000000000   0000000000000000"
              "\n  0000000000000000     0000000000000000000000000000000000000     0000000000000000"
              "\n  000000000000000       00000000000000000000000000000000000       000000000000000"
              "\n 0000000000000000       00000000000000000000000000000000000       0000000000000000"
              "\n 0000000000000000       00000000000000000000000000000000000       0000000000000000"
              "\n00000000000000000       00000000000000000000000000000000000       00000000000000000"
              "\n00000000000000000       00000000000000000000000000000000000       00000000000000000"
              "\n000000000000000000     0000000000000000000000000000000000000     000000000000000000"
              "\n00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
              "\n00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
              "\n00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
              "\n00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
              "\n 000000000000000000000000000000000000000000000000000000000000000000000000000000000"
              "\n 0000000000000000                                                 0000000000000000"
              "\n  000000000000000                                                 000000000000000"
              "\n  0000000000000000                                               0000000000000000"
              "\n   00000000000000000                                           00000000000000000"
              "\n    00000000000000000                                         00000000000000000"
              "\n     000000000000000000                                     000000000000000000"
              "\n      0000000000000000000                                 0000000000000000000"
              "\n        00000000000000000000                           00000000000000000000"
              "\n         00000000000000000000000                   00000000000000000000000"
              "\n           0000000000000000000000000000000000000000000000000000000000000"
              "\n             000000000000000000000000000000000000000000000000000000000"
              "\n               00000000000000000000000000000000000000000000000000000"
              "\n                 0000000000000000000000000000000000000000000000000"
              "\n                    0000000000000000000000000000000000000000000"
              "\n                         00000000000000000000000000000000000"
              "\n                            0000000000000000000000000")


print("Welcome to Hangman!")
con = input("To continue press C: ")
dictionary = open('Dictionary')
full_dictionary = dictionary.readlines()
guess = ""
guesses = []
safe = False
saves = 6
hangman_states(saves)
word = full_dictionary[random.randint(1, 45425)].lower().replace("\n", "")
correct_guesses = list("_" * len(word))
correct_letters = 0

while saves > 0:
    print(" ".join(correct_guesses))
    print("Letters already guessed: " + ", ".join(guesses))
    guess = input("Guess a letter or the full word: ").lower()
    if guess in guesses or not guess.isalpha():
        print("You've already guessed that or what you entered is invalid!")
        continue
    else:
        guesses.append(guess.upper())
        guesses.sort()
    if guess in word and len(guess) == 1:
        safe = True
        for i in range(word.count(guess)):
            index = word.index(guess)
            correct_guesses[index] = guess
            correct_letters += 1
    elif guess == word:
        correct_letters = len(word)
    else:
        saves -= 1
    if correct_letters == len(word):
        hangman_states(10)
        break
    hangman_states(saves)
if saves == 0:
    print("Correct Answer: " + word)
    print("Oh No! You Lost! To play again, rerun the program.")
else:
    print("Hooray! You Won! To play again, rerun the program.")