from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage
from kivy.animation import Animation
import numpy, random, time, threading


class MyApp(App):

    def __init__(self):
        super().__init__()
        Window.size = (800, 600)
        wind = str(Window.size)
        self.wid = int(wind[1:wind.find(',')])
        self.hei = int(wind[wind.find(' ') + 1:-1])
        self.razm = (self.wid / self.hei)
        self.fl = FloatLayout()
        self.score = 0
        self.anch_score = AnchorLayout(anchor_y="top", anchor_x="left")
        self.btn_score = Button(text=str(self.score), font_size=30, size_hint=(0.1, 0.1*self.razm), background_color=[132/255, 132/255, 132/255, 1], background_normal='', background_down='')
        self.anch_score.add_widget(self.btn_score)
        self.fl.add_widget(self.anch_score)
        self.start_move, self.end_move = None, None
        self.size = 5
        self.objs = numpy.zeros((self.size, self.size), dtype=Button)
        self.key = 0
        self.imgs = ["red_diamond.png", "green_diamond.png", "blue_diamond.png", "yellow_diamond.png"]
        self.colors = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 0, 1]]
        self.position = numpy.zeros((self.size, self.size), "int")
        self.tegs = numpy.zeros((self.size, self.size), 'int')
        self.anim_com = 0
        self.old_cord = [None, None]
        self.new_cord = [None, None]
        self.edited_blocks = []
        for i in range(self.size):
            for j in range(self.size):
                k = random.randint(1, 4)
                self.position[i][j] = k
                self.objs[i][j] = Button(size_hint=((1 - 0.01 * self.size) / self.size, self.razm * (1 - self.size * 0.01) / self.size),
                                         pos=(0.005 * self.wid + j * self.wid / self.size, 0.005 * self.wid + (self.size - 1 - i) * self.wid / self.size), background_normal='', background_down='')
                self.objs[i][j].bind(on_touch_down=self.SaveTouch)
                self.objs[i][j].bind(on_touch_up=self.UseSwipe)
                self.fl.add_widget(self.objs[i][j])
                '''img = AsyncImage(source=self.imgs[k - 1], pos=self.objs[i][j].pos)
                self.objs[i][j].add_widget(img)'''
        self.activation_without_animation([0, 0], [0, 0])
        self.Create()

    def build(self):
        return self.fl

    def Create(self):
        for i in range(4):
            for x, y in numpy.argwhere(self.position == i+1):
                self.objs[x][y].background_color = self.colors[i]
                '''img = AsyncImage(source=self.imgs[i], pos=self.objs[x][y].pos)
                self.objs[x][y].clear_widgets()
                self.objs[x][y].add_widget(img)'''

    def StopAnimation(self, anim, obj):
        # print(anim, obj)
        self.activation(self.old_cord, self.new_cord)

    def SaveTouch(self, obj, touch):
        if touch.pos[1] > self.wid:
            return -1
        if not self.start_move:
            self.start_move = touch.pos
            #print(self.start_move)
            self.key = 1

    def UseSwipe(self, obj, touch):
        if touch.pos[1] > self.wid:
            return -1
        if not self.end_move and self.key:
            self.end_move = touch.pos
            # print(self.end_move)
            dx, dy = [self.end_move[0] - self.start_move[0], self.end_move[1] - self.start_move[1]]
            x, y = int((self.start_move[0] - 0.005 * self.wid) * self.size / self.wid), self.size - 1 - int((self.start_move[1] - 0.005 * self.wid) * self.size / self.wid)
            left, right, down, up = -1, -1, -1, -1
            if y < 9:
                down = y + 1
            if y > 0:
                up = y - 1
            if x > 0:
                left = x - 1
            if x < 9:
                right = x + 1
            if abs(dx) == abs(dy):
                pass
            if abs(dx) > abs(dy):
                if dx > 0 and right != -1:
                    anim1 = Animation(x=self.objs[y][x].pos[0], y=self.objs[y][x].pos[1], duration=0.5)
                    anim2 = Animation(x=self.objs[y][right].pos[0], y=self.objs[y][right].pos[1], duration=0.5)
                    anim1.bind(on_complete=self.StopAnimation)
                    self.old_cord, self.new_cord = [y, x], [y, right]
                    anim1.start(self.objs[y][right])
                    anim2.start(self.objs[y][x])
                    self.objs[y][x], self.objs[y][right] = self.objs[y][right], self.objs[y][x]
                    self.position[y][x], self.position[y][right] = self.position[y][right], self.position[y][x]
                elif dx < 0 and left != -1:
                    anim1 = Animation(x=self.objs[y][x].pos[0], y=self.objs[y][x].pos[1], duration=0.5)
                    anim2 = Animation(x=self.objs[y][left].pos[0], y=self.objs[y][left].pos[1], duration=0.5)
                    anim1.bind(on_complete=self.StopAnimation)
                    self.old_cord, self.new_cord = [y, x], [y, left]
                    anim1.start(self.objs[y][left])
                    anim2.start(self.objs[y][x])
                    self.objs[y][x], self.objs[y][left] = self.objs[y][left], self.objs[y][x]
                    self.position[y][x], self.position[y][left] = self.position[y][left], self.position[y][x]
            else:
                if dy > 0 and up != -1:
                    anim1 = Animation(x=self.objs[y][x].pos[0], y=self.objs[y][x].pos[1], duration=0.5)
                    anim2 = Animation(x=self.objs[up][x].pos[0], y=self.objs[up][x].pos[1], duration=0.5)
                    anim1.bind(on_complete=self.StopAnimation)
                    self.old_cord, self.new_cord = [y, x], [up, x]
                    anim1.start(self.objs[up][x])
                    anim2.start(self.objs[y][x])
                    self.objs[y][x], self.objs[up][x] = self.objs[up][x], self.objs[y][x]
                    self.position[y][x], self.position[up][x] = self.position[up][x], self.position[y][x]
                elif dy < 0 and down != -1:
                    anim1 = Animation(x=self.objs[y][x].pos[0], y=self.objs[y][x].pos[1], duration=0.5)
                    anim2 = Animation(x=self.objs[down][x].pos[0], y=self.objs[down][x].pos[1], duration=0.5)
                    anim1.bind(on_complete=self.StopAnimation)
                    self.old_cord, self.new_cord = [y, x], [down, x]
                    anim1.start(self.objs[down][x])
                    anim2.start(self.objs[y][x])
                    self.objs[y][x], self.objs[down][x] = self.objs[down][x], self.objs[y][x]
                    self.position[y][x], self.position[down][x] = self.position[down][x], self.position[y][x]
            # self.Create()
            self.key = 0
        elif not self.key:
            self.end_move, self.start_move = None, None

    def activation_without_animation(self, pos_1, pos_2):
        # при возможности избавитсья от нужды жкзмепляра, ибо выглядит криво
        # функция для активации, при попытке изменения запускается жтот сркипт
        # и проверяет возомжно ли изменение поля, если да то возварзает 1
        # меняем местами
        self.position[pos_1[0]][pos_1[1]], self.position[pos_2[0]][pos_2[1]] = self.position[pos_2[0]][pos_2[1]], \
                                                                               self.position[pos_1[0]][pos_1[1]]
        self.update()
        if self.tegs.any() > 0:
            while self.tegs.any() > 0:  # при случае считаь при заполеннии  для усорения
                self.score += self.tegs.sum()
                # print(self.score)
                # вызщываем уборщика и он подметает матрицу
                self.delete()
                self.update()
            return 1
        # меняем местамив в слуае неудачи
        self.position[pos_1[0]][pos_1[1]], self.position[pos_2[0]][pos_2[1]] = self.position[pos_2[0]][pos_2[1]], \
                                                                               self.position[pos_1[0]][pos_1[1]]
        return 0

    def activation(self, pos_1, pos_2):
        '''self.position[pos_1[0]][pos_1[1]], self.position[pos_2[0]][pos_2[1]] = self.position[pos_2[0]][pos_2[1]], \
                                                                               self.position[pos_1[0]][pos_1[1]]'''
        self.update()
        if self.tegs.any() > 0:
            while self.tegs.any() > 0:  # при случае считать при заполеннии  для ускорения
                self.score += self.tegs.sum()
                self.btn_score.text=str(self.score)
                # print(self.score)
                # вызщываем уборщика и он подметает матрицу
                self.delete_with_animation()
                self.update()
            return 1
        # меняем местамив в слуае неудачи
        # self.position[pos_1[0]][pos_1[1]], self.position[pos_2[0]][pos_2[1]] = self.position[pos_2[0]][pos_2[1]], \
        #                                                                        self.position[pos_1[0]][pos_1[1]]
        y, x = pos_1
        y_new, x_new = pos_2
        anim1 = Animation(x=self.objs[y][x].pos[0], y=self.objs[y][x].pos[1], duration=0.5)
        anim2 = Animation(x=self.objs[y_new][x_new].pos[0], y=self.objs[y_new][x_new].pos[1], duration=0.5)
        anim1.start(self.objs[y_new][x_new])
        anim2.start(self.objs[y][x])
        self.objs[y][x], self.objs[y_new][x_new] = self.objs[y_new][x_new], self.objs[y][x]
        self.position[y][x], self.position[y_new][x_new] = self.position[y_new][x_new], self.position[y][x]
        return 0

    def update(self):
        # заполяняет target полями для очищения(Везле где больше нуля трбуется смена)
        for id in range(self.size):
            string = self.position[id]
            index = 2
            while index < len(string):
                if string[index] != string[index - 1]:
                    index += 2
                elif string[index - 1] != string[index - 2]:
                    index += 1
                else:
                    self.tegs[id][index - 2:index + 1] = [x + 1 for x in self.tegs[id][index - 2:index + 1]]  # заполняем
                    index += 1
        # транспонируем и проверяем диагональные значения
        self.tegs, self.position = self.tegs.transpose(), self.position.transpose()
        for id in range(self.size):
            string = self.position[id]
            index = 2
            while index < len(string):
                if string[index] != string[index - 1]:
                    index += 2
                elif string[index - 1] != string[index - 2]:
                    index += 1
                else:
                    self.tegs[id][index - 2:index + 1] = [x + 1 for x in self.tegs[id][index - 2:index + 1]]  # заполняем
                    index += 1
        self.tegs, self.position = self.tegs.transpose(), self.position.transpose()

    def delete(self):
        # фunction для чистки матрицы
        for x, y in numpy.argwhere(self.tegs):  # неявно вызывает nonzero() поэтому работает быстрее place()
            self.position[x][y] = 0
            # все...больше не могу...ахххх...это прекрасно...
            self.tegs = numpy.zeros((self.size, self.size), 'int')  # менее эффективно чем протсо прирванивать к 0
        for x in range(self.size):
            a = self.position[..., x]  # для читаемости
            self.position[..., x] = numpy.concatenate((a[a == 0], a[a != 0]), axis=None) # соединяем и преобразуем в инт
            # animation
        for x, y in numpy.argwhere(self.position == 0):
            k = random.randint(1, 4)
            self.position[x][y] = k
        self.Create()

    def delete_with_animation(self):
        # фunction для чистки матрицы
        for x, y in numpy.argwhere(self.tegs):  # неявно вызывает nonzero() поэтому работает быстрее place()
            self.position[x][y] = 0
            self.objs[x][y].background_color = [0, 0, 0, 0]
            # все...больше не могу...ахххх...это прекрасно...
            self.tegs = numpy.zeros((self.size, self.size), 'int')  # менее эффективно чем протсо прирванивать к 0
        print(self.position)
        for x in range(self.size):
            key = 0
            y = self.size - 1
            while y > -1 and self.position[y][x]:
                y -= 1
            while y > -1 and not self.position[y][x]:
                key += 1
                y -= 1
            while y > -1 and self.position[y][x]:
                anim1 = Animation(y=self.objs[y+key][x].pos[1], duration=0.5)
                anim1.bind(on_complete=self.CompleteAnimation)
                anim1.start(self.objs[y][x])
                # self.objs[y][x], self.objs[y+key][x] = self.objs[y+key][x], self.objs[y][x]
                self.position[y][x], self.position[y+key][x] = self.position[y+key][x], self.position[y][x]
                y -= 1
            '''for y in range(self.size - 1, -1, -1):
                y_new = y + numpy.count_nonzero(self.position[..., x][y + 1:] == 0)
                print(x, y, y_new)
                if y != y_new and self.position[y][x]:
                    key = max(key, y_new - y)
                    anim1 = Animation(y=self.objs[y_new][x].pos[1], duration=0.5)
                    anim1.bind(on_complete=self.CompleteAnimation)
                    anim2 = Animation(y=self.objs[y][x].pos[1], duration=0.5)
                    anim2.bind(on_complete=self.CompleteAnimation)
                    anim1.start(self.objs[y][x])
                    # anim2.start(self.objs[y_new][x])
                    self.objs[y][x], self.objs[y_new][x] = self.objs[y_new][x], self.objs[y][x]
                    self.position[y][x], self.position[y_new][x] = self.position[y_new][x], self.position[y][x]
                elif not self.position[y][x]:
                    while y < self.size and not self.position[y][x]:
                        self.objs[y][x].pos[1] += key * self.wid / self.size'''
        self.edited_blocks = []
        for x, y in numpy.argwhere(self.position == 0):
            k = random.randint(1, 4)
            self.position[x][y] = k
            self.edited_blocks.append([x, y])
        print(self.position)
        self.CompleteAnimation(0, 0)
        '''thread = threading.Thread(target=self.CompleteAnimation(0, 0))
        thread.start()'''

    def CompleteAnimation(self, anim, obj):
        # time.sleep(0.5)
        for el in self.edited_blocks:
            x, y = el
            self.objs[x][y].background_color = self.colors[self.position[x][y] - 1]


if __name__ == '__main__':
    MyApp().run()