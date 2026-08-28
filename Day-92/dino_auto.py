import time
import pyautogui
# screen = pyautogui.position()
# print(screen)
# print(pyautogui.size())

time.sleep(5)
while True:
    img = pyautogui.screenshot(region=(300, 750, 600, 150))
    img.save("dino.png")

    # dark_pixels = 0
    dark_x = []

    for x in range(img.width):
        for y in range(0, 60):
            r, g, b = img.getpixel((x, y))

            if r < 100 and g < 100 and b < 100:
                # dark_pixels += 1
                dark_x.append(x)
    jumped = False
    if dark_x and min(dark_x) < 150 and not jumped:
        pyautogui.press("space")
        jumped = True
    jumped = False
        