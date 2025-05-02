from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from controllers.auth_controller import AuthController
from views.employee_view import EmployeeView
from views.admin_view import AdminView

class LoginView(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        
        self.db_manager = db_manager
        self.auth_controller = AuthController(db_manager)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Configuración de la ventana
        self.setWindowTitle('Time Tracker - Login')
        self.setFixedSize(450, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Logo
        logo_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap('resources/images/logo.png')
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaledToWidth(200, Qt.SmoothTransformation))
        else:
            logo_label.setText("Time Tracker")
            logo_label.setFont(QFont("Arial", 18, QFont.Bold))
        
        logo_layout.addStretch()
        logo_layout.addWidget(logo_label)
        logo_layout.addStretch()
        main_layout.addLayout(logo_layout)
        
        # Título
        title_label = QLabel("Iniciar Sesión")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Formulario de login
        form_layout = QVBoxLayout()
        
        # Usuario
        username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su nombre de usuario")
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        
        # Contraseña
        password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        main_layout.addLayout(form_layout)
        
        # Botón de login
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button)
        
        # Espacio en blanco
        main_layout.addStretch()
        
        # Copyright
        copyright_label = QLabel("© 2025 Time Tracker")
        copyright_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(copyright_label)
    
    def handle_login(self):
        """Maneja el evento de login"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return
        
        user = self.auth_controller.login(username, password)
        
        if user:
            # Iniciar sesión exitosa
            self.hide()
            
            if user.is_admin():
                # Abrir vista de administrador
                self.admin_view = AdminView(self.db_manager, user)
                self.admin_view.show()
            else:
                # Abrir vista de empleado
                self.employee_view = EmployeeView(self.db_manager, user)
                self.employee_view.show()
        else:
            # Error de login
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")