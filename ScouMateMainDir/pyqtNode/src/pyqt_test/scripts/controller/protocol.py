from enum import IntEnum
from pydantic import BaseModel
from typing import Generic, TypeVar

import base64

# Create a TypeVar that is bound to BaseModel
T_GEN = TypeVar('T_GEN', bound=BaseModel)

class Servo_Stop_Cmd(BaseModel):
    T: int
    S: int

class Servo_Pos_Cmd(BaseModel):
    T:int
    id:int
    pos:int
    pos2:int
    spd:int
    acc:int

class GCS_CMD(IntEnum):
    STATUS = 5

    JOYSTICK_VAL = 10

    SERVO_STOP = 20
    SERVO_POS = 21

    MOTOR_STOP = 30
    MOTOR_POS = 31

    CAMERA_STREAM_ALL = 40
    CAMERA_STREAM_CAM1 = 41
    CAMERA_STREAM_CAM2 = 42
    CAMERA_STREAM_CAM3 = 43
    CAMERA_STREAM_CAM4 = 44

    CAMERA_OSD = 45
    CAMERA_RECORDING = 46
    CAMERA_IMAGE_CAPTURE = 47

    CAMERA_ZOOM = 49

    VOICE_DATA = 60

class GCS_Packet(BaseModel, Generic[T_GEN]): 
    cmd:int
    data:T_GEN

class Status_MSG(BaseModel):
    battery:float
    voltage:float

class GCS_Status_Msg(BaseModel):
    cmd:int
    data:Status_MSG

class GCS_OSD_Data(BaseModel):
    enable:bool

class GCS_Camera_Stream_Data(BaseModel):
    id: int

class GCS_VOICE_DATA(BaseModel):
    enable:bool
    # id: int
    # audio_data: str  # Store Base64 encoded string
    # sample_rate: int
    # channels: int
    

    # @classmethod
    # def from_bytes(cls, audio_bytes: bytes, sample_rate: int, channels: int, id: int = 1):
    #     print("From_Bytes")
    #     """Encodes audio bytes to Base64 and creates a GCS_VOICE_DATA instance."""
    #     encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
    #     return cls(id=id,audio_data=encoded_audio, sample_rate=sample_rate, channels=channels)

    # def to_bytes(self) -> bytes:
    #     """Decodes Base64 back to raw audio bytes."""
    #     return base64.b64decode(self.audio_data)


servo_stop_cmd = Servo_Stop_Cmd(T=1, S=1).model_dump()
servo_pos_cmd = Servo_Pos_Cmd(T=1, id=1, pos=0, pos2=0, spd=1000, acc=100)
