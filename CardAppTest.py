#
#	Unit tests for the Card and Deck classes
#
\
import unittest
from collections import defaultdict

from CardApp import Color, Card, Deck

class TestCardObject(unittest.TestCase):
	def createCard(self, color, value):
		"""
			Method to create a Card object.  Used for assertraises
			:param color: The card color.
			:param value: The card value.
			:return: the Card object created
		"""
		return Card(color, value)

	def runTests(self):
		"""
			Main method to run the tests.  No parameters.
		"""
		self.testConstructor()
		self.testStr()
		self.testScore()

	def testConstructor(self):
		"""
			Unit test the card constructor.
		"""
		# failures first
		with self.assertRaises(ValueError) as assertEx:
			card = self.createCard(None, 1)
		self.assertEqual(str(assertEx.exception),"color must be specified")
		with self.assertRaises(ValueError) as assertEx:
			card = self.createCard("red", 1)
		self.assertEqual(str(assertEx.exception),"color must be a Color value")
		with self.assertRaises(ValueError) as assertEx:
			card = self.createCard(Color.red, None)
		self.assertEqual(str(assertEx.exception),"value must be specified")
		with self.assertRaises(ValueError) as assertEx:
			card = self.createCard(Color.red, "one")
		self.assertEqual(str(assertEx.exception),"value must be an integer value")
		with self.assertRaises(ValueError) as assertEx:
			card = self.createCard(Color.red, 0)
		self.assertEqual(str(assertEx.exception),"value must be greater than zero")
		with self.assertRaises(ValueError) as assertEx:
			card = self.createCard(Color.red, -1)
		self.assertEqual(str(assertEx.exception),"value must be greater than zero")

		# then success
		card = self.createCard(Color.red, 5)
		self.assertEqual(card.color, Color.red)
		self.assertEqual(card.value, 5)

	def testStr(self):
		"""
			test the __str__ method
		"""
		card = self.createCard(Color.green, 10)
		self.assertEqual(str(card), "color:Colors.green, value: 10")

	def testScore(self):
		"""
			test the getScore method
		"""
		card = self.createCard(Color.red, 5)
		self.assertEqual(card.getScore(), Color.red.value * 5)


class TestDeckObject(unittest.TestCase):
	def createDeck(self, cards):
		"""
			Method to create a Deck object.  Used for assertraises
			:param cards: the list of cards.
			:return: the Deck object created
		"""
		return Deck(cards)

	def createCards(self):
		"""
			Create a list of cards for the deck.  Not implemented as a test setup method so it can
			be called on demand.
			:return: The list of cards
		"""
		cards = []
		for color in Color:
			for val in range(10, 0, -1):
				cards.append(Card(color,val))
		return cards

	def runTests(self):
		"""
			Main method to run the tests.  No parameters.
		"""
		self.testConstructor()
		self.testShuffle()
		self.testDeal()
		self.testSortCards()
		self.testPlayGame()

	def testConstructor(self):
		"""
			Unit test the deck constructor.
		"""
		# failures first
		with self.assertRaises(ValueError) as assertEx:
			deck = self.createDeck(None)
		self.assertEqual(str(assertEx.exception),"cards must be specified")
		with self.assertRaises(ValueError) as assertEx:
			deck = self.createDeck("the cards")
		self.assertEqual(str(assertEx.exception),"cards must be a list")
		with self.assertRaises(ValueError) as assertEx:
			deck = self.createDeck([])
		self.assertEqual(str(assertEx.exception),"the list of cards cannot be empty")
		with self.assertRaises(ValueError) as assertEx:
			deck = self.createDeck([1,2,3,4])
		self.assertEqual(str(assertEx.exception),"the list of cards must contain only Card objects")
		cards = self.createCards()
		cards[10] = 1
		with self.assertRaises(ValueError) as assertEx:
			deck = self.createDeck(cards)
		self.assertEqual(str(assertEx.exception),"the list of cards must contain only Card objects")
		cards = self.createCards()
		# verify that deck.cards contains the same values as the input card list.
		# this is by object, not "value of" the object.
		deck = self.createDeck(cards)
		self.assertEqual(cards, deck.cards)
		# but they are NOT the same list!
		x = cards.pop(0)
		self.assertNotEqual(cards,deck.cards)
		# and that the lengths are what they should be
		self.assertEqual(len(cards),len(deck.cards)-1)

	def testShuffle(self):
		"""
			Test the shuffle method
		"""
		deck = self.createDeck(self.createCards())
		for i in range(5):
			# save the current order of the cards
			save = [card for card in deck.cards]
			deck.shuffle()
			# verify order has changed
			self.assertNotEqual(save, deck.cards)
			# also verify the list sizes are the same
			self.assertEqual(len(save),len(deck.cards))
			# and that all the cards are still present
			for card in save:
				self.assertTrue(card in deck.cards)

	def testDeal(self):
		"""
			Test the deal method
		"""
		deck = self.createDeck(self.createCards())
		with self.assertRaises(ValueError) as assertEx:
			dealt = deck.deal(None)
		self.assertEqual(str(assertEx.exception),"number of cards must be specified")
		with self.assertRaises(ValueError) as assertEx:
			dealt = deck.deal("one")
		self.assertEqual(str(assertEx.exception),"number of cards must be an integer value")
		with self.assertRaises(ValueError) as assertEx:
			dealt = deck.deal(0)
		self.assertEqual(str(assertEx.exception),"number of cards must be greater than zero")
		with self.assertRaises(ValueError) as assertEx:
			dealt = deck.deal(-1)
		self.assertEqual(str(assertEx.exception),"number of cards must be greater than zero")
		# verify that the default deal is one card and that it is the top card
		card = deck.cards[0]
		origLen = len(deck.cards)
		dealt = deck.deal()
		# verify the return is a single element list and the sole element is the first card
		self.assertTrue(type(dealt) == list)
		self.assertEqual(len(dealt), 1)
		self.assertEqual(card, dealt[0])
		# verify that the deck has lost the card
		self.assertEqual(len(deck.cards), origLen-1)
		self.assertTrue(card not in deck.cards)
		# the same for several cards
		cards = deck.cards[0:5]
		origLen = len(deck.cards)
		dealt = deck.deal(5)
		# verify the return is a 5 element list and the elements are the first 5 cards
		self.assertTrue(type(dealt) == list)
		self.assertEqual(len(dealt), 5)
		self.assertEqual(cards, dealt)
		# verify that the deck has lost the cards
		self.assertEqual(len(deck.cards), origLen-5)
		for card in dealt:
			self.assertTrue(card not in deck.cards)
		# verify that we cannot overdraw the deck
		with self.assertRaises(ValueError) as assertEx:
			dealt = deck.deal(len(deck.cards)+1)
		self.assertEqual(str(assertEx.exception),"number of cards is greater than the size of the deck")
		# but we CAN deal the whole deck
		save = deck.cards
		origLen = len(save)
		dealt = deck.deal(len(deck.cards))
		self.assertTrue(type(dealt) == list)
		self.assertEqual(len(dealt), origLen)
		self.assertEqual(len(deck.cards), 0)
		self.assertEqual(save, dealt)

	def testSortCards(self):
		"""
			Test the sortCards method
		"""
		deck = self.createDeck(self.createCards())
		deck.shuffle()
		# a dict to hold the cards broken down by color
		d = defaultdict(list)
		for card in deck.cards:
			d[card.color].append(card)
		
		with self.assertRaises(ValueError) as assertEx:
			sortedCards = deck.sortCards(None)
		self.assertEqual(str(assertEx.exception),"color list must be specified")
		with self.assertRaises(ValueError) as assertEx:
			sortedCards = deck.sortCards("red, yellow, blue")
		self.assertEqual(str(assertEx.exception),"color list must be a list")
		with self.assertRaises(ValueError) as assertEx:
			sortedCards = deck.sortCards([])
		self.assertEqual(str(assertEx.exception),"color list cannot be empty")
		with self.assertRaises(ValueError) as assertEx:
			sortedCards = deck.sortCards([Color.red,"yellow",Color.green])
		self.assertEqual(str(assertEx.exception),"the list of colors must contain only Color values")
		# purposely out of order
		colorList = [Color.red, Color.yellow]
		sortedCards = deck.sortCards(colorList)
		# verify the sorted list contains only red and yellow cards
		self.assertTrue(type(sortedCards) == list)
		self.assertEqual(len(sortedCards), len(d[Color.red]) + len(d[Color.yellow]))
		# verify that all red and yellow cards are in the sorted list
		for card in d[Color.red]:
			self.assertTrue(card in sortedCards)
		for card in d[Color.yellow]:
			self.assertTrue(card in sortedCards)
		# verify we have red cards followed by yellow cards and that each group is subsorted in ascending value
		# order
		idx = 0
		for color in colorList:
			# min card valus is 1
			lastValue = 0
			for i in range(len(d[color])):
				card = sortedCards[idx]
				self.assertEqual(card.color,color)
				self.assertTrue(card.value > lastValue)
				lastValue = card.value
				idx += 1

	def testPlayGame(self):
		"""
			Test the playGame method
		"""
		deck = self.createDeck(self.createCards())
		# we only shuffle the deck in the beginning
		deck.shuffle()
		# test by playing the game multiple times since it's by chance.
		for i in range(3):
			player1Cards,player2Cards,winner = deck.playGame()
			# verify that the returned cards are each a 3 element list and the winner is a string.
			# the winner must be one of 3 values.
			self.assertTrue(type(player1Cards) == list)
			self.assertTrue(type(player2Cards) == list)
			self.assertTrue(type(winner) == str)
			self.assertIn(winner, ["Player 1", "Player 2", "Tie"]) 
			self.assertEqual(len(player1Cards), 3)
			self.assertEqual(len(player2Cards), 3)
			# calculate the score according to the requirements
			score1 = score2 = 0
			for card in player1Cards:
				score1 += card.getScore()
			for card in player2Cards:
				score2 += card.getScore()
			# verify that the winner is truely the player with the highest score
			if (score1 > score2):
				self.assertEqual(winner, "Player 1")
			elif (score1 < score2):
				self.assertEqual(winner, "Player 2")
			else:
				self.assertEqual(winner, "Tie")



if (__name__ == '__main__'):
	test = TestCardObject()
	test.runTests()

	test = TestDeckObject()
	test.runTests()
	


