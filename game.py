import pygame
import random

pygame.init()

# -------------------------
# Window + fonts + clock
# -------------------------


WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

FONT = pygame.font.SysFont("Selima", 36)
SMALL = pygame.font.SysFont("Selima", 24)
clock = pygame.time.Clock()

# -------------------------
# Colors (change these)
# -------------------------
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
CORAL = (255, 127, 80)
PINK = (255, 170, 200)
PURPLE = (180, 120, 255)
BLUE = (120, 180, 255)
YELLOW = (255, 220, 100)
MINT = (150, 255, 220)
GREEN = (120,255,150)
BG_COLOR = PURPLE  # background color for scenes

# -------------------------
# Words / categories
# -------------------------
categories = {
    "Animals": ["Dog", "Cat", "Lion", "Tiger", "Elephant", "Giraffe", "Zebra", "Kangaroo", "Panda", 
               "Monkey", "Fox", "Wolf", "Deer", "Bear", "Dolphin", "Whale", "Eagle", "Owl", "Snake", "Rabbit"],

    "Movies": ["Sholay", "Dilwale Dulhania Le Jayenge", "Kabhi Khushi Kabhie Gham", "3 Idiots"," Dangal", "Lagaan", "Taare Zameen Par", 
               "Bajrangi Bhaijaan", "Chennai Express","PK", "Andaz Apna Apna", "Bahubali", "Om Shanti Om", "Barfi",
                  "Zindagi Na Milegi Dobara", "Gully Boy", "Queen", "Padmaavat", "Chak De India", "Rockstar"],

    "Objects":["Chair", "Table", "Lamp", "Book", "Pen", "Phone", "Mug", "Backpack", "Watch", "Glass", "Pillow", "Key",
                       "Bottle", "Wallet", "Notebook", "Fan", "Shoe", "Remote", "Camera", "Umbrella"]
}

# -------------------------
# Game state variables
# -------------------------

state = "menu"   # "menu", "categories", "game"
selected_category = None
word = ""
display = []
guessed = set()
max_lives = 6
lives = max_lives

# -------------------------
# Utility drawing functions
# -------------------------

def draw_text(text, font, color, x, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))
    return surf

def center_text(text, font, color, cx, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (cx - surf.get_width()//2, y))
    return surf

# draw a rounded rectangle button and return its rect
def draw_button(text, x, y, w, h, color, hover_color, text_color=WHITE):
    mx, my = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mx, my)
    pygame.draw.rect(screen, hover_color if is_hover else color, rect, border_radius=12)
    txt = FONT.render(text, True, text_color)
    screen.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))
    return rect

# -------------------------
# Hangman drawing (visible)
# -------------------------


def draw_hangman(current_lives):
    base_col = WHITE
    # stand
    pygame.draw.line(screen, base_col, (150, 500), (350, 500), 6)
    pygame.draw.line(screen, base_col, (250, 500), (250, 150), 6)
    pygame.draw.line(screen, base_col, (250, 150), (400, 150), 6)
    pygame.draw.line(screen, base_col, (400, 150), (400, 200), 6)

    # small bounce animation for head/body
    offset = int((pygame.time.get_ticks() % 50) / 10)  # 0..4

    wrong = max_lives - current_lives
    if wrong >= 1:
        pygame.draw.circle(screen, base_col, (400, 230 + offset), 30, 4)  # head
    if wrong >= 2:
        pygame.draw.line(screen, base_col, (400, 260 + offset), (400, 340 + offset), 4)  # body
    if wrong >= 3:
        pygame.draw.line(screen, base_col, (400, 280 + offset), (360, 310 + offset), 4)  # left arm
    if wrong >= 4:
        pygame.draw.line(screen, base_col, (400, 280 + offset), (440, 310 + offset), 4)  # right arm
    if wrong >= 5:
        pygame.draw.line(screen, base_col, (400, 340 + offset), (370, 380 + offset), 4)  # left leg
    if wrong >= 6:
        pygame.draw.line(screen, base_col, (400, 340 + offset), (430, 380 + offset), 4)  # right leg

# -------------------------
# Helpers to start/reset game
# -------------------------

def start_game(category_name):
    global selected_category, word, display, guessed, lives, state
    selected_category = category_name
    word = random.choice(categories[category_name]).lower()
    display = ["_" for _ in word]
    guessed = set()
    lives = max_lives
    state = "game"

# -------------------------
# Main loop
# -------------------------

running = True
while running:
    screen.fill(BG_COLOR)

    # event handling (single loop, handles everything)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # mouse clicks: check current state's buttons after we draw them
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if state == "menu":
                # Create rectangles in the same places we draw buttons below and check collision
                start_rect = pygame.Rect(350, 250, 200, 60)
                quit_rect = pygame.Rect(350, 340, 200, 60)
                cat_rect = pygame.Rect(350, 430, 200, 60)  # for "Categories" button

                if start_rect.collidepoint(mx, my):
                    state = "categories"
                elif quit_rect.collidepoint(mx, my):
                    running = False
                elif cat_rect.collidepoint(mx, my):
                    state = "categories"

            elif state == "categories":
                # check each category button rect positions (match drawing positions below)
                y = 200
                for cat_name in categories:
                    rect = pygame.Rect(350, y, 200, 60)
                    if rect.collidepoint(mx, my):
                        start_game(cat_name)
                        break
                    y += 90

                # back button
                back_rect = pygame.Rect(50, 50, 120, 40)
                if back_rect.collidepoint(mx, my):
                    state = "menu"

            elif state == "game":
                # add an on-screen "Back to Menu" and "Restart" clickable areas
                back_rect = pygame.Rect(20, 20, 140, 40)
                restart_rect = pygame.Rect(180, 20, 140, 40)
                if back_rect.collidepoint(mx, my):
                    state = "menu"
                if restart_rect.collidepoint(mx, my):
                    start_game(selected_category)

        # keyboard input (only used during game)
        if event.type == pygame.KEYDOWN and state == "game":
            guess = event.unicode.lower()
            if guess.isalpha() and len(guess) == 1:
                if guess in guessed:
                    pass  # already tried
                else:
                    guessed.add(guess)
                    if guess in word:
                        # reveal letters
                        for i, ch in enumerate(word):
                            if ch == guess:
                                display[i] = guess
                    else:
                        lives -= 1

    # -------------------------
    # DRAW UI per state
    # -------------------------
    
    if state == "menu":
        center_text(" HANGMAN ^_^ ", FONT, YELLOW, WIDTH//2, 80)

        # draw three buttons: Start, Quit, Categories

        draw_button("Start Game", 350, 250, 200, 60, PINK, BLUE)
        draw_button("Quit", 350, 340, 200, 60, BLUE, GREEN)
        draw_button("Categories", 350, 430, 200, 60, CORAL, YELLOW)

    elif state == "categories":
        center_text("Choose a Category", FONT, WHITE, WIDTH//2, 60)
        y = 200
        for cat in categories:
            draw_button(cat, 350, y, 200, 60, BLUE, CORAL)
            y += 90
        # back button
        draw_button("Back", 50, 50, 120, 20, BLUE, PINK)

    elif state == "game":
        # draw hangman to left
        draw_hangman(lives)

        # draw word (centered area on right)
        word_str = " ".join(display)
        surf = FONT.render(word_str, True, WHITE)
        screen.blit(surf, (500, 200))

        # guessed letters
        guessed_text = "Guessed: " + ", ".join(sorted(guessed))
        draw_text(guessed_text, SMALL, WHITE, 500, 260)

        # lives display (hearts)
        draw_text("Lives: " + " X " * lives, SMALL, WHITE, 500, 320)

        # instructions
        draw_text("Type letters on your keyboard", SMALL, YELLOW, 500, 360)

        # buttons: Back and Restart
        draw_button("Back to Menu", 20, 20, 160, 40, BLUE, PINK)
        draw_button("Restart", 200, 20, 120, 40, PINK, BLUE)

        # win/lose messages
        if "_" not in display:
            center_text("Yayyyy... you won!!", FONT, YELLOW, 650, 450)
        if lives <= 0:
            center_text(f"Game Over! Word: {word}", FONT, PINK, 650, 450)

    # update display and tick
    pygame.display.update()
    clock.tick(60)

pygame.quit()
