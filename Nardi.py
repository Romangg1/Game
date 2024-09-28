import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk


# Класс, необходимый для открытия основного окна
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.goal_black = 0
        self.goal_white = 0
        self.root.title('Главное меню')
        self.root.geometry('400x200')
        self.root.resizable(False, False)

        self.play_button = tk.Button(root, text='Начать', command=self.play, bg='blue', fg='white')
        self.play_button.pack(fill=tk.X, padx=5, pady=5)

        self.rules_button = tk.Button(root, text='Правила', command=self.rules, bg='blue', fg='white')
        self.rules_button.pack(fill=tk.X, padx=5, pady=5)

        self.exit_button = tk.Button(root, text='Выход', command=root.quit, bg='blue', fg='white')
        self.exit_button.pack(fill=tk.X, padx=5, pady=20)

    # Открытие игрового окна
    def play(self):
        self.root.withdraw()
        GameWindow(self.root)

    # Открытие окна правил
    def rules(self):
        rules_window = tk.Toplevel(self.root)
        rules_window.geometry('700x400')
        rules_window.title('Правила игры')
        rules_window.resizable(False, False)

        rules_text = tk.Text(rules_window, wrap=tk.WORD)
        rules_text.insert(tk.END, '''
        Правила нарды в игре:
        1. Играют два игрока: Игрок 1 (белые фишки) и Игрок 2 (черные фишки).
        2. Игроки по очереди бросают два кубика и делают ходы, равные выпавшим 
        числам.
        3. Белые фишки движутся вправо, черные фишки движутся влево.
        4. Цель игры - первым пройти свои фишки через всё поле и вывести их за 
        его пределы.
        5. Если фишка белого цвета достигает правого края поля, она убирается с поля, и Игрок 1 получает очко.
        6. Если фишка черного цвета достигает левого края поля, она убирается с поля, и Игрок 2 получает очко.
        7. Игра продолжается до тех пор, пока один из игроков не наберет 11 очков. Этот игрок объявляется победителем.
        8. Если после броска кубиков игрок не может сделать ход, ход переходит к следующему игроку.
        9. После каждого хода количество оставшихся ходов обновляется. Если ходов не осталось, ход переходит к другому игроку.
        ''')
        rules_text.config(state=tk.DISABLED)  # Запрещаем редактирование текста
        rules_text.pack()

# Окно игрового поля
class GameWindow:
    def __init__(self, root):
        self.root = root
        self.win_white = 0
        self.win_black = 0
        self.current_player = 1
        self.remaining_moves = [0, 0]
        self.white_chip_positions = [0] * 11
        self.black_chip_positions = [10] * 11  # Начальная позиция чёрных на одну меньше
        self.white_chip_in_goal = 0
        self.black_chip_in_goal = 0

        # Добавляем массив для учета фишек на каждой позиции (стек фишек)
        self.position_stack = [[0] * 11 for _ in range(11)]

        self.game_window = tk.Toplevel(root)
        self.game_window.title('Игровое окно\n')
        self.game_window.geometry('900x600')
        self.game_window.configure(bg='white')
        self.game_window.resizable(False, False)
        self.game_window.protocol('WM_DELETE_WINDOW', self.return_to_main_menu)

        self.dice_images = [ImageTk.PhotoImage(Image.open(f"image/{i + 1}.png").resize((50, 50))) for i in range(6)]
        self.black_chip = ImageTk.PhotoImage(Image.open("image/black.png").resize((50, 50)))
        self.white_chip = ImageTk.PhotoImage(Image.open("image/white.png").resize((50, 50)))
 
        # Создаем места для отображения бросков кубиков
        self.dice_label1 = tk.Label(self.game_window, image=self.dice_images[0])
        self.dice_label1.grid(row=6, column=1)

        self.dice_label2 = tk.Label(self.game_window, image=self.dice_images[0])
        self.dice_label2.grid(row=6, column=2)

        # Создаем места для отображения счета игроков
        self.create_score_labels()

        # Создаем игровое поле
        self.game_field = tk.Canvas(self.game_window, width=550, height=550, bg='bisque')
        self.game_field.grid(row=0, column=1, rowspan=6, columnspan=2)

        self.draw_board()

        # Создаем кнопки для броска кубиков и выхода из игры
        self.dice_button = tk.Button(self.game_window, text='Бросить кубики\n', bg='brown', fg='white',
                                     command=self.roll_dice)
        self.dice_button.grid(row=5, column=0)

        self.exit_button = tk.Button(self.game_window, text='Выход\n', command=self.return_to_main_menu, bg='brown',
                                     fg='white')
        self.exit_button.grid(row=5, column=3)

    def create_score_labels(self):
        self.player1_label = tk.Label(self.game_window, text='Игрок 1\n', fg='blue', bg='white')
        self.player1_label.grid(row=0, column=0, sticky='nsew')
        self.player1_score = tk.IntVar()
        self.player1_score.set(0)
        self.player1_score_label = tk.Label(self.game_window, text='1', bg='white')
        self.player1_score_label.grid(row=1, column=0, sticky='nsew')

        self.turn = tk.StringVar()
        self.turn.set('Ход: Игрок 1')
        self.turn_label = tk.Label(self.game_window, textvariable=self.turn, bg='white')
        self.turn_label.grid(row=2, column=0, sticky='nsew')

        self.player2_label = tk.Label(self.game_window, text='Игрок 2', fg='red', bg='white')
        self.player2_label.grid(row=3, column=0, sticky='nsew')

        self.player2_score = tk.IntVar()
        self.player2_score.set(0)
        self.player2_score_label = tk.Label(self.game_window, text='2', bg='white')
        self.player2_score_label.grid(row=4, column=0, sticky='nsew')

    def draw_board(self):
        for i in range(11):
            for j in range(11):
                self.game_field.create_rectangle(i * 50, j * 50, i * 50 + 50, j * 50 + 50)

        for i in range(11):
            self.game_field.create_image(25, 25 + i * 50, image=self.white_chip, tags=f'white_chip_{i}')
            self.game_field.create_image(525, 525 - i * 50, image=self.black_chip, tags=f'black_chip_{i}')

        for i in range(11):
            self.game_field.tag_bind(f'white_chip_{i}', '<Button-1>', self.move_chip)
            self.game_field.tag_bind(f'black_chip_{i}', '<Button-1>', self.move_chip)

    def roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        #dice1 = 6
        #dice2 = 6

        if dice1 == dice2:
            self.remaining_moves = [dice1, dice1, dice2, dice2] if self.current_player == 1 else [-dice1, -dice1, -dice2, -dice2]
        else:
            self.remaining_moves = [dice1, dice2] if self.current_player == 1 else [-dice1, -dice2]

        self.dice_label1.configure(image=self.dice_images[dice1 - 1])
        self.dice_label2.configure(image=self.dice_images[dice2 - 1])

        if dice1 == dice2:
            self.turn.set(f'Ход: Игрок {self.current_player}, \nкубики: {dice1}, {dice2}, {dice2}, {dice2}')
        else:
            self.turn.set(f'Ход: Игрок {self.current_player}, \nкубики: {dice1}, {dice2}')

    def move_chip(self, event):
        if not self.remaining_moves or self.remaining_moves == [0, 0]:
            self.turn.set('Бросьте\n кубики!')
            return

        item = self.game_field.find_withtag(tk.CURRENT)[0]
        item_tags = self.game_field.gettags(item)
        chip_tag = [tag for tag in item_tags if 'chip' in tag][0]
        chip_color, chip_number = chip_tag.split('_chip_')
        chip_number = int(chip_number)

        if (self.current_player == 1 and chip_color == 'white') or (self.current_player == 2 and chip_color == 'black'):
            move = self.remaining_moves.pop(0)
            if chip_color == 'white':
                old_position = self.white_chip_positions[chip_number]
                self.white_chip_positions[chip_number] += move
                new_position = self.calculate_new_position(self.white_chip_positions[chip_number], 'white')
                if self.white_chip_positions[chip_number] > 10:
                    self.white_chip_in_goal +=1

                # Увеличиваем высоту фишки на новом месте
                stack_level = self.position_stack[self.white_chip_positions[chip_number] % 11].count('white')
                new_position = (new_position[0], new_position[1] - stack_level * 25)  # Смещение на 10 пикселей по Y
                self.position_stack[self.white_chip_positions[chip_number] % 11].append('white')
            else:
                old_position = self.black_chip_positions[chip_number]
                self.black_chip_positions[chip_number] += move
                new_position = self.calculate_new_position(self.black_chip_positions[chip_number], 'black')
                if self.black_chip_positions[chip_number] < 0:
                    self.black_chip_in_goal +=1
                # Увеличиваем высоту фишки на новом месте
                stack_level = self.position_stack[self.black_chip_positions[chip_number] % 11].count('black')
                new_position = (new_position[0], new_position[1] + stack_level * 25)  # Смещение на 10 пикселей по Y
                self.position_stack[self.black_chip_positions[chip_number] % 11].append('black')
            if self.black_chip_in_goal >=11:
                messagebox.showinfo("Победа!", "Победил черный 1!")
                self.game_window.destroy()
                self.game_window.destroy()
                root.deiconify()
            if self.white_chip_in_goal >=11:
                messagebox.showinfo("Победа!", "Победил белый!")
                self.game_window.destroy()
                self.root.deiconify()

            # Перемещаем фишку на новые координаты
            self.game_field.coords(item, new_position)

            if not self.remaining_moves:
                self.current_player = 1 if self.current_player == 2 else 2
                self.turn.set(f'Ход: Игрок {self.current_player}')
            else:
                self.turn.set(f'Ход: Игрок {self.current_player}, \nходов: {list(map(abs, self.remaining_moves))}')

    def calculate_new_position(self, position, color):
        if position < 18:  # Нижний ряд
            return (position * 50 + 25, 525 if color == 'white' else 25)
        elif position < 22:  # Правый столбец
            return (525, (position - 11) * 50 + 25 if color == 'white' else 525 - (position - 11) * 50)
        elif position < 33:  # Верхний ряд
            return ((32 - position) * 50 + 25, 25 if color == 'white' else 525)
        else:  # Левый столбец
            return (25, (44 - position) * 50 + 25 if color == 'white' else 525 - (44 - position) * 50)


    def return_to_main_menu(self):
        self.game_window.destroy()
        self.root.deiconify()



if __name__ == '__main__':
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
