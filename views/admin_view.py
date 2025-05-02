import datetime, os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QMessageBox, QFrame,
                           QTabWidget, QTableWidget, QTableWidgetItem,
                           QComboBox, QDateEdit, QHeaderView, QDialog,
                           QFormLayout, QLineEdit)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QFont

from controllers.admin_controller import AdminController


class AdminView(QMainWindow):
    def __init__(self, db_manager, user):
        super().__init__()
        
        self.db_manager = db_manager
        self.user = user
        self.admin_controller = AdminController(db_manager)
        
        self.init_ui()
        self.load_data()
        
        # Configurar un temporizador para actualizar datos en tiempo real
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000)  # Actualizar cada 30 segundos
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Configuración de la ventana
        self.setWindowTitle('Employee Time Tracker - Panel de Administración')
        self.setMinimumSize(1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Header con información del usuario
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        # Título
        title_label = QLabel("Panel de Administración")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_layout.addWidget(title_label)
        
        # Spacer
        header_layout.addStretch()
        
        # Información del usuario
        user_info = QLabel(f"Admin: {self.user.full_name}")
        user_info.setFont(QFont("Arial", 12))
        header_layout.addWidget(user_info)
        
        # Botón de logout
        self.logout_button = QPushButton("Cerrar Sesión")
        self.logout_button.clicked.connect(self.handle_logout)
        header_layout.addWidget(self.logout_button)
        
        main_layout.addWidget(header_frame)
        
        # Contenido principal (pestañas)
        self.tab_widget = QTabWidget()
        
        # Pestaña de monitoreo en tiempo real
        self.realtime_tab = QWidget()
        realtime_layout = QVBoxLayout(self.realtime_tab)
        
        # Controles de filtrado
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        
        filter_layout.addWidget(QLabel("Filtrar por:"))
        
        self.user_filter = QComboBox()
        self.user_filter.addItem("Todos los usuarios", -1)
        filter_layout.addWidget(self.user_filter)
        
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.refresh_data)
        filter_layout.addWidget(self.refresh_button)
        
        filter_layout.addStretch()
        
        realtime_layout.addWidget(filter_frame)
        
        # Tabla de usuarios activos
        self.active_users_table = QTableWidget()
        self.active_users_table.setColumnCount(8)
        self.active_users_table.setHorizontalHeaderLabels([
            "Usuario", "Estado Actual", "Hora de Inicio", "Tiempo de Trabajo", 
            "Tiempo de Descanso", "Tiempo de Almuerzo", "Tiempo en Baño", "Tiempo en Reuniones"
        ])
        self.active_users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        realtime_layout.addWidget(self.active_users_table)
        
        self.tab_widget.addTab(self.realtime_tab, "Monitoreo en Tiempo Real")
        
        # Pestaña de reportes históricos
        self.reports_tab = QWidget()
        reports_layout = QVBoxLayout(self.reports_tab)
        
        # Controles de filtrado para reportes
        report_filter_frame = QFrame()
        report_filter_layout = QHBoxLayout(report_filter_frame)
        
        report_filter_layout.addWidget(QLabel("Usuario:"))
        self.report_user_filter = QComboBox()
        self.report_user_filter.addItem("Todos los usuarios", -1)
        report_filter_layout.addWidget(self.report_user_filter)
        
        report_filter_layout.addWidget(QLabel("Desde:"))
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addDays(-7))
        report_filter_layout.addWidget(self.from_date)
        
        report_filter_layout.addWidget(QLabel("Hasta:"))
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        report_filter_layout.addWidget(self.to_date)
        
        self.generate_report_button = QPushButton("Generar Reporte")
        self.generate_report_button.clicked.connect(self.generate_report)
        report_filter_layout.addWidget(self.generate_report_button)
        
        reports_layout.addWidget(report_filter_frame)
        
        # Tabla de reportes
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(9)
        self.reports_table.setHorizontalHeaderLabels([
            "Usuario", "Fecha", "Hora de Inicio", "Hora de Fin", "Tiempo de Trabajo", 
            "Tiempo de Descanso", "Tiempo de Almuerzo", "Tiempo en Baño", "Tiempo en Reuniones"
        ])
        self.reports_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        reports_layout.addWidget(self.reports_table)
        
        self.tab_widget.addTab(self.reports_tab, "Reportes Históricos")
        
        # Pestaña de gestión de usuarios
        self.users_tab = QWidget()
        users_layout = QVBoxLayout(self.users_tab)
        
        # Controles para gestión de usuarios
        users_controls_frame = QFrame()
        users_controls_layout = QHBoxLayout(users_controls_frame)
        
        self.add_user_button = QPushButton("Agregar Usuario")
        self.add_user_button.clicked.connect(self.show_add_user_dialog)
        users_controls_layout.addWidget(self.add_user_button)
        
        self.edit_user_button = QPushButton("Editar Usuario")
        self.edit_user_button.clicked.connect(self.show_edit_user_dialog)
        users_controls_layout.addWidget(self.edit_user_button)
        
        self.delete_user_button = QPushButton("Eliminar Usuario")
        self.delete_user_button.clicked.connect(self.delete_user)
        users_controls_layout.addWidget(self.delete_user_button)

        self.import_users_button = QPushButton("Cargar Usuarios Masivamente")
        self.import_users_button.clicked.connect(self.show_import_users_dialog)
        users_controls_layout.addWidget(self.import_users_button)
        
        users_controls_layout.addStretch()
        
        users_layout.addWidget(users_controls_frame)
        
        # Tabla de usuarios
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Usuario", "Nombre Completo", "Rol"
        ])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        users_layout.addWidget(self.users_table)
        
        self.tab_widget.addTab(self.users_tab, "Gestión de Usuarios")
        
        main_layout.addWidget(self.tab_widget)
    
    def load_data(self):
        """Carga datos iniciales"""
        # Cargar usuarios para filtros
        users = self.admin_controller.get_all_users()
        
        for user in users:
            self.user_filter.addItem(user['full_name'], user['id'])
            self.report_user_filter.addItem(user['full_name'], user['id'])
        
        # Cargar tabla de usuarios
        self.load_users_table()
        
        # Cargar datos en tiempo real
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos en tiempo real"""
        # Obtener el filtro de usuario seleccionado
        user_id = self.user_filter.currentData()
        
        # Obtener datos actualizados
        active_sessions = self.admin_controller.get_active_sessions(user_id)
        
        # Actualizar tabla
        self.active_users_table.setRowCount(len(active_sessions))
        
        for row, session in enumerate(active_sessions):
            # Usuario
            self.active_users_table.setItem(row, 0, QTableWidgetItem(session['username']))
            
            # Estado actual
            self.active_users_table.setItem(row, 1, QTableWidgetItem(self.get_activity_name(session['current_activity'])))
            
            # Hora de inicio
            login_time = datetime.datetime.fromisoformat(session['login_time'])
            self.active_users_table.setItem(row, 2, QTableWidgetItem(login_time.strftime('%H:%M:%S')))
            
            # Tiempos de actividades
            self.active_users_table.setItem(row, 3, QTableWidgetItem(self.format_seconds(session['total_work_time'])))
            self.active_users_table.setItem(row, 4, QTableWidgetItem(self.format_seconds(session['total_break_time'])))
            self.active_users_table.setItem(row, 5, QTableWidgetItem(self.format_seconds(session['total_lunch_time'])))
            self.active_users_table.setItem(row, 6, QTableWidgetItem(self.format_seconds(session['total_bathroom_time'])))
            self.active_users_table.setItem(row, 7, QTableWidgetItem(self.format_seconds(session['total_meeting_time'])))
    
    def generate_report(self):
        """Genera un reporte histórico"""
        # Obtener filtros
        user_id = self.report_user_filter.currentData()
        from_date = self.from_date.date().toString("yyyy-MM-dd")
        to_date = self.to_date.date().toString("yyyy-MM-dd")
        
        # Obtener datos de reporte
        report_data = self.admin_controller.get_historical_report(user_id, from_date, to_date)
        
        # Actualizar tabla
        self.reports_table.setRowCount(len(report_data))
        
        for row, record in enumerate(report_data):
            # Usuario
            self.reports_table.setItem(row, 0, QTableWidgetItem(record['username']))
            
            # Fecha
            self.reports_table.setItem(row, 1, QTableWidgetItem(record['date']))
            
            # Hora de inicio
            if record['login_time']:
                login_time = datetime.datetime.fromisoformat(record['login_time'])
                self.reports_table.setItem(row, 2, QTableWidgetItem(login_time.strftime('%H:%M:%S')))
            else:
                self.reports_table.setItem(row, 2, QTableWidgetItem("--"))
            
            # Hora de fin
            if record['logout_time']:
                logout_time = datetime.datetime.fromisoformat(record['logout_time'])
                self.reports_table.setItem(row, 3, QTableWidgetItem(logout_time.strftime('%H:%M:%S')))
            else:
                self.reports_table.setItem(row, 3, QTableWidgetItem("Activo"))
            
            # Tiempos de actividades
            self.reports_table.setItem(row, 4, QTableWidgetItem(self.format_seconds(record['total_work_time'])))
            self.reports_table.setItem(row, 5, QTableWidgetItem(self.format_seconds(record['total_break_time'])))
            self.reports_table.setItem(row, 6, QTableWidgetItem(self.format_seconds(record['total_lunch_time'])))
            self.reports_table.setItem(row, 7, QTableWidgetItem(self.format_seconds(record['total_bathroom_time'])))
            self.reports_table.setItem(row, 8, QTableWidgetItem(self.format_seconds(record['total_meeting_time'])))
    
    def load_users_table(self):
        """Carga la tabla de usuarios"""
        users = self.admin_controller.get_all_users()
        
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.users_table.setItem(row, 1, QTableWidgetItem(user['username']))
            self.users_table.setItem(row, 2, QTableWidgetItem(user['full_name']))
            self.users_table.setItem(row, 3, QTableWidgetItem(user['role']))
    
    def show_add_user_dialog(self):
        """Muestra diálogo para agregar usuario"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Nuevo Usuario")
        dialog.setMinimumWidth(300)
        
        layout = QFormLayout(dialog)
        
        # Campos
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        fullname_input = QLineEdit()
        
        role_input = QComboBox()
        role_input.addItem("Empleado", "employee")
        role_input.addItem("Administrador", "admin")
        
        # Agregar campos al layout
        layout.addRow("Usuario:", username_input)
        layout.addRow("Contraseña:", password_input)
        layout.addRow("Nombre Completo:", fullname_input)
        layout.addRow("Rol:", role_input)
        
        # Botones
        button_box = QHBoxLayout()
        save_button = QPushButton("Guardar")
        cancel_button = QPushButton("Cancelar")
        
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        
        layout.addRow("", button_box)
        
        # Conectar eventos
        save_button.clicked.connect(lambda: self.add_user(
            username_input.text(),
            password_input.text(),
            fullname_input.text(),
            role_input.currentData(),
            dialog
        ))
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec_()
    
    def add_user(self, username, password, full_name, role, dialog):
        """Agrega un nuevo usuario"""
        if not username or not password or not full_name:
            QMessageBox.warning(dialog, "Error", "Todos los campos son obligatorios")
            return
        
        success = self.admin_controller.add_user(username, password, full_name, role)
        
        if success:
            QMessageBox.information(dialog, "Éxito", "Usuario agregado correctamente")
            dialog.accept()
            
            # Recargar datos
            self.load_users_table()
            
            # Actualizar filtros
            self.user_filter.clear()
            self.report_user_filter.clear()
            self.user_filter.addItem("Todos los usuarios", -1)
            self.report_user_filter.addItem("Todos los usuarios", -1)
            
            users = self.admin_controller.get_all_users()
            for user in users:
                self.user_filter.addItem(user['full_name'], user['id'])
                self.report_user_filter.addItem(user['full_name'], user['id'])
        else:
            QMessageBox.warning(dialog, "Error", "Error al agregar usuario. El nombre de usuario podría estar en uso.")
    
    def show_edit_user_dialog(self):
        """Muestra diálogo para editar usuario"""
        # Verificar si hay una fila seleccionada
        selected_items = self.users_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Por favor seleccione un usuario para editar")
            return
        
        row = selected_items[0].row()
        user_id = int(self.users_table.item(row, 0).text())
        
        # Obtener datos del usuario
        user = self.admin_controller.get_user_by_id(user_id)
        
        if not user:
            QMessageBox.warning(self, "Error", "No se pudo obtener información del usuario")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Usuario")
        dialog.setMinimumWidth(300)
        
        layout = QFormLayout(dialog)
        
        # Campos
        username_input = QLineEdit(user['username'])
        username_input.setEnabled(False)  # No permitir cambiar el nombre de usuario
        
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Dejar en blanco para mantener la actual")
        
        fullname_input = QLineEdit(user['full_name'])
        
        role_input = QComboBox()
        role_input.addItem("Empleado", "employee")
        role_input.addItem("Administrador", "admin")
        
        # Establecer rol actual
        index = role_input.findData(user['role'])
        if index >= 0:
            role_input.setCurrentIndex(index)
        
        # Agregar campos al layout
        layout.addRow("Usuario:", username_input)
        layout.addRow("Nueva Contraseña:", password_input)
        layout.addRow("Nombre Completo:", fullname_input)
        layout.addRow("Rol:", role_input)
        
        # Botones
        button_box = QHBoxLayout()
        save_button = QPushButton("Guardar")
        cancel_button = QPushButton("Cancelar")
        
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        
        layout.addRow("", button_box)
        
        # Conectar eventos
        save_button.clicked.connect(lambda: self.update_user(
            user_id,
            password_input.text(),
            fullname_input.text(),
            role_input.currentData(),
            dialog
        ))
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec_()
    
    def update_user(self, user_id, password, full_name, role, dialog):
        """Actualiza un usuario existente"""
        if not full_name:
            QMessageBox.warning(dialog, "Error", "El nombre completo es obligatorio")
            return
        
        success = self.admin_controller.update_user(user_id, password, full_name, role)
        
        if success:
            QMessageBox.information(dialog, "Éxito", "Usuario actualizado correctamente")
            dialog.accept()
            
            # Recargar datos
            self.load_users_table()
            
            # Actualizar filtros
            self.user_filter.clear()
            self.report_user_filter.clear()
            self.user_filter.addItem("Todos los usuarios", -1)
            self.report_user_filter.addItem("Todos los usuarios", -1)
            
            users = self.admin_controller.get_all_users()
            for user in users:
                self.user_filter.addItem(user['full_name'], user['id'])
                self.report_user_filter.addItem(user['full_name'], user['id'])
        else:
            QMessageBox.warning(dialog, "Error", "Error al actualizar usuario")
    
    def delete_user(self):
        """Elimina un usuario"""
        # Verificar si hay una fila seleccionada
        selected_items = self.users_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Por favor seleccione un usuario para eliminar")
            return
        
        row = selected_items[0].row()
        user_id = int(self.users_table.item(row, 0).text())
        username = self.users_table.item(row, 1).text()
        
        # Confirmar eliminación
        reply = QMessageBox.question(self, "Confirmar Eliminación", 
                                    f"¿Está seguro de que desea eliminar al usuario '{username}'?\n\n"
                                    "Esta acción no se puede deshacer y eliminará todos los registros de tiempo asociados.",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply != QMessageBox.Yes:
            return
        
        success = self.admin_controller.delete_user(user_id)
        
        if success:
            QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
            
            # Recargar datos
            self.load_users_table()
            
            # Actualizar filtros
            self.user_filter.clear()
            self.report_user_filter.clear()
            self.user_filter.addItem("Todos los usuarios", -1)
            self.report_user_filter.addItem("Todos los usuarios", -1)
            
            users = self.admin_controller.get_all_users()
            for user in users:
                self.user_filter.addItem(user['full_name'], user['id'])
                self.report_user_filter.addItem(user['full_name'], user['id'])
        else:
            QMessageBox.warning(self, "Error", "Error al eliminar usuario")
    
    def handle_logout(self):
        """Maneja el evento de logout"""
        self.close()
        from views.login_view import LoginView
        self.login_view = LoginView(self.db_manager)
        self.login_view.show()
    
    def get_activity_name(self, activity_type):
        """Obtiene el nombre legible de una actividad"""
        activity_names = {
            "work": "Trabajo",
            "break": "Descanso",
            "lunch": "Almuerzo",
            "bathroom": "Baño",
            "meeting": "Reunión"
        }
        
        return activity_names.get(activity_type, "Desconocido")
    
    def format_seconds(self, seconds):
        """Formatea segundos a HH:MM:SS"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def show_import_users_dialog(self):
        """Muestra el diálogo para importar usuarios desde un archivo CSV"""
        from PyQt5.QtWidgets import QFileDialog

        # Abrir diálogo para seleccionar archivo
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo CSV", "", "Archivos CSV (*.csv)"
        )

        if not file_path:
            return

        # Crear y mostrar diálogo de configuración de importación
        dialog = QDialog(self)
        dialog.setWindowTitle("Importar Usuarios")
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)

        # Instrucciones
        instructions = QLabel(
            "El archivo CSV debe tener el siguiente formato:\n"
            "usuario,contraseña,nombre_completo,rol\n\n"
            "El rol debe ser 'admin' o 'employee'."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Nombre del archivo
        file_label = QLabel(f"Archivo seleccionado: {os.path.basename(file_path)}")
        layout.addWidget(file_label)

        # Botones
        button_layout = QHBoxLayout()
        import_button = QPushButton("Importar")
        cancel_button = QPushButton("Cancelar")

        button_layout.addWidget(import_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Conectar eventos
        import_button.clicked.connect(lambda: self.import_users_from_csv(file_path, dialog))
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()

def import_users_from_csv(self, file_path, dialog):
    """Importa usuarios desde un archivo CSV"""
    import csv
    
    try:
        # Leer archivo CSV
        users_to_import = []
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Saltar encabezado si existe
            header = next(reader, None)
            if header and header[0].lower() == 'usuario':
                pass  # Saltar encabezado
            else:
                # Si no hay encabezado, volver al inicio del archivo
                file.seek(0)
                reader = csv.reader(file)
            
            # Leer filas
            for row in reader:
                if len(row) >= 4:
                    users_to_import.append({
                        'username': row[0].strip(),
                        'password': row[1].strip(),
                        'full_name': row[2].strip(),
                        'role': row[3].strip().lower()
                    })
        
        # Validar datos
        invalid_rows = []
        for i, user in enumerate(users_to_import):
            if not all([user['username'], user['password'], user['full_name']]):
                invalid_rows.append(i + 1)
            elif user['role'] not in ['admin', 'employee']:
                invalid_rows.append(i + 1)
        
        if invalid_rows:
            error_msg = f"Se encontraron {len(invalid_rows)} filas con formato inválido (filas: {', '.join(map(str, invalid_rows))})"
            QMessageBox.warning(dialog, "Error", error_msg)
            return
        
        # Importar usuarios
        success_count = 0
        error_count = 0
        
        for user in users_to_import:
            result = self.admin_controller.add_user(
                user['username'], 
                user['password'], 
                user['full_name'], 
                user['role']
            )
            
            if result:
                success_count += 1
            else:
                error_count += 1
        
        # Mostrar resultado
        if error_count == 0:
            QMessageBox.information(
                dialog, 
                "Importación Exitosa", 
                f"Se importaron {success_count} usuarios correctamente."
            )
        else:
            QMessageBox.warning(
                dialog, 
                "Importación Parcial", 
                f"Se importaron {success_count} usuarios correctamente.\n"
                f"No se pudieron importar {error_count} usuarios (posiblemente ya existen)."
            )
        
        # Actualizar tabla de usuarios
        self.load_users_table()
        
        # Actualizar filtros de usuarios
        self.user_filter.clear()
        self.report_user_filter.clear()
        self.user_filter.addItem("Todos los usuarios", -1)
        self.report_user_filter.addItem("Todos los usuarios", -1)
        
        users = self.admin_controller.get_all_users()
        for user in users:
            self.user_filter.addItem(user['full_name'], user['id'])
            self.report_user_filter.addItem(user['full_name'], user['id'])
        
        dialog.accept()
        
    except Exception as e:
        QMessageBox.critical(dialog, "Error", f"Error al importar usuarios: {str(e)}")