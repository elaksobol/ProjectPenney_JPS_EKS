# ProjectPenney_JPS_EKS

## Explaination of game

### This project is based off of a variation of Penney's Game called the Humble-Nishiyama Randomness Game. 

### Penney's Game is a two player game that was created by Walter Penney. The game involves flipping coins to see if you recieve the heads or tails logo in a sequence. To play, the first player chooses a sequence of three predictions about if the coin will land on heads or tails. An example would be tails, heads, heads (THH). After the first player chooses their combination, the second player will choose their own with the knowledge of the first player's choice. The game will then begin as the players flip a coin until one of their sequences appears. The appearance of such sequence brings the game to a close, with the player who choose the sequence winning. 
### Our interest of this game comes with the fact that it is nontransitive, meaning the second player can always choose to have better odds if they know the first player's choice of sequence. To recieve these better odds, the second player's sequence should be the opposite of the first player's middle choice, and then the first player's first two choices. An example of this is if the first player chooses a sequence that is HTH then the second player must choose HHT to have a better probability of winning.

### The variation, the Humble-Nishiyama Randomness Game, uses cards instead of coins. To do this, the players choose reds or blacks instead of heads or tails. There are two ways to score for this card game. First there is the traditional way, in which all cards are used and if a player's sequence is shown then they recieve a point, also known as a "trick". This game ends when all cards flipped over. The second is the Ron way, in which all cards are used and if a player's sequence is shown they recieve a point per card in the pile that was flipped over. This game also ends when all cards are flipped over. An example of this is when the first player chooses black, black, black and the second player chooses red, black, black. After flipping five cards, the sequence red, black, black appears through cards three, four, and five. If playing the traditional way, the second player recieves one point and the game continues. If playing the Ron way, the second player recieves five points and the game continues. 

## Explain the purpose

### This game has been looked into throughly when using the traditional way. Our purpose of this investigation, is to see how the probabilities change when using the Ron way. 

## "How-to" run the code

### To run the code, the user will open a terminal and add the code from the repository using cd and the path to the downloaded code. After, the user will run main.py which will prompt them to answer a question. This question will offer the user to enter 1, which will allow them to visualize the newest heatmaps, enter 2, which will allow them the user to add and score additional decks (the amount of their choosing), or enter 3, which will allow the user to quit the program. 

## Findings

### After running the code with 2,500,000 decks we realized that by scoring the traditional way there is a greater chance of ties than the Ron way. Our heatmaps show that the highest probability for a tie scored the traditional way is 35% (when the two sequences are RRR and BBB), while the highest probability for a tie scored the Ron way is 4%. (when the two sequences are BBR and RRB). 

### The optimal choice for player one (in our heatmaps shown as Player One) would be the sequences RBR or BRB. This is assuming that player two knows the probabilities and will select a sequence with the best odds after seeing player one's choice. When player one chooses either of these sequences, player two's highest chances of winning are only around 80% while any other choice for player one will allow player two's highest chances of winning to raise to around 88-99% when scoring traditionally. This is the same for Ron's way. When player one chooses either of these sequences, player two's highest chances of winning are only around 92% while any other choice for player one will allow player two's highest chances of winning to raise to around 96-100% when scoring Ron's way.  

### The optimal choice for player two (in our heatmaps shown Player Two) when scoring the traditional way, would be the opposite of player one's second choice, player one's first choice, and player one's first choice. This stays true to the Penney's Game's rules. However, when scoring the Ron way there are two exceptions. If player one chooses RBR, the traditional scoring probabilities show that player two should choose RRB. However, the greatest probability when scoring Ron's way would be if player two chooses BBR (92%) instead of RRB (86%). The same exception 