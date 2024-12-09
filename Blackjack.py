import random 
playerIn=True
dealerIn=True


#deck of cards 
deck=[2,3,4,5,6,7,8,9,10 , 2,3,4,5,6,7,8,9,10 , 2,3,4,5,6,7,8,9,10 , 2,3,4,5,6,7,8,9,10 ,
      'Jack','Queen','King','Ace' , 'Jack','Queen','King','Ace' , 'Jack','Queen','King','Ace' , 'Jack','Queen','King','Ace']
playerhand=[]
dealerhand=[]

#deal the cards
def deal_Card(turn):
    card = random.choice(deck)
    turn.append(card)
    deck.remove(card)

#calculate the total
def calculate_total(turn):
    total = 0
    face_cards = ['Jack','Queen','King',]
    for card in turn:
        if card in range(1,11):
            total += card
        elif card in face_cards:
            total += 10
        else:
            if total > 11:
                total += 1
            else:
                total += 11
    return total

#check the winner
def revealdealer():
    if len(dealerhand) == 2:
        return dealerhand[0]
    elif len(dealerhand) > 2:
        return dealerhand[0], dealerhand[1]
    

#loop
for _ in range(2):
    deal_Card(dealerhand)
    deal_Card(playerhand)

while playerIn or dealerIn:
    print(f"Dealer has a {revealdealer()} and X")
    print(f"You have a {playerhand} for a total of {calculate_total(playerhand)}")

    if playerIn:
        stayOrHit = input("1: Stay\n2: Hit\n")
    
    if calculate_total(dealerhand) > 16:
        dealerIn = False
    else:
        deal_Card(dealerhand)

    if stayOrHit == "1":
        playerIn = False
    else:
        deal_Card(playerhand)

    if calculate_total(playerhand) >= 21:
        break
    elif calculate_total(dealerhand) >= 21:
        break

    if calculate_total(playerhand) == 21:
        print(f"\nYou have {playerhand} for a total of {calculate_total(playerhand)} and the dealer has {dealerhand} for a total of {calculate_total(dealerhand)}")
        print("Blackjack! You win!")
    elif calculate_total(dealerhand) == 21:
        print(f"\nYou have {playerhand} for a total of {calculate_total(playerhand)} and the dealer has {dealerhand} for a total of {calculate_total(dealerhand)}")
        print("Blackjack! Dealer wins!")

    elif calculate_total(playerhand)>21:
        print(f"\nYou have {playerhand} for a total of {calculate_total(playerhand)} and the dealer has {dealerhand} for a total of {calculate_total(dealerhand)}")
        print("You Bust! Dealer wins!")

    elif calculate_total(dealerhand)>21:
        print(f"\nYou have {playerhand} for a total of {calculate_total(playerhand)} and the dealer has {dealerhand} for a total of {calculate_total(dealerhand)}")
        print("Dealer Bust! You win!")

    elif 21-calculate_total(dealerhand)<21-calculate_total(playerhand):
        print(f"\nYou have {playerhand} for a total of {calculate_total(playerhand)} and the dealer has {dealerhand} for a total of {calculate_total(dealerhand)}")
        print("Dealer wins!")
    elif 21-calculate_total(dealerhand)>21-calculate_total(playerhand):
        print(f"\nYou have {playerhand} for a total of {calculate_total(playerhand)} and the dealer has {dealerhand} for a total of {calculate_total(dealerhand)}")
        print("You win!")

