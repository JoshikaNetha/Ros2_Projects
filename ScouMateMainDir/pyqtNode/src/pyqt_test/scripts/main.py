from threading import Thread

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QTimer

import sys
import cv2
import time
import os
import base64
import json

# from video import VideoThread
# from tcpServer import TCPServer
# from joystick_controller import UXVJoystickController
# from voice_Recorder import VoiceRecorder
# from controller.protocol import (
#     GCS_CMD,
#     GCS_Packet,
#     GCS_OSD_Data,
#     GCS_Camera_Stream_Data,
#     GCS_VOICE_DATA
# )
# from core.config import settings
import os



class RoverGCS(QtWidgets.QMainWindow):
    def __init__(self):
        super(RoverGCS,self).__init__()

        self.init()

    def init(self):
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "mainWindow.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("ScoutMate GCS")

        self.startRecordBtn : QPushButton
        self.stopRecordBtn  : QPushButton
        self.captureBtn     : QPushButton
        self.osdOnBtn       : QPushButton
        self.osdOffBtn      : QPushButton
        self.zoomInBtn      : QPushButton
        self.zoomOutBtn     : QPushButton
        self.closeBtn       : QPushButton

        self.cameraAllButton    : QPushButton
        self.cameraFrontButton  : QPushButton
        self.cameraBackButton   : QPushButton
        self.cameraLeftButton   : QPushButton
        self.cameraRightButton  : QPushButton
        self.voiceCommand       : QPushButton 

        self.videoLabel     : QLabel

        self.startRecordBtn.clicked.connect(self.startRecording)
        self.stopRecordBtn.clicked.connect(self.stopRecording)
        self.captureBtn.clicked.connect(self.takeSnapshot)
        self.osdOnBtn.clicked.connect(self.osd_On)
        self.osdOffBtn.clicked.connect(self.osd_Off)
        self.zoomInBtn.clicked.connect(self.zoom_in)
        self.zoomOutBtn.clicked.connect(self.zoom_out)
        self.closeBtn.clicked.connect(self.close)

        # self.cameraAllButton.clicked.connect(self.enableAllCamera)
        # self.cameraFrontButton.clicked.connect(self.enableFrontCamera)
        # self.cameraBackButton.clicked.connect(self.enableBackCamera)
        # self.cameraLeftButton.clicked.connect(self.enableLeftCamera)
        # self.cameraRightButton.clicked.connect(self.enableRightCamera)

        # Initialize zoom factor (1.0 means no zoom)
        self.zoom_factor = 1.0

        # self.videoLabel.setScaledContents(True)
        # self.videoThread = VideoThread(self)
        # self.videoThread.image_update_signal.connect(self.update_image)
        # self.videoThread.start()

        # Start TCP Server in a separate thread
        # def run_tcp_server(server:TCPServer):
        #     server.start()

        # self.server = TCPServer(host="0.0.0.0", port=9000, client_timeout=10)

        # self.tcp_server_thread:Thread = Thread(target=run_tcp_server, args=[self.server], daemon=True)
        # self.tcp_server_thread.start()

        # self.osdInformation: GCS_Packet[GCS_OSD_Data] = GCS_Packet(
        #     cmd=GCS_CMD.CAMERA_OSD,
        #     data=GCS_OSD_Data(enable=True)
        # )

        # self.cameraStreamInfo: GCS_Packet[GCS_Camera_Stream_Data] = GCS_Packet(
        #     cmd=GCS_CMD.CAMERA_STREAM_ALL,
        #     data=GCS_Camera_Stream_Data(id=0)
        # )

        # self.voiceStreamInfo: GCS_Packet[GCS_VOICE_DATA] = GCS_Packet(
        #     cmd=GCS_CMD.VOICE_DATA,
        #     data = GCS_VOICE_DATA(enable=False)

        # )
        self.joystickController = None
        # if settings.JOYSTICK_ENABLE:
            # self.joystickController = UXVJoystickController(self.server.sendData)
            # self.joystickController.start()
        

        # Voice Command handlers
        # self.voiceCommand.clicked.connect(self.voiceCmd_single_click)
        # self.voice_button_timer = QTimer()
        # self.voice_button_timer.setSingleShot(True)
        # self.voice_button_timer.timeout.connect(self.voiceCmd_handle_single_click)
        # self.is_listening = False  # Track listening state
        # self.frames = None

        self.show()


    def dialogBox(self,image):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        if image:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Snapshot",
            "",
            "Images (*.png *.jpg *.bmp);;All Files (*)",
            options=options)
            return file_path
        else:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Video",
            "",
            "Videos (*.mp4 *.avi);;All Files (*)",
            options=options)
            return file_path


    def startRecording(self):
        # Open a Save File Dialog

        file_path = self.dialogBox(False)

        # If a valid file path is selected
        if file_path:
            if not file_path.lower().endswith(('.mp4', '.avi')):
                file_path += ".mp4"  # Append default extension if not provided

            # self.videoThread.startRecording(file_path)


    def stopRecording(self):
        print("stop recording")
        # self.videoThread.stopRecording()


    def takeSnapshot(self):
        # Open a Save File Dialog

        file_path = self.dialogBox(True)

        # If a valid file path is selected
        if file_path:
            # Ensure a valid file extension is present
            valid_extensions = {".png", ".jpg", ".bmp"}
            _, ext = os.path.splitext(file_path)

            if ext.lower() not in valid_extensions:
                # Default to PNG if no extension is provided
                file_path += ".png"

            # Capture the current frame from the video thread
            current_frame = self.videoThread.current_frame
            if current_frame is not None:

                # Save the frame using OpenCV
                success = cv2.imwrite(file_path, current_frame)
                if success:
                    print(f"Snapshot saved at {file_path}")
                else:
                    print(f"Error saving snapshot at {file_path}")
            else:
                print("No frame captured!")


    def osd_On(self):
        print("OSD OON")
    #     self.osdInformation.data.enable = True
    #     # self.server.sendData(data=self.osdInformation.model_dump())


    def osd_Off(self):
        print("OSD OFF")
    #     self.osdInformation.data.enable = False
    #     # self.server.sendData(data=self.osdInformation.model_dump())


    def update_image(self, qt_img):
        # If zoom is applied and a current frame is available, recalc the QImage.
        if self.zoom_factor != 1.0 and self.videoThread.current_frame is not None:
            # Use the original frame (a NumPy array)
            frame = self.videoThread.current_frame
            zoomed_frame = self.apply_zoom(frame, self.zoom_factor)
            # Convert zoomed frame from BGR (OpenCV) to RGB
            rgb_image = cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.videoLabel.setPixmap(QPixmap.fromImage(qt_img))


    def apply_zoom(self, frame, zoom_factor):
        """
        Crop and resize the given frame to simulate zoom.
        :param frame: The original frame (numpy array)
        :param zoom_factor: A float value; >1 means zoom in, <1 means zoom out.
        :return: The zoomed frame (numpy array)
        """
        if zoom_factor == 1.0:
            return frame  # No zoom applied

        # Get original dimensions
        h, w, _ = frame.shape

        # For zoom in, we want to crop a smaller region from the center.
        # For zoom out, one typical approach is to use the whole frame,
        # but you might decide to pad it instead. Here we only implement zoom in.
        # Calculate the crop dimensions (smaller than original)
        crop_w = int(w / zoom_factor)
        crop_h = int(h / zoom_factor)

        # Calculate top-left corner of the crop region (centered)
        start_x = (w - crop_w) // 2
        start_y = (h - crop_h) // 2

        # Crop the frame
        cropped = frame[start_y:start_y+crop_h, start_x:start_x+crop_w]

        # Resize the cropped region back to the original frame size for display
        zoomed = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
        return zoomed


    def zoom_in(self):
        """Increase the zoom factor."""
        self.zoom_factor *= 1.1  # Increase by 10%
        print("Zoom In: ", self.zoom_factor)


    def zoom_out(self):
        """Decrease the zoom factor (minimum 1.0)."""
        self.zoom_factor /= 1.1  # Decrease by 10%
        if self.zoom_factor < 1.0:
            self.zoom_factor = 1.0
        print("Zoom Out: ", self.zoom_factor)

    # def enableAllCamera(self):
    #     self.cameraStreamInfo.data.id = 0
        # self.server.sendData(self.cameraStreamInfo.model_dump())
         
    # def enableFrontCamera(self):        # Start TCP Server in a separate thread
    #     # def run_tcp_server(server:TCPServer):
    #     #     server.start()

    #     # self.server = TCPServer(host="0.0.0.0", port=9000, client_timeout=10)

    #     # self.tcp_server_thread:Thread = Thread(target=run_tcp_server, args=[self.server], daemon=True)
    #     # self.tcp_server_thread.start()
    #     self.cameraStreamInfo.data.id = 1
    #     # self.server.sendData(self.cameraStreamInfo.model_dump())
    # def enableBackCamera(self):
    #     self.cameraStreamInfo.data.id = 2
    #     # self.server.sendData(self.cameraStreamInfo.model_dump())
    # def enableLeftCamera(self):
    #     self.cameraStreamInfo.data.id = 3
    #     # self.server.sendData(self.cameraStreamInfo.model_dump())
    # def enableRightCamera(self):
    #     self.cameraStreamInfo.data.id = 4
    #     # self.server.sendData(self.cameraStreamInfo.model_dump())

    # def voiceCmd_single_click(self):
    #     """Handles single click event with a delay to detect double-click"""
    #     if self.is_listening:
    #         self.voice_button_timer.stop()
    #         self.voiceCmd_handle_double_click()
    #     else:
    #         self.voice_button_timer.start(250)  # Wait for double click detection

    # def voiceCmd_handle_single_click(self):
    #     """Handle single click - Start listening"""
    #     self.voiceCommand.setText("Stop Listening")  # Change button text
    #     self.voiceStreamInfo.data.enable = True
        # self.server.sendData(data=self.voiceStreamInfo.model_dump())
        
        # Start AudioRecorder thread
        # self.voice_recorder = VoiceRecorder()
        # self.voice_recorder.voice_signal.connect(self.voiceCmd_sendData)  # Process audio data
        # self.voice_recorder.start()
        # self.is_listening = True

    # def voiceCmd_handle_double_click(self):
    #     """Handle double click - Stop listening"""
    #     self.voiceCommand.setText("Start Listening")  # Change button text
    #     self.voiceStreamInfo.data.enable = False
    #     # self.server.sendData(data=self.voiceStreamInfo.model_dump())
        

    def voiceCmd_sendData(self, data):
        self.frames = data   

    def close(self):
        # self.videoThread.close()
        # self.server.stop()
        time.sleep(0.5)
        QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RoverGCS()
    app.exec_()
