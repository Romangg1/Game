from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import random

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("1600x845")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=845, width=1600, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

rectangles = [
    (51.0, 60.0, 181.0, 280.0, "#AD7F3A"),
    (1431.0, 60.0, 1561.0, 280.0, "#AE354B"),
    (1431.0, 347.0, 1561.0, 567.0, "#AD354B"),
    (51.0, 347.0, 181.0, 567.0, "#659CC4"),
]

# Создание прямоугольников из списка
for rect in rectangles:
    canvas.create_rectangle(rect[0], rect[1], rect[2], rect[3], fill=rect[4], outline="")

# Массив фиолетовых прямоугольников
purple_blocks = [
    (1299.0, 100.0, 1389.0, 270.0),
    (1202.0, 100.0, 1292.0, 270.0),
    (1105.0, 100.0, 1195.0, 270.0),
    (1008.0, 100.0, 1098.0, 270.0),
    (911.0, 100.0, 1001.0, 270.0),
    (814.0, 100.0, 904.0, 270.0),
    (717.0, 100.0, 807.0, 270.0),
    (620.0, 100.0, 710.0, 270.0),
    (523.0, 100.0, 613.0, 270.0),
    (426.0, 100.0, 516.0, 270.0),
    (329.0, 100.0, 419.0, 270.0),
    (232.0, 100.0, 322.0, 270.0),
    (232.0, 381.0, 322.0, 551.0),
    (329.0, 381.0, 419.0, 551.0),
    (426.0, 381.0, 516.0, 551.0),
    (523.0, 381.0, 613.0, 551.0),
    (620.0, 381.0, 710.0, 551.0),
    (717.0, 381.0, 807.0, 551.0),
    (814.0, 381.0, 904.0, 551.0),
    (911.0, 381.0, 1001.0, 551.0),
    (1008.0, 381.0, 1098.0, 551.0),
    (1105.0, 381.0, 1195.0, 551.0),
    (1202.0, 381.0, 1292.0, 551.0),
    (1299.0, 381.0, 1389.0, 551.0),
]

# Создание фиолетовых прямоугольников
for block in purple_blocks:
    canvas.create_rectangle(block[0], block[1], block[2], block[3], fill="#9B30FF", outline="")

# Массив всех доступных блоков для пирата
blocks = [
    (1299.0, 381.0, 1389.0, 551.0),  # Блок 1
    (1202.0, 381.0, 1292.0, 551.0),  # Блок 2
    (1105.0, 381.0, 1195.0, 551.0),  # Блок 3
    (1008.0, 381.0, 1098.0, 551.0),  # Блок 4
    (911.0, 381.0, 1001.0, 551.0),   # Блок 5
    (814.0, 381.0, 904.0, 551.0),    # Блок 6
    (717.0, 381.0, 807.0, 551.0),    # Блок 7
    (620.0, 381.0, 710.0, 551.0),    # Блок 8
    (523.0, 381.0, 613.0, 551.0),    # Блок 9
    (426.0, 381.0, 516.0, 551.0),    # Блок 10
    (329.0, 381.0, 419.0, 551.0),    # Блок 11
    (232.0, 381.0, 322.0, 551.0),    # Блок 12
    (232.0, 100.0, 322.0, 270.0),
    (329.0, 100.0, 419.0, 270.0),
    (426.0, 100.0, 516.0, 270.0),
    (523.0, 100.0, 613.0, 270.0),
    (620.0, 100.0, 710.0, 270.0),
    (717.0, 100.0, 807.0, 270.0),
    (814.0, 100.0, 904.0, 270.0),
    (911.0, 100.0, 1001.0, 270.0),
    (1008.0, 100.0, 1098.0, 270.0),
    (1105.0, 100.0, 1195.0, 270.0),
    (1202.0, 100.0, 1292.0, 270.0),
    (1299.0, 100.0, 1389.0, 270.0),
]

# Установка начального положения пират
pirat_image = PhotoImage(file=relative_to_assets("pirat.png"))
initial_block = blocks[0]  # Начальная клетка - первая
pirat_x = initial_block[0]
pirat_y = initial_block[3]
pirat_id = canvas.create_image(pirat_x, pirat_y, image=pirat_image, anchor="sw", tag="pirat")
canvas.image_pirat = pirat_image

# Переменные для хранения состояния и данных
selected_block = None
outline_id = None  # Идентификатор обводки
highlight_ids = []  # Для хранения обводок подсвеченных клеток
stop_animation = [False]
animation_complete = [False]  # Флаг завершения анимации
dice_rolls = [0, 0]  # Значения кубиков
current_position = 0  # Текущая позиция пирата (начинаем с первой клетки)


def highlight_blocks():
    global highlight_ids

    # Убираем старые подсветки
    for highlight_id in highlight_ids:
        canvas.delete(highlight_id)
    highlight_ids.clear()

    # Подсвечиваем клетку для оставшегося кубика
    if dice_rolls[0] > 0:
        next_position = current_position + dice_rolls[0]
        if 0 <= next_position < len(blocks):
            x1, y1, x2, y2 = blocks[next_position]
            highlight_id = canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=3)
            highlight_ids.append(highlight_id)

    if dice_rolls[1] > 0:
        next_position = current_position + dice_rolls[1]
        if 0 <= next_position < len(blocks):
            x1, y1, x2, y2 = blocks[next_position]
            highlight_id = canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=3)
            highlight_ids.append(highlight_id)



def select_pirat(event):
    global outline_id, selected_block

    # Если пират уже выделен, снимаем выделение
    if outline_id:
        canvas.delete(outline_id)
        outline_id = None

    # Выделяем пирата синим цветом
    x1, y1, x2, y2 = blocks[current_position]
    outline_id = canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=3)
    selected_block = current_position

    # Подсвечиваем доступные для хода клетки
    highlight_blocks()


def move_to_block(event):
    global current_position

    # Определяем координаты клика
    clicked_x, clicked_y = event.x, event.y

    # Проверяем, попал ли клик в одну из подсвеченных клеток
    for i, block in enumerate(blocks):
        x1, y1, x2, y2 = block
        if x1 <= clicked_x <= x2 and y1 <= clicked_y <= y2:
            # Определяем, перемещается ли пират по кубику 1 или 2
            if i == current_position + dice_rolls[0]:
                # Перемещение по первому кубику
                canvas.coords(pirat_id, blocks[i][0], blocks[i][3])
                current_position = i
                dice_rolls[0] = 0  # Обнуляем первый кубик

                # Удаляем первое изображение кубика
                canvas.delete("image1")

            elif i == current_position + dice_rolls[1]:
                # Перемещение по второму кубику
                canvas.coords(pirat_id, blocks[i][0], blocks[i][3])
                current_position = i
                dice_rolls[1] = 0  # Обнуляем второй кубик

                # Удаляем второе изображение кубика
                canvas.delete("image2")

            # Убираем старые подсветки и выделение
            canvas.delete(outline_id)
            for highlight_id in highlight_ids:
                canvas.delete(highlight_id)
            highlight_ids.clear()

            # Если оба кубика использованы, удаляем подсветку
            if dice_rolls[0] == 0 and dice_rolls[1] == 0:
                print("Оба кубика использованы. Доступных ходов больше нет.")
            else:
                # Подсвечиваем оставшуюся клетку
                highlight_blocks()

            print(f"Пират переместился на {i + 1} клетку")
            break


def update_random_image_1():
    if stop_animation[0]:
        return

    random_image_number = random.randint(1, 6)
    dice_rolls[0] = random_image_number  # Обновляем значение первого кубика
    random_image_path = relative_to_assets(f"{random_image_number}.png")
    random_image = PhotoImage(file=random_image_path)

    canvas.delete("image1")
    canvas.create_image(688.0, 702.0, image=random_image, tag="image1")
    canvas.image1 = random_image

    if not animation_complete[0]:
        window.after(100, update_random_image_1)


def update_random_image_2():
    if stop_animation[0]:
        return

    random_image_number = random.randint(1, 6)
    dice_rolls[1] = random_image_number  # Обновляем значение второго кубика
    random_image_path = relative_to_assets(f"{random_image_number}.png")
    random_image = PhotoImage(file=random_image_path)

    canvas.delete("image2")
    canvas.create_image(838.0, 702.0, image=random_image, tag="image2")
    canvas.image2 = random_image

    if not animation_complete[0]:
        window.after(100, update_random_image_2)


def start_random_images():
    global stop_animation, animation_complete
    stop_animation[0] = False
    animation_complete[0] = False
    update_random_image_1()
    update_random_image_2()
    window.after(1000, show_final_images)


def show_final_images():
    global stop_animation, animation_complete
    stop_animation[0] = True
    animation_complete[0] = True

    # Показ окончательных значений кубиков
    print(f"Кубики показали: {dice_rolls[0]} и {dice_rolls[1]}")

    # Задержка перед удалением изображений кубиков
    window.after(2000, delete_dice_images)


def delete_dice_images():
    # Удаление изображений кубиков после задержки
    canvas.delete("image1")
    canvas.delete("image2")


# Кнопка для броска кубиков
roll_button_image = PhotoImage(file=relative_to_assets("bros.png"))
roll_button = Button(image=roll_button_image, borderwidth=0, highlightthickness=0, command=start_random_images, relief="flat")
roll_button.place(x=1100.0, y=650.0, width=191.0, height=104.0)

# Назначаем события для выбора пирата и клика по клетке
canvas.tag_bind("pirat", "<Button-1>", select_pirat)
canvas.bind("<Button-1>", move_to_block)

window.mainloop()

