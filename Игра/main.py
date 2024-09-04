from tkinter import *
from Game import Game

class Application(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x780")
        self.resizable(width=False, height=False)
        self.title("Лабораторная работа №4 - 5") 

        #Все окна программы 
        self.menu = Frame_Menu(self)
        self.setup = Frame_Setup(self)
        self.games = Frame_Games(self)
        self.end = Frame_End(self)

        #Открытие меню
        self.swap_frame("menu")

    def swap_frame(self, frame_name, text=None):
        if frame_name == "menu":
            self.menu.open()
        elif frame_name == "setup":
            self.setup.open()
        elif frame_name == "game":
            size_map = self.setup.grid_size.get()
            n_enemy = self.setup.quantity_enemies.get()
            n_obstacle = self.setup.quantity_obstacle.get()
            n_chupacabra = self.setup.quantity_сhupacabra.get()
            self.games.open(size_map, n_enemy, n_obstacle, n_chupacabra)
        elif frame_name == "end":
            self.end.open(text)


class Basic_Frame(Frame):
    #Стили оформления текста 
    txt_basic = {
        "anchor": "center",
        "background": "#01926A",
        "foreground": "#292929",
        "font": ("Segoe script", 20)
    }

    txt_small = {
        "anchor": "center",
        "background": "#01926A",
        "foreground": "#292929",
        "font": ("Segoe script", 10)
    }

    text_huge = {
        "anchor": "center",
        "background": "#01926A",
        "foreground": "#292929",
        "font": ("Arial Black", 45)
    } 

    def __init__(self, parent):
        super().__init__(parent, bg='#01926A', width=800, height=780)
        
        self.grid_propagate(0)
        self.parent = parent #Окно Tk

    def open(self):
        self.pack()

    def close(self, frame_name):
        self.pack_forget()
        self.parent.swap_frame(frame_name)


class Frame_Menu(Basic_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #------------------Создание сетки---------------------
        for c in range(1): self.columnconfigure(index=c, weight=1)
        for r in range(3): self.rowconfigure(index=r, weight=1)
        #-----------------Лабораторная работа № 4----------------------
        Label(
            self, text = "Лабораторная работа № 4 - 5", **self.txt_basic
        ).grid(row=0, column=0, columnspan=2, ipadx=70, ipady=6, padx=5, pady=5)
        #----------------------Кнопка Играть--------------------------------
        Button(
            self, text = "Играть", **self.txt_basic,
            command=lambda: self.close("game")
        ).grid(row=1, column=0, ipadx=70, ipady=6, padx=5, pady=5)
        #---------------------Кнопка Настройки--------------------------------
        Button(
            self, text = "Настройки", **self.txt_basic,
            command=lambda: self.close("setup")
        ).grid(row=2, column=0, ipadx=70, ipady=6, padx=5, pady=5)


class Frame_Setup(Basic_Frame):

    def __init__(self, parent):
        super().__init__(parent)

        #------------------Создание сетки---------------------
        for c in range(4): self.columnconfigure(index=c, weight=1)
        for r in range(7): self.rowconfigure(index=r, weight=1)

        #-------------Надпись Настройки---------------------------
        Label( self, text = "Настройки", **self.txt_basic)\
            .grid(row=0, column=0)

        #-------------Выбор размера поля----------------
        self.grid_size = IntVar(value=480)#Размер

        Label(self, text = "Размер поля", **self.txt_small)\
            .grid(row=1, column=0)

        for i, j in zip([480, 720], range(2, 4)):
            Radiobutton(
                self, **self.txt_small, text=str(i) + "x" + str(i), value=i, 
                variable=self.grid_size
            ).grid(row=j, column=0)

        #-------------Выбор Количество волков------------------
        self.quantity_enemies = IntVar(value=2)#Количество

        Label(self, text = "Количество волков", **self.txt_small).\
            grid(row=1, column=2)

        for i, j in zip(range(2, 6), range(2, 6)):
            Radiobutton(
                self, **self.txt_small, text=str(i), value=i, 
                variable=self.quantity_enemies
            ).grid(row=j, column=2)

        #-------------Выбор количество Домиков------------------
        self.quantity_obstacle = IntVar(value=2)#Количество

        Label(self, text = "Количество Домиков", **self.txt_small).\
            grid(row=1, column=1)

        for i, j in zip(range(2, 6), range(2, 6)):
            Radiobutton(
                self, **self.txt_small, text=str(i), value=i, 
                variable=self.quantity_obstacle
            ).grid(row=j, column=1)

        #-------------Выбор количество Чупакабр------------------
        self.quantity_сhupacabra = IntVar(value=2)#Количество

        Label(self, text = "Количество Чупакабр", **self.txt_small).\
            grid(row=1, column=3)

        for i, j in zip(range(2, 6), range(2, 6)):
            Radiobutton(
                self, **self.txt_small, text=str(i), value=i, 
                variable=self.quantity_сhupacabra
            ).grid(row=j, column=3)

        #-------------Кнопка меню------------------
        Button(self, text = "Меню", **self.txt_basic,
            command=lambda: self.close("menu")
        ).grid(row=6, column=3)


class Frame_Games(Basic_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #------------------Создание сетки---------------------
        for c in range(10): self.columnconfigure(index=c, weight=1)
        for r in range(10): self.rowconfigure(index=r, weight=1)

        Label(
            self, text = "Количество жизней:", **self.txt_basic
        ).grid(row=0, column=0, sticky="E")

        Label(
            self, text = "прыжок:", **self.txt_basic
        ).grid(row=0, column=8, sticky="E")

        self.lbl_hp = Label(
            self, **self.txt_basic
        )

        self.lbl_jump = Label(
            self, **self.txt_basic
        )

    def open(self, size_map, n_enemy, n_obstacle, n_chupacabra):
        self.pack()

        #Создание холста для игры с определенными параметрами
        self.canvas = Canvas(self, width=size_map+48, height=size_map-48, bg = "#66C901")

        #Создание экземпляра класса Game
        game = Game()

        #Установка количества объектов разных типов в игре
        game.count_type_0= n_obstacle
        game.count_type_1= n_enemy
        game.count_type_2= n_chupacabra

        #Установка функций, которые будут вызваны при победе или поражении в игре
        game.function_win = lambda: self.close("end", "Победа")
        game.function_lose = lambda: self.close("end", "Помер")

        #Запуск игры
        game.Start(self.canvas, window)

        #Установка переменных для отображения здоровья игрока и кд прыжков
        self.lbl_hp.config(textvariable=game.player.hp)
        self.lbl_jump.config(textvariable=game.player.lbl_jump)

        #Размещение меток для отображения здоровья и прыжков на главном окне
        self.lbl_hp.grid(row=0, column=1, sticky="W")
        self.lbl_jump.grid(row=0, column=9, sticky="W")

        #Размещение холста на окне
        self.canvas.grid(row=1, column=0, columnspan=10, rowspan=9)

    def close(self, frame_name, text):
        
        self.canvas.destroy()
        self.pack_forget()
        self.parent.swap_frame(frame_name, text=text)


class Frame_End(Basic_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #------------------Создание сетки---------------------
        for c in range(1): self.columnconfigure(index=c, weight=1)
        for r in range(7): self.rowconfigure(index=r, weight=1)

        #------------------------Помер\Ты прошел игру--------------------------------
        self.lbl_text = StringVar()

        Label(self, textvariable=self.lbl_text, **self.text_huge)\
            .grid(row=2, column=0, columnspan=2, ipadx=70, ipady=6, padx=5, pady=5)
        #----------------------Кнопка Играть снова--------------------------------
        Button(
            self, text = "Играть снова", **self.txt_basic,
            command=lambda: self.close("game")
        ).grid(row=5, column=0, ipadx=70, ipady=6, padx=5, pady=5)
        #---------------------Кнопка Меню--------------------------------
        Button(
            self, text = "Меню", **self.txt_basic,
            command=lambda: self.close("menu")
        ).grid(row=6, column=0, ipadx=70, ipady=6, padx=5, pady=5)

    def open(self, text):
        self.lbl_text.set(text)
        super().open()

if __name__ == '__main__':
    window = Application()
    window.mainloop()