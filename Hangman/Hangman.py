hangman1={6:'''
        ____________
         |''',
        5:'''
        ____________
         |
         O''',
        4:'''
        ____________
         |
         O
        /''',
        3:'''
        ____________
         |
         O
        / \\''',
        2:'''
        ____________
         |
         O
        / \\
         |''',
        1:'''
        ____________
         |
         O
        / \\
         |
        /''',
        0:'''
        ____________
         |
         O
        / \\
         |
        / \\ '''}




import random

print('Welcome to Hangman Game designed by Grace\n')

#my level words -word list contains my hard words and easy list contains my easy words

word = ['SECRETARIAT', 'DANGEROUSLY', 'FURIOUSLY', 'MISTAKENLY', 'HEADPHONES', 'KEYBOARDIST', 'TELEPHONEE', 'DEVELOPMENT', 'REGRESSION', 'CLASSIFICATION', 
        'AIRPLANES', 'DUSSELDORF', 'BAVARIA', 'COMPUTERS', 'TELEVISION', 'WILDERNESS', 'MONITORING', 'PORTFOLIO', 'GARDEROBENSTÄNDER', 'ENVIRONMENT', 
        'BATTERY', 'ANGELINA', 'MANCHESTER', 'LIVERPOOL', 'FOOTBALL', 'AUSTRALIA', 'TANZANIA', 'RWANDA', 'MALAYSIA', 'PROGRAMMING']

easy = ['BEARD', 'MAYBE', 'PENCIL', 'TABLE', 'BOOTCAMP', 'ANDRIOD', 'CAMERA', 'FEEDBACK', 'MEETING']


while True:

  #my error messages
  error = '\u26A0 Invalid Letter \u26A0\n'
  used_message = '\u26A0 The letter is already chosen! Pick another one \u26A0\n'
  wrong_length = '\u26A0 Invalid input! Enter only one letter \u26A0\n'

  used_letters = []
  play = input('\nAre you ready to play? Yes or No: ')
  level  = input('\nChoose a level.\nEnter 1 for easy\nEnter 2 for advanced: ')

#level choosing
  if level == '1':
    words = random.choice(easy)
    mistake_count = 6
    print(f'\nYou have only {mistake_count} guesses')

  elif level == '2':
    words = random.choice(word)
    mistake_count = 4
    print(f'\nYou have only {mistake_count} guesses')
  else:
    print('Invalid Choice. Choose 1 or 2')

  hidden_word = '-' * len(words)
  hidden_word = list(hidden_word)



  if play.lower().startswith('y'):
    game_on = True
  else:
    break

  print('\nHidden word is {}\n'.format(''.join(hidden_word)))

  while game_on:

    while mistake_count > 0 and '-' in hidden_word:

      picked_letter = input('Please guess a letter: ').upper()

# my checkpoints for my inputed letter
      if picked_letter.isalpha() == False:
        print(error)
        continue

      if len(picked_letter) > 1:
        print(wrong_length)
        continue

      if picked_letter in used_letters:
        print(used_message)

      else:
        used_letters.append(picked_letter)


#my code for comparing the inputed letter to the secret word


      if words.count(picked_letter) > 0 and picked_letter in words:
        print(f'Correct! The word contains the letter {picked_letter}')

      else:
        mistake_count -= 1
        print(f'WRONG!! Number of Guess left: {mistake_count}')
        print(hangman1[mistake_count])

      for index, letter in zip(range(len(hidden_word)), words):
        hidden_word = list(hidden_word)
        if picked_letter == letter and picked_letter in words:
          hidden_word[index] = picked_letter

      hidden_word = ''.join(hidden_word)
      print(f'{hidden_word}\n')
      print('===============================================================\n')




    if mistake_count == 0 or '-' not in hidden_word:
      if '-' not in hidden_word:
        print(f'CONGRATULATIONS, YOU WON\U0001F3C5\n')
      else:
        print(f'\U0001F480 GAME IS LOST, YOU ARE HANGED \U0001F480 \nTHE WORD IS {words}\n')
    break

  play_again = input('Do you want to play again? Yes or No: ')

  if play_again.startswith('y') == True:
    continue
  else:
    break

