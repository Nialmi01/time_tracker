class User:
    def __init__(self, id=None, username=None, password=None, full_name=None, role=None, created_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role
        self.created_at = created_at
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto User a partir de una fila de la base de datos"""
        if not row:
            return None
            
        return cls(
            id=row['id'],
            username=row['username'],
            password=row['password'],
            full_name=row['full_name'],
            role=row['role'],
            created_at=row['created_at']
        )
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role == 'admin'