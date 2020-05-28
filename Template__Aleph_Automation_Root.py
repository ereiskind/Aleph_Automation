import tkinter as tk

from Template__GUI_Functions_Class import MainAppController

def main():

    controller = MainAppController()

    # Build Gui and start it
    root = tk.Tk()
    root.title('Main Application')

    controller.init_view(root)


    print ('Bye Bye') # Prints to terminal when window closes



if __name__ == "__main__":
    main()