import pygame
import time
import sys
import threading
from pydantic import BaseModel, Field

from core.config import settings

class JoyStickCMD(BaseModel):
    pitch:float         = Field(default=0, serialization_alias="p")
    roll:float          = Field(default=0, serialization_alias="r")
    yaw:float           = Field(default=0, serialization_alias="y")
    servo:float         = Field(default=0, serialization_alias="s")
    servo_lock:bool     = Field(default=False, serialization_alias="s_l")
    # buttons:list[bool]  = Field(default=[0]*13, serialization_alias="b")

class UXVJoystickController(threading.Thread):
    def __init__(self,sendCallBack):

        super().__init__(daemon=True)
        self.is_active = True
        # Stop event for gracefully stopping the thread.
        self._stop_event = threading.Event()
        self.send_callback = sendCallBack 
        self._init()

    def _init(self):

        # Initialize pygame and joystick.

        pygame.init()
        pygame.joystick.init()

        if settings.JOYSTICK_ENABLE:
            joystick_count = pygame.joystick.get_count()
            if joystick_count == 0:
                print("No joystick connected.")
                pygame.quit()
                sys.exit()

            # Use the first joystick
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick '{self.joystick.get_name()}' initialized with "
                f"{self.joystick.get_numaxes()} axes and {self.joystick.get_numbuttons()} buttons.")
        


        # Initial values for comparison.
        self.joy0 = 0
        self.joy1 = 0
        self.joy2 = 0
        self.joy3 = 0
        self.joy4 = 0
        self.joy5 = 0

        self.cmd:JoyStickCMD = JoyStickCMD()

    def run(self):
        try:
            while not self._stop_event.is_set():
                # Process pygame events.
                pygame.event.pump()
                for event in pygame.event.get():
                    # Toggle servo fixation when button 9 is pressed.
                    if event.type == pygame.JOYBUTTONDOWN and event.button == settings.JOYSTICK_FIX_SERVO_BUTTON:
                        self.cmd.servo_lock = not self.cmd.servo_lock


                self.cmd.pitch = self.joystick.get_axis(settings.JOYSTICK_MOVE_FRONT)
                self.cmd.roll = self.joystick.get_axis(settings.JOYSTICK_MOVE_SIDEWAYS)
                self.cmd.yaw = self.joystick.get_axis(settings.JOYSTICK_YAW)

                self.send_callback(self.cmd.model_dump())  # If using Pydantic v2

                # self.cmd.servo = self.joystick.get_axis(settings.JOYSTICK_SERVO_MOVE)

                pygame.time.wait(100)

        except Exception as e:
            print("Exception in JoystickController:", e)
        finally:
            self.cleanup()

    def stop(self):
        """Signal the thread to stop."""
        self.is_active = False
        self._stop_event.set()

    def cleanup(self):
        """Clean up resources before shutting down the thread."""
        self.is_active = False
        pygame.joystick.quit()
        pygame.quit()
        print("JoystickController stopped and pygame cleaned up.")

# joystickController = UXVJoystickController()

# if settings.JOYSTICK_ENABLE:
#     joystickController.start()



# def main():
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         joystickController.stop()


# if __name__ == "__main__":
#     main()
