import sys
import vlc
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrismPlayer")
        self.setGeometry(100, 100, 800, 600)

        # Create a VLC instance
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        self.init_ui()

        # timer is used to update the seekbar 
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_seekbar)


    def init_ui(self):
        #used for displaying video inside the window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.video_widget = QVideoWidget(self)
        self.media_player.set_hwnd(int(self.video_widget.winId()))

        # Buttons
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.stop_button = QPushButton("Stop", self)
        self.open_button = QPushButton("Open", self)
        self.fullscreen_button = QPushButton("Fullscreen", self)

        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.open_button.clicked.connect(self.open_file)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # draws buttons  
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.fullscreen_button)

        #draws the seek bar
        self.seek_bar = QSlider(Qt.Horizontal, self)
        self.seek_bar.setRange(0, 1000)
        self.seek_bar.sliderMoved.connect(self.set_position)
       
        #draws the black box for video and the seek bar
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget)
        main_layout.addWidget(self.seek_bar)
        main_layout.addLayout(control_layout)
        central_widget.setLayout(main_layout)


    def play_video(self):
        self.media_player.play()
        self.timer.start()

    def pause_video(self):
        self.media_player.pause()

    def stop_video(self):
        self.media_player.stop()
        self.timer.stop()
    
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.mov)"
        )
        if file_path:
            media = self.vlc_instance.media_new(file_path)
            self.media_player.set_media(media)
            self.media_player.set_hwnd(int(self.video_widget.winId()))
            self.play_video()

    def update_seekbar(self):
        if self.media_player.is_playing():
            pos = self.media_player.get_position()  # 0.0 to 1.0
            self.seek_bar.setValue(int(pos * 1000))

    def set_position(self, value):
        self.media_player.set_position(value / 1000.0)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())