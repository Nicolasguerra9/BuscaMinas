import tkinter as tk
import random
import time

class BuscaminasGUI:
    def __init__(self, master):
        self.master = master
        self.filas = 5
        self.columnas = 5
        self.num_bombas = 5
        self.tiempo_inicio = None
        self.botones = []

        self.generar_bombas()
        self.crear_interfaz()

    def generar_bombas(self):
        self.tablero = [[' ' for _ in range(self.columnas)] for _ in range(self.filas)]
        bombas_generadas = 0
        while bombas_generadas < self.num_bombas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if self.tablero[fila][columna] != '*':
                self.tablero[fila][columna] = '*'
                bombas_generadas += 1

    def mostrar_bomba(self, fila, columna):
        if self.tablero[fila][columna] == '*':
            for i in range(self.filas):
                for j in range(self.columnas):
                    if self.tablero[i][j] == '*':
                        self.botones[i][j].config(text='X', state='disabled', relief='sunken', bg='red')
            self.mostrar_mensaje("¡Has perdido! Una bomba ha explotado.")
        else:
            num_bombas_alrededor = self.contar_bombas_alrededor(fila, columna)
            self.botones[fila][columna].config(text=str(num_bombas_alrededor), state='disabled', relief='sunken', bg='light green')

    def contar_bombas_alrededor(self, fila, columna):
        count = 0
        for i in range(max(0, fila - 1), min(self.filas, fila + 2)):
            for j in range(max(0, columna - 1), min(self.columnas, columna + 2)):
                if self.tablero[i][j] == '*':
                    count += 1
        return count

    def mostrar_mensaje(self, mensaje):
        self.mensaje.config(text=mensaje)

    def crear_interfaz(self):
        self.master.title("Buscaminas")

        for i in range(self.filas):
            fila_botones = []
            for j in range(self.columnas):
                boton = tk.Button(self.master, text=' ', width=4, height=2, bg='grey',
                                  command=lambda f=i, c=j: self.mostrar_bomba(f, c))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

        self.mensaje = tk.Label(self.master, text="")
        self.mensaje.grid(row=self.filas, columnspan=self.columnas)

def main():
    root = tk.Tk()
    juego = BuscaminasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
