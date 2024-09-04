import tkinter as tk 
import random

class Basic_Entity():

    # изображения для различных направлений движения
	ImageDown = None 
	ImageUp = None 
	ImageLeft = None 
	ImageRight = None

	game_pause = False

	def __init__(self, canvas, x, y):
        # canvas - это холст, на котором будет расположен объект
		self.canvas = canvas
		self.x, self.y = x, y
		self.image = self.ImageDown
        # создаем объект на холсте
		self.entity = self.canvas.create_image(self.x, self.y, image=self.image[0], anchor='nw')

        # получаем размеры холста
		self.width = int(self.canvas["width"])
		self.height = int(self.canvas["height"])

	def animations(self, ind):
        # метод для анимации объекта, меняет изображение каждые 3 кадра
 		self.canvas.itemconfig(self.entity, image=self.image[ind%3])

	def movement(self, direction):
        # метод для движения объекта в заданном направлении
		if direction == "Up":
			self.canvas.move(self.entity, 0, -48)
			self.image = self.ImageUp
		elif direction == "Down":
			self.canvas.move(self.entity, 0, 48)
			self.image = self.ImageDown
		elif direction == "Left":
			self.canvas.move(self.entity, -48, 0)
			self.image = self.ImageLeft
		elif direction == "Right":
			self.canvas.move(self.entity, 48, 0)
			self.image = self.ImageRight

        # проверяем, находится ли объект за границами холста
		obj_pos = self.canvas.coords(self.entity)

		if obj_pos[0] < 0:
            # если объект вышел за левую границу холста, перемещаем его в правый край
			self.canvas.coords(self.entity, self.width-48, obj_pos[1])
		elif obj_pos[0] >= self.width and obj_pos[0]< 5000:
            # если объект вышел за правую границу холста, перемещаем его в левый край
			self.canvas.coords(self.entity, 0, obj_pos[1])
		elif obj_pos[1] < 0:
            # если объект вышел за верхнюю границу холста, перемещаем его в нижнюю границу
			self.canvas.coords(self.entity, obj_pos[0], self.height-48)
		elif obj_pos[1] >= self.height and obj_pos[1]< 5000:
            # если объект вышел за нижнюю границу холста, перемещаем его в верхнюю границу
			self.canvas.coords(self.entity, obj_pos[0], 0)

	def hide(self, ind, pos=None):
		if pos == None:
			pos = self.canvas.coords(self.entity)
		if not self.game_pause:
        # перемещаем объект за границы холста
			self.canvas.coords(self.entity, 100000, 100000)
			ind -= 1
			if ind <= 0:
				self.canvas.coords(self.entity, pos[0], pos[1])
			else:
				self.canvas.after(1000,self.hide, ind, pos)
		else:
			self.canvas.after(1,self.hide, ind, pos)


class Player(Basic_Entity):

	# список врагов, который используется всеми объектами класса
	enemys = []

	# Создаем словарь для хранения направлений игрока
	direction = {
		"w": "Up",
		"a": "Left",
		"s": "Down",
		"d": "Right"
	}

	# Переменные для прыжка игрока
	jump = False
	kd_jump = True

	def __init__(self, canvas, x, y):
		# Загружаем изображения для разных направлений движения игрока
		self.ImageDown = [tk.PhotoImage(file = "image/Player/Down.gif", format = 'gif -index %i' %i) for i in range(3)]
		self.ImageUp = [tk.PhotoImage(file = "image/Player/Up.gif", format = 'gif -index %i' %i) for i in range(3)]
		self.ImageLeft = [tk.PhotoImage(file = "image/Player/Left.gif", format = 'gif -index %i' %i) for i in range(3)]
		self.ImageRight = [tk.PhotoImage(file = "image/Player/Right.gif", format = 'gif -index %i' %i) for i in range(3)]
		super().__init__(canvas, x, y)
		self.hp = tk.IntVar(value=100)
		self.lbl_jump = tk.StringVar(value="Можно")

	def keypress(self, event):
		try:
			# Проверяем, прыгает ли игрок, и двигаемся соответствующим образом
			if self.jump == True and self.kd_jump == True:
				self.movement(self.direction[event.keysym])
				self.movement(self.direction[event.keysym])
				self.movement(self.direction[event.keysym])
				self.movement(self.direction[event.keysym])
				# Запрещаем игроку прыгать после выполнения прыжка на 5 секунд
				self.kd_jump = False
				self.update_time(5)
			else:
				self.movement(self.direction[event.keysym])
		except:
			pass

	def update_time(self, index):
		if not self.game_pause:
			self.lbl_jump.set(value=str(index))
			index -=1
			if index > 0:
				self.canvas.after(1000, self.update_time, index)
			else:
				self.kd_jump = True
				self.lbl_jump.set(value="Можно")
		else:
			self.canvas.after(1, self.update_time, index)

	def Check_Damage(self):
		# Проверяем столкновение игрока и врага
		for enemy in self.enemys:
			if self.canvas.coords(self.entity) == self.canvas.coords(enemy.entity):
				# Если игрок и враг находятся на одной позиции, то у игрока отнимается здоровье
				self.hp.set(self.hp.get()-4)
				return True
		return False


class Enemy_type_0():
	def __init__(self, canvas, x, y):
		# Создаем экземпляр класса Enemy_type_0 с заданными параметрами
		# canvas - холст на котором будет нарисована картинка врага
		# x, y - координаты, где будет нарисована картинка врага
		self.Image = tk.PhotoImage(file = "image/Obstacle.png")
		# Загружаем изображение врага из файла "image/Obstacle.png"
		self.entity = canvas.create_image(x, y, image = self.Image, anchor='nw')
		# Создаем изображение врага на холсте canvas в координатах x, y
		# с использованием изображения, загруженного ранее и привязываем его к левому верхнему углу

	def hide(self):
		# Метод, который скрывает объект врага. Ничего не делает, так как не реализовано удаление объекта.
		pass


class Enemy_type_1(Basic_Entity):
	def __init__(self, canvas, x, y):
		# Загрузка изображений для разных направлений движения
		self.ImageDown = [tk.PhotoImage(file = "image/Enemy_1/Down.gif", format = 'gif -index %i' %i) for i in range(3)]
		self.ImageUp = [tk.PhotoImage(file = "image/Enemy_1/Up.gif", format = 'gif -index %i' %i) for i in range(3)]
		self.ImageLeft = [tk.PhotoImage(file = "image/Enemy_1/Left.gif", format = 'gif -index %i' %i) for i in range(3)]
		self.ImageRight = [tk.PhotoImage(file = "image/Enemy_1/Right.gif", format = 'gif -index %i' %i) for i in range(3)]
		# Вызов конструктора родительского класса
		super().__init__(canvas, x, y)

	# Определение функции move, используя лямбда-функцию
	move = lambda self: self.movement(random.choice(("Up", "Left", "Down", "Right")))


class Enemy_type_2(Basic_Entity):
    
    # Объявляем список всех врагов второго типа.
    enemys_type_2 = []
    
    def __init__(self, canvas, x, y, player):
        self.player = player
        
        # Загружаем изображения для врагов.
        self.ImageDown = [tk.PhotoImage(file = "image/Enemy_2/Down.gif", format = 'gif -index %i' %i) for i in range(3)]
        self.ImageUp = [tk.PhotoImage(file = "image/Enemy_2/Up.gif", format = 'gif -index %i' %i) for i in range(3)]
        self.ImageLeft = [tk.PhotoImage(file = "image/Enemy_2/Left.gif", format = 'gif -index %i' %i) for i in range(3)]
        self.ImageRight = [tk.PhotoImage(file = "image/Enemy_2/Right.gif", format = 'gif -index %i' %i) for i in range(3)]
        
        # Вызываем конструктор базового класса.
        super().__init__(canvas, x, y)

    def move(self):
        # Получаем позиции игрока и врага.
        player_pos = self.canvas.coords(self.player.entity)
        enemy_pos = self.canvas.coords(self.entity)
        
        # Вычисляем расстояния между игроком и врагом по осям X и Y.
        distance_X = enemy_pos[0] - player_pos[0]
        distance_Y = enemy_pos[1] - player_pos[1]
        
        # Выбираем направление движения врага на основе расстояний по осям X и Y.
        if abs(distance_X) > abs(distance_Y) and distance_X > 0:
            self.movement("Left")
            self.image = self.ImageLeft
        elif abs(distance_X) > abs(distance_Y) and distance_X < 0:
            self.movement("Right")
            self.image = self.ImageRight
        elif abs(distance_X) <= abs(distance_Y) and distance_Y < 0:
            self.movement("Down")
            self.image = self.ImageDown
        elif abs(distance_X) <= abs(distance_Y) and distance_Y > 0:
            self.movement("Up")
            self.image = self.ImageUp

    def movement(self, direction):
        # Получаем текущую позицию врага.
        enemy_pos = self.canvas.coords(self.entity)
        
        # Обновляем позицию врага в зависимости от направления.
        if direction == "Up":
            enemy_pos = [x+y for x, y in zip(enemy_pos, [0, -48])]
        elif direction == "Down":
            enemy_pos = [x+y for x, y in zip(enemy_pos, [0, 48])]
        elif direction == "Left":
            enemy_pos = [x+y for x, y in zip(enemy_pos, [-48, 0])]
        elif direction == "Right":
            enemy_pos = [x+y for x, y in zip(enemy_pos, [48, 0])]
        
        # Проверяем, есть ли препятствия на новой позиции в новой позиции 
        obstacles = False 

        for enemy in self.enemys_type_2:
            if enemy_pos == self.canvas.coords(enemy.entity):
                obstacles = True
                break

        if not obstacles:
            self.canvas.coords(self.entity, *enemy_pos)


class Fire():

	def __init__(self, canvas):
		self.canvas = canvas

		# Загрузка изображения огня
		self.Image = [tk.PhotoImage(file = "image/Fire.gif", format = 'gif -index %i' %i) for i in range(8)]
		
		# Создание сущности на холсте с начальными координатами (10000, 10000) и изображением self.Image[0]
		self.entity = self.canvas.create_image(10000, 10000, image = self.Image[0], anchor='nw')

		# Запуск анимации огня
		self.animations(0)

	def animations(self, ind):
		# Установка изображения огня на сущность на холсте
		self.canvas.itemconfig(self.entity,image=self.Image[ind%8])

	def Fire_on(self, event):
		# Получение координат курсора мыши при щелчке
		x = (event.x//48) * 48
		y = (event.y//48) * 48
		
		# Установка координат сущности на холсте на полученные координаты
		self.canvas.coords(self.entity, x, y)
		
	def Fire_off(self):
		# Скрытие сущности за пределами холста
		self.canvas.coords(self.entity, 10000, 10000)