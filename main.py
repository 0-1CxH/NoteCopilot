from src.server import NoteCopilotServer
import os

if __name__ == '__main__':
    # Get the absolute path to the static folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(current_dir, "static")
    
    server = NoteCopilotServer(static_folder=static_folder)
    server.run(debug=True, port=5000)