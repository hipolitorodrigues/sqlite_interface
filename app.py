import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Dict, Any, List, Tuple, Union
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import os
from pathlib import Path

class ResponsiveFrame(ttk.Frame):
    """Responsive frame that adapts to window resizing."""
    
    def __init__(self, master: Any, **kwargs: Any) -> None:
        """  
        Initializes the responsive frame.  

        Args:  
            master: Parent widget  
            kwargs: Additional arguments for the frame  
        """
        super().__init__(master, **kwargs)
        self.pack_propagate(False)

class DatabaseManager:
    """Manager for connections and operations with the SQLite database."""
    
    def __init__(self) -> None:
        """Initializes the database manager."""
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self.current_db_path: Optional[str] = None
        self.db_info: Dict[str, List[str]] = {}  # Stores tables and views per database.
    
    def connect(self, db_path: str) -> bool:
        """  
        Connects to the SQLite database.  

        Args:  
            db_path: Path to the database file  

        Returns:  
            bool: True if the connection was successful, False otherwise  
        """
        try:
            if self.connection:
                self.close()
                
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            self.current_db_path = db_path
            self._update_db_info()
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return False
    
    def create_database(self, db_path: str) -> bool:
        """  
        Creates a new SQLite database.  

        Args:  
            db_path: Path to the new database file  

        Returns:  
            bool: True if the creation was successful, False otherwise  
        """
        try:
            # Only establishes the connection, which creates an empty database file.
            conn = sqlite3.connect(db_path)
            conn.close()
            
            # Conecta ao banco recém-criado
            return self.connect(db_path)
        except sqlite3.Error as e:
            print(f"Error creating the database: {e}")
            return False
    
    def close(self) -> None:
        """Closes the current connection to the database."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            self.current_db_path = None
    
    def execute_query(self, query: str) -> Tuple[bool, Union[List[Tuple], str], Optional[List[str]]]:
        """  
        Executes an SQL query.  

        Args:  
            query: SQL query to be executed  

        Returns:  
            Tuple containing:  
                bool: True if successful, False otherwise  
                Union[List[Tuple], str]: Results or error message  
                Optional[List[str]]: Column names if available  
        """
        if not self.connection or not self.cursor:
            return False, "There is no active connection to the database", None
        
        try:
            self.cursor.execute(query)
            
            # Check if it is a SELECT query or similar that returns data.
            if query.strip().upper().startswith(("SELECT", "PRAGMA", "SHOW")):
                results = self.cursor.fetchall()
                column_names = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
                self.connection.commit()  # Even for SELECTs, to be sure.
                return True, results, column_names
            else:
                # For commands like INSERT, UPDATE, DELETE, CREATE, etc.
                self.connection.commit()
                
                # After CREATE TABLE or DROP TABLE, update the database information.
                if any(cmd in query.strip().upper() for cmd in ["CREATE TABLE", "DROP TABLE", "ALTER TABLE"]):
                    self._update_db_info()
                    
                return True, f"Comando executado com sucesso. Linhas afetadas: {self.cursor.rowcount}", None
                
        except sqlite3.Error as e:
            return False, f"Erro ao executar consulta: {e}", None
    
    def get_tables(self) -> List[str]:
        """
        Gets the list of tables from the current database.

        Returns:
        List[str]: List of table names
        """
        if not self.connection or not self.cursor:
            return []
        
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [row[0] for row in self.cursor.fetchall()]
            return tables
        except sqlite3.Error as e:
            print(f"Erro ao obter tabelas: {e}")
            return []
    
    def get_table_info(self, table_name: str) -> List[Tuple[str, str]]:
        """
        Gets information about the columns of a table.

        Args:
        table_name: Name of the table

        Returns:
        List[Tuple[str, str]]: List of tuples (column_name, column_type)
        """
        if not self.connection or not self.cursor:
            return []
        
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [(row[1], row[2]) for row in self.cursor.fetchall()]  # (name, type)
            return columns
        except sqlite3.Error as e:
            print(f"Erro ao obter informações da tabela: {e}")
            return []
    
    def _update_db_info(self) -> None:
        """Updates information about the current database."""
        if not self.connection or not self.cursor:
            return
        
        self.db_info = {}
        try:
            # Get tables
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            self.db_info['tables'] = [row[0] for row in self.cursor.fetchall()]
            
            # Get views
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
            self.db_info['views'] = [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao atualizar informações do banco: {e}")

class ApplicationUI:
    """  
    Main application interface using ttkbootstrap with superhero theme.  
    Implements a responsive layout according to the provided specifications.  
    """
    
    def __init__(self, root: tk.Tk, db_manager: DatabaseManager) -> None:
        """  
        Initializes the application interface.  

        Args:  
            root: Main Tkinter window  
            db_manager: Database manager  
        """
        self.root = root
        self.root.title("Just a SQLite Interface")
        self.root.geometry("1280x800")
        self.root.minsize(800, 600)
        
        # Reference to the database manager
        self.db_manager = db_manager
        
        # Application of the superhero theme
        self.style = ttk.Style(theme="superhero")
        
        # Dictionary to store button references
        self.buttons: Dict[str, ttk.Button] = {}
        
        # Configuration for responsive resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Interface initialization
        self._setup_main_container()
        self._setup_top_section()
        self._setup_left_section()
        self._setup_main_content()
        self._setup_bottom_section()
        
        # Status bar for user feedback
        self.status_var = tk.StringVar(value="Pronto")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W, 
            padding=(10, 2)
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")
        
    def _setup_main_container(self) -> None:
        """Configures the main container that will occupy the entire window."""
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Grid configuration for the main container (2x2)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=3)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=3)
        
    def _setup_top_section(self) -> None:
        """Configures the top section."""
        self.top_section = ResponsiveFrame(
            self.main_container,
            bootstyle="secondary",
            padding=10
        )
        self.top_section.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Configuration to make the buttons responsive
        self.top_section.grid_columnconfigure(0, weight=1)
        
        # Creation of buttons based on the second image (B-01 to B-64)
        self._create_button_grid()
        
    def _create_button_grid(self) -> None:
        """Creates the button grid in the top section, storing references to each button."""
        # Frame for the buttons
        self.buttons_frame = ttk.Frame(self.top_section)
        self.buttons_frame.pack(fill=BOTH, expand=YES)
        
        # Definition of the number of buttons and columns
        button_count = 64
        cols_per_row = 32
        
        # Grid configuration for responsiveness
        for i in range(cols_per_row):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Creation of buttons with explicit references
        for i in range(button_count):
            row = i // cols_per_row
            col = i % cols_per_row
            
            # Creation of the button with ID
            button_id = f"B-{i+1:02d}"
            
            # Creates the button and stores it in the dictionary for later access
            self.buttons[button_id] = ttk.Button(
                self.buttons_frame,
                text=button_id,
                bootstyle="info-outline",
                command=lambda bid=button_id: self._button_click(bid)
            )
            self.buttons[button_id].grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Configuring some buttons for specific functions
        self.set_button_command("B-01", self._create_new_database)
        self.set_button_command("B-02", self._open_database)
        self.set_button_command("B-03", self._close_database)
        self.set_button_command("B-04", self._refresh_db_tree)
    
    def set_button_command(self, button_id: str, command: callable) -> None:
        """  
        Defines a specific function for a button.  

        Args:  
            button_id: Button identifier (e.g., "B-01")  
            command: Function to be executed when the button is clicked  
        """
        if button_id in self.buttons:
            self.buttons[button_id].configure(command=command)
            if button_id == "B-01":
                self.buttons[button_id].configure(text="New DB")
            elif button_id == "B-02":
                self.buttons[button_id].configure(text="Open DB")
            elif button_id == "B-03":
                self.buttons[button_id].configure(text="Close DB")
            elif button_id == "B-04":
                self.buttons[button_id].configure(text="Update")
            print(f"Function assigned to the {button_id} button")
        else:
            print(f"{button_id} button not found")
            
    def _button_click(self, button_id: str) -> None:
        """  
        Placeholder function for button actions.  

        Args:  
            button_id: Identifier of the clicked button  
        """
        print(f"Botão {button_id} clicado - Ainda sem função específica definida")
    
    def _create_new_database(self) -> None:
        """Creates a new SQLite database."""
        file_path = filedialog.asksaveasfilename(
            title="Create New Database",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")],
            defaultextension=".db"
        )
        
        if file_path:
            if self.db_manager.create_database(file_path):
                self.status_var.set(f"Database created: {os.path.basename(file_path)}")
                self._update_db_tree()
                # Adds a query suggestion to create a table
                self.query_text.delete(1.0, tk.END)
                self.query_text.insert(tk.END, """-- Example of table creation
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT,
    data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
);""")
            else:
                self.status_var.set("Error creating the database")
    
    def _open_database(self) -> None:
        """Opens an existing SQLite database."""
        file_path = filedialog.askopenfilename(
            title="Open Database",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.db_manager.connect(file_path):
                self.status_var.set(f"Connected to the bank: {os.path.basename(file_path)}")
                self._update_db_tree()
            else:
                self.status_var.set("Error connecting to the database")
    
    def _close_database(self) -> None:
        """Closes the current connection to the database."""
        if self.db_manager.current_db_path:
            self.db_manager.close()
            self.status_var.set("Database connection closed")
            self._clear_db_tree()
        else:
            self.status_var.set("No open databases to close")
    
    def _refresh_db_tree(self) -> None:
        """Updates the database navigation tree."""
        if self.db_manager.current_db_path:
            self._update_db_tree()
            self.status_var.set("Árvore de navegação atualizada")
        else:
            self.status_var.set("Nenhum banco aberto para atualizar")
        
    def _setup_left_section(self) -> None:
        """Configures the left section (green in the reference image)."""
        self.left_section = ResponsiveFrame(
            self.main_container,
            bootstyle="success",
            padding=10
        )
        self.left_section.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Título para a seção esquerda
        self.left_content = ttk.Label(
            self.left_section,
            text="Database Navigation",
            font=("TkDefaultFont", 14),
            bootstyle="inverse-success"
        )
        self.left_content.pack(pady=(0, 10), fill=X)
        
        # Treeview para exibir a estrutura do banco
        self.db_tree = ttk.Treeview(
            self.left_section, 
            bootstyle="success",
            selectmode="browse"
        )
        self.db_tree.heading("#0", text="Database", anchor=W)
        
        # Scrollbar para o treeview
        self.tree_scroll = ttk.Scrollbar(
            self.left_section,
            orient=VERTICAL,
            command=self.db_tree.yview,
            bootstyle="success-round"
        )
        self.db_tree.configure(yscrollcommand=self.tree_scroll.set)
        
        # Layout da árvore de navegação
        self.db_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        
        # Evento de seleção na árvore
        self.db_tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        
    def _update_db_tree(self) -> None:
        """Atualiza a árvore de navegação com as tabelas e views do banco atual."""
        self._clear_db_tree()
        
        if not self.db_manager.current_db_path:
            return
            
        # Nó raiz para o banco atual
        db_name = os.path.basename(self.db_manager.current_db_path)
        db_node = self.db_tree.insert("", END, text=db_name, open=True, values=("database",))
        
        # Nó para tabelas
        tables_node = self.db_tree.insert(db_node, END, text="Tabelas", open=True, values=("tables",))
        
        # Adiciona cada tabela
        for table in self.db_manager.db_info.get('tables', []):
            table_node = self.db_tree.insert(tables_node, END, text=table, values=("table", table))
            
            # Adiciona colunas da tabela
            columns = self.db_manager.get_table_info(table)
            for col_name, col_type in columns:
                self.db_tree.insert(table_node, END, text=f"{col_name} ({col_type})", values=("column", table, col_name))
        
        # Nó para views
        views_node = self.db_tree.insert(db_node, END, text="Views", open=True, values=("views",))
        
        # Adiciona cada view
        for view in self.db_manager.db_info.get('views', []):
            self.db_tree.insert(views_node, END, text=view, values=("view", view))
    
    def _clear_db_tree(self) -> None:
        """Clears the database navigation tree."""
        for item in self.db_tree.get_children():
            self.db_tree.delete(item)
    
    def _on_tree_select(self, event) -> None:
        """
        Manipula a seleção de itens na árvore de navegação.
        
        Args:
            event: Evento de seleção
        """
        selected_item = self.db_tree.selection()[0]
        item_values = self.db_tree.item(selected_item, "values")
        
        if not item_values:
            return
            
        item_type = item_values[0]
        
        # Se selecionou uma tabela, gera uma consulta SELECT
        if item_type == "table" and len(item_values) > 1:
            table_name = item_values[1]
            self.query_text.delete(1.0, tk.END)
            self.query_text.insert(tk.END, f"SELECT * FROM {table_name} LIMIT 100;")
        
        # Se selecionou uma view, gera uma consulta SELECT
        elif item_type == "view" and len(item_values) > 1:
            view_name = item_values[1]
            self.query_text.delete(1.0, tk.END)
            self.query_text.insert(tk.END, f"SELECT * FROM {view_name} LIMIT 100;")
            
    def _setup_main_content(self) -> None:
        """Configura a área de conteúdo principal (dividida em azul e vermelho na referência)."""
        # Container para as seções de conteúdo
        self.content_container = ttk.Frame(self.main_container)
        self.content_container.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configuração para dividir em duas partes (azul/vermelho)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(1, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Seção superior (azul na referência) - Para consultas SQL
        self.upper_content = ResponsiveFrame(
            self.content_container,
            bootstyle="primary",
            padding=10
        )
        self.upper_content.grid(row=0, column=0, sticky="nsew", pady=(0, 2))
        
        # Área de entrada para consultas SQL
        self.query_label = ttk.Label(
            self.upper_content,
            text="SQL Query:",
            font=("TkDefaultFont", 12),
            bootstyle="inverse-primary"
        )
        self.query_label.pack(anchor=W, pady=(0, 5))
        
        self.query_text = tk.Text(
            self.upper_content,
            height=10,
            width=80,
            font=("Consolas", 12)
        )
        self.query_text.pack(fill=BOTH, expand=YES, pady=5)
        
        # Botões para ações de consulta
        self.query_buttons_frame = ttk.Frame(self.upper_content)
        self.query_buttons_frame.pack(fill=X, pady=5)
        
        self.execute_button = ttk.Button(
            self.query_buttons_frame,
            text="Executar Consulta",
            bootstyle="primary",
            command=self._execute_query
        )
        self.execute_button.pack(side=LEFT, padx=5)
        
        self.clear_button = ttk.Button(
            self.query_buttons_frame,
            text="Limpar",
            bootstyle="primary-outline",
            command=lambda: self.query_text.delete(1.0, tk.END)
        )
        self.clear_button.pack(side=LEFT, padx=5)
        
        # Bottom section (red in the reference) - For results
        self.lower_content = ResponsiveFrame(
            self.content_container,
            bootstyle="danger",
            padding=10
        )
        self.lower_content.grid(row=1, column=0, sticky="nsew", pady=(2, 0))
        
        # Area for displaying results
        self.results_label = ttk.Label(
            self.lower_content,
            text="Results:",
            font=("TkDefaultFont", 12),
            bootstyle="inverse-danger"
        )
        self.results_label.pack(anchor=W, pady=(0, 5))
        
        # Frame para conter o treeview e scrollbars
        self.results_frame = ttk.Frame(self.lower_content)
        self.results_frame.pack(fill=BOTH, expand=YES)
        
        # Treeview to display query results
        self.results_tree = ttk.Treeview(
            self.results_frame,
            bootstyle="danger",
            show="headings"
        )
        
        # Scrollbars para o treeview
        self.results_y_scroll = ttk.Scrollbar(
            self.results_frame,
            orient=VERTICAL,
            command=self.results_tree.yview,
            bootstyle="danger-round"
        )
        self.results_tree.configure(yscrollcommand=self.results_y_scroll.set)
        
        self.results_x_scroll = ttk.Scrollbar(
            self.results_frame,
            orient=HORIZONTAL,
            command=self.results_tree.xview,
            bootstyle="danger-round"
        )
        self.results_tree.configure(xscrollcommand=self.results_x_scroll.set)
        
        # Results layout
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        self.results_y_scroll.grid(row=0, column=1, sticky="ns")
        self.results_x_scroll.grid(row=1, column=0, sticky="ew")
        
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        
    def _execute_query(self) -> None:
        """Executes the SQL query from the text area and displays the results."""
        if not self.db_manager.current_db_path:
            messagebox.showwarning("Warning", "No database open.")
            return
        
        query = self.query_text.get(1.0, tk.END).strip()
        
        if not query:
            messagebox.showwarning("Warning", "Empty query.")
            return
        
        success, result, column_names = self.db_manager.execute_query(query)
        
        if success:
            if isinstance(result, list):
                # Clears the results tree
                for col in self.results_tree["columns"]:
                    self.results_tree.heading(col, text="")
                
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)
                
                if not result:
                    self.status_var.set("Consulta executada com sucesso, mas nenhum resultado foi retornado.")
                    # Configures the treeview with a single column to display "No results"
                    self.results_tree["columns"] = ["message"]
                    self.results_tree.heading("message", text="Mensagem")
                    self.results_tree.column("message", width=400)
                    self.results_tree.insert("", tk.END, values=["Nenhum resultado encontrado."])
                    return
                
                # Configura as colunas do treeview com os nomes das colunas do resultado
                self.results_tree["columns"] = column_names
                
                for col in column_names:
                    self.results_tree.heading(col, text=col, anchor=W)
                    self.results_tree.column(col, width=100, minwidth=50)
                
                # Insere os dados do resultado
                for row in result:
                    # Converte todos os valores para string (para evitar problemas com None, etc.)
                    string_row = [str(value) if value is not None else "" for value in row]
                    self.results_tree.insert("", tk.END, values=string_row)
                
                self.status_var.set(f"Consulta executada com sucesso. {len(result)} registros encontrados.")
                
                # Atualiza a árvore de navegação após comandos que modificam a estrutura
                if any(cmd in query.strip().upper() for cmd in ["CREATE", "DROP", "ALTER"]):
                    self._update_db_tree()
            else:
                # Resultado é uma mensagem
                self.status_var.set(result)
                
                # Configure o treeview com uma coluna apenas para mostrar a mensagem
                for col in self.results_tree["columns"]:
                    self.results_tree.heading(col, text="")
                
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)
                
                self.results_tree["columns"] = ["message"]
                self.results_tree.heading("message", text="Mensagem")
                self.results_tree.column("message", width=400)
                self.results_tree.insert("", tk.END, values=[result])
                
                # Atualiza a árvore de navegação após comandos que modificam a estrutura
                if any(cmd in query.strip().upper() for cmd in ["CREATE", "DROP", "ALTER"]):
                    self._update_db_tree()
        else:
            # Mostra mensagem de erro
            messagebox.showerror("Erro SQL", result)
            self.status_var.set("Erro ao executar consulta.")
        
    def _setup_bottom_section(self) -> None:
        """Configura a seção inferior caso necessário."""
        # Esta seção não é necessária de acordo com o layout original
        pass

class Application:
    """Main application class following the MVC pattern."""
    
    def __init__(self) -> None:
        """Initializes the application."""
        self.root = tk.Tk()
        
        # Creates the database manager
        self.db_manager = DatabaseManager()
        
        # Create the user interface
        self.ui = ApplicationUI(self.root, self.db_manager)
        
    def run(self) -> None:
        """Runs the main application loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()