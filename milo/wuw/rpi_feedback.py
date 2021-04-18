from milo.wuw.__interface__ import WUWFeedbackInterface
import RPi.GPIO as GPIO


class RPIWUWFeedback(WUWFeedbackInterface):
    def __init__(self, gpio_led: int):
        self.gpio_led = gpio_led
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_led, GPIO.OUT)

    def start_listening_feedback(self):
        GPIO.output(self.gpio_led, GPIO.HIGH)

    def end_listening_feedback(self):
        GPIO.output(self.gpio_led, GPIO.LOW)

    def terminate(self):
        GPIO.cleanup()
