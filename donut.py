import math
import time
import os

# Screen size
width = 80
height = 24

# Donut parameters
R1 = 1  # Inner radius
R2 = 2  # Outer radius
K2 = 5  # Distance from viewer to donut
K1 = width * K2 * 3 / (8 * (R1 + R2))  # Scaling factor based on screen size

# Characters used for luminance
chars = '.,-~:;=!*#$@'

A = 0  # Rotation angle around X-axis
B = 0  # Rotation angle around Z-axis

while True:
    output = [' '] * (width * height)  # Screen buffer
    zbuffer = [0] * (width * height)   # Z-buffer for depth calculations

    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    for theta in [i * 0.07 for i in range(int(2 * math.pi / 0.07))]:
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        for phi in [i * 0.02 for i in range(int(2 * math.pi / 0.02))]:
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            # Calculate coordinates of the point on the torus surface
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D (x, y, z) coordinates after rotation
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA

            ooz = 1 / z  # One over z (for depth calculation)

            # Projected 2D coordinates on the screen
            xp = int(width / 2 + K1 * ooz * x)
            yp = int(height / 2 - K1 * ooz * y)  # Note the minus sign for correct orientation

            # Calculate luminance (brightness)
            L = cosphi * costheta * sinB - cosA * costheta * sinphi \
                - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

            # Choose luminance character if L > 0
            if L > 0:
                luminance_index = int(L * 8)
                if luminance_index >= len(chars):
                    luminance_index = len(chars) - 1
                if 0 <= xp < width and 0 <= yp < height:
                    idx = xp + yp * width
                    if ooz > zbuffer[idx]:
                        zbuffer[idx] = ooz
                        output[idx] = chars[luminance_index]

    # Clear the screen and display the frame
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(height):
        print(''.join(output[i * width:(i + 1) * width]))

    # Update rotation angles
    A += 0.04
    B += 0.02
    time.sleep(0.03)
