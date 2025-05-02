import sqlite3
import os
import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL"""
        try:
            if not self.connection:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return False
    
    def fetch_all(self, query, params=None):
        """Ejecuta una consulta y devuelve todos los resultados"""
        try:
            if not self.connection:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al realizar consulta: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Ejecuta una consulta y devuelve un solo resultado"""
        try:
            if not self.connection:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al realizar consulta: {e}")
            return None
    
    def setup_database(self):
        """Configura la base de datos con las tablas necesarias"""
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        
        self.connect()
        
        # Leer y ejecutar el esquema SQL
        with open('database/schema.sql', 'r') as f:
            schema = f.read()
        
        # Dividir por punto y coma para ejecutar múltiples instrucciones
        statements = schema.split(';')
        for statement in statements:
            if statement.strip():
                self.execute_query(statement)
        
        # Verificar si existe el usuario administrador, si no, crearlo
        admin = self.fetch_one("SELECT * FROM users WHERE username = ?", ("admin",))
        if not admin:
            self.execute_query(
                "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                ("admin", "admin123", "Administrator", "admin")
            )
        
        self.disconnect()