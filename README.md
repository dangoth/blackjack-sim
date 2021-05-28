# Blackjack strategy simulator

A simulation of Blackjack hands, primarily for testing the dealer bust strategy of going for >= 16, but also for trying to outdo the dealer's 17. Includes a choice of:
* 1-6 players to simulate
* Target value for player hands
* 1-6 decks to be used simultaneously for the games
* Reshuffling of decks upon % deck utilization

Dealer plays a soft 17, i.e. if the dealer's hand includes an ace (11) and the total hand value is 17, the dealer hits. Otherwise it stops at or above 17, as most casinos suggest.


## To be added
* Multiple iterations to be ran at the time, deck reshuffling to be implemented simultaneously
* Multiprocessing to utilize every core

## Changelog

* v0.1.1 - sanitized input, numbered players in endgame screen. leaving prints for future changes
* v0.1 - Working single-iteration run
