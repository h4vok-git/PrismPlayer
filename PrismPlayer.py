import sys
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrismPlayer")
        self.setGeometry(100, 100, 300, 100)
        # this creates the VLC instance  
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        
        open_button = QPushButton("Open Video", self)
        open_button.clicked.connect(self.open_file)
        open_button.setGeometry(100, 40, 100, 40)  

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.mov)"
        )
        if file_path:
            media = self.vlc_instance.media_new(file_path)
            self.media_player.set_media(media)
            self.media_player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())