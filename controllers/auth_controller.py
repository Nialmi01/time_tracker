from models.user import User

class AuthController:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def login(self, username, password):
        """Realiza la autenticación de un usuario"""
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Buscar usuario
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        params = (username, password)
        
        user_data = self.db_manager.fetch_one(query, params)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        if user_data:
            # Crear objeto de usuario
            return User.from_db_row(user_data)
        
        return None