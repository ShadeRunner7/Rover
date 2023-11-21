import math
import sqlite3
#import serial
import FA
from sqlite3 import Error
import tkinter as tk
from tkinter import messagebox
import sys
from rover_script import *

isready = False
array = []
userstart = None 
userend = None

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maze (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                row INTEGER,
                col INTEGER,
                value INTEGER
            )
        ''')
        conn.commit()
    except Error as e:
        print(e)

def insert_maze(conn, maze):
    try:
        cursor = conn.cursor()
        for row_num, row in enumerate(maze):
            for col_num, value in enumerate(row):
                cursor.execute('''
                    INSERT INTO maze (row, col, value)
                    VALUES (?, ?, ?)
                ''', (row_num, col_num, value))
        conn.commit()
    except Error as e:
        print(e)

def retrieve_maze(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM maze')
        rows = cursor.fetchall()

        # Assuming the maze dimensions are fixed (11x11), you can reconstruct the array
        retrieved_array = [[0 for _ in range(11)] for _ in range(11)]

        for row in rows:
            retrieved_array[row[1]][row[2]] = row[3]

        return retrieved_array

    except Error as e:
        print(e)

def save_maze_to_database(maze):
    try:
        conn = create_connection('maze.db')
        if conn is not None:
            create_table(conn)

            # Empty the existing table
            cursor = conn.cursor()
            cursor.execute('DELETE FROM maze')
            conn.commit()

            # Insert the new maze
            insert_maze(conn, maze)
            conn.close()
            print("Maze saved to database successfully.")
    except Error as e:
        print(e)

def check_port():
    global userstart
    global userend
    comPort = entry.get()
    open_comms(comPort)
    try:
        start_x_val = int(start_x.get())
        start_y_val = int(start_y.get())
        end_x_val = int(end_x.get())
        end_y_val = int(end_y.get())
    except ValueError:
        start_x_val = None
        start_y_val = None
        end_x_val = None
        end_y_val = None
    userstart = (start_x_val, start_y_val)
    userend = (end_x_val,end_y_val)

    try:
        start_x_val = int(start_x.get())
        start_y_val = int(start_y.get())
        end_x_val = int(end_x.get())
        end_y_val = int(end_y.get())
        if 0<start_x_val<10 and 0<start_y_val<10 and 0<end_x_val<10 and 0<end_y_val<10:
            userstart = (start_x_val, start_y_val)
            userend = (end_x_val,end_y_val)
            root.destroy()  # Close the Tkinter window'

        else:
            messagebox.showerror("Error", "Coordinate must be between 0 and 10.")
    except ValueError:
        messagebox.showerror("Error", "Give coordinates in right format.")


def retrieve_maze_from_database():
    try:
        conn = create_connection('maze.db')
        if conn is not None:
            retrieved_maze = retrieve_maze(conn)
            conn.close()
            try:
                printarray(retrieved_maze)
                return retrieved_maze
            except:
                print("No maze")
    except Error as e:
        print(e)


def create_grid_app(master, array):
    rows = len(array)
    cols = len(array[0])
    grid_values = array

    def toggle_value(row, col):
        nonlocal grid_values
        global userend
        global userstart    
        grid_values[row][col] = 1 - grid_values[row][col]
       
       
        # Change color based on the value in the array
        if grid_values[row][col] == 1:
            buttons[row][col].configure(bg='red')
        else:
            buttons[row][col].configure(bg='green')
       
    # Specify the coordinates where you want the buttons to be blue
    blue_coordinates = [userend,userstart]  # Add your desired coordinates
    grid_values[userend[0]][userend[1]]=0
    grid_values[userstart[0]][userstart[1]]=0
    buttons = [
        [
            tk.Button(
                master,
                text="",
                image=tk.PhotoImage(width=1, height=1),
                width=30,
                height=30,
                compound="c",
                bg='blue' if (row, col) in blue_coordinates else ('red' if grid_values[row][col] == 1 else 'green'),
                command=(lambda row=row, col=col: toggle_value(row, col)) if (row, col) not in blue_coordinates else None
            )
            for col in range(0, cols)
        ]
        for row in range(0, rows)
    ]

    for row, button_row in enumerate(buttons):
        for col, button in enumerate(button_row):
            button.grid(row=row, column=col)

    # Create the "Start" button below the grid
    def on_button_click():
        # Add meaningful functionality here
        print("Start button clicked!")
        global isready
        isready=True
        root.destroy()

    start_button = tk.Button(master, text="Start", command=on_button_click)
    start_button.grid(row=rows, columnspan=cols)

# Create the root window
root = tk.Tk()
root.title("Port Checker")

# Create and place widgets in the window
label_port = tk.Label(root, text="Enter Port Number:")
label_port.pack(pady=10)

entry = tk.Entry(root)
entry.insert(0, 3)
entry.pack(pady=10)

label_start = tk.Label(root, text="Enter Start Coordinates (0-10):")
label_start.pack(pady=5)

start_x = tk.Entry(root, width=5)
start_x.insert(0, 9)
start_x.pack(pady=5)
start_y = tk.Entry(root, width=5)
start_y.insert(0, 1)
start_y.pack(pady=5)

label_end = tk.Label(root, text="Enter End Coordinates (0-10):")
label_end.pack(pady=5)

end_x = tk.Entry(root, width=5)
end_x.insert(0, 3)
end_x.pack(pady=5)
end_y = tk.Entry(root, width=5)
end_y.insert(0, 3)
end_y.pack(pady=5)

button = tk.Button(root, text="Check Port", command=check_port)
button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

def printarray(array):
    for row in array:
        for element in row:
            print(element, end="\t")
        print()
# Code under if __name__ == "__main__": should be indented properly

def main():
    global array
    
    maze = array
    
    start = userstart
    end = userend
    print(type(start))
    print(type(start[0]))
    path = a_star(maze, start, end)
    navigate()
    printarray(maze)
    save_maze_to_database(array)

if __name__ == "__main__":
    root = tk.Tk()
    retrieved_maze = retrieve_maze_from_database()
    defaultarray = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
    if not retrieved_maze:
        # If no maze is retrieved, use the default maze
        retrieved_maze = defaultarray
    array = retrieved_maze

    create_grid_app(root, array)
    root.mainloop()
    
    print("skipped")
    if isready == False:
        print("Ei valmiina")
        sys.exit()
    print("koodia")
    main()