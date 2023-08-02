import random

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':11,'Queen':12,'King':13,'Ace':14}

class Card():

  def __init__(self,suit,rank):
    self.suit = suit
    self.rank = rank
    self.value = values[rank]

  def __str__(self):
    return self.rank + " of " + self.suit

class Deck():

  def __init__(self):
    
    self.all_cards = []

    for suit in suits:
      for rank in ranks:
        created_card = Card(suit,rank)
        self.all_cards.append(created_card)

  def shuffle(self):
    
    random.shuffle(self.all_cards)

  def deal_one(self):
    return self.all_cards.pop()

class Player():

  def __init__(self,name):

    self.name = name
    self.all_cards = [] # a players current hand

  def remove_one(self):
    return self.all_cards.pop(0)

  def add_cards(self,new_cards):
    if type(new_cards) == type([]):
      self.all_cards.extend(new_cards)
    else:
      self.all_cards.append(new_cards)

  def __str__(self):
    return "{} has {} cards".format(self.name,len(self.all_cards))


# game setup
player_one = Player("Player 1")
player_two = Player("Player 2")

new_deck = Deck()
new_deck.shuffle()

for x in range(26):
  player_one.add_cards(new_deck.deal_one())
  player_two.add_cards(new_deck.deal_one())

game_on = True

round_num = 0
war_rounds = 0
table = [] # cards on the table

# main game loop
while game_on:
  
  #draw cards and add to the table
  player_one_card = player_one.remove_one()
  player_two_card = player_two.remove_one()
  table = [player_one_card, player_two_card]

  # compare cards and, if at_war is false give winner the cards and continue
  # if at_war is true continue to war
  if player_one_card.value > player_two_card.value:
    player_one.add_cards(table)
    at_war = False
  elif player_one_card.value < player_two_card.value:
    player_two.add_cards(table)
    at_war = False
  else:
    at_war = True 
  print("\nRound {} Results:".format(round_num))
  print("{} drew {}".format(player_one.name, player_one_card))
  print("{} drew {}".format(player_two.name, player_two_card))
  print("WAR: {}".format(at_war))

  # nested war loop
  while at_war:
    war_rounds = 1

    # check if either player does not have enough cards for war
    # if a player has < 4 cards, the war cannot be completed
    # the game is over and the winner keeps the cards on the table
    if  len(player_one.all_cards) < 4:
      at_war = False
      player_two.add_cards(table)
      winner = player_two
      break
    if  len(player_two.all_cards) < 4:
      at_war = False
      player_one.add_cards(table)
      winner = player_one
      break

    # both players have enough cards, add six cards to the table
    # draw two more cards, add them to the table and compare
    table.extend([player_one.remove_one(), 
                  player_one.remove_one(), 
                  player_one.remove_one(),
                  player_two.remove_one(), 
                  player_two.remove_one(), 
                  player_two.remove_one()
                  ])
    
    player_one_card = player_one.remove_one()
    player_two_card = player_two.remove_one()
    
    table.extend([player_one_card, player_two_card])

    if player_one_card.value > player_two_card.value:
      player_one.add_cards(table)
      at_war = False
    elif player_one_card.value < player_two_card.value:
      player_two.add_cards(table)
      at_war = False
    else:
      at_war = True
      war_rounds += 1
      
    if at_war==False:
      print("\n\tWAR ATTRITION: {} rounds".format(war_rounds))
      print("\t{} drew {}".format(player_one.name, player_one_card))
      print("\t{} drew {}".format(player_two.name, player_two_card))
      table = []
      war_rounds = 0

  # round is complete
  # print card count for this round
  # check for winner
  # index round number
  print(player_one)
  print(player_two)
  for player in [player_one, player_two]:
    if  len(player.all_cards) == 52:
      game_on = False
      winner = player
  round_num += 1  

# game is over, declare the winner
print("\n\n####### The winner is : {} #######".format(winner.name))
