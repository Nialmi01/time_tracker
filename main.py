import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from database.db_manager import DatabaseManager
from views.login_view import LoginView
from utils.config import load_config

def main():
    # Cargar configuraciones
    config = load_config()
    
    # Inicializar base de datos
    db_manager = DatabaseManager(config['database_path'])
    db_manager.setup_database()
    
    # Inicializar aplicación
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('resources/images/app_icon.png'))
    app.setApplicationName('Employee Time Tracker')
    
    # Mostrar ventana de login
    login_window = LoginView(db_manager)
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    