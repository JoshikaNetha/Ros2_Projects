import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        # Load .env file if exists
        load_dotenv()

        self.TCP_GCS_IP: str = os.getenv("TCP_GCS_IP", "0.0.0.0")
        self.TCP_GCS_PORT: int = int(os.getenv("TCP_GCS_PORT", 9000))


        self.JOYSTICK_ENABLE: bool          = self.is_true(os.getenv("JOYSTICK_ENABLE", "true"))
        self.JOYSTICK_FIX_SERVO_BUTTON: int = int(os.getenv("JOYSTICK_FIX_SERVO_BUTTON", 9))
        self.JOYSTICK_MOVE_FRONT: int       = int(os.getenv("JOYSTICK_MOVE_FRONT", 3))
        self.JOYSTICK_MOVE_SIDEWAYS: int    = int(os.getenv("JOYSTICK_MOVE_SIDEWAYS", 2))
        self.JOYSTICK_YAW: int              = int(os.getenv("JOYSTICK_YAW", 0))
        self.JOYSTICK_SERVO_MOVE: int       = int(os.getenv("JOYSTICK_SERVO_MOVE", 4))

        self.ROVER_IP: str                  = os.getenv("ROVER_IP", "0.0.0.0")
        self.ROVER_RTSP_PORT: int           = int(os.getenv("ROVER_RTSP_PORT", 8554))
        self.ROVER_RTSP_LINK: str           = os.getenv("ROVER_RTSP_LINK", "stream")

        self.VOICE_SAMPLE_RATE:int          = int(os.getenv("VOICE_SAMPLE_RATE", 44100))
        self.VOICE_CHANNELS:int             = int(os.getenv("VOICE_CHANNELS", 1))
        self.VOICE_CHUNK:int                = int(os.getenv("VOICE_CHUNK", 1024))

    def is_true(self, val:str):
        return val.lower() in ['true', '1']

settings = Settings()