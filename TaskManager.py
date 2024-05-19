import tkinter as tk  # Importa el módulo tkinter para la interfaz gráfica
from tkinter import messagebox  # Importa el módulo messagebox para mostrar diálogos de mensajes
import json  # Importa el módulo json para trabajar con archivos JSON
import os  # Importa el módulo os para interactuar con el sistema operativo

# Clase que representa una tarea
class Task:
    def __init__(self, id, description, completed=False):
        self.id = id  # Identificador único de la tarea
        self.description = description  # Descripción de la tarea
        self.completed = completed  # Estado de la tarea (False por defecto, indicando que no está completada)

    # Método para marcar una tarea como completada
    def mark_as_completed(self):
        self.completed = True  # Cambia el estado de la tarea a completada

# Clase principal de la aplicación de gestión de tareas
class TaskManagerApp:
    def __init__(self, master):
        self.master = master  # Ventana principal de la aplicación
        self.master.title("Gestor de Tareas")  # Establece el título de la ventana
        self.master.configure(bg="#FFFF99")  # Configura el color de fondo de la ventana
        self.master.geometry("600x300")  # Establece el tamaño de la ventana

        self.load_tasks()  # Carga las tareas desde el archivo JSON al iniciar la aplicación

        # Estilo para las etiquetas
        label_style = {"bg": "#FFFF99", "fg": "black", "font": ("Arial", 12, "bold")}

        # Etiqueta para "Tareas Pendientes"
        self.pending_label = tk.Label(self.master, text="Tareas Pendientes", **label_style)
        self.pending_label.grid(row=0, column=2, padx=5, pady=5)  # Posiciona la etiqueta en la interfaz

        # Etiqueta para "Tareas Completadas"
        self.completed_label = tk.Label(self.master, text="Tareas Completadas", **label_style)
        self.completed_label.grid(row=0, column=3, padx=5, pady=5)  # Posiciona la etiqueta en la interfaz

        # Etiqueta para la entrada de la descripción de la tarea
        self.description_label = tk.Label(self.master, text="Indique la tarea:", bg="#FFFF99")
        self.description_label.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")

        # Casilla de entrada para la descripción de la tarea
        self.description_entry = tk.Entry(self.master)
        self.description_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="ew")
        self.description_entry.bind("<Return>", lambda event: self.add_task())  # Permite agregar una tarea al presionar Enter

        # Botón para agregar tarea
        self.add_button = tk.Button(self.master, text="Agregar Tarea", command=self.add_task)
        self.add_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 2))

        # Botón para eliminar tarea
        self.remove_button = tk.Button(self.master, text="Eliminar Tarea", command=self.remove_task)
        self.remove_button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=2)

        # Botón para mostrar todas las tareas
        self.show_button = tk.Button(self.master, text="Mostrar Todas las Tareas", command=self.show_all_tasks)
        self.show_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=2)

        # Botón para marcar como completada
        self.mark_completed_button = tk.Button(self.master, text="Marcar como Completada", command=self.mark_completed)
        self.mark_completed_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 5))

        # Botón para salir
        self.exit_button = tk.Button(self.master, text="Salir", command=self.on_exit)
        self.exit_button.grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 5))

        # Marco para mostrar las tareas pendientes
        self.pending_tasks_frame = tk.Frame(self.master, bg="#FFFF99")
        self.pending_tasks_frame.grid(row=1, column=2, rowspan=8, padx=5, pady=5, sticky="nsew")

        # Marco para mostrar las tareas completadas
        self.completed_tasks_frame = tk.Frame(self.master, bg="#FFFF99")
        self.completed_tasks_frame.grid(row=1, column=3, rowspan=8, padx=5, pady=5, sticky="nsew")

        # Configura la lista de tareas pendientes
        self.pending_tasks_listbox = tk.Listbox(self.pending_tasks_frame, selectmode=tk.SINGLE, width=30, height=10, bg="#FFFFCC")
        self.pending_tasks_listbox.pack(fill="both", expand=True)
        self.pending_tasks_listbox.bind("<Delete>", lambda event: self.remove_task())  # Permite eliminar una tarea al presionar Delete

        # Configura la lista de tareas completadas
        self.completed_tasks_listbox = tk.Listbox(self.completed_tasks_frame, selectmode=tk.SINGLE, width=30, height=10, bg="#FFFFCC")
        self.completed_tasks_listbox.pack(fill="both", expand=True)
        self.completed_tasks_listbox.bind("<Delete>", lambda event: self.remove_task())  # Permite eliminar una tarea al presionar Delete

        # Actualiza las listas de tareas en la interfaz
        self.update_lists()

    # Método para agregar una nueva tarea
    def add_task(self):
        description = self.description_entry.get().strip()  # Obtiene la descripción ingresada por el usuario
        if not description:
            messagebox.showerror("Error", "No ha indicado ninguna tarea")  # Muestra un mensaje de error si la descripción está vacía
            return
        task_id = len(self.pending_tasks) + len(self.completed_tasks) + 1  # Genera un ID único para la tarea
        task = Task(task_id, description)  # Crea una nueva tarea con los datos ingresados
        self.pending_tasks.append(task)  # Agrega la tarea a la lista de tareas pendientes
        self.pending_tasks_listbox.insert(tk.END, f"{task.id}. {description}")  # Agrega la tarea a la lista de tareas pendientes en la interfaz
        self.description_entry.delete(0, tk.END)  # Limpia el campo de entrada

    # Método para eliminar una tarea
    def remove_task(self):
        selected_task_index_pending = self.pending_tasks_listbox.curselection()  # Obtiene la tarea seleccionada en la lista de tareas pendientes
        selected_task_index_completed = self.completed_tasks_listbox.curselection()  # Obtiene la tarea seleccionada en la lista de tareas completadas

        if selected_task_index_pending:
            task = self.pending_tasks[selected_task_index_pending[0]]  # Si hay una tarea seleccionada en la lista de pendientes, la obtiene
            answer = messagebox.askyesno("Eliminar Tarea", f"¿Estás seguro de eliminar la tarea '{task.description}'?")  # Confirma si el usuario desea eliminar la tarea
            if answer:
                self.pending_tasks.remove(task)  # Elimina la tarea de la lista de pendientes
                self.pending_tasks_listbox.delete(selected_task_index_pending)  # Elimina la tarea de la lista de la interfaz
                self.update_lists()  # Actualiza las listas de tareas en la interfaz
        elif selected_task_index_completed:
            task = self.completed_tasks[selected_task_index_completed[0]]  # Si hay una tarea seleccionada en la lista de completadas, la obtiene
            answer = messagebox.askyesno("Eliminar Tarea", f"¿Estás seguro de eliminar la tarea '{task.description}'?")  # Confirma si el usuario desea eliminar la tarea
            if answer:
                self.completed_tasks.remove(task)  # Elimina la tarea de la lista de completadas
                self.completed_tasks_listbox.delete(selected_task_index_completed)  # Elimina la tarea de la lista de la interfaz
                self.update_lists()  # Actualiza las listas de tareas en la interfaz
        else:
            messagebox.showerror("Error", "No ha seleccionado ninguna tarea")  # Si no hay ninguna tarea seleccionada, muestra un mensaje de error

    # Método para mostrar todas las tareas
    def show_all_tasks(self):
        pending_tasks_text = "Tareas Pendientes:\n"  # Construye el texto para mostrar todas las tareas pendientes
        if not self.pending_tasks:
            pending_tasks_text += "No hay tareas pendientes.\n"
        else:
            for task in self.pending_tasks:
                pending_tasks_text += f"{task.id}. {task.description}\n"

        completed_tasks_text = "\nTareas Completadas:\n"  # Construye el texto para mostrar todas las tareas completadas
        if not self.completed_tasks:
            completed_tasks_text += "No hay tareas completadas.\n"
        else:
            for task in self.completed_tasks:
                completed_tasks_text += f"{task.id}. {task.description}\n"

        all_tasks_text = pending_tasks_text + completed_tasks_text  # Combina el texto de tareas pendientes y completadas
        if not self.pending_tasks and not self.completed_tasks:
            all_tasks_text = "No hay tareas pendientes ni completadas."
        
        messagebox.showinfo("Todas las Tareas", all_tasks_text)  # Muestra todas las tareas en un cuadro de diálogo

    # Método para marcar una tarea como completada
    def mark_completed(self):
        selected_task_index = self.pending_tasks_listbox.curselection()  # Obtiene la tarea seleccionada en la lista de tareas pendientes
        if selected_task_index:
            task = self.pending_tasks[selected_task_index[0]]  # Obtiene la tarea seleccionada
            task.mark_as_completed()  # Marca la tarea como completada
            self.completed_tasks.append(task)  # Agrega la tarea a la lista de tareas completadas
            self.pending_tasks.remove(task)  # Elimina la tarea de la lista de tareas pendientes
            self.pending_tasks_listbox.delete(selected_task_index)  # Elimina la tarea de la lista de la interfaz
            self.update_lists()  # Actualiza las listas de tareas en la interfaz
        else:
            messagebox.showerror("Error", "No ha seleccionado ninguna tarea")  # Si no hay ninguna tarea seleccionada, muestra un mensaje de error

    # Método para actualizar las listas de tareas en la interfaz
    def update_lists(self):
        self.pending_tasks_listbox.delete(0, tk.END)  # Limpia la lista de tareas pendientes en la interfaz
        self.completed_tasks_listbox.delete(0, tk.END)  # Limpia la lista de tareas completadas en la interfaz

        for task in self.pending_tasks:  # Agrega las tareas pendientes a la lista de la interfaz
            description = f"{task.id}. {task.description}"
            self.pending_tasks_listbox.insert(tk.END, description)

        for task in self.completed_tasks:  # Agrega las tareas completadas a la lista de la interfaz
            description = f"{task.id}. {task.description}"
            self.completed_tasks_listbox.insert(tk.END, description)

    # Método para guardar las tareas en un archivo JSON
    def save_tasks(self):
        with open("tasks.json", "w") as file:
            data = {
                "pending_tasks": [(task.id, task.description, task.completed) for task in self.pending_tasks],  # Serializa las tareas pendientes
                "completed_tasks": [(task.id, task.description, task.completed) for task in self.completed_tasks]  # Serializa las tareas completadas
            }
            json.dump(data, file)  # Guarda los datos en el archivo JSON

    # Método para cargar las tareas desde un archivo JSON
    def load_tasks(self):
        if os.path.exists("tasks.json"):  # Verifica si el archivo JSON existe
            with open("tasks.json", "r") as file:
                data = json.load(file)  # Carga los datos desde el archivo JSON
                self.pending_tasks = [Task(*task) for task in data["pending_tasks"]]  # Crea las tareas pendientes desde los datos cargados
                self.completed_tasks = [Task(*task) for task in data["completed_tasks"]]  # Crea las tareas completadas desde los datos cargados
        else:
            self.pending_tasks = []  # Inicializa la lista de tareas pendientes vacía si no existe el archivo
            self.completed_tasks = []  # Inicializa la lista de tareas completadas vacía si no existe el archivo

    # Método para manejar el evento de salida de la aplicación
    def on_exit(self):
        self.save_tasks()  # Guarda las tareas antes de salir
        self.master.quit()  # Cierra la ventana principal de la aplicación

# Función principal que inicia la aplicación
def main():
    root = tk.Tk()  # Crea la ventana principal
    app = TaskManagerApp(root)  # Crea la instancia de la aplicación
    root.protocol("WM_DELETE_WINDOW", app.on_exit)  # Maneja el evento de cierre de la ventana
    root.geometry("550x300")  # Fija el tamaño de la ventana
    root.resizable(False, False)  # Evita que la ventana se pueda redimensionar
    root.mainloop()  # Inicia el bucle principal de la aplicación

# Ejecuta la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
