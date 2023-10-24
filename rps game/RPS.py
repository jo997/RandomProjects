import pygame
import random

# Instructions
print("Welcome to Rock, Paper, Scissors!")
print("Press 'r' for Rock, 'p' for Paper, and 's' for Scissors.")
print("Press 'q' to quit.\n")

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_SIZE = (800, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Rock, Paper, Scissors")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (0, 0, 255)

# Load images
rock_img = pygame.image.load('rock.png')
paper_img = pygame.image.load('paper.png')
scissors_img = pygame.image.load('scissors.png')

# Define choices and corresponding images
CHOICES = ['Rock', 'Paper', 'Scissors']
CHOICE_IMAGES = {
    'Rock': rock_img,
    'Paper': paper_img,
    'Scissors': scissors_img
}

# Initialize win counters
player_wins = 0
computer_wins = 0

def draw_text(text, font, color, surface, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        textobj = font.render(line, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y + i * 30)
        surface.blit(textobj, textrect)

def user_choice():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'Rock'
                elif event.key == pygame.K_p:
                    return 'Paper'
                elif event.key == pygame.K_s:
                    return 'Scissors'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def computer_choice():
    return random.choice(CHOICES)

def determine_winner(user, computer):
    global player_wins, computer_wins
    
    if user == computer:
        return "It's a tie!"
    elif (user == 'Rock' and computer == 'Scissors') or (user == 'Paper' and computer == 'Rock') or (user == 'Scissors' and computer == 'Paper'):
        player_wins += 1
        return "You win!"
    else:
        computer_wins += 1
        return "Computer wins!"

def main():
    global player_wins, computer_wins
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        WINDOW.fill(WHITE)
        
        user = user_choice()
        comp = computer_choice()

        draw_text("Your Choice:", font, BLACK, WINDOW, 50, 50)
        draw_text("Computer's Choice:", font, BLACK, WINDOW, 450, 50)
        
        WINDOW.blit(CHOICE_IMAGES[user], (50, 100))
        WINDOW.blit(CHOICE_IMAGES[comp], (450, 100))

        result = determine_winner(user, comp)
        draw_text(result, font, FONT_COLOR, WINDOW, 300, 300)
        
        draw_text(f"Player Wins: {player_wins}", font, FONT_COLOR, WINDOW, 50, 500)
        draw_text(f"Computer Wins: {computer_wins}", font, FONT_COLOR, WINDOW, 450, 500)
        draw_text("Just press R, P or S to play the game. Q to exit.", font, BLACK, WINDOW, 50, 530)
        
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()