import os
import select
import sys
import rclpy

from std_msgs.msg import Int32MultiArray
from rclpy.qos import QoSProfile

if os.name == 'nt':
    import msvcrt
else:
    import termios
    import tty

MAX_SERVO_1_POS = 100
MIN_SERVO_1_POS = 0
MAX_SERVO_2_POS = 100
MIN_SERVO_2_POS = 0

SERVO_STEP_SIZE = 1

msg = """
Control Your Manipulator!
---------------------------
Moving around:
        ↑
   ←    ↓    →

↑/↓ : control servo 1 position
←/→ : control servo 2 position

space key : reset positions

CTRL-C to quit
"""

e = """
Communications Failed
"""



def get_key(settings):
    if os.name == 'nt':
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            return key
        else:
            return ''
    else:
        tty.setcbreak(sys.stdin.fileno())
        key = ord(sys.stdin.read(1))
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))

        # Handle arrow keys
        if key == 27:
            second_key = ord(sys.stdin.read(1))
            if second_key == 91:
                third_key = ord(sys.stdin.read(1))
                if third_key == 65:
                    return '↑'  # Up arrow
                elif third_key == 66:
                    return '↓'  # Down arrow
                elif third_key == 67:
                    return '→'  # Right arrow
                elif third_key == 68:
                    return '←'  # Left arrow

        return chr(key)

def print_positions(servo_1_position, servo_2_position):
    pass


def constrain(input_val, low_bound, high_bound):
    if input_val < low_bound:
        input_val = low_bound
    elif input_val > high_bound:
        input_val = high_bound
    else:
        input_val = input_val

    return input_val


def main():
    settings = None
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rclpy.init()

    qos = QoSProfile(depth=10)
    node = rclpy.create_node('teleop_keyboard')
    pub = node.create_publisher(Int32MultiArray, 'servo_positions', qos)

    status = 0
    servo_1_position = 50
    servo_2_position = 50

    try:
        print(msg)
        while(1):
            key = get_key(settings)
            if key == '↓':
                servo_1_position = constrain(
                    servo_1_position + SERVO_STEP_SIZE,
                    MIN_SERVO_1_POS,
                    MAX_SERVO_1_POS
                )
                status = status + 1
                print_positions(servo_1_position, servo_2_position)
            elif key == '↑':
                servo_1_position = constrain(
                    servo_1_position - SERVO_STEP_SIZE,
                    MIN_SERVO_1_POS,
                    MAX_SERVO_1_POS
                )
                status = status + 1
                print_positions(servo_1_position, servo_2_position)
            elif key == '→':
                servo_2_position = constrain(
                    servo_2_position - SERVO_STEP_SIZE,
                    MIN_SERVO_2_POS,
                    MAX_SERVO_2_POS
                )
                status = status + 1
                print_positions(servo_1_position, servo_2_position)
            elif key == '←':
                servo_2_position = constrain(
                    servo_2_position + SERVO_STEP_SIZE,
                    MIN_SERVO_2_POS,
                    MAX_SERVO_2_POS
                )
                status = status + 1
                print_positions(servo_1_position, servo_2_position)
            elif key == ' ':
                servo_1_position = 50
                servo_2_position = 50
                print_positions(servo_1_position, servo_2_position)
            else:
                if (key == '\x03'):
                    break

            # if status == 20:
            #     print(msg)
            #     status = 0

            positions = Int32MultiArray()
            positions.data = [servo_1_position, servo_2_position]
            pub.publish(positions)

    except Exception as e:
        print(e)

    finally:
        positions = Int32MultiArray()
        positions.data = [50, 50]
        pub.publish(positions)

        if os.name != 'nt':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    main()
