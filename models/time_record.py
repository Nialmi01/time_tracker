import datetime

class TimeRecord:
    def __init__(self, id=None, user_id=None, login_time=None, logout_time=None, 
                 total_work_time=0, total_break_time=0, total_lunch_time=0,
                 total_bathroom_time=0, total_meeting_time=0, date=None):
        self.id = id
        self.user_id = user_id
        self.login_time = login_time
        self.logout_time = logout_time
        self.total_work_time = total_work_time
        self.total_break_time = total_break_time
        self.total_lunch_time = total_lunch_time
        self.total_bathroom_time = total_bathroom_time
        self.total_meeting_time = total_meeting_time
        self.date = date if date else datetime.date.today().strftime("%Y-%m-%d")
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto TimeRecord a partir de una fila de la base de datos"""
        if not row:
            return None
            
        return cls(
            id=row['id'],
            user_id=row['user_id'],
            login_time=row['login_time'],
            logout_time=row['logout_time'],
            total_work_time=row['total_work_time'],
            total_break_time=row['total_break_time'],
            total_lunch_time=row['total_lunch_time'],
            total_bathroom_time=row['total_bathroom_time'],
            total_meeting_time=row['total_meeting_time'],
            date=row['date']
        )

class ActivityLog:
    def __init__(self, id=None, record_id=None, activity_type=None, 
                 start_time=None, end_time=None, duration=0):
        self.id = id
        self.record_id = record_id
        self.activity_type = activity_type
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto ActivityLog a partir de una fila de la base de datos"""
        if not row:
            return None
            
        return cls(
            id=row['id'],
            record_id=row['record_id'],
            activity_type=row['activity_type'],
            start_time=row['start_time'],
            end_time=row['end_time'],
            duration=row['duration']
        )