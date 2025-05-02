import datetime
from models.user import User

class AdminController:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_all_users(self):
        """Obtiene todos los usuarios"""
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Consultar usuarios
        query = "SELECT * FROM users ORDER BY username"
        users = self.db_manager.fetch_all(query)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return users
    
    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID"""
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Consultar usuario
        query = "SELECT * FROM users WHERE id = ?"
        params = (user_id,)
        
        user = self.db_manager.fetch_one(query, params)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return user
    
    def add_user(self, username, password, full_name, role):
        """Agrega un nuevo usuario"""
        # Validar parámetros
        if not username or not password or not full_name or not role:
            return False
        
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Verificar si el usuario ya existe
        query = "SELECT id FROM users WHERE username = ?"
        params = (username,)
        
        existing_user = self.db_manager.fetch_one(query, params)
        
        if existing_user:
            self.db_manager.disconnect()
            return False
        
        # Insertar nuevo usuario
        query = """
            INSERT INTO users 
            (username, password, full_name, role) 
            VALUES (?, ?, ?, ?)
        """
        params = (username, password, full_name, role)
        
        result = self.db_manager.execute_query(query, params)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return result
    
    def update_user(self, user_id, password, full_name, role):
        """Actualiza un usuario existente"""
        # Validar parámetros
        if not user_id or not full_name or not role:
            return False
        
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Actualizar usuario
        if password:
            # Si se proporciona una nueva contraseña, actualizarla
            query = """
                UPDATE users 
                SET password = ?, full_name = ?, role = ? 
                WHERE id = ?
            """
            params = (password, full_name, role, user_id)
        else:
            # Si no se proporciona contraseña, mantener la actual
            query = """
                UPDATE users 
                SET full_name = ?, role = ? 
                WHERE id = ?
            """
            params = (full_name, role, user_id)
        
        result = self.db_manager.execute_query(query, params)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return result
    
    def delete_user(self, user_id):
        """Elimina un usuario"""
        # Validar parámetros
        if not user_id:
            return False
        
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Iniciar transacción
        self.db_manager.execute_query("BEGIN TRANSACTION")
        
        try:
            # Eliminar registros de tiempo relacionados
            query = "DELETE FROM activity_logs WHERE record_id IN (SELECT id FROM time_records WHERE user_id = ?)"
            params = (user_id,)
            self.db_manager.execute_query(query, params)
            
            query = "DELETE FROM time_records WHERE user_id = ?"
            params = (user_id,)
            self.db_manager.execute_query(query, params)
            
            # Eliminar usuario
            query = "DELETE FROM users WHERE id = ?"
            params = (user_id,)
            self.db_manager.execute_query(query, params)
            
            # Confirmar transacción
            self.db_manager.execute_query("COMMIT")
            
            result = True
        except Exception as e:
            # Revertir transacción en caso de error
            self.db_manager.execute_query("ROLLBACK")
            print(f"Error al eliminar usuario: {e}")
            result = False
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return result
    
    def get_active_sessions(self, user_id=None):
        """Obtiene sesiones activas de los usuarios"""
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Preparar consulta
        if user_id and user_id != -1:
            query = """
                SELECT u.username, t.*, 
                (SELECT activity_type FROM activity_logs 
                WHERE record_id = t.id AND end_time IS NULL) as current_activity
                FROM time_records t
                JOIN users u ON t.user_id = u.id
                WHERE t.logout_time IS NULL AND t.user_id = ?
                ORDER BY t.login_time DESC
            """
            params = (user_id,)
        else:
            query = """
                SELECT u.username, t.*, 
                (SELECT activity_type FROM activity_logs 
                WHERE record_id = t.id AND end_time IS NULL) as current_activity
                FROM time_records t
                JOIN users u ON t.user_id = u.id
                WHERE t.logout_time IS NULL
                ORDER BY t.login_time DESC
            """
            params = None
        
        active_sessions = self.db_manager.fetch_all(query, params)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return active_sessions
    
    def get_historical_report(self, user_id=None, from_date=None, to_date=None):
        """Obtiene reporte histórico de tiempos"""
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Preparar consulta
        query = """
            SELECT u.username, t.*
            FROM time_records t
            JOIN users u ON t.user_id = u.id
            WHERE 1=1
        """
        params = []
        
        if user_id and user_id != -1:
            query += " AND t.user_id = ?"
            params.append(user_id)
        
        if from_date:
            query += " AND t.date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND t.date <= ?"
            params.append(to_date)
        
        query += " ORDER BY t.date DESC, u.username"
        
        report_data = self.db_manager.fetch_all(query, params if params else None)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return report_data