import pygame
import time
import numpy as np

class BoardGUI:
  def __init__(self, rows, cols):
    print(pygame.__file__)
    self.ROWS = rows
    self.COLS = cols
    self.COUNTERDIAMETER = 50
    # Play are dimensions
    self.PLAYX = 50
    self.PLAYY = 25
    self.PLAYWIDTH = self.COLS * (self.COUNTERDIAMETER + 25) + 25
    self.PLAYHEIGHT = self.ROWS * (self.COUNTERDIAMETER + 25) + 25
    self.COLGAP = (self.PLAYWIDTH - self.COLS * self.COUNTERDIAMETER) / (self.COLS + 1)
    self.ROWGAP = (self.PLAYHEIGHT - self.ROWS * self.COUNTERDIAMETER) / (self.ROWS + 1)
    # Window dimensions
    WINDOWWIDTH = self.PLAYWIDTH + 50 * 2
    WINDOWHEIGHT = self.PLAYHEIGHT + 50 *2
    self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.init()

  def action(self, board):
    while True:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        if event.type == pygame.MOUSEBUTTONUP:
          for col in range(self.COLS):
            refX = self.PLAYX + col * self.COUNTERDIAMETER + (col + 1) * self.COLGAP
            if refX < mouse_x < refX + self.COUNTERDIAMETER:
              return col
      time.sleep(0.5)


  def end_game(self):
    print("Press Space to play again")
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return False
        elif event.type == pygame.KEYUP:
          if event.key == pygame.K_SPACE:
            return True
      time.sleep(0.5)


  def update(self, board):
    # Copy and Flip the board for the purpose of visualisation from top left
    board = np.flipud(board)
    # Fill in the Window and playing frame
    self.DISPLAYSURF.fill((255, 255, 255))
    pygame.draw.rect(self.DISPLAYSURF, (0, 0, 255),
                     (self.PLAYX, self.PLAYY, self.PLAYWIDTH, self.PLAYHEIGHT), 0)
    # Draw the counters
    for row in range(self.ROWS):
      for col in range(self.COLS):
        dcol = int(self.PLAYX + self.COUNTERDIAMETER * col + self.COLGAP * (col + 1) + self.COUNTERDIAMETER / 2)
        drow = int(self.PLAYY + self.COUNTERDIAMETER * row + self.ROWGAP * (row + 1) + self.COUNTERDIAMETER / 2)
        if board[row, col] == 0:
          pygame.draw.circle(self.DISPLAYSURF, (255, 0, 0), (dcol, drow), int(self.COUNTERDIAMETER / 2), 0)
        elif board[row, col] == 1:
          pygame.draw.circle(self.DISPLAYSURF, (255, 255, 0), (dcol, drow), int(self.COUNTERDIAMETER / 2))
        else:
          pygame.draw.circle(self.DISPLAYSURF, (255, 255, 255), (dcol, drow), int(self.COUNTERDIAMETER / 2))
    pygame.display.update()
