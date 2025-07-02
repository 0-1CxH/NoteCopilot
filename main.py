from src.server import NoteCopilotServer
import os

if __name__ == '__main__':
    # Get the absolute path to the static folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(current_dir, "static")
    notes_folder  = os.path.join(current_dir, "notes_save")
    ai_services_config_path  = os.path.join(current_dir, "services.yaml")
    ai_functions_config_path  = os.path.join(current_dir, "functions.yaml")
    
    server = NoteCopilotServer(
        static_folder=static_folder, 
        notes_folder=notes_folder,
        ai_services_config_path=ai_services_config_path,
        ai_functions_config_path=ai_functions_config_path,
    )
    server.run(debug=True, port=27871)