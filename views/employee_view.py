import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QMessageBox, QFrame,
                           QStackedWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from controllers.timer_controller import TimerController

class EmployeeView(QMainWindow):
    def __init__(self, db_manager, user):
        super().__init__()
        
        self.db_manager = db_manager
        self.user = user
        self.timer_controller = TimerController(db_manager, user)
        
        # Variables de estado
        self.current_activity = "work"  # Por defecto comienza en trabajo
        self.is_tracking = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_display)
        self.start_time = None
        self.elapsed_seconds = 0
        
        self.init_ui()
        self.start_session()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Configuración de la ventana
        self.setWindowTitle('Employee Time Tracker')
        self.setMinimumSize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Header con información del usuario
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Nombre de usuario
        user_info = QLabel(f"Usuario: {self.user.full_name}")
        user_info.setFont(QFont("Arial", 12))
        header_layout.addWidget(user_info)
        
        # Fecha actual
        date_label = QLabel(f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')}")
        date_label.setFont(QFont("Arial", 12))
        header_layout.addWidget(date_label)
        
        # Spacer
        header_layout.addStretch()
        
        # Botón de logout
        self.logout_button = QPushButton("Cerrar Sesión")
        self.logout_button.clicked.connect(self.handle_logout)
        header_layout.addWidget(self.logout_button)
        
        main_layout.addWidget(header_frame)
        
        # Contenido principal
        content_layout = QHBoxLayout()
        
        # Panel izquierdo - Controles de tiempo
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        # Título
        title_label = QLabel("Control de Tiempo")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title_label)
        
        # Tiempo transcurrido
        time_frame = QFrame()
        time_layout = QVBoxLayout(time_frame)
        
        time_title = QLabel("Tiempo actual:")
        time_title.setFont(QFont("Arial", 12))
        time_layout.addWidget(time_title)
        
        self.time_display = QLabel("00:00:00")
        self.time_display.setFont(QFont("Monospace", 36, QFont.Bold))
        self.time_display.setAlignment(Qt.AlignCenter)
        time_layout.addWidget(self.time_display)
        
        self.activity_label = QLabel("Actividad: Trabajo")
        self.activity_label.setFont(QFont("Arial", 14))
        self.activity_label.setAlignment(Qt.AlignCenter)
        time_layout.addWidget(self.activity_label)
        
        left_layout.addWidget(time_frame)
        
        # Botones de actividades
        activities_frame = QFrame()
        activities_layout = QVBoxLayout(activities_frame)
        
        activities_title = QLabel("Cambiar actividad:")
        activities_title.setFont(QFont("Arial", 12))
        activities_layout.addWidget(activities_title)
        
        
        # Botones de actividad
        self.work_button = QPushButton("Trabajo")
        self.work_button.setCheckable(True)  # Hacer que el botón sea seleccionable
        self.work_button.setChecked(True)    # Inicialmente seleccionado
        self.work_button.clicked.connect(lambda: self.toggle_activity("work"))
        activities_layout.addWidget(self.work_button)
        
        self.break_button = QPushButton("Descanso")
        self.break_button.setCheckable(True)
        self.break_button.clicked.connect(lambda: self.toggle_activity("break"))
        activities_layout.addWidget(self.break_button)
        
        self.lunch_button = QPushButton("Almuerzo")
        self.lunch_button.setCheckable(True)
        self.lunch_button.clicked.connect(lambda: self.toggle_activity("lunch"))
        activities_layout.addWidget(self.lunch_button)
        
        self.bathroom_button = QPushButton("Baño")
        self.bathroom_button.setCheckable(True)
        self.bathroom_button.clicked.connect(lambda: self.toggle_activity("bathroom"))
        activities_layout.addWidget(self.bathroom_button)
        
        self.meeting_button = QPushButton("Reunión")
        self.meeting_button.setCheckable(True)
        self.meeting_button.clicked.connect(lambda: self.toggle_activity("meeting"))
        activities_layout.addWidget(self.meeting_button)
        
        left_layout.addWidget(activities_frame)
        
        content_layout.addWidget(left_panel, 1)
        
        # Panel derecho - Estadísticas
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        # Título
        stats_title = QLabel("Estadísticas de Hoy")
        stats_title.setFont(QFont("Arial", 16, QFont.Bold))
        stats_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(stats_title)
        
        # Estadísticas
        stats_frame = QFrame()
        stats_layout = QVBoxLayout(stats_frame)
        
        # Tiempo de trabajo
        self.work_time_label = QLabel("Tiempo de trabajo: 00:00:00")
        self.work_time_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.work_time_label)
        
        # Tiempo de descanso
        self.break_time_label = QLabel("Tiempo de descanso: 00:00:00")
        self.break_time_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.break_time_label)
        
        # Tiempo de almuerzo
        self.lunch_time_label = QLabel("Tiempo de almuerzo: 00:00:00")
        self.lunch_time_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.lunch_time_label)
        
        # Tiempo de baño
        self.bathroom_time_label = QLabel("Tiempo en baño: 00:00:00")
        self.bathroom_time_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.bathroom_time_label)
        
        # Tiempo de reuniones
        self.meeting_time_label = QLabel("Tiempo en reuniones: 00:00:00")
        self.meeting_time_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.meeting_time_label)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        stats_layout.addWidget(separator)
        
        # Hora de inicio
        self.login_time_label = QLabel("Hora de inicio: --:--:--")
        self.login_time_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.login_time_label)
        
        # Tiempo total de sesión
        self.total_time_label = QLabel("Tiempo total: 00:00:00")
        self.total_time_label.setFont(QFont("Arial", 12))
        stats_layout.addWidget(self.total_time_label)
        
        right_layout.addWidget(stats_frame)
        right_layout.addStretch()
        
        content_layout.addWidget(right_panel, 1)
        
        main_layout.addLayout(content_layout)
    
    def start_session(self):
        """Inicia la sesión de trabajo"""
        # Registrar login en la base de datos
        success = self.timer_controller.start_session()
        
        if success:
            self.is_tracking = True
            self.start_time = datetime.datetime.now()
            self.timer.start(1000)  # Actualizar cada segundo
            
            # Actualizar etiqueta de hora de inicio
            self.login_time_label.setText(f"Hora de inicio: {self.start_time.strftime('%H:%M:%S')}")
            
            # Marcar el botón de trabajo como activo
            self.work_button.setStyleSheet("background-color: #8aff8a;")
            self.current_activity = "work"
            self.activity_label.setText("Actividad: Trabajo")
        else:
            QMessageBox.warning(self, "Error", "Error al iniciar la sesión")
    
    def handle_logout(self):
        """Maneja el evento de logout"""
        reply = QMessageBox.question(self, "Confirmación", 
                                     "¿Estás seguro de que deseas cerrar sesión?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.end_session()
            self.close()
            from views.login_view import LoginView
            self.login_view = LoginView(self.db_manager)
            self.login_view.show()
    
    def end_session(self):
        """Finaliza la sesión de trabajo"""
        if self.is_tracking:
            self.timer.stop()
            self.is_tracking = False
            # Registrar logout en la base de datos
            self.timer_controller.end_session()
    
    def update_time_display(self):
        """Actualiza la visualización del tiempo"""
        if self.is_tracking:
            self.elapsed_seconds += 1
            
            # Actualizar tiempo visualizado
            hours, remainder = divmod(self.elapsed_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.time_display.setText(time_str)
            
            # Actualizar estadísticas
            self.update_statistics()
    
    def change_activity(self, activity_type):
        """Cambia la actividad actual"""
        if self.current_activity == activity_type:
            return
        
        # Registrar cambio de actividad
        self.timer_controller.change_activity(activity_type)
        
        # Actualizar estado
        self.current_activity = activity_type
        
        # Actualizar etiqueta de actividad
        activity_names = {
            "work": "Trabajo",
            "break": "Descanso",
            "lunch": "Almuerzo",
            "bathroom": "Baño",
            "meeting": "Reunión"
        }
        
        self.activity_label.setText(f"Actividad: {activity_names[activity_type]}")
        
        # Actualizar estadísticas
        self.update_statistics()
    
    def update_statistics(self):
        """Actualiza las estadísticas mostradas"""
        stats = self.timer_controller.get_current_statistics()
        
        if stats:
            # Formatear tiempos para visualización
            work_time = self.format_seconds(stats['total_work_time'])
            break_time = self.format_seconds(stats['total_break_time'])
            lunch_time = self.format_seconds(stats['total_lunch_time'])
            bathroom_time = self.format_seconds(stats['total_bathroom_time'])
            meeting_time = self.format_seconds(stats['total_meeting_time'])
            total_time = self.format_seconds(stats['total_time'])
            
            # Actualizar etiquetas
            self.work_time_label.setText(f"Tiempo de trabajo: {work_time}")
            self.break_time_label.setText(f"Tiempo de descanso: {break_time}")
            self.lunch_time_label.setText(f"Tiempo de almuerzo: {lunch_time}")
            self.bathroom_time_label.setText(f"Tiempo en baño: {bathroom_time}")
            self.meeting_time_label.setText(f"Tiempo en reuniones: {meeting_time}")
            self.total_time_label.setText(f"Tiempo total: {total_time}")
    
    def format_seconds(self, seconds):
        """Formatea segundos a HH:MM:SS"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana"""
        if self.is_tracking:
            reply = QMessageBox.question(self, "Confirmación", 
                                        "¿Estás seguro de que deseas salir?\nSe cerrará tu sesión actual.",
                                        QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.end_session()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    def toggle_activity(self, activity_type):
        """Alterna entre actividades al hacer clic en los botones"""
        # Obtener el botón que se ha pulsado
        sender_button = self.sender()
        is_checked = sender_button.isChecked()

        # Lista de todos los botones
        activity_buttons = {
            "work": self.work_button,
            "break": self.break_button,
            "lunch": self.lunch_button,
            "bathroom": self.bathroom_button,
            "meeting": self.meeting_button
        }

        # Si se está desmarcando la actividad actual
        if self.current_activity == activity_type and not is_checked:
            # No permitir desmarcar la actividad actual sin seleccionar otra
            sender_button.setChecked(True)
            return

        # Si se está marcando una nueva actividad
        if is_checked and self.current_activity != activity_type:
            # Desmarcar el botón anterior
            activity_buttons[self.current_activity].setChecked(False)

            # Cambiar a la nueva actividad
            self.change_activity(activity_type)

            # Actualizar estado visual
            for act_type, button in activity_buttons.items():
                if act_type == activity_type:
                    button.setStyleSheet("background-color: #8aff8a;")  # Verde claro para actividad actual
                else:
                    button.setStyleSheet("")  # Estilo predeterminado
        elif not is_checked:
            # Si se intenta desmarcar, volver a marcar (siempre debe haber una actividad)
            sender_button.setChecked(True)