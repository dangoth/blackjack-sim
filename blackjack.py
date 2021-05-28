from multiprocessing import Process
import os
import random


class Player:

    def __init__(self, target):
        self.score = {"win":0, "lose":0, "draw":0}
        self.hand = []
        self.target = target
        self.playing = False
        self.dealer = False

    def __str__(self):
        return f'{self.score["win"]} wins, {self.score["lose"]} losses and {self.score["draw"]} draws'

    def getScore(self, player):
        return sum(player.hand)

    def drawCard(self, Deck, player):
        choice = random.randint(0, Deck.numCards-1)
        player.hand.append(Deck.cards[choice])
        Deck.cards.pop(choice)
        Deck.numCards -= 1
        print(f"Player's new hand is {player.hand}")

    def dealerDecide(self, player):
        currSum = sum(player.hand)
        print(f"Hand sum in dealer decide function is {currSum}")
        if currSum > 21:
            if 11 in player.hand:
                player.hand[player.hand.index(11)] = 1
                player.dealerDecide(player)
            else:
                player.playing = False
                print("Dealer busted")
                return
        #soft 17 - dealer hits if sum is 17 with ace in hand
        elif currSum == self.target:
            if 11 in player.hand:
                player.hand[player.hand.index(11)] = 1
                print("Dealer decides to hit")
                player.drawCard(deck, player)
                player.dealerDecide(player)
            else:
                print("Dealer decides to stand")
                return
        elif currSum < self.target:
            print("Dealer decides to hit")
            player.drawCard(deck, player)
            player.dealerDecide(player)
        else:
            print("Dealer decides to stand")
            return


    def decide(self, player):
        currSum = sum(player.hand)
        print(f"Hand sum in player decide function is {currSum}")
        if currSum > 21:
            if 11 in player.hand:
                print("Player has an 11, recalculating as 1")
                player.hand[player.hand.index(11)] = 1
                print(f"Should have changed hand, new hand is {player.hand}")
                player.decide(player)
            else:
                player.playing = False
                print("Player busted")
                return
        elif currSum < self.target:
            print("Player decides to hit")
            player.drawCard(deck, player)
            player.decide(player)
        else:
            print("Player decides to stand")
            return


class Deck:

    def __init__(self):
        self.cards = []
        self.numDecks = 0
        self.numCards = 0
        self.percentToShuffle = 0
        self.numCards = 0

    def shuffle(self):
        self.cards = []
        for i in range(self.numDecks):
            self.cards += [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        self.numCards = self.numDecks * 52


class Game:

    def __init__(self):
        self.players = []
        self.playerCount = 0
        self.playerTarget = 0

    def play_game(self, players, deck):
        random.seed()
        if deck.numDecks*52 // deck.numCards < deck.percentToShuffle:
            deck.shuffle()
        for player in self.players:
            player.playing = True
            player.drawCard(deck, player)
            player.drawCard(deck, player)

        for player in self.players[1:]:
            print(f"New player choses, his hand is {player.hand}")
            player.decide(player)

        #dealer
        print("Dealer choses")
        players[0].dealerDecide(player)

        print("Post game evaluation")
        scores = []
        for player in self.players:
            if player.playing:
                scores.append(player.getScore(player))
            else:
                scores.append(0)
        winning = max(scores)
        print(f"Scores are {scores}, winning is {winning}")
        #dealer has the highest score
        if winning == scores[0]:
            if scores.count(scores[0]) == 1:
                print("Dealer wins")
                players[0].score['win'] += 1
            else:
                #dealer drew with 1 or more players
                print("Draw between dealer and 1 or more players")
                for i in range(len(scores)):
                    if scores[i] == 0:
                        continue
                    if scores[i] == scores[0]:
                        players[i].score['draw'] += 1
                    else:
                        players[i].score['lose'] += 1
        #dealer lost
        elif winning > scores[0]:
            print("One or more players won")
            for i in range(len(scores)):
                if scores[i] == 0:
                    continue
                if scores[i] == winning:
                    players[i].score['win'] += 1
                else:
                    players[i].score['lose'] += 1

        for _ in range(len(players)):
            if _ == 0:
                print(f"Dealer has {players[_]}")
            else:
                print(f"Player {_} has {players[_]}")


if __name__ == "__main__":

    def get_int(variable, maximum):
        playerInput = input(f"Select {variable} (1-{maximum}) ")
        try:
            playerInput = int(playerInput)
        except ValueError:
            print("Input must be an integer")
            playerInput = get_int(variable, maximum)
        playerInput = int(playerInput)
        if not 0 < playerInput <= maximum:
            print(f"Value must be between 1-{maximum}")
            playerInput = get_int(variable, maximum)
        return playerInput

    def create_players(playerCount, playerTarget):
        #dealer
        game.players.append(Player(target=17))
        for i in range(game.playerCount):
            game.players.append(Player(game.playerTarget))
        game.players[0].dealer = True

    game = Game()

    game.playerCount = get_int("player count besides the dealer", 6)
    game.playerTarget = get_int("target value (when to stand)", 21)

    create_players(game.playerCount, game.playerTarget)

    deck = Deck()
    deck.numDecks = get_int("number of decks", 6)
    deck.numCards = deck.numDecks * 52
    deck.percentToshuffle = max(40, get_int("percentage of cards left to shuffle the deck", 95))
    deck.shuffle()

    game.play_game(game.players, deck)
