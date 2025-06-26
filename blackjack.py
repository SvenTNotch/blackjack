import random
import time

INITIAL_HAND_SIZE = 2
DEFAULT_HIT = 1
NUMBER_OF_DECKS = 1
BLACKJACK = 21
DEALER_STOP = 17
DEALER_VISIBLE_CARD = 0.5 #percentage

#CHEATS


deck_1 = {
    "A": 4,
    "2": 4,
    "3": 4,
    "4": 4,
    "5": 4,
    "6": 4,
    "7": 4,
    "8": 4,
    "9": 4,
    "10": 4,
    "J": 4,
    "Q": 4,
    "K": 4
}

deck_values_1 = {
    "A": [1, 11],
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}

winning_values_1 = {
    "BLACKJACK": 2.5,
    "NORMAL": 2
}


def get_bet():
    while True:
        amount = input("How much do you want to loose? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Can't be 0.")
        else:
            print("Must be a number.")
    return amount


def make_deck(deck_count, deck):
    all_cards = []
    for _ in range(deck_count):
        for card, card_count in deck.items():
            for _ in range(card_count):
                all_cards.append(card)
    deck_copy = all_cards[:]
    return deck_copy


def refill_deck(current_deck, number_of_decks, deck):
    if current_deck == []:
            current_deck = make_deck(number_of_decks, deck)
    return current_deck


def hit(hand, usable_deck, number_of_hits):
    for _ in range(number_of_hits):
        usable_deck = refill_deck(usable_deck, NUMBER_OF_DECKS, deck_1)
        random_card = random.choice(usable_deck)
        hand.append(random_card)
        usable_deck.remove(random_card)
    return hand, usable_deck


def initial_hand(initial_hand_size, usable_deck):
    player_hand = []
    player_hand, usable_deck = hit(player_hand, usable_deck, initial_hand_size)
    
    return player_hand, usable_deck


def hit_stay(player_hand, usable_deck, total):
    break_loop = False
    choice = input("To get another card say: 'hit'\nIf you're fine with your hand say: 'stay'\nYour choice: ").lower()
    if choice == "hit":
        player_hand, usable_deck = hit(player_hand, usable_deck, DEFAULT_HIT)
        print(f"Your hand: {player_hand}")
        total = calculate_total(player_hand, deck_values_1)
        print(f"{total}")                    #print(usable_deck) #add cheating system sa skrivenim kodom kada ti da opciju za hit/stay
    elif choice == "stay":
        break_loop = True
    else:
        print("Cmon M8")

    return player_hand, usable_deck, total, break_loop


def dealer_start(initial_hand_size, usable_deck):
    dealer_hand, usable_deck = initial_hand(initial_hand_size, usable_deck)
    dealer_hand_hidden = []
    for card in range(len(dealer_hand)):
        if card + 1 <= len(dealer_hand) * DEALER_VISIBLE_CARD:
            dealer_hand_hidden.append(dealer_hand[card])
        elif card + 1 > len(dealer_hand) * DEALER_VISIBLE_CARD:
            dealer_hand_hidden.append("X")
        else:
            print("Something went wrong.")
    
    return dealer_hand, dealer_hand_hidden, usable_deck


def dealer_play(dealer_hand, dealer_total, usable_deck):
    while True:
        if dealer_total <= DEALER_STOP:
            dealer_hand, usable_deck = hit(dealer_hand, usable_deck, DEFAULT_HIT)
            dealer_total = calculate_total(dealer_hand, deck_values_1)
        else:
            break
    
    return dealer_hand, dealer_total, usable_deck


def calculate_total(player_hand, value):
    total = 0
    aces = 0
    for card in player_hand:
            if card == "A":
                aces += 1
            else:
                total += value.get(card)
    for _ in range(aces):
        if total > BLACKJACK - value.get("A")[1]:
                    total += value.get("A")[0]
        else:
            total += value.get("A")[1]
    return total


def blackjack_bust(total, player_hand, usable_deck):
    player_alive = True
    player_blackjack = False
    while True:
        if total > BLACKJACK:
            print("BUST")
            player_alive = False
            break
        elif total == BLACKJACK:
            player_blackjack = True
            break
        else:
            player_hand, usable_deck, total, break_loop = hit_stay(player_hand, usable_deck, total)
            if break_loop:
                break
    
    return player_hand, usable_deck, total, player_alive, player_blackjack


def check_winnings(player_blackjack, player_alive, bet, player_hand, total, dealer_hand, dealer_total):
    if player_blackjack:
            winnings = bet * winning_values_1.get("BLACKJACK")
            print(f"YOU GOT A BLACKJACK!!!!!!!!!!!!\nWith The hand: {player_hand}")
            print(f"YOU WON: {winnings}$")
    elif player_alive == False:
            print("You busted :(")
            print(f"You lost: {bet}$")
    elif player_alive:
        if dealer_total > BLACKJACK:
            winnings = bet * winning_values_1.get("NORMAL")
            print(f"The dealer busted!")
            print(f"YOU WON: {winnings}$")
        elif dealer_total == BLACKJACK:
            print(f"The dealer got a BLACKJACK!!!!!!!!!!!!\nWith The hand: {dealer_hand}")
            print(f"You lost: {bet}$")
        else:
            print(f"Your hand: {total}")
            print(f"Dealer's hand: {dealer_total}")
            print(f"The dealer's score was higher than yours by: {dealer_total - total}")
            print(f"You lost: {bet}$")



if __name__ == "__main__":
    print()
    dealer_alive = True
    usable_deck = make_deck(NUMBER_OF_DECKS, deck_1)
    while True:
        bet = get_bet()
        if bet == 1000000:
            print("A MILLION DOLLARS")
            break
        print(f"You are betting {bet}$")
        
        player_hand, usable_deck = initial_hand(INITIAL_HAND_SIZE, usable_deck)
        print(f"Your starting hand: {player_hand}")
        total = calculate_total(player_hand, deck_values_1)
        print(f"{total}")
        #print(usable_deck)   #add cheating system sa skrivenim kodom kada te pita za bet
        
        dealer_hand, dealer_hand_hidden, usable_deck = dealer_start(INITIAL_HAND_SIZE, usable_deck)
        #print(f"The dealer's hand: {dealer_hand}") #add cheating system where you see the full dealer hand
        print(f"The dealer's hand: {dealer_hand_hidden}")
        dealer_total = calculate_total(dealer_hand, deck_values_1)
        #print(f"The dealer's total is: {dealer_total}") #add cheating system where you see the full dealer hand
        #print(usable_deck)

        player_hand, usable_deck, total, player_alive, player_blackjack = blackjack_bust(total, player_hand, usable_deck)

        print(f"The dealer's revealed hand: {dealer_hand}")
        dealer_hand, dealer_total, usable_deck = dealer_play(dealer_hand, dealer_total, usable_deck)
        print(f"The final dealer's hand is: {dealer_hand}")
        print(f"The final dealer's hand total is: {dealer_total}")

        check_winnings(player_blackjack, player_alive, bet, player_hand, total, dealer_hand, dealer_total)
        