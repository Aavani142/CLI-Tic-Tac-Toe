from typing import List, Optional, Tuple

# board positions: list of 9 elements, each "X", "O", or " " (space)
def print_board(board: List[str]) -> None:
    """Prints the board in a human-friendly 3x3 layout."""
    def cell(i):
        return board[i] if board[i] != " " else str(i+1)
    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()

def available_moves(board: List[str]) -> List[int]:
    return [i for i, v in enumerate(board) if v == " "]

def winner(board: List[str]) -> Optional[str]:
    wins = [
        (0,1,2), (3,4,5), (6,7,8),  # rows
        (0,3,6), (1,4,7), (2,5,8),  # cols
        (0,4,8), (2,4,6)            # diags
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return None

def is_draw(board: List[str]) -> bool:
    return " " not in board and winner(board) is None

def minimax(board: List[str], depth: int, is_maximizing: bool, ai_player: str, human_player: str) -> Tuple[int, Optional[int]]:
    """
    Minimax returns tuple (score, move_index)
    score: positive if ai_player is winning, negative if human is winning
    We include depth to prefer faster wins / slower losses.
    """
    win = winner(board)
    if win == ai_player:
        return 10 - depth, None
    if win == human_player:
        return depth - 10, None
    if is_draw(board):
        return 0, None

    if is_maximizing:
        best_score = -999
        best_move = None
        for move in available_moves(board):
            board[move] = ai_player
            score, _ = minimax(board, depth+1, False, ai_player, human_player)
            board[move] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = 999
        best_move = None
        for move in available_moves(board):
            board[move] = human_player
            score, _ = minimax(board, depth+1, True, ai_player, human_player)
            board[move] = " "
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move

def ai_move(board: List[str], ai_player: str, human_player: str) -> int:
    """Choose best move for the AI using minimax."""
    _, move = minimax(board, 0, True, ai_player, human_player)
    # `move` should never be None here unless board is terminal
    return move if move is not None else available_moves(board)[0]

def human_turn(board: List[str], human_player: str) -> None:
    """Ask human for a move and place it."""
    while True:
        raw = input("Enter your move (1-9): ").strip()
        if raw.lower() in ("q","quit","exit"):
            print("Exiting game.")
            exit(0)
        if not raw.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        pos = int(raw) - 1
        if pos < 0 or pos > 8:
            print("Number must be between 1 and 9.")
            continue
        if board[pos] != " ":
            print("That cell is already taken. Choose another.")
            continue
        board[pos] = human_player
        break

def play():
    print("Tic-Tac-Toe vs Unbeatable AI (Minimax)")
    print("Board positions:")
    print_board([str(i+1) for i in range(9)])
    # Choose symbols
    human_player = ""
    while human_player not in ("X","O"):
        human_player = input("Choose your symbol (X/O). X goes first: ").strip().upper() or "X"
        if human_player not in ("X","O"):
            print("Please type X or O.")
    ai_player = "O" if human_player == "X" else "X"

    
    turn = "human" if human_player == "X" else "ai"
    print(f"You are {human_player}. AI is {ai_player}. {('You' if turn=='human' else 'AI')} goes first.")

    while True:
        board = [" "] * 9
        game_over = False
        current = turn

        while not game_over:
            print_board(board)
            if current == "human":
                human_turn(board, human_player)
            else:
                print("AI is thinking...")
                move = ai_move(board, ai_player, human_player)
                board[move] = ai_player
            
            w = winner(board)
            if w:
                print_board(board)
                if w == human_player:
                    print("You win! 🎉")
                else:
                    print("AI wins. Better luck next time.")
                game_over = True
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw.")
                game_over = True
                break
            current = "ai" if current == "human" else "human"

        
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y","yes"):
            print("Thanks for playing.")
            break
       
        first = input("Who goes first next game? (you/ai/auto) [auto]: ").strip().lower()
        if first == "you":
            turn = "human"
        elif first == "ai":
            turn = "ai"
        else:
            
            turn = "ai" if turn == "human" else "human"

if __name__ == "__main__":
    play()
