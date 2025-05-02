import datetime
from models.time_record import TimeRecord, ActivityLog

class TimerController:
    def __init__(self, db_manager, user):
        self.db_manager = db_manager
        self.user = user
        self.current_record_id = None
        self.current_activity_id = None
        self.current_activity = "work"
        self.start_time = datetime.datetime.now()
    
    def start_session(self):
        """Inicia una sesión de trabajo"""
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Verificar si ya existe un registro para hoy
        today = datetime.date.today().strftime("%Y-%m-%d")
        query = """
            SELECT * FROM time_records 
            WHERE user_id = ? AND date = ? AND logout_time IS NULL
        """
        params = (self.user.id, today)
        
        existing_record = self.db_manager.fetch_one(query, params)
        
        if existing_record:
            # Ya existe un registro abierto
            self.current_record_id = existing_record['id']
        else:
            # Crear nuevo registro
            now = datetime.datetime.now().isoformat()
            
            query = """
                INSERT INTO time_records 
                (user_id, login_time, date) 
                VALUES (?, ?, ?)
            """
            params = (self.user.id, now, today)
            
            self.db_manager.execute_query(query, params)
            
            # Obtener el ID del registro creado
            query = "SELECT last_insert_rowid() as id"
            result = self.db_manager.fetch_one(query)
            
            if result:
                self.current_record_id = result['id']
        
        # Iniciar actividad de trabajo
        self.start_activity("work")
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return self.current_record_id is not None
    
    def end_session(self):
        """Finaliza la sesión de trabajo"""
        if not self.current_record_id:
            return False
        
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Finalizar la actividad actual
        self.end_activity()
        
        # Actualizar registro
        now = datetime.datetime.now().isoformat()
        
        query = """
            UPDATE time_records 
            SET logout_time = ? 
            WHERE id = ?
        """
        params = (now, self.current_record_id)
        
        result = self.db_manager.execute_query(query, params)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return result
    
    def start_activity(self, activity_type):
        """Inicia una nueva actividad"""
        if not self.current_record_id:
            return False
        
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Finalizar actividad anterior si existe
        if self.current_activity_id:
            self.end_activity()
        
        # Registrar inicio de actividad
        now = datetime.datetime.now().isoformat()
        
        query = """
            INSERT INTO activity_logs 
            (record_id, activity_type, start_time) 
            VALUES (?, ?, ?)
        """
        params = (self.current_record_id, activity_type, now)
        
        self.db_manager.execute_query(query, params)
        
        # Obtener el ID de la actividad creada
        query = "SELECT last_insert_rowid() as id"
        result = self.db_manager.fetch_one(query)
        
        if result:
            self.current_activity_id = result['id']
            self.current_activity = activity_type
            self.start_time = datetime.datetime.now()
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return self.current_activity_id is not None
    
    def end_activity(self):
        """Finaliza la actividad actual"""
        if not self.current_activity_id:
            return False
        
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Calcular duración
        now = datetime.datetime.now()
        duration = int((now - self.start_time).total_seconds())
        
        # Actualizar actividad
        query = """
            UPDATE activity_logs 
            SET end_time = ?, duration = ? 
            WHERE id = ?
        """
        params = (now.isoformat(), duration, self.current_activity_id)
        
        self.db_manager.execute_query(query, params)
        
        # Actualizar tiempos totales en el registro
        time_field = f"total_{self.current_activity}_time"
        
        query = f"""
            UPDATE time_records 
            SET {time_field} = {time_field} + ? 
            WHERE id = ?
        """
        params = (duration, self.current_record_id)
        
        self.db_manager.execute_query(query, params)
        
        # Resetear actividad actual
        self.current_activity_id = None
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        return True
    
    def change_activity(self, activity_type):
        """Cambia a una nueva actividad"""
        self.end_activity()
        return self.start_activity(activity_type)
    
    def get_current_statistics(self):
        """Obtiene estadísticas de la sesión actual"""
        if not self.current_record_id:
            return None
        
        # Conectar a la base de datos
        self.db_manager.connect()
        
        # Obtener datos del registro actual
        query = "SELECT * FROM time_records WHERE id = ?"
        params = (self.current_record_id,)
        
        record = self.db_manager.fetch_one(query, params)
        
        # Cerrar conexión
        self.db_manager.disconnect()
        
        if not record:
            return None
        
        # Calcular tiempo total
        login_time = datetime.datetime.fromisoformat(record['login_time'])
        total_time = int((datetime.datetime.now() - login_time).total_seconds())
        
        # Retornar estadísticas
        return {
            'login_time': record['login_time'],
            'total_work_time': record['total_work_time'],
            'total_break_time': record['total_break_time'],
            'total_lunch_time': record['total_lunch_time'],
            'total_bathroom_time': record['total_bathroom_time'],
            'total_meeting_time': record['total_meeting_time'],
            'total_time': total_time
        }