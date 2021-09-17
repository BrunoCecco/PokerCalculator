#poker bot
import pandas as pd
import itertools
import numpy as np

'''
define array of cards (excluding the jokers and 8-10

define ranks of different card combinations (e.g. poker, full house, triples, pairs)
- to do this, assign a score to each possible combination of cards

scores have range of 11 because the highest card is added onto the base score
e.g. a pair of aces and a pair of kings would have score (24 + 11 = 35)

Highest single card - 2 to 11 
Pair - 12 to 21
Two Pairs - 22 to 31
3 of a Kind - 32 to 41
Straight - 42 to 51
Flush - 52 to 61
Full House - 62 to 71
Four of a Kind - 72 to 81
Straight Flush - 82 to 90
Royal Flush - 91 (80+11)

First round -
1. input your 2 cards
2. calculate current score
3. calculate probability of getting each score from the current hand (use expected/total outcomes)
4. if probability of getting a score > 22 is higher than 50%, output "bet"
5. go to flop 

Flop -
1. input the 3 cards
2. calculate new probability of getting each score with all 5 cards
3. if a probability of getting a score > 22 is higher than 50%, output "bet"

Second flop -
1. input the new card
2. calculate new probability of getting each score with all 6 cards
3. if a probability of getting a score > 22 is higher than 50%, output "bet"

Third flop -
1. input the new card
2. calculate new probability of getting each score with all 7 cards
3. if a probability of getting a score > 22 is higher than 50%, output "bet"

'''

# create array of cards
def initialize_deck():
    numbers = list(range(2, 12)) # ranges from card 2 to ace
    suits = ["H", "S", "D", "C"]
    deck = []
    for i in numbers:
        for j in suits:
           deck.append(str(i)+j)
    return deck


# function to work out possible combinations
def combinations(arr, n):
    arr = np.asarray(arr)
    t = np.dtype([('', arr.dtype)]*n)
    result = np.fromiter(itertools.combinations(arr, n), t)
    return result.view(arr.dtype).reshape(-1, n)


def check_score(cards): # make sure numbers is a sorted array
    letters = [i[1] for i in cards]
    numbers = [int(i[0]) for i in cards]
    score = 0
    
    singles = []
    pairs = []
    triple = []
    quadruple = []
    flush = [] # needs to have 5 string values to be some flush 
    
    # check numbers
    for i in numbers:
        if numbers.count(i) == 4 and i not in quadruple:
            quadruple.append(i)
        elif numbers.count(i) == 3 and i not in triple:
            triple.append(i)
        elif numbers.count(i) == 2 and i not in pairs:
            pairs.append(i)
        elif numbers.count(i) == 1:
            singles.append(i)            

    # check letters (i.e. flush)
    for i in letters:
        if letters.count(i) == 5: 
            flush.append(i)

    # check for possible hand combinations, with highest scoring combs first
    # this way we can use if, elif to get the highest scoring combination for the hand

    # royal and straight flush
    straight = check_straight(numbers)
    if len(flush) == 5 and straight == True: # check for straight flush first         
        if straight == True:
            score = "%.4f" % (80 + numbers[4] + (numbers[3]/10) + (numbers[2]/100) + (numbers[1]/1000) + (numbers[0]/10000))
    elif len(quadruple) == 1: # check for poker (4 of a kind)
        score = "%.1f" % (70 + quadruple[0] + (singles[0]/10))
    
    elif len(pairs) >= 1 and len(triple) == 1: # check for full house
        score = "%.1f" % (60 + triple[0] + (pairs[0]/10))

    elif len(flush) == 5: # check for a flush
        score = "%.4f" % (50 + numbers[4] + (numbers[3]/10) + (numbers[2]/100) + (numbers[1]/1000) + (numbers[0]/10000))

    elif straight == True: # check for a straight
        score = "%.4f" % (40 + numbers[4] + (numbers[3]/10) + (numbers[2]/100) + (numbers[1]/1000) + (numbers[0]/10000))

    elif len(triple) == 1: # check for a triple
        score = "%.2f" % (30 + triple[0] + (singles[1]/10) + (singles[0]/100))

    elif len(pairs) == 2: # check for two pairs        
        score = "%.2f" % (20 + pairs[1] + (pairs[0]/10) + (singles[0]/100))

    elif len(pairs) == 1: # check for a single pair
        score = "%.3f" % (10 + pairs[0] + (singles[2]/10) + (singles[1]/100) + (singles[0]/1000))

    else: # the highest single card
        score = "%.4f" % (numbers[4] + (numbers[3]/10) + (numbers[2]/100) + (numbers[1]/1000) + (numbers[0]/10000))

    return score
    

def check_straight(numbers):
    straight = (numbers == list(range(min(numbers), max(numbers)+1)))
    return straight

def calculate_probabilities(scores, all_outcomes):
    probabilities = {
        "lowscore": 0,
        "TwoPairs": 0,
        "Triple": 0,
        "Straight": 0,
        "Flush": 0,
        "FullHouse": 0,
        "Poker": 0,
        "Straight/RoyalFlush": 0,
    }
    for i in scores:
        if float(i) < 20:
            probabilities["lowscore"] = probabilities.get("lowscore") + (1/all_outcomes)
        elif 20 < float(i) < 32:
            probabilities["TwoPairs"] = probabilities.get("TwoPairs") + (1/all_outcomes)
        elif 30 < float(i) < 42:
            probabilities["Triple"] = probabilities.get("Triple") + (1/all_outcomes)
        elif 40 < float(i) < 52:
            probabilities["Straight"] = probabilities.get("Straight") + (1/all_outcomes)
        elif 50 < float(i) < 62:
            probabilities["Flush"] = probabilities.get("Flush") + (1/all_outcomes)
        elif 60 < float(i) < 72:
            probabilities["FullHouse"] = probabilities.get("FullHouse") + (1/all_outcomes)
        elif 70 < float(i) < 82:
            probabilities["Poker"] = probabilities.get("Poker") + (1/all_outcomes)
        else:
            probabilities["Straight/RoyalFlush"] = probabilities.get("Straight/RoyalFlush") + (1/all_outcomes)
    return probabilities.items()

    
def pre_flop(card1, card2):    
    # ask user for their hole cards
    hole = np.array([str(card1), str(card2)])
    deck.remove(card1)
    deck.remove(card2)
    flop_combs = combinations(deck, 3)
    scores = []
    # calculate probability of each flop combination happening with the two hole cards
    for i in flop_combs: 
        i = np.append(i, hole) # add the hole cards to all the flop combinations
        i = np.sort(i)
        scores.append(check_score(i)) # get score of the current hand i          
    probabilities = calculate_probabilities(scores, len(flop_combs))
    print("Pre-flop probabilities: ", probabilities)

def first_flop(hand):
    hand_score = check_score(hand)
    scores = []
    for i in deck:
        i = np.append(i, hand)
        # get all possible combinations from the next flop card and the current hand
        next_flop_combs = combinations(i, 5) # 6C5 combinations
        for j in next_flop_combs:
            j = np.sort(j)
            scores.append(check_score(j))
    probabilities = calculate_probabilities(scores, len(deck))
    print("On flop probabilities: ", probabilities)
    
    print("Current highest score: ", hand_score)
    
    
    

## main program ##

deck = initialize_deck() 
## pre flop:
## for each possible combination of 3 cards, add them to the whole cards and then calculate their score
## then, calculate probability of each combination happening (expected/total outcomes)
## finally, rank the scores by their probability
card1 = input("Enter first card in the format: '5S' for the 5 of spades ")
card2 = input("Enter second card in the format: '5S' for the 5 of spades ")

pre_flop(card1, card2)

## on flop:
## add the flop and hole cards and check the score
## if score higher than 20, output "bet"
## calculate score and probability of each possible combination of hands for the next flop card
## i.e. there will be 6C5*52 combinations

card3 = input("Enter first flop card in the format: '5S' for the 5 of spades ")
card4 = input("Enter second flop card in the format: '5S' for the 5 of spades ")
card5 = input("Enter third flop card in the format: '5S' for the 5 of spades ")
hand = np.array([card1, card2, card3, card4, card5])

first_flop(hand)









































    




