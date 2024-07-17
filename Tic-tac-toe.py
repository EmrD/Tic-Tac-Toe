import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("420x350")
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.tree = [self.board, [], []]
        self.win = "Yet_None"
        self.exit_game = False
        self.order = "O"

        self.create_widgets()

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text="", font=('Helvetica', 14, 'bold'))
        self.info_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.root, text="", width=10, height=3, font=('Helvetica', 14, 'bold'),
                                   command=lambda row=i, col=j: self.make_move(row, col))
                row_buttons.append(button)
                button.grid(row=i+1, column=j, padx=5, pady=5)
            self.buttons.append(row_buttons)

    def make_move(self, row, col):
        inpt = row * 3 + col + 1
        if is_free(self.board, inpt):
            self.board, self.tree = play_game(inpt, self.board, self.tree)
            self.update_board()

            if is_finish(self.board):
                self.win = who_win(self.board)
                if self.win == "Yet_None":
                    self.win = "None"
                self.show_result()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                value = self.board[i * 3 + j]
                text = "X" if value == "X" else "O" if value == "O" else ""
                color = "blue" if value == "X" else "red" if value == "O" else "black"
                self.buttons[i][j]["text"] = text
                self.buttons[i][j]["fg"] = color

        if self.win != "Yet_None":
            self.info_label.config(text=f"Win: {self.win}", fg="red")
        else:
            self.info_label.config(text="")

    def show_result(self):
        messagebox.showinfo("Game Over", f"The winner is: {self.win}")
        self.root.destroy()

def is_free(this_board, inpt):
    if this_board[inpt-1] == "X" or this_board[inpt-1] == "O":
        return False
    else:
        return True

def who_win(this_board):
    for i in range(0, 7, 3):
        if (this_board[i] == 'X' and this_board[i+1] == 'X' and this_board[i+2] == 'X') or \
           (this_board[i] == 'O' and this_board[i+1] == 'O' and this_board[i+2] == 'O'):
            return this_board[i+1]

    for i in range(3):
        if (this_board[i] == 'X' and this_board[i+3] == 'X' and this_board[i+6] == 'X') or \
           (this_board[i] == 'O' and this_board[i+3] == 'O' and this_board[i+6] == 'O'):
            return this_board[i+3]

    if (this_board[0] == 'X' and this_board[4] == 'X' and this_board[8] == 'X') or \
       (this_board[0] == 'O' and this_board[4] == 'O' and this_board[8] == 'O'):
        return this_board[4]

    if (this_board[2] == 'X' and this_board[4] == 'X' and this_board[6] == 'X') or \
       (this_board[2] == 'O' and this_board[4] == 'O' and this_board[6] == 'O'):
        return this_board[4]

    return "Yet_None"

def is_finish(this_board):
    if who_win(this_board) == "Yet_None":
        for i in range(9):
            if this_board[i] != "X" and this_board[i] != "O":
                return False
        return True
    else:
        return True

def create_children(board, turn):
    if is_finish(board):
        return []
    tree = []
    for i in range(0, 9):
        board_copy = list(board)
        if board_copy[i] == "X" or board_copy[i] == "O":
            continue
        board_copy[i] = turn
        tree.append(board_copy)
    return list(tree)

def bf_creator(root, turn):
    tree = []
    queue = [(tree, root, turn)]
    tree.append(root)
    while queue != []:
        elem = queue[0]
        queue.remove(elem)
        children = create_children(elem[1], elem[2])
        tmp_turn = "O" if elem[2] == "X" else "X"
        for child in children:
            elem[0].append([child])
            queue.append((elem[0][-1], child, tmp_turn))
    return tree

def leaves(tree):
    last_children = []
    queue = [tree]
    while queue != []:
        elem = queue[0]
        queue.remove(elem)
        if len(elem) == 1:
            last_children.append(elem[0])
        elif len(elem) > 1:
            for child in elem[1:]:
                queue.append(child)
    return last_children

def probability(this_tree):
    probabilities = []
    for i in this_tree[1:]:
        all_leaves = leaves(i)
        count = 0
        for leaf in all_leaves:
            if who_win(leaf) == "X":
                count -= 100
            elif who_win(leaf) == "O":
                count += 1

        not_append = False
        if probabilities != []:
            for a in i[1:]:
                if who_win(a[0]) == "X" and probabilities != []:
                    not_append = True
                    break

        if not_append == False:
            probabilities.append([count/len(all_leaves), i[0]])
    return probabilities

def play_ai(this_tree, board):
    bigger = []
    for i in probability(this_tree):
        if bigger == []:
            bigger = i
        elif i[0] > bigger[0]:
            bigger = i
    return bigger[1]

def play_game(inpt, board, tree):
    board[inpt-1] = "X"
    if is_finish(board) == False:
        play_len = 0
        for i in range(0, 9):
            if board[i] == "X" or board[i] == "O":
                play_len += 1
        if play_len <= 1:
            tree = bf_creator(board, "O")
        else:
            for j in tree[1:]:
                for i in j[1:]:
                    if i[0] == board:
                        tree = i
                        break
        board = play_ai(tree, board)
    return board, tree

if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()
