import pyxel


class App:
    __cell_size = 10
    
    # w/h - количество клеток на поле 
    def __init__(self, w, h, cell_size=None):
        if cell_size is not None:
            self.__cell_size = cell_size
        
        self.__field = [[False for j in range(w)] for i in range(h)]
        self.__field_b = [[False for j in range(w)] for i in range(h)]
        
        pyxel.init(width = w * self.__cell_size, height = h * self.__cell_size, title='livegame')
        pyxel.mouse(True)
        pyxel.run(self.update_set, self.draw)
        
        
    def update_set(self):
        x = pyxel.mouse_x // self.__cell_size
        y = pyxel.mouse_y // self.__cell_size 
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):   
            self.__field[y][x] = True 
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.__field[y][x] = False  
            
        elif pyxel.btnp(pyxel.KEY_RETURN):
            pyxel.run(self.update_game, self.draw)
    
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        
        x, y = 0, 0
        while y < len(self.__field):
            while x < len(self.__field[y]):
                if self.__field[y][x]:
                    pyxel.rect(
                        x * self.__cell_size, 
                        y * self.__cell_size, 
                        self.__cell_size, 
                        self.__cell_size, 
                        pyxel.COLOR_WHITE
                    )
                x += 1
            x = 0
            y += 1
    
    
    def update_game(self):
        x, y = 0, 0
        while y < len(self.__field):
            while x < len(self.__field[y]):
                count_neighbors = self.__count_neighbors(x, y)
                
                if not self.__field[y][x] and count_neighbors == 3:
                   self.__field_b[y][x] = True
                elif self.__field[y][x] and (count_neighbors < 2 or count_neighbors > 3):
                    self.__field_b[y][x] = False
                else:
                    self.__field_b[y][x] = self.__field[y][x] 
                x += 1
            x = 0
            y += 1
        
        for y in range(len(self.__field)):
            for x in range(len(self.__field[y])):
                self.__field[y][x] = self.__field_b[y][x]
                
    
    # проверка клеток вокруг
    def __count_neighbors(self, x: int, y: int) -> int:
        count: int = 0
        
        y_pl = (y + 1) % len(self.__field)
        x_pl = (x + 1) % len(self.__field[0])
        
        # int(True) == 1
        # int(False) == 0
        
        count += int(self.__field[y-1][x-1])   # [*][*][*]
        count += int(self.__field[y-1][x])     # [ ][x][ ]  
        count += int(self.__field[y-1][x_pl])  # [ ][ ][ ]
        
        count += int(self.__field[y][x-1])     # [ ][ ][ ]
        count += int(self.__field[y][x_pl])    # [*][x][*]  
                                               # [ ][ ][ ]
                                             
        count += int(self.__field[y_pl][x-1])  # [ ][ ][ ]
        count += int(self.__field[y_pl][x])    # [ ][x][ ]  
        count += int(self.__field[y_pl][x_pl]) # [*][*][*]
        
        return count