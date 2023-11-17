Here are three folders, to test any of the code just flash the content of a folder to the pico running CircuitPython

RTOS - This is the RTOS implementation

Regular - This is without RTOS with a long delay between button presses being registered

Regular_B_Check - This is also without RTOS, but i try to meet the same responsiveness of the button, but this results in pystack errors if the button is pressed too much. I try doing this by constantly checking for the button at the same speed as RTOS is checking.