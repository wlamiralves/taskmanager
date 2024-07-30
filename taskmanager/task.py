import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import csv
import os
from datetime import datetime
import sqlite3
import webbrowser

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title('Gerenciador de Tarefas')

        # Lista para armazenar as tarefas
        self.tasks = []
        self.deleted_tasks = []

        # Configurações do banco de dados
        self.conn = sqlite3.connect('task_manager.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Estilos
        self.font_large = ('Helvetica', 18, 'bold')
        self.font_medium = ('Helvetica', 12)
        self.bg_color = '#f7f7f7'  # Cor de fundo
        self.button_fg = '#333333'  # Cor do texto dos botões
        self.button_bg = '#d0d0d0'  # Cor de fundo dos botões
        self.button_active_bg = '#c0c0c0'  # Cor de fundo dos botões ao passar o mouse

        # Mapeamento de prioridades para cores de fundo
        self.priority_button_colors = {
            'alta': '#ffdddd',
            'média': '#fff5cc',
            'baixa': '#ddffdd'
        }
        self.priority_display_colors = {
            'alta': '#ffaaaa',
            'média': '#ffcc99',
            'baixa': '#ccffcc'
        }

        # Configuração da interface gráfica
        self.setup_gui()

        # Carregar tarefas iniciais
        self.load_tasks_from_file()

        # Contagem inicial de tarefas
        self.update_task_count()

    def setup_gui(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, padx=20, pady=20, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Centraliza o frame principal na tela
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Título
        self.title_label = tk.Label(self.main_frame, text='Gerenciador de Tarefas', font=self.font_large, bg=self.bg_color)
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        # Frame para entrada de tarefas e exibição
        self.tasks_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.tasks_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Caixa de entrada de tarefas
        self.task_entry = tk.Entry(self.tasks_frame, width=50, font=self.font_medium)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Botão para adicionar tarefa
        self.add_button = tk.Button(self.tasks_frame, text='Adicionar', font=self.font_medium, bg=self.button_bg, fg=self.button_fg, activebackground=self.button_active_bg, command=self.add_task_gui)
        self.add_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Listbox para exibição de tarefas
        self.tasks_listbox = tk.Listbox(self.tasks_frame, width=60, height=15, font=self.font_medium, selectmode=tk.SINGLE, bg='#ffffff', bd=2, relief=tk.SUNKEN)
        self.tasks_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Scrollbar para Listbox
        self.scrollbar = tk.Scrollbar(self.tasks_frame, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
        self.scrollbar.grid(row=1, column=2, sticky='ns')  # Ao lado do Listbox

        self.tasks_listbox.config(yscrollcommand=self.scrollbar.set)

        # Frame para os botões de interação
        self.button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.button_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        # Botões para interação com tarefas
        self.edit_button = tk.Button(self.button_frame, text='Editar', font=self.font_medium, bg=self.button_bg, fg=self.button_fg, activebackground=self.button_active_bg, command=self.edit_task_gui)
        self.edit_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.remove_button = tk.Button(self.button_frame, text='Remover', font=self.font_medium, bg=self.button_bg, fg=self.button_fg, activebackground=self.button_active_bg, command=self.remove_task_gui)
        self.remove_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.clear_button = tk.Button(self.button_frame, text='Limpar Lista', font=self.font_medium, bg=self.button_bg, fg=self.button_fg, activebackground=self.button_active_bg, command=self.clear_tasks)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.restore_button = tk.Button(self.button_frame, text='Lixeira', font=self.font_medium, bg=self.button_bg, fg=self.button_fg, activebackground=self.button_active_bg, command=self.restore_tasks_gui)
        self.restore_button.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        self.report_button = tk.Button(self.button_frame, text='Emitir Relatório', font=self.font_medium, bg=self.button_bg, fg=self.button_fg, activebackground=self.button_active_bg, command=self.generate_report)
        self.report_button.grid(row=0, column=4, padx=5, pady=5, sticky='ew')

        # Label para link do perfil do GitHub
        self.github_label = tk.Label(self.main_frame, text='@wlamiralves', font=self.font_medium, fg='#000000', cursor='hand2', bg=self.bg_color)
        self.github_label.grid(row=3, column=0, columnspan=4, pady=(10, 0))
        self.github_label.bind('<Button-1>', lambda event: self.open_github_profile())

        # Configurações de redimensionamento
        self.main_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.tasks_frame.rowconfigure(1, weight=1)

        # Vincular a tecla Enter ao botão de adicionar tarefa
        self.task_entry.bind('<Return>', self.add_task_on_enter)

        # Adicionar o evento de duplo clique para exibir detalhes da tarefa
        self.tasks_listbox.bind('<Double-1>', self.show_task_details)

    def open_github_profile(self):
        webbrowser.open_new_tab('https://github.com/wlamiralves')

    def add_task_gui(self):
        task = self.task_entry.get().strip()  # Remover espaços em branco desnecessários
        if task:
            priority = self.get_task_priority(task)
            self.tasks.append({'task': task, 'priority': priority, 'timestamp': datetime.now()})
            self.sort_tasks()  # Reordenar tarefas após adição
            self.update_task_listbox()
            self.save_tasks_to_file()  # Salvar tarefas após adicionar uma nova tarefa
            self.update_task_count()
            self.task_entry.delete(0, tk.END)  # Limpar entrada de tarefa
        else:
            messagebox.showwarning('Tarefa Vazia', 'Digite uma tarefa para adicionar.')

    def add_task_on_enter(self, event):
        self.add_task_gui()

    def edit_task_gui(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            old_task = self.tasks[index]['task']
            new_task = simpledialog.askstring('Editar Tarefa', 'Digite a nova tarefa:', initialvalue=old_task)

            if new_task:
                priority = self.get_task_priority(new_task)
                self.tasks[index] = {'task': new_task, 'priority': priority, 'timestamp': datetime.now()}
                self.sort_tasks()  # Reordenar tarefas após edição
                self.update_task_listbox()
                self.save_tasks_to_file()  # Salvar tarefas após editar uma tarefa
                self.root.after(100, self.show_task_edited_message, old_task, new_task)
        except IndexError:
            messagebox.showwarning('Seleção Inválida', 'Por favor, selecione uma tarefa para editar.')

    def show_task_edited_message(self, old_task, new_task):
        messagebox.showinfo('Tarefa Editada', f'Tarefa "{old_task}" alterada para "{new_task}".')

    def remove_task_gui(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            task_to_remove = self.tasks[index]
            self.insert_deleted_task_record(task_to_remove['task'], task_to_remove['priority'], task_to_remove['timestamp'])
            self.remove_task(task_to_remove['task'])
            self.show_task_removed_message(task_to_remove['task'])
        except IndexError:
            messagebox.showwarning('Seleção Inválida', 'Por favor, selecione uma tarefa para remover.')

    def show_task_removed_message(self, task):
        messagebox.showinfo('Tarefa Removida', f'Tarefa "{task}" removida com sucesso.')

    def remove_task(self, task):
        self.tasks = [t for t in self.tasks if t['task'] != task]
        self.update_task_listbox()
        self.save_tasks_to_file()  # Salvar tarefas após remover uma tarefa
        self.update_task_count()

    def clear_tasks(self):
        confirmed = messagebox.askyesno('Limpar Lista de Tarefas', 'Tem certeza que deseja limpar a lista de tarefas?')
        if confirmed:
            for task in self.tasks:
                self.insert_deleted_task_record(task['task'], task['priority'], task['timestamp'])
            self.tasks.clear()
            self.update_task_listbox()
            self.save_tasks_to_file()  # Salvar tarefas após limpar a lista
            self.update_task_count()
            messagebox.showinfo('Lista Limpa', 'Lista de tarefas foi limpa.')

    def restore_tasks_gui(self):
        self.deleted_tasks = self.get_deleted_tasks()
        if not self.deleted_tasks:
            messagebox.showinfo('Lixeira', 'Não há tarefas removidas para restaurar.')
            return

        restore_window = tk.Toplevel(self.root)
        restore_window.title('Lixeira')
        restore_window.geometry('400x300')

        restore_listbox = tk.Listbox(restore_window, width=60, height=15, font=self.font_medium, selectmode=tk.SINGLE, bg='#ffffff', bd=2, relief=tk.SUNKEN)
        restore_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for task in self.deleted_tasks:
            restore_listbox.insert(tk.END, f'{task["task"]} - Prioridade: {task["priority"]} - Data: {task["timestamp"].strftime("%d/%m/%Y %H:%M:%S")}')

        def restore_task(event=None):
            selected_task_index = restore_listbox.curselection()
            if selected_task_index:
                selected_task = self.deleted_tasks[selected_task_index[0]]
                self.tasks.append({'task': selected_task['task'], 'priority': selected_task['priority'], 'timestamp': selected_task['timestamp']})
                self.sort_tasks()
                self.update_task_listbox()
                self.save_tasks_to_file()  # Salvar tarefas após restaurar
                self.remove_deleted_task_record(selected_task['task'])
                restore_window.destroy()
                self.update_task_count()
            else:
                messagebox.showwarning('Seleção Inválida', 'Selecione uma tarefa para restaurar.')

        def delete_task():
            selected_task_index = restore_listbox.curselection()
            if selected_task_index:
                selected_task = self.deleted_tasks[selected_task_index[0]]
                self.remove_deleted_task_record(selected_task['task'])
                restore_window.destroy()
                self.update_task_listbox()
                self.update_task_count()
            else:
                messagebox.showwarning('Seleção Inválida', 'Selecione uma tarefa para excluir permanentemente.')

        restore_button = tk.Button(restore_window, text='Restaurar', command=restore_task)
        restore_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(restore_window, text='Excluir Permanentemente', command=delete_task)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        restore_listbox.bind('<Double-1>', restore_task)  # Adiciona a funcionalidade de restaurar com duplo clique
        restore_window.grab_set()  # Torna a janela de restauração modal

    def generate_report(self):
        report_date = simpledialog.askstring('Emitir Relatório', 'Digite a data para o relatório (DD/MM/YYYY):')
        if report_date:
            try:
                report_date = datetime.strptime(report_date, '%d/%m/%Y')
                file_path = self.create_report_file(report_date)
                messagebox.showinfo('Relatório Gerado', f'Relatório gerado com sucesso: {file_path}')
            except ValueError:
                messagebox.showwarning('Data Inválida', 'Formato de data inválido. Utilize o formato DD/MM/YYYY.')

    def create_report_file(self, report_date):
        file_path = os.path.join(os.path.expanduser('~/Downloads'), f'relatório_{report_date.strftime("%d_%m_%Y")}.csv')
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['task', 'priority', 'timestamp']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                if task['timestamp'].date() == report_date.date():
                    writer.writerow({
                        'task': task['task'],
                        'priority': task['priority'],
                        'timestamp': task['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
                    })
        return file_path

    def get_task_priority(self, task):
        priority = simpledialog.askstring('Definir Prioridade', f'Defina a prioridade para a tarefa "{task}" (alta, média, baixa):')
        return priority if priority in self.priority_button_colors else 'baixa'

    def update_task_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            priority = task['priority']
            task_text = f'{task["task"]} - Prioridade: {priority} - Data: {task["timestamp"].strftime("%d/%m/%Y %H:%M:%S")}'
            color = self.priority_display_colors.get(priority, '#ffffff')
            self.tasks_listbox.insert(tk.END, task_text)
            self.tasks_listbox.itemconfig(tk.END, {'fg': '#000000', 'bg': color})

    def update_task_count(self):
        count = len(self.tasks)
        self.root.title(f'Gerenciador de Tarefas - Total de Tarefas: {count}')

    def load_tasks_from_file(self):
        if os.path.exists('tasks.csv'):
            with open('tasks.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.tasks = []
                for row in reader:
                    self.tasks.append({
                        'task': row['task'],
                        'priority': row['priority'],
                        'timestamp': datetime.strptime(row['timestamp'], '%d/%m/%Y %H:%M:%S')
                    })
                self.sort_tasks()
                self.update_task_listbox()

    def save_tasks_to_file(self):
        with open('tasks.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['task', 'priority', 'timestamp']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    'task': task['task'],
                    'priority': task['priority'],
                    'timestamp': task['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
                })

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS deleted_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                priority TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                deleted_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_report_record(self, file_path):
        self.cursor.execute('INSERT INTO reports (file_path, created_at) VALUES (?, ?)',
                            (file_path, datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        self.conn.commit()

    def insert_deleted_task_record(self, task, priority, timestamp):
        self.cursor.execute('INSERT INTO deleted_tasks (task, priority, timestamp, deleted_at) VALUES (?, ?, ?, ?)',
                            (task, priority, timestamp.strftime('%d/%m/%Y %H:%M:%S'), datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        self.conn.commit()

    def remove_deleted_task_record(self, task):
        self.cursor.execute('DELETE FROM deleted_tasks WHERE task = ?', (task,))
        self.conn.commit()

    def get_deleted_tasks(self):
        self.cursor.execute('SELECT task, priority, timestamp FROM deleted_tasks ORDER BY deleted_at DESC')
        rows = self.cursor.fetchall()
        return [{'task': row[0], 'priority': row[1], 'timestamp': datetime.strptime(row[2], '%d/%m/%Y %H:%M:%S')} for row in rows]

    def sort_tasks(self):
        self.tasks.sort(key=lambda x: (self.priority_order(x['priority']), x['timestamp']))

    def priority_order(self, priority):
        order = {'alta': 1, 'média': 2, 'baixa': 3}
        return order.get(priority, 4)  # 4 para qualquer outro caso

    def show_task_details(self, event):
        try:
            index = self.tasks_listbox.curselection()[0]
            task = self.tasks[index]
            details_message = f"Tarefa: {task['task']}\nPrioridade: {task['priority']}\nData: {task['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}"
            messagebox.showinfo("Detalhes da Tarefa", details_message)
        except IndexError:
            messagebox.showwarning('Seleção Inválida', 'Por favor, selecione uma tarefa para visualizar os detalhes.')

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskManager(root)
    root.geometry('800x500')  # Define o tamanho inicial da janela
    root.mainloop()
