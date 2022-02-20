#Mechanic to choose decks from a pot
import random
numDecks = int(input('How many decks are there?'))
potOrder = list(range(1,(numDecks+1)))
#pO = potOrder
cont = input('Press enter to pull first deck or enter "n" to quit.')
while ((potOrder != []) & (cont.lower() != 'n')):
    deck = str(potOrder.pop(random.randint(0,len(potOrder)-1)))
    cont = input('Deck number: ' + deck
                 +', Pull next deck? Press enter or enter "n" to quit.')

