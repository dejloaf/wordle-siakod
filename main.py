import random
import pygame
import Trie

pygame.init()

# цвета
black = (40, 40, 40)
white = (255, 255, 255)
silver = (220, 220, 220)
dodged_blue = (30, 144, 255)
green = (0, 250, 154)
yellow = (255, 215, 0)
gray = (105, 105, 105)

# экран
width = 500
height = 700
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Вордли')
turn = 0
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

huge_font = pygame.font.Font('freesansbold.ttf', 56)
medium_font = pygame.font.Font('freesansbold.ttf', 48)
small_font = pygame.font.Font('freesansbold.ttf', 24)
secret_word = Trie.trie.pick_secret_words()[random.randint(0, len(Trie.trie.pick_secret_words()) - 1)]
game_over = False
letters = 0
turn_active = True


def is_russian_letter(char):
    return char.lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def en_to_ru(char):
    if is_russian_letter(char):
        return char.lower()

    mapping = {
        'q': 'й',
        'w': 'ц',
        'e': 'у',
        'r': 'к',
        't': 'е',
        'y': 'н',
        'u': 'г',
        'i': 'ш',
        'o': 'щ',
        'p': 'з',
        '[': 'х',
        ']': 'ъ',
        'a': 'ф',
        's': 'ы',
        'd': 'в',
        'f': 'а',
        'g': 'п',
        'h': 'р',
        'j': 'о',
        'k': 'л',
        'l': 'д',
        ';': 'ж',
        "'": 'э',
        'z': 'я',
        'x': 'ч',
        'c': 'с',
        'v': 'м',
        'b': 'и',
        'n': 'т',
        'm': 'ь',
        ',': 'б',
        '.': 'ю',
        '/': '.'
    }

    if char not in mapping.keys():
        return char

    return mapping[char]


def convert_text(text):
    return ''.join([en_to_ru(char) for char in text])


def draw_piece_text(row, col):
    global board
    font_sizes = {u'\u044e': 63, u'\u0448': 63, u'\u0436': 65, u'\u0443': 72, u'\u0449': 61,
                  u'\u0433': 76, u'\u043c': 69, u'\u0442': 74, u'\u0444': 61, u'\u044b': 65,
                  u'\u0434': 64}
    font_width = font_sizes.get(board[row][col], 70)
    piece_text = huge_font.render(board[row][col], True, black)
    screen.blit(piece_text, (col * 80 + font_width, row * 80 + 60))


def draw_board():
    global turn
    global board

    for col in range(5):
        for row in range(6):
            # рисуем ячейку
            rect = pygame.Rect(col * 80 + 50, row * 80 + 50, 75, 75)
            pygame.draw.rect(screen, silver, rect, border_radius=2)

            # выводим букву в ячейке
            draw_piece_text(row, col)

    # рисуем стрелки
    if turn < 6 and not game_over:
        draw_arrow((12, turn * 80 + 68), (30, 75))
        draw_arrow2((481, turn * 80 + 68), (30, 75))


first_row = "йцукенгшщзхъ"
second_row = "фывапролджэ"
third_row = "ячсмитьбю"


def draw_cell(x, y):
    rect = pygame.Rect(x, y, 35, 35)
    pygame.draw.rect(screen, silver, rect, border_radius=3)


def draw_text(x, y, text):
    text = small_font.render(text, True, black)
    screen.blit(text, (x, y))


def draw_keyboard():
    x_offset = (width - 10 * 50) // 2
    y_offset = (height - 150)

    for i, char in enumerate(first_row):
        x = x_offset + i * 40 + 12
        y = y_offset
        draw_cell(x, y)
        draw_text(x + 10, y + 5, char)

    for i, char in enumerate(second_row):
        x = x_offset + i * 40 + 33
        y = y_offset + 45
        draw_cell(x, y)
        draw_text(x + 10, y + 5, char)

    for i, char in enumerate(third_row):
        x = x_offset + i * 40 + 73
        y = y_offset + 90
        draw_cell(x, y)
        draw_text(x + 10, y + 5, char)


def get_coordinates(char):
    for i in range(len(first_row)):
        if char == first_row[i]:
            return i * 40 + (width - 10 * 50) // 2 + 12, (height - 150)
        elif i < len(second_row) and char == second_row[i]:
            return i * 40 + (width - 10 * 50) // 2 + 33, (height - 150) + 45
        elif i < len(third_row) and char == third_row[i]:
            return i * 40 + (width - 10 * 50) // 2 + 73, (height - 150) + 90
    return 0, 0


def draw_arrow(pos, size):
    start_x, start_y = pos
    end_x, end_y = start_x + size[0], start_y + size[1] / 2
    mid_y = start_y + size[1] / 4
    points = [(start_x, start_y), (end_x, mid_y), (start_x, end_y)]
    pygame.draw.lines(screen, silver, False, points, 10)


def draw_arrow2(pos, size):
    start_x, start_y = pos
    end_x, end_y = start_x - size[0], start_y + size[1] / 2
    mid_y = start_y + size[1] / 4
    points = [(start_x, start_y), (end_x, mid_y), (start_x, end_y)]
    pygame.draw.lines(screen, silver, False, points, 10)


def check_words_board():
    global turn
    global board
    global secret_word
    for col in range(5):
        for row in range(6):
            current_char = board[row][col]
            if current_char in secret_word and turn > row:
                if current_char == secret_word[col]:
                    pygame.draw.rect(screen, green, [col * 80 + 50, row * 80 + 50, 75, 75], border_radius=2)
                else:
                    pygame.draw.rect(screen, yellow, [col * 80 + 50, row * 80 + 50, 75, 75], border_radius=2)
            elif turn > row:
                pygame.draw.rect(screen, gray, [col * 80 + 50, row * 80 + 50, 75, 75], border_radius=2)


def check_words_keyboard():
    global turn
    global board
    global secret_word

    guessed_indexes = []
    for col in range(5):
        for row in range(6):
            current_char = board[row][col]
            if current_char in secret_word:
                indexes = [i for i, char in enumerate(secret_word) if char == current_char]
                for index in indexes:
                    if index == col and turn > row:
                        x, y = get_coordinates(current_char)
                        pygame.draw.rect(screen, green, [x, y, 35, 35], border_radius=2)
                        draw_text(x + 10, y + 5, current_char)
                        guessed_indexes.append(index)
                    elif index not in guessed_indexes and turn > row:
                        x, y = get_coordinates(current_char)
                        pygame.draw.rect(screen, yellow, [x, y, 35, 35], border_radius=2)
                        draw_text(x + 10, y + 5, current_char)
                        guessed_indexes.append(index)
            elif turn > row:
                x, y = get_coordinates(current_char)
                pygame.draw.rect(screen, gray, [x, y, 35, 35], border_radius=2)
                draw_text(x + 10, y + 5, current_char)


word = ""
error_message = False
running = True

game_running = False


def start_screen():
    global button1, button2

    screen.fill(white)
    text = medium_font.render("вордли", True, black)
    text_rect = text.get_rect(center=(width / 2, height / 5))
    screen.blit(text, text_rect)

    button1 = pygame.Rect(150, 350, 200, 50)
    button2 = pygame.Rect(150, 450, 200, 50)

    text1 = small_font.render("Начать игру", True, black)
    text2 = small_font.render("Выйти из игры", True, black)
    text_rect1 = text1.get_rect(center=button1.center)
    text_rect2 = text2.get_rect(center=button2.center)
    pygame.draw.rect(screen, silver, button1, border_radius=2)
    pygame.draw.rect(screen, silver, button2, border_radius=2)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)

    pygame.display.update()


def handle_events():
    global running, game_running, word, letters, turn, game_over, error_message

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(event.pos):
                game_running = True
            if button2.collidepoint(event.pos):
                running = False
        if check_for_text_input(event):
            continue
        if check_for_keydown(event):
            continue


def check_for_text_input(event):
    global turn_active, word, letters, board

    if event.type == pygame.TEXTINPUT and turn_active and not game_over:
        entry = convert_text(event.text)
        if is_russian_letter(entry):
            board[turn][letters] = entry.lower()
            letters += 1
            word += entry.lstrip()
        return True

    return False


def check_for_keydown(event):
    global game_running, letters, word, error_message, turn, game_over, board, secret_word, turn_active

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_running = False
            start_screen()
            turn = 0
            letters = 0
            word = ""
            game_over = False
            secret_word = Trie.trie.pick_secret_words()[
                random.randint(0, len(Trie.trie.pick_secret_words()) - 1)]
            board = [[" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "]]

        elif event.key == pygame.K_BACKSPACE and letters > 0:
            board[turn][letters - 1] = ' '
            letters -= 1
            word = word[:-1]
            error_message = False

        elif event.key == pygame.K_SPACE and not letters < 5 and not game_over:
            if Trie.trie.search_word(word):
                turn += 1
                word = ""
                letters = 0
            else:
                error_message = True

        elif event.key == pygame.K_SPACE and game_over:
            turn = 0
            letters = 0
            word = ""
            game_over = False
            secret_word = Trie.trie.pick_secret_words()[
                random.randint(0, len(Trie.trie.pick_secret_words()) - 1)]
            board = [[" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "],
                     [" ", " ", " ", " ", " "]]

        if letters == 5:
            turn_active = False
        if letters < 5:
            turn_active = True

    pygame.display.update()


def game_loop():
    global game_running, game_over

    screen.fill(white)

    draw_board()

    if not game_over:
        draw_keyboard()
        check_words_keyboard()
    check_words_board()

    for row in range(0, 6):
        for col in range(0, 5):
            draw_piece_text(row, col)

    guess = ''
    for row in range(0, 6):
        guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
        if guess == secret_word and row < turn:
            game_over = True

    if turn == 6:
        if guess == secret_word:
            winner_text = huge_font.render('Отлично!', True, black)
            screen.blit(winner_text, (118, 580))
        else:
            game_over = True
            loser_text = medium_font.render('Неудача :(', True, black)
            screen.blit(loser_text, (120, 580))
            loser_text2 = small_font.render('секретное слово: ' + secret_word, True, dodged_blue)
            screen.blit(loser_text2, (102, 640))

    if error_message:
        error_text = small_font.render('слово не найдено', True, black)
        screen.blit(error_text, (139, 16))

    if game_over and turn < 6:
        winner_text = huge_font.render('Отлично!', True, black)
        screen.blit(winner_text, (118, 580))

    pygame.display.update()


start_screen()

while running:
    handle_events()
    if game_running:
        game_loop()

pygame.quit()
