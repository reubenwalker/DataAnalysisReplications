import random
import numpy as np
#Numpy alternative
#Mechanic to choose decks from a pot
numDecks = int(input('How many decks are there?'))
potOrder = list(np.random.permutation(range(1,(numDecks+1))))
cont = ''
while ((potOrder != []) & (cont.lower() != 'q')):
    cont = input('Print next deck? Press enter or enter "q" to quit.\n')
    if(cont.lower() == 'q'):
        print('Have fun!')
        break
    print('Deck number: ' + str(potOrder.pop()))
    if(potOrder == []):
        print("That's all the decks!")
    
