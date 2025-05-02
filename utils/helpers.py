import datetime

def format_seconds(seconds):
    """Formatea segundos a HH:MM:SS"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def format_time_for_display(datetime_str):
    """Formatea una cadena de fecha/hora ISO para visualización"""
    if not datetime_str:
        return "--"
    
    try:
        dt = datetime.datetime.fromisoformat(datetime_str)
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return datetime_str

def calculate_total_time(login_time, logout_time=None):
    """Calcula el tiempo total entre dos marcas de tiempo"""
    if not login_time:
        return 0
    
    try:
        start = datetime.datetime.fromisoformat(login_time)
        end = datetime.datetime.fromisoformat(logout_time) if logout_time else datetime.datetime.now()
        
        return int((end - start).total_seconds())
    except ValueError:
        return 0

def get_date_range(days=7):
    """Obtiene un rango de fechas desde hoy hacia atrás"""
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)
    
    return start_date, end_date