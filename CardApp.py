from enum import Enum
from random import Random

# an enumeration for the colors.  by default green = 1, yellow = 2, red = 3
Color = Enum("Colors", ("green","yellow","red"))

class Card(object):
	"""
	A playing card with a color and numerical value.
	"""
	def __init__(self, color, value):
		"""
			Card object constructor.

			:param color: The card color.  Mandatory and must be a Color value.
			:param value: The card value.  Mandatory and must be an integer value > 0.
			:return: returns nothing
		"""
		if (color is None):
			raise ValueError("color must be specified")
		if (type(color) != Color):
			raise ValueError("color must be a Color value")
		if (value is None):
			raise ValueError("value must be specified")
		if (type(value) != int):
			raise ValueError("value must be an integer value")
		if (value <= 0):
			raise ValueError("value must be greater than zero")
		
		self.color = color
		self.value = value
	
	def __str__(self):
		"""
			String represntation of a Card including color and value
			:return: the string value
		"""
		return "color:%s, value: %d" % (self.color,self.value)

	def getScore(self):
		"""
			Calulate the score of a Card based on its color and value.
			:return: the score as an integer value
		"""
		return self.color.value * self.value

class Deck(object):
	"""
		A deck of cards
	"""
	def __init__(self, cards):
		"""
			Deck object constructor.

			:param cards: The cards in the deck.  Mandatory and must be a non-empty list of card objects.
			:return: returns nothing
		"""
		if (cards is None):
			raise ValueError("cards must be specified")
		if (type(cards) != list):
			raise ValueError("cards must be a list")
		if (len(cards) == 0):
			raise ValueError("the list of cards cannot be empty")
		for item in cards:
			if (type(item) != Card):
				raise ValueError("the list of cards must contain only Card objects")
		# copy the card list passed in so changes to the list passed in are not reflected in deck.cards
		self.cards = []
		self.cards.extend(cards)
		# used for shuffling, so create it once
		self._random = Random()

	def shuffle(self):
		"""
			Shuffle the cards in the deck, altering the order of the cards in the deck.
			:return: nothing
		"""
		# just use Random.shuffle() to do the work!
		self._random.shuffle(self.cards)

	def deal(self, numberOfCards = 1):
		"""
			Deal one or more cards from the top of the deck, removing them from the deck.
			:param: numberOfCards: Must be an integer value > 0 and cannot exceed the number of cards in the deck.
				Default is one.
			:return: a list of cards dealt even if it is just one card.
		"""
		if (numberOfCards == None):
			raise ValueError("number of cards must be specified")
		if (type(numberOfCards) != int):
			raise ValueError("number of cards must be an integer value")
		if (numberOfCards <= 0):
			raise ValueError("number of cards must be greater than zero")
		if (numberOfCards > len(self.cards)):
			raise ValueError("number of cards is greater than the size of the deck")
		cardsDealt = self.cards[:numberOfCards]
		self.cards = self.cards[numberOfCards:]
		return cardsDealt

	def sortCards(self, colorList):
		"""
			Sort the cards by color and value.  The order of the colors is specified and the value sort is
			by the ascending card value.  The order of the cards in the deck is not changed as the color list 
			may be a subset of the card colors in the deck.
			:param: colorList: The list of colors specifying the order of the colors in the sorted result.
				Mandatory and must be a nonempty list of Color values.
			:return: the sorted list
		"""
		if (colorList is None):
			raise ValueError("color list must be specified")
		if (type(colorList) != list):
			raise ValueError("color list must be a list")
		if (len(colorList) == 0):
			raise ValueError("color list cannot be empty")
		for item in colorList:
			if (type(item) != Color):
				raise ValueError("the list of colors must contain only Color values")
		# the overal sorted list returned
		sortedCards = []
		# a temporary list of cards separated by color in the order determined by colorList
		l = []
		for color in colorList:
			l.append([card for card in self.cards if card.color == color])
		# sort each card in the color specific lists by value, then append that list to the
		# list returned.  the result is a list of cards sorted by color and value
		for sublist in l:
			sortedCards.extend(sorted(sublist, key=lambda card: card.value)) 
		return sortedCards

	def playGame(self):
		"""
			Play a simple game.  2 players, each is dealt a card in turn.  the player with the
			highest score wins.  The score fopr a "hand" is the sum of the scores of the cards
			in the hand.
			:return: a tuple consisting of the first player's hand (a list of cards), that of
				the second player, and a string listing the winner - "Player 1", "Player 2",
				or "Tie"
		"""
		player1Cards,player1Score = [],0
		player2Cards,player2Score = [],0
		for i in range(3):
			player1Cards.extend(self.deal())
			player2Cards.extend(self.deal())
		for card in player1Cards:
			player1Score += card.getScore()
		for card in player2Cards:
			player2Score += card.getScore()
		if (player1Score > player2Score):
			winner = "Player 1"
		elif (player1Score == player2Score):
			winner = "Tie"
		else:
			winner = "Player 2"
		return player1Cards,player2Cards,winner


def runApp():
	"""
		simple functinal test
	"""
	# a list of cards purposely out of order
	cards = []
	for color in Color:
		for val in range(10, 0, -1):
			cards.append(Card(color,val))
	# create the deck
	deck = Deck(cards)
	# sort the cards just by yellow(2) and green(1)
	sortedCards = deck.sortCards([Color.yellow, Color.green])
	for card in sortedCards:
		print(card)
	print("===============")
	# same but by a different color order
	sortedCards = deck.sortCards([Color.red, Color.yellow, Color.green])
	for card in sortedCards:
		print(card)

	# shuffle the deck to randomize the order
	deck.shuffle()

	# play a game.  2 players, each is dealt 3 cards in turn.  the player with the
	# highest score wins
	player1Cards,player2Cards,winner = deck.playGame()
	print("Player 1 cards %s, player2 cards %s, winner %s" % (player1Cards,player2Cards,winner))
	
	

##################################################################################################

if (__name__ == '__main__'):
	runApp()
	

