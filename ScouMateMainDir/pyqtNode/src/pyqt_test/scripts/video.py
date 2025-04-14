import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import cv2

from core.config import settings

class VideoThread(QThread):

    image_update_signal = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.rtsp_link = f"rtsp://{settings.ROVER_IP}:{settings.ROVER_RTSP_PORT}/{settings.ROVER_RTSP_LINK}"
        self.current_frame = None  # Store the latest frame
        self.alive = False
        self.cap:cv2.VideoCapture = None       
        self.out = None  # For VideoWriter
        self.recording = False  # Flag indicating recording state


    def connect(self):
        try:
            if self.cap:
                self.cap.release()
            while self.alive:
                print("Trying to connect to RTSP")
                self.cap = cv2.VideoCapture(self.rtsp_link)
                if self.cap.isOpened():
                    return
                time.sleep(1)
        except Exception as e:
            print(f"[ERROR] Not able to open: {self.rtsp_link}")
            time.sleep(1)

    def run(self):
        self.alive = True
        self.connect()
        while self.alive:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    self.connect()
                    continue
                self.current_frame = frame  # Store the latest frame
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                # Scale the image to fit the videoWidget's dimensions while keeping the aspect ratio
                self.image_update_signal.emit(qt_image)
                
                if self.recording:
                    # Write the current frame to the video file if recording
                    self.out.write(frame)
            except Exception as e:
                print(f"Error in frame processing: {e}")
                self.connect()

    def startRecording(self,file_path):
        if self.recording:
            print("Recording is already in progress.")
            return

        print("Starting video recording...")

        # Start capturing video from the camera (or a video source)
        if not self.cap.isOpened():
            print("Error: Camera not accessible.")
            return

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for .mp4
        height, width, _ = self.current_frame.shape
        self.out = cv2.VideoWriter(file_path, fourcc, 20.0, (width, height))  # Adjust frame size as needed

        if not self.out.isOpened():
            print(f"Failed to open VideoWriter for file: {file_path}")
            return

        self.recording = True  # Flag indicating that recording is active
        print(f"Recording started, saving to {file_path}...")


    def stopRecording(self):
        if self.recording:
            self.recording = False
            print("Stopping recording...")

            if self.out:
                self.out.release()
            self.out = None
        else:
            print("No recording in progress.")


    def close(self):
        self.alive = False
        if self.cap:
            self.cap.release()
       
