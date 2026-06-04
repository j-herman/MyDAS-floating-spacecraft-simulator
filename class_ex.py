import time
import math
from smbus2 import SMBus
import pigpio

# =========================
# ESC CONFIG
# =========================

ESC_PIN = 18

ARM_US = 1000
NEUTRAL_US = 1500
MAX_US = 2000

# =========================
# LSM9DS1 ADDRESSES
# =========================

AG_ADDR = 0x6B
MAG_ADDR = 0x1E

OUT_X_L_G = 0x18
OUT_Y_L_G = 0x1A
OUT_Z_L_G = 0x1C

OUT_X_L_M = 0x28

# Sensitivities (same as your system)
GYRO_SCALE = 0.07
MAG_SCALE = 0.58

# =========================
# BUS + ESC INIT
# =========================

bus = SMBus(1)

pi = pigpio.pi()

if not pi.connected:
    raise RuntimeError("pigpio daemon not running")

# =========================
# HELPERS
# =========================

def set_esc(us):
    pi.set_servo_pulsewidth(ESC_PIN, us)


def read_word(addr, reg):

    low = bus.read_byte_data(addr, reg)
    high = bus.read_byte_data(addr, reg + 1)

    value = (high << 8) | low

    if value >= 32768:
        value -= 65536

    return value


def read_gyro():

    x = read_word(AG_ADDR, OUT_X_L_G)
    y = read_word(AG_ADDR, OUT_Y_L_G)
    z = read_word(AG_ADDR, OUT_Z_L_G)

    return (
        x * GYRO_SCALE,
        y * GYRO_SCALE,
        z * GYRO_SCALE
    )


def read_mag():

    x = read_word(MAG_ADDR, OUT_X_L_M)
    y = read_word(MAG_ADDR, OUT_X_L_M + 2)
    z = read_word(MAG_ADDR, OUT_X_L_M + 4)

    return (x, y, z)

# =========================
# MAIN
# =========================

try:

    print("System starting...")

    # SAFE START
    set_esc(ARM_US)
    time.sleep(3)

    set_esc(1700)
    time.sleep(2)

    print("Running control loop\n")

    while True:

        # ==========================================
        # SENSOR READS (DIRECT I2C)
        # ==========================================

        gx, gy, gz = read_gyro()

        gz = gz-1.37459

        mx, my, mz = read_mag()

        # ==========================================
        # STUDENT CONTROL BLOCK
        # ==========================================

        # DEFAULT SAFE OUTPUT (REMOVE WHEN CONTROLLING)
        set_esc(NEUTRAL_US)

        # ==========================================
        # DEBUG PRINT
        # ==========================================

        print(
            f"gz = {gz:8.2f} dps   "
            f"mag = {my:10.2f}   "
        )

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nStopping...")

finally:

    print("Shutting down ESC")

    set_esc(ARM_US)
    time.sleep(1)

    pi.set_servo_pulsewidth(ESC_PIN, 0)

    bus.close()
    pi.stop()

    print("Cleanup complete")
