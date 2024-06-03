import os
import time
import logging
import psutil
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw
from plyer import notification

# Setup logging
logging.basicConfig(filename='image_converter.log', level=logging.INFO, 
                    format='%(asctime)s: %(levelname)s: %(message)s')

# Global variable to control the conversion process
is_paused = False

# Global variable to control the deletion of original files
delete_original = False

def create_image(width, height, color1, color2):
    # Create an image with the given size and colors
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(((width // 2, 0), (width, height)), fill=color2)

    return image

def setup_tray_icon():
    # Icon image
    icon_image = create_image(64, 64, 'black', 'blue')
    
   # Tray icon menu
    menu = (item('Pause/Resume', lambda : toggle_pause()), 
            item('Delete Originals', lambda : toggle_delete_original(), checked=lambda item: delete_original),
            item('Exit', lambda : exit_app()))
    icon = pystray.Icon("image_converter", icon_image, "Image Converter", menu)

    icon.run()

def toggle_delete_original():
    global delete_original
    delete_original = not delete_original
    logging.info(f"Delete Originals: {delete_original}")

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    logging.info(f"Paused: {is_paused}")

def exit_app():
    os._exit(1)

def show_notification(title, message):
    if hasattr(notification, 'notify') and callable(notification.notify):
        notification.notify(title=title, message=message, app_name="Image Converter")
    else:
        logging.warning("Notification function is not available.")



class Watcher:
    DIRECTORY_TO_WATCH = "C:/Users/anx/Downloads"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                # Log memory usage
                memory_usage = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
                logging.info(f"Memory usage: {memory_usage:.2f} MB")
                time.sleep(5)
        except:
            self.observer.stop()
            logging.error("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if event.is_directory or event.src_path.lower().endswith('.tmp'):
            return None

        Handler.process_event(event.src_path)

    @staticmethod
    def on_modified(event):
        if event.is_directory:
            return None

        Handler.process_event(event.src_path)

    @staticmethod
    def process_event(path):
        # Wait a bit to ensure the file is fully downloaded and renamed
        time.sleep(5)  # Wait for 5 seconds; adjust as needed

        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            logging.info(f"Received file event - {path}.")
            try:
                if os.path.exists(path):
                    convert_to_webp(path)
            except Exception as e:
                logging.error(f"Error converting file {path}: {e}")

def convert_to_webp(path):
    global is_paused, delete_original
    if is_paused:
        return

    if path.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_name, file_extension = os.path.splitext(path)
        original_size = os.path.getsize(path)
        show_notification("Conversion Started", f"Converting {os.path.basename(path)}")
        image = Image.open(path)
        webp_path = f"{file_name}.webp"
        image.save(webp_path, "WEBP")
        new_size = os.path.getsize(webp_path)
        logging.info(f"Converted {path} to {file_name}.webp")
        logging.info(f"Original file size: {original_size} bytes, New file size: {new_size} bytes")
        show_notification("Conversion Finished", f"Converted {os.path.basename(path)} to WebP")

        if delete_original:
            try:
                os.remove(path)
                logging.info(f"Deleted {path}")
            except Exception as e:
                logging.error(f"Error deleting {path}: {e}")

if __name__ == '__main__':
    threading.Thread(target=setup_tray_icon).start()
    w = Watcher()
    w.run()
