import pygame, sys
from SudokuSolver import solve_sudoku, string_to_integer, integer_to_string, is_valid # importing from SudokuSolver


# the sudoku grid
grid = [
    ["","","","","","","","",""],
    ["","","","","","","","",""],
    ["","","","","","","","",""],
    ["","","","","","","","",""],
    ["","","","","","","","",""],
    ["","","","","","","","",""],
    ["","","","","","","","",""],
    ["","","","","","","","",""],
    ["","","","","","","","",""]
]
# CONSTANTS
WIDTH = 702
HEIGHT = 702
BLACK = (0, 0, 0)

# initialize game
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Sudoku Solver")

# the only valid keys
VALID_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3,
              pygame.K_4, pygame.K_5, pygame.K_6,
              pygame.K_7, pygame.K_8, pygame.K_9,
              pygame.K_TAB, pygame.K_SPACE, pygame.K_BACKSPACE]
GRIDSIZE = 78
GRID_WIDTH = WIDTH // GRIDSIZE
GRID_HEIGHT = HEIGHT // GRIDSIZE

shadow_grid = pygame.Surface((GRIDSIZE, GRIDSIZE))
shadow_grid.fill((200,200,200,10))

base_font = pygame.font.Font(None, 70)

# drawing the 4 lines that make the 3x3 squares
def draw_lines():
    pygame.draw.line(WIN, BLACK, (233, 0), (233, 701), width=2)
    pygame.draw.line(WIN, BLACK, (467, 0), (467, 701), width=2)
    pygame.draw.line(WIN, BLACK, (0, 233), (701, 233), width=2)
    pygame.draw.line(WIN, BLACK, (0, 467), (701, 467), width=2)
    
# drawing the grid(9x9 squares)
def draw_grid():
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(WIN, (150, 150, 150), r)
            else:
                rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(WIN, (255, 255, 255), rr)

# drawing the grid(numbers)
def draw_numbers(grid):
    surf = pygame.Surface(WIN.get_size(), pygame.SRCALPHA).convert_alpha() # creates a clear surface
    r = 0
    for row in grid:
        c = 0
        for cell in row:
            text_surface = base_font.render(cell, True, BLACK).convert_alpha()
            surf.blit(text_surface, (c * GRIDSIZE + 26, r * GRIDSIZE + 20))
            c+=1
        r+=1

    WIN.blit(surf, (0,0))

# shadow the selected grid
def draw_shadow(grid):
    if selected_cell:
        WIN.blit(shadow_grid, (selected_cell[0]*GRIDSIZE, selected_cell[1]*GRIDSIZE))
        


selected_cell = None
# the main function
def main():
    global grid, selected_cell
    run = True
    solved = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # checking for user clicks
            if event.type == pygame.MOUSEBUTTONDOWN and solved == False:
                pos = pygame.mouse.get_pos()
                col = pos[0] // GRIDSIZE
                row = pos[1] // GRIDSIZE
                selected_cell = [col, row]

            # checking for keys pressed
            if event.type == pygame.KEYDOWN and event.key in VALID_KEYS: # the key can only be 1,2,3..9 or TAB
                if event.key == pygame.K_TAB: # if the key is TAB solve the puzzle
                    string_to_integer(grid)
                    solve_sudoku(grid)
                    integer_to_string(grid)
                    solved = True  # don't let the user change the grid anymore

                elif selected_cell != None: # else add to the grid that number
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_SPACE: # spacebar and backspace deletes the number
                        grid[selected_cell[1]][selected_cell[0]] = None
                        selected_cell = None
                    elif is_valid(grid, event.unicode, selected_cell[1], selected_cell[0]): # if the position is valid
                        user_text = event.unicode
                        grid[selected_cell[1]][selected_cell[0]] = user_text
                        selected_cell = None
                    else: # if the event isn't valid
                        selected_cell = None

        # drawing everthing and updating the display
        draw_grid()
        draw_lines()
        draw_numbers(grid)
        draw_shadow(grid)
        
        pygame.display.update()

    # exit routine
    pygame.quit()
    exit()
    
if __name__ == '__main__':
    main()
