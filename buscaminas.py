import tkinter as tk
import random
import time

class BuscaminasGUI:
    def __init__(self, master):
        self.master = master
        self.filas = 5
        self.columnas = 5
        self.num_bombas = 5
        self.artificieros_disponibles = self.num_bombas
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

    def contar_bombas_alrededor(self, fila, columna):
        count = 0
        for i in range(max(0, fila - 1), min(self.filas, fila + 2)):
            for j in range(max(0, columna - 1), min(self.columnas, columna + 2)):
                if self.tablero[i][j] == '*':
                    count += 1
        return count

    def mostrar_bomba(self, fila, columna):
        if self.tablero[fila][columna] == '*':
            for i in range(self.filas):
                for j in range(self.columnas):
                    if self.tablero[i][j] == '*':
                        self.botones[i][j].config(text='X', state='disabled', relief='sunken')
        else:
            num_bombas_alrededor = self.contar_bombas_alrededor(fila, columna)
            self.botones[fila][columna].config(text=str(num_bombas_alrededor), state='disabled', relief='sunken')

    def asignar_artificiero(self, fila, columna):
        if self.tablero[fila][columna] == '*':
            self.mostrar_bomba(fila, columna)
            self.mostrar_mensaje("No puedes asignar un artificiero en una celda con una bomba.")
        elif self.artificieros_disponibles > 0:
            self.tablero[fila][columna] = 'A'
            self.artificieros_disponibles -= 1
            self.botones[fila][columna].config(text='A', state='disabled', relief='raised')
            self.mostrar_mensaje("Artificiero asignado correctamente.")
        else:
            self.mostrar_mensaje("No tienes artificieros disponibles.")

    def desasignar_artificiero(self, fila, columna):
        if self.tablero[fila][columna] == 'A':
            self.tablero[fila][columna] = ' '
            self.artificieros_disponibles += 1
            self.botones[fila][columna].config(text=' ', state='normal', relief='raised')
            self.mostrar_mensaje("Artificiero desasignado correctamente.")
        else:
            self.mostrar_mensaje("No hay un artificiero asignado en esta celda.")

    def cortar_cable(self):
        for fila in self.tablero:
            if '*' in fila and 'A' not in fila:
                self.mostrar_bomba(fila.index('*'), fila.index('*'))
                self.mostrar_mensaje("¡Has perdido! Una bomba ha explotado.")
                return
        self.mostrar_mensaje("¡Felicidades! Has desactivado todas las bombas.")
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        self.mostrar_mensaje(f"Te tomó {int(tiempo_transcurrido)} segundos salvar la ciudad.")

    def mostrar_mensaje(self, mensaje):
        self.mensaje.config(text=mensaje)

    def crear_interfaz(self):
        self.master.title("Buscaminas")

        for i in range(self.filas):
            fila_botones = []
            for j in range(self.columnas):
                boton = tk.Button(self.master, text=' ', width=4, height=2,
                                  command=lambda f=i, c=j: self.mostrar_bomba(f, c))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

        self.mensaje = tk.Label(self.master, text="")
        self.mensaje.grid(row=self.filas, columnspan=self.columnas)

        asignar_artificiero_btn = tk.Button(self.master, text="Asignar Artificiero",
                                            command=lambda: self.mostrar_asignar_artificiero())
        asignar_artificiero_btn.grid(row=self.filas + 1, column=0)

        desasignar_artificiero_btn = tk.Button(self.master, text="Desasignar Artificiero",
                                               command=lambda: self.mostrar_desasignar_artificiero())
        desasignar_artificiero_btn.grid(row=self.filas + 1, column=1)

        cortar_cable_btn = tk.Button(self.master, text="Cortar Cable", command=self.cortar_cable)
        cortar_cable_btn.grid(row=self.filas + 1, column=2)

        self.tiempo_inicio = time.time()

    def mostrar_asignar_artificiero(self):
        asignar_artificiero_window = tk.Toplevel()
        asignar_artificiero_window.title("Asignar Artificiero")

        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] != '*':
                    boton = tk.Button(asignar_artificiero_window, text=f"{i},{j}",
                                      command=lambda f=i, c=j: self.asignar_artificiero(f, c))
                    boton.grid(row=i, column=j)

    def mostrar_desasignar_artificiero(self):
        desasignar_artificiero_window = tk.Toplevel()
        desasignar_artificiero_window.title("Desasignar Artificiero")

        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] == 'A':
                    boton = tk.Button(desasignar_artificiero_window, text=f"{i},{j}",
                                      command=lambda f=i, c=j: self.desasignar_artificiero(f, c))

                    boton.grid(row=i, column=j)

def main():
    root = tk.Tk()
    juego = BuscaminasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
