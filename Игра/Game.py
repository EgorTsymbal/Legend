import tkinter as tk
import Enemy as enm
import random

class Game():
    
    #Создание лямбда-функций, которые будут вызываться при победе или поражении в игре
    function_win = lambda x=None: print("win")
    function_lose = lambda x=None: print("lose")

    #Создание списков для хранения анимаций, позиций и перемещений объектов
    obj_anim = []
    obj_pos = []
    obj_move = []

    #Создание списка для хранения врагов
    enemys = []

    #Установка переменной для определения состояния паузы игры
    game_pause = False

    #Установка количества объектов разных типов в игре
    count_type_0= 3
    count_type_1= 3
    count_type_2= 3

    def Start(self, canvas, window):
        #Присваивание значения переданного холста экземпляру класса
        self.canvas = canvas
        #Присваивание значения переданного окна экземпляру класса
        self.window = window

        #Получение ширины и высоты холста из его свойств и присваивание их экземплярам класса
        self.width = self.canvas["width"]
        self.height = self.canvas["height"]

        #Вычисление количества клеток вдоль осей X и Y на основе ширины и высоты холста
        self.N_X = int(self.width) // 48
        self.N_Y = int(self.height) // 48

        self.exits = False

        #даление всех элементов на холсте и очистка списков объектов и врагов
        self.canvas.delete("all")
        self.obj_anim.clear()
        self.obj_pos.clear()
        self.enemys.clear()
        self.obj_move.clear()

        #Создание игрока 
        player_position = self.new_position()
        self.obj_pos.append(player_position)
        self.player = enm.Player(self.canvas, *player_position)
        self.obj_anim.append(self.player)

        #Создание огня
        self.fire = enm.Fire(self.canvas)
        self.obj_anim.append(self.fire)

        #Создание выхода 
        self.exit_pos = self.new_position()
        self.obj_pos.append(self.exit_pos)
        self.ImageExit = tk.PhotoImage(file = "image/Exit.png")
        self.exit = self.canvas.create_image(*self.exit_pos, image = self.ImageExit, anchor='nw')

        #Создание волков 
        for i in range(self.count_type_1):
            enemy_position = self.new_position()
            self.obj_pos.append(enemy_position)
            enemy = enm.Enemy_type_1(self.canvas, *enemy_position)
            self.enemys.append(enemy)
            self.obj_anim.append(enemy)
            self.obj_move.append(enemy)

        #Создание Чупакабр 
        enemys_type_2 = []
        for i in range(self.count_type_2):
            enemy_position = self.new_position()
            self.obj_pos.append(enemy_position)
            enemy = enm.Enemy_type_2(self.canvas, *enemy_position, self.player)
            self.enemys.append(enemy)
            self.obj_anim.append(enemy)
            self.obj_move.append(enemy)
            enemys_type_2.append(enemy)
        for enemy in enemys_type_2:
            enemy.enemys_type_2 = enemys_type_2

        #Создание домиков
        for i in range(self.count_type_0):
            enemy_position = self.new_position()
            self.obj_pos.append(enemy_position)
            enemy = enm.Enemy_type_0(self.canvas, *enemy_position)
            self.enemys.append(enemy)

        #Передача игроку всех врагов 
        self.player.enemys = self.enemys

        #Бинды
        self.window.bind("<KeyPress>",self.player.keypress)
        self.window.bind("<Button-3>", lambda event: self.jump(True))
        self.window.bind("<ButtonRelease-3>", lambda event: self.jump(False))
        self.window.bind("<space>", self.pause)
        self.window.bind("<Button-1>", lambda event: self.Fire(event))

        #Анимации, передвижения и тд 
        self.update_animations(0)
        self.update_damage()
        self.update_exit()
        self.Fire_update()
        self.canvas.after(1000, self.update_movement)
    #----------------огонь------------------------------------
    def Fire(self, event):
        if not self.game_pause:
            self.fire.Fire_on(event)
            self.canvas.after(2000, self.Fire_off)
            self.window.bind("<Button-1>", lambda event: print("None"))

    def Fire_off(self):
        if not self.game_pause:
            self.fire.Fire_off()
            self.window.bind("<Button-1>", lambda event: self.Fire(event))
        else:
            self.canvas.after(1, self.Fire_off)


    def Fire_update(self):
        fire_pos = self.canvas.coords(self.fire.entity)
        for enemy in self.enemys:
            if self.canvas.coords(enemy.entity) == fire_pos:
                enemy.hide(5)
                self.fire.Fire_off()
        if not self.exits:
            self.canvas.after(10, self.Fire_update)
    #---------------Пауза------------------------       
    def pause(self, event):
        self.game_pause = not self.game_pause
        self.player.game_pause = self.game_pause
        for enemy in self.enemys:
            enemy.game_pause = self.game_pause
        if not self.game_pause:
            self.window.bind("<KeyPress>",self.player.keypress)
        else:
            self.window.bind("<KeyPress>", lambda event: print("pause"))

    #----------------Активация прыжка----------------------------
    def jump(self, active):
        self.player.jump = active

    #получение урона 
    def update_damage(self):
        if not self.game_pause:
            if self.player.Check_Damage():
                if self.player.hp.get() <=0:
                    self.close()
                    self.function_lose()
                if not self.exits:
                    self.canvas.after(200, self.update_damage)
            else:
                if not self.exits:
                    self.canvas.after(1, self.update_damage)
        else:
            self.canvas.after(1, self.update_damage)

    #Проверка выхода 
    def update_exit(self):
        if self.exit_pos == self.canvas.coords(self.player.entity):
            self.close()
            self.function_win()
        if not self.exits:
            self.canvas.after(1, self.update_exit)
    #анимации всех обьектов 
    def update_animations(self, ind):
        if not self.game_pause:
            for entity in self.obj_anim:
                entity.animations(ind)
            ind+=1
        if not self.exits:
            self.canvas.after(150, self.update_animations, ind)
    #Передвижение врагов 
    def update_movement(self):
        if not self.game_pause:
            for enemy in self.obj_move:
                enemy.move()
        if not self.exits:
            self.canvas.after(600, self.update_movement)
    #Создание новых координат для спавна обьектов 
    def new_position(self):
        x = random.randint(0, self.N_X-1)*48
        y = random.randint(0, self.N_Y-1)*48
        position = [x,y]
        if position in self.obj_pos:
            position = self.new_position()
        return position

    #Закрытие игры 
    def close(self):
        self.window.unbind("<KeyPress>")
        self.window.unbind("<Button-3>")
        self.window.unbind("<ButtonRelease-3>")
        self.window.unbind("<space>")
        self.window.unbind("<Button-1>")
        self.exits = True


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=480, height=480)
    game = Game()
    game.Start(canvas, window)
    canvas.pack()
    window.mainloop()