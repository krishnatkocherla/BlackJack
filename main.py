# Created in PyCharm with Python using the Pygame library

# Image Credits:
# Card png images from "https://code.google.com/archive/p/vector-playing-cards/"
# Back of card png image from "http://clipart-library.com/clipart/8cEbeEMLi.htm"

# importing libraries
import pygame
import random
import os
import sys
pygame.init()


# creating & shuffling list of cards
# all card images are stored in a list called deck, which is in the same folder as the code
# os.listdir() puts all of the names of the files in the argument into a list
# the order of the list is then randomized, simulating the shuffling of the deck
# this allows the list, cards, to represent a deck of cards that is freshly shuffled
cards = os.listdir("deck")
random.shuffle(cards)
index_to_rank = {}


# storing value of cards in game based on index
for card in range(len(cards)):
    for value in range(2, 11):
        if str(value) in cards[card]:
            index_to_rank[card] = value
            break
    if "ace" in cards[card]:
        index_to_rank[card] = 1
    elif card not in index_to_rank:
        index_to_rank[card] = 10


# loading & resizing dealt cards
back = pygame.image.load("back.png")
back = pygame.transform.scale(back, (100, 140))
for i in range(len(cards)):
    cards[i] = pygame.image.load("deck/"+cards[i])
    cards[i] = pygame.transform.scale(cards[i], (100, 140))
player_cards = []
player_cards.extend((cards[2], cards[3]))
card_to_place = {
    2: (550, 700),
    3: (750, 700),
    4: (350, 700),
    5: (950, 700),
    6: (150, 700),
    7: (850, 500),
    8: (250, 500),
    9: (1050, 500),
    10: (50, 500)
}

# number of dealer points (ace can be 1 or 11; whichever is advantageous)
if index_to_rank[0] == 1:
    if index_to_rank[1] == 1:
        dealerSum = 12
    else:
        dealerSum = 11 + index_to_rank[1]
if index_to_rank[1] == 1:
    dealerSum = 11 + index_to_rank[0]
else:
    dealerSum = index_to_rank[0] + index_to_rank[1]

# game window
screen = pygame.display.set_mode((1300, 900))
pygame.display.set_caption("Blackjack")
running = True
allow_press = False

# instructions to display
font = pygame.font.Font('freesansbold.ttf', 20)
font2 = pygame.font.Font('freesansbold.ttf', 20)
text = font.render("Hit to gain a random card to get as close to 21 as possible without going over. When you are done stand.", True, (0, 0, 0))
text2 = font2.render("All cards are face value. Face cards are 10. Aces are 1 or 11. Click H to hit and S to stand", True, (0, 0, 0))
textRect = text.get_rect()
textRect2 = text2.get_rect()
textRect.center = (600, 50)
textRect2.center = (600, 100)


# display_cards is a function for continuously displaying cards on the screen
# no value is returned
# the argument dealer_display is boolean whether to display the dealer's hidden card
def display_cards(dealer_display):
    screen.blit(cards[2], (450, 500))
    screen.blit(cards[3], (650, 500))
    if dealer_display:
        screen.blit(cards[0], (450, 150))
        screen.blit(cards[1], (650, 150))
    for player_card in range(2, len(player_cards)):
        screen.blit(cards[player_card+2], (card_to_place[player_card]))


# player_points returns points as list of all possible points (all ace configurations possible)
# a list of integers is returned
# both arguments are integers
def player_points(num_of_aces, count_of_player):
    all_counts = [count_of_player]
    if num_of_aces == 1:
        if (all_counts[0] + 11) > 21:
            all_counts[0] += 1
        else:
            all_counts[0] += 1
            all_counts.append(all_counts[0] + 10)
    if num_of_aces == 2:
        if (all_counts[0] + 12) > 21:
            all_counts[0] += 2
        else:
            all_counts[0] += 2
            all_counts.append(all_counts[0] + 10)
    if num_of_aces == 3:
        if (all_counts[0] + 13) > 21:
            all_counts[0] += 3
        else:
            all_counts[0] += 3
            all_counts.append(all_counts[0] + 10)
    if num_of_aces == 4:
        if (all_counts[0] + 14) > 21:
            all_counts[0] += 4
        else:
            all_counts[0] += 4
            all_counts.append(all_counts[0] + 10)
    return all_counts


# compare_counts checks if the player hit over 21, if not it compares the points of the player to that of the dealer.
# no value is returned
# "player_counts" is a list of integers and stand is a boolean variable
def compare_counts(player_counts, stand):
    bust = True
    max_count = 0
    for count in player_counts:
        if count < 22:
            bust = False
            max_count = max(max_count, count)
    if bust is True:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Your count is greater than 21. You lose!", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (650, 450)
        screen.blit(text, textRect)
        display_cards(True)
        pygame.display.update()
        pygame.time.wait(3000)
        sys.exit()
    if max_count == 21:
        global dealerSum
        if dealerSum < 21:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render("You have 21. You Win!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (650, 450)
            screen.blit(text, textRect)
            display_cards(True)
            pygame.display.update()
            pygame.time.wait(3000)
            sys.exit()
        else:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render("You and the dealer have 21. Tie!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (650, 450)
            screen.blit(text, textRect)
            display_cards(True)
            pygame.display.update()
            pygame.time.wait(3000)
            sys.exit()
    else:
        if stand:
            if max_count > dealerSum:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render("You beat the dealer. You win!", True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (650, 450)
                screen.blit(text, textRect)
                display_cards(True)
                pygame.display.update()
                pygame.time.wait(3000)
                sys.exit()
            if max_count < dealerSum:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render("The dealer beat you. You lose!", True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (650, 450)
                screen.blit(text, textRect)
                display_cards(True)
                pygame.display.update()
                pygame.time.wait(3000)
                sys.exit()
            if max_count == dealerSum:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render("You and the dealer have the same count. Tie!", True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (650, 450)
                screen.blit(text, textRect)
                display_cards(True)
                pygame.display.update()
                pygame.time.wait(3000)
                sys.exit()


# the name of the procedure is "stand_or_hit"
# the procedure takes the key the player presses as an input
# the procedure does not return any value
def stand_or_hit(key_pressed):
    if key_pressed != pygame.K_h and key_pressed != pygame.K_s:
        return
    ace_count = 0
    player_sums = [0]
    if key_pressed == pygame.K_h:
        player_cards.append(cards[len(player_cards) + 2])
    for player_card in range(2, len(player_cards) + 2):
        if index_to_rank[player_card] == 1:
            ace_count = ace_count + 1
        else:
            player_sums[0] += index_to_rank[player_card]
    player_sums = player_points(ace_count, player_sums[0])
    if key_pressed == pygame.K_h:
        compare_counts(player_sums, False)
    if key_pressed == pygame.K_s:
        compare_counts(player_sums, True)


initial = True
init_ace_count = 0
while running:
    screen.fill("#35654d")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if allow_press and event.type == pygame.KEYDOWN:
            allow_press = False
            # calls student developed procedure "stand_or_hit" that takes the key pressed as the argument
            stand_or_hit(event.key)
    # displaying cards & text
    screen.blit(cards[0], (450, 150))
    screen.blit(back, (650, 150))
    display_cards(False)
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
    pygame.display.update()
    if initial:
        initial = False
        if index_to_rank[2] == 1:
            if index_to_rank[3] == 10:
                compare_counts([21], True)
        elif index_to_rank[3] == 1:
            if index_to_rank[2] == 10:
                compare_counts([21], True)
    allow_press = True
