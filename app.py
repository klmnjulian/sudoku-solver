from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static')

# Sudoku solver functions
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        # set row and col to the values of an empty field
        row, col = find

    # loop through 1-9
    for i in range(1, 10):
        # checks if the number i is valid for the pos (row, col)
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True
            
            bo[row][col] = 0
    
    return False

def valid(bo, num, pos):
    # checks the row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    
    # checks the column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
        
    # check 3x3 box using integer division
    # Boxes:
    # [[0], [1], [2],
    #  [3], [4], [5],
    #  [6], [7], [8]]

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get Sudoku board from form input
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = request.form.get(f'cell-{i}-{j}')
                if value:
                    board[i][j] = int(value)
                else:
                    board[i][j] = 0

        # Solve the Sudoku puzzle
        solve(board)

        # Render template with solved Sudoku
        return render_template('index.html', board=board, solved=True)

    # Render template with empty Sudoku board
    return render_template('index.html', board=None, solved=False)

if __name__ == '__main__':
    app.run(debug=True)
