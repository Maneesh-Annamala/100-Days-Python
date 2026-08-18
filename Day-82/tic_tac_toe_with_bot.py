import random
board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
def game_board():
    for i in range(5):

        if i % 2 == 0:
            print(f"{board[i//2][0]} | {board[i//2][1]} | {board[i//2][2]}")

        else:
            print("---+---+---")

def winner_check():
    #rows
    if board[0][0] != " " and board[0][0] == board[0][1] == board[0][2]:
        value = board[0][0]
        return value

    elif board[1][0] != " " and board[1][0] == board[1][1] == board[1][2]:
        value = board[1][0]
        return value

    elif board[2][0] != " " and board[2][0] == board[2][1] == board[2][2]:
        value = board[2][0]
        return value

    #columns
    elif board[0][0] != " " and board[0][0] == board[1][0] == board[2][0]:

        return board[0][0]
    
    elif board[0][1] != " " and board[0][1] == board[1][1] == board[2][1]:
        return board[0][1]
    
    elif board[0][2] != " " and board[0][2] == board[1][2] == board[2][2]:
        return board[0][2]

    #diagonals
    elif board[0][0] != " " and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    elif board[0][2] != " " and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

def board_full():
    for row in board:
        for cell in row:
            if cell == " ":
                return False

    return True

def computer_choice():
    choose = [0,1,2]
    choosed = random.choice(choose)
    return choosed


def game():
    
    while True:
        game_board()
        print("Player move")
        try:
            player_row = int(input("Choose the row from 1-3: "))-1
            player_column = int(input("choose the column from 1-3: "))-1
        except ValueError:
            print("Enter only numbers")
            continue
        if player_row < 0 or player_row > 2 or player_column < 0 or player_column > 2:
            print("You choosed out of the box.Please choose values that suits the sizw of box(1-3)")
            continue
        if board[player_row][player_column] == " ":
            board[player_row][player_column] = "x"
        else:
            print("That place is occupied choose another one")
            continue
        if board_full():
            print("Its a Draw")
            return
        returned_value = winner_check()
        if returned_value:
            print("Player won the gamme")
            return
        
        #computer move
        print("\n"*30)
        game_board()
        print("Computer move")
        computer_row = computer_choice()
        computer_column = computer_choice()
        while board[computer_row][computer_column] != " ":
            computer_row = computer_choice()
            computer_column = computer_choice()
        board[computer_row][computer_column] = "o"
        is_computer = winner_check()
        if is_computer:
            print("Computer won the game")
            return
        print("\n"*30)

if __name__ == "__main__":
    game()
        

