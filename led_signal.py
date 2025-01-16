import machine
timer = None
# Initialize GPIO2 pin as output (Onboard LED for ESP12-F)
led = machine.Pin(2, machine.Pin.OUT)
def blink_led(timer):
    led.value(not led.value())  # Toggle LED state

def start_blinking(speed=500):
    global timer  # Declare timer as global to modify it
    # Create and start the timer (Timer 0)
    if timer is None:  # Only create the timer if it's not already created
        timer = machine.Timer(0)
        timer.init(period=speed, mode=machine.Timer.PERIODIC, callback=blink_led)
        print("LED blinking started.")
def stop_blinking():
    global timer  # Access the global timer
    if timer is not None:
        timer.deinit()  # Stop the timer
        timer = None  # Reset the global timer to None
        print("LED blinking stopped.")
