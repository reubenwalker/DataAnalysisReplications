#Mechanic to choose decks from a pot
import random
n = int(input('How many decks are there?'))
potOrder = list(range(1,(n+1)))
#pO = potOrder
cont = input('Press enter to pull first deck or enter "n" to quit.')
while ((potOrder != []) & (cont.lower() != 'n')):
    deck = str(pO.pop(random.randint(0,len(pO)-1)))
    cont = input('Deck number: ' + deck
                 +', Pull next deck? Press enter or enter "n" to quit.')
    print(deck)

#Numpy alternative
#Mechanic to choose decks from a pot
n = int(input('How many decks are there?'))
potOrder = list(np.random.permutation(range(1,(n+1))))
pO = potOrder
cont = ''
while ((pO != []) & (cont.lower() != 'n')):
    cont = input('Print next deck? Press enter or enter "n" to quit.')
    print('Deck number: ' + str(pO.pop()))

