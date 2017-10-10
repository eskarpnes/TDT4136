from tkinter import *

class VentanaPlay():

    def __init__(self):

        self.matriz = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

        self.all_buttons = []

        self.ventana = Tk()
        self.ventana.title('Ejemplo')

        #self.long_x = len(self.matriz)

        #self.long_y = len(self.matriz[0])

        self.creaMatriz()

    def run(self):
        self.ventana.mainloop()


    def creaMatriz(self):
        for y, row in enumerate(self.matriz):
            buttons_row = []
            for x, element in enumerate(row):
                boton = Button(self.ventana, width=10, height=5, command=lambda a=x,b=y: self.onButtonPressed(a,b))
                boton.grid(row=y, column=x)
                buttons_row.append( boton )
            self.all_buttons.append( buttons_row )

    def onButtonPressed(self, x, y):
        print( "pressed: x=%s y=%s" % (x, y) )
        if self.all_buttons[y][x]['bg'] == 'red':
            self.all_buttons[y][x]['bg'] = 'green'
        else:
            self.all_buttons[y][x]['bg'] = 'red'

VentanaPlay().run()