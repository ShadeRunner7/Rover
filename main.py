import sqlite3
import FA
#import serial
#import sys

from rover_script import *
from tkinter import *
from tkinter import ttk
from sqlite3 import Error

class GUI:    
    def __init__(self, root, maze, angle, dist):
        self.root = root
        root.title("Test GUI")
        s = ttk.Style()
        self.map_buttons = []
        self.maze = []
        
        for x in range(len(maze)):
            self.maze.append(maze[x])
        
        self.start_and_goal = self.check()
        #print(self.start_and_goal)
        
        self.null_img = PhotoImage(width=0, height=0)
        s.configure('grid.TLabel', 
            #compound='c',
            image=self.null_img,
            padding=25)
        s.configure('grid.TLabel', background='white')
        s.configure('wall.grid.TLabel', background='red')
        s.configure('start.grid.TLabel', background='green')
        s.configure('goal.grid.TLabel', background='blue')
        
        self.MAP_WIDTH = MAP_WIDTH = 11     
        
        frame = ttk.Frame(root, padding="30") #padding="left, top, right, bottom"
        frame.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        
        mapframe = ttk.Frame(frame, padding=(5, 5, 5, 30))
        mapframe.grid(column=2, row=0, rowspan=1000)
        
        for x in range(MAP_WIDTH):
            ttk.Label(mapframe, text=str(x)).grid(column=x+1, row=0)
            ttk.Label(mapframe, text=str(x)).grid(column=0, row=x+1)
        
        for x in range((MAP_WIDTH)**2):
            r = int(x/MAP_WIDTH)%MAP_WIDTH + 1
            col = x%MAP_WIDTH + 1
            match self.maze[x]:
                case '1':
                    style_ = 'wall.grid.TLabel'
                case '2':
                    style_ = 'start.grid.TLabel'
                case '3':
                    style_ = 'goal.grid.TLabel'
                case _:
                    style_ = 'grid.TLabel'
            self.map_buttons.append(ttk.Button(mapframe,
                style=style_,
                command=(lambda y=x: self.click_f(y))))
            self.map_buttons[x].grid(column=col, row=r, sticky='NWES')
            
        ROW = 0
        ttk.Label(frame, text="Port Number").grid(column=0, row=ROW, columnspan=2)
        ROW += 1
        
        self.Port_Number = ttk.Spinbox(frame, from_=0, to=10, width=2)
        self.Port_Number.set(3) #Port default value
        self.Port_Number.grid(column=0, row=ROW, columnspan=2)
        ROW += 1
        
        ttk.Label(frame).grid(column=0, row=ROW)
        ROW += 1
        
        ttk.Label(frame, text="Angle").grid(column=0, row=ROW)
        ttk.Label(frame, text="Distance").grid(column=1, row=ROW)
        ROW += 1
        
        self.Move_Angle = ttk.Spinbox(frame, from_=80, to=90, increment=.5, width=4)
        self.Move_Angle.set(angle)
        self.Move_Angle.grid(column=0, row=ROW)
        
        self.Dist = ttk.Spinbox(frame, from_=85, to=100, increment=.5, width=4)
        self.Dist.set(dist)
        self.Dist.grid(column=1, row=ROW)
        ROW += 1
        
        ttk.Label(frame).grid(column=0, row=ROW)
        ROW += 1
        
        ttk.Button(frame, text="Flip", command=self.flip).grid(column=0, row=ROW, columnspan=2)
        ROW += 1
        
        ttk.Label(frame).grid(column=0, row=ROW)
        ROW += 1
        
        ttk.Button(frame, text="Start", command=(lambda: self.run())).grid(column=0, row=ROW, columnspan=2)
        ROW += 1
        
        ttk.Label(frame).grid(column=0, row=ROW)
        ROW += 1
        
        Quit_Button = ttk.Button(frame, text="Quit", command=self.close)
        Quit_Button.grid(column=0, row=ROW, columnspan=2)
        ROW += 1
        
        Quit_Button.focus()
        #root.bind("<Return>")
    
    def click_f(self, num):
        opt = self.map_buttons[num]['style']
        match self.start_and_goal:
            case 0 | 2:
                self.map_buttons[num]['style'] = 'start.grid.TLabel'
                self.maze[num] = '2'
                self.start_and_goal += 1
                if opt == 'goal.grid.TLabel':
                    self.start_and_goal -= 2
            case 1:
                self.map_buttons[num]['style'] = 'goal.grid.TLabel'
                self.maze[num] = '3'
                self.start_and_goal += 2
                if opt == 'start.grid.TLabel':
                    self.start_and_goal -= 1
            case 3:                
                match opt:
                    case 'grid.TLabel':
                        self.map_buttons[num]['style'] = 'wall.grid.TLabel'
                        self.maze[num] = '1'
                    case 'wall.grid.TLabel':
                        self.map_buttons[num]['style'] = 'grid.TLabel'
                        self.maze[num] = '0'
                    case 'start.grid.TLabel':
                        self.map_buttons[num]['style'] = 'grid.TLabel'
                        self.maze[num] = '0'
                        self.start_and_goal -= 1
                    case 'goal.grid.TLabel':
                        self.map_buttons[num]['style'] = 'grid.TLabel'
                        self.maze[num] = '0'
                        self.start_and_goal -= 2
        #print(self.start_and_goal)
    
    def check(self):
        """Return following:
        Return 0 when there is no start or end point
        Return 1 when there is a start
        Return 2 when there is a goal
        Return 3 when there is both
        """
        ret = 0
        for x in range(len(self.maze)):
            if self.maze[x] == '2':
                ret += 1
            if self.maze[x] == '3':
                ret += 2
        return ret
    
    def close(self):
        maze = ""
        for x in range(len(self.maze)):
            maze += self.maze[x]
        angle = self.Move_Angle.get()
        dist = self.Dist.get()
        SQL().save_maze(maze, angle, dist)
        self.root.destroy()

    def run(self):
        start = ()
        end = ()
        maze = [['' for i in range(self.MAP_WIDTH)] for j in range(self.MAP_WIDTH)]
                
        for x in range(len(self.maze)):
            if self.maze[x] == '2':
                start = int(x/self.MAP_WIDTH)%self.MAP_WIDTH, x%self.MAP_WIDTH
                #print("Start found at ", x)
            if self.maze[x] == '3':
                end = int(x/self.MAP_WIDTH)%self.MAP_WIDTH, x%self.MAP_WIDTH
                #print("End found at ", x)
        
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_WIDTH):
                if int(self.maze[x * self.MAP_WIDTH + y]) == (2 | 3):
                    maze[x][y] = 0
                else:
                    maze[x][y] = int(self.maze[x * self.MAP_WIDTH + y])
        #print(maze)
        
        #print(start, end)
        
        port = int(self.Port_Number.get())
        angle = float(self.Move_Angle.get())
        dist = float(self.Dist.get())
        
        try:
            open_comms(port)
            print("Connection successful")
        except:
            print("Is the rover on?")
            print("Port number: ", int(self.Port_Number.get()))
        
        path = a_star(maze, start, end)
        navigate(angle, dist)
    
    def flip(self):
        flip = 0
        for x in range(len(self.maze)):
            if self.maze[x] == '2':
                self.map_buttons[x]['style'] = 'goal.grid.TLabel'
                self.maze[x] = '3'
                x += 1
                flip += 1
            if self.maze[x] == '3':
                self.map_buttons[x]['style'] = 'start.grid.TLabel'
                self.maze[x] = '2'
                flip += 1
            if flip == 2:
                break
                


class SQL:
    def __init__(self):
        self.conn = sqlite3.connect('maze.db')
        self.cursor = self.conn.cursor()
    
    def get_maze(self):
        try:
            self.cursor.execute('SELECT * FROM maze LIMIT 1')
            maze_array = self.cursor.fetchall()
            
            return maze_array
            
        except Error as e:
            print(e)
        self.conn.close()
    
    def save_maze(self, maze, angle, dist):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS maze (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    maze_string TEXT,
                    angle NUMERIC,
                    distance NUMERIC                
                )
            ''')
            self.conn.commit()
            self.cursor.execute('DELETE FROM maze')
            self.conn.commit()
            self.cursor.execute('''
                    INSERT INTO maze (maze_string, angle, distance)
                    VALUES (?, ?, ?)
                ''', (maze, angle, dist))
            self.conn.commit()
        except Error as e:
            print(e)
        

def main():
    saved_maze = SQL().get_maze()[0]
    #print(saved_maze)
    default_maze = ""
    default_maze_array = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                          [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                          [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                          [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                          [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    
    for x in range(len(default_maze_array)):
        for y in range(len(default_maze_array[0])):
            default_maze += str(default_maze_array[x][y])
    if not saved_maze:
        maze = default_maze
        angle = 86
        dist = 87.5
    else:
        maze = str(saved_maze[1])
        angle = float(saved_maze[2])
        dist = float(saved_maze[3])
    
    
    root = Tk()
    GUI(root, maze, angle, dist)
    root.mainloop()

if __name__ == "__main__":
    main()