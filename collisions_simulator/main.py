import pygame
import tkinter as tk
from time import sleep
from sys import exit
from funcs import get_v1, get_v2

#-----Tkinter begin-----
root = tk.Tk()
root.geometry("300x400")
root.configure(bg="grey12")

massL = tk.IntVar()
massR = tk.IntVar()

speedL = tk.IntVar()
speedR = tk.IntVar()

def close_window():
    root.destroy()
    print("Tkinter window closed\nSimulation starting in:\n")
    for i in range(3, 0, -1):
        sleep(1)
        print(i)

massL_slider = tk.Scale(root, from_=60, to=1, orient="vertical", variable=massL, troughcolor="red")
massL_slider.place(x=10,y=10)

massR_slider = tk.Scale(root, from_=60, to=1, orient="vertical", variable=massR, troughcolor="blue")
massR_slider.place(x=210,y=10)

speedL_slider = tk.Scale(root, from_=10, to=1, orient="vertical", variable=speedL, troughcolor="darkred")
speedL_slider.place(x=50,y=10)

speedR_slider = tk.Scale(root, from_=10, to=1, orient="vertical", variable=speedR, troughcolor="darkblue")
speedR_slider.place(x=250,y=10)

title = tk.Label(root, text="    mass   speed                                             mass    speed", bg="grey12", fg="white", font=("Arial", 8))
title.place(x=0, y=125)

button = tk.Button(root, text="FINISH", command=close_window, width = 12, height=3, bg="black", fg="grey")
button.place(x=105, y=320)

root.mainloop()

#-----Tkinter ends, pygame begin-----
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulation1")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)

massL = massL.get()
massR = massR.get()
speedL = speedL.get()
speedR = speedR.get()*-1

sizeL = massL*2
sizeR = massR*2

lX = 0
lY = 300

rX = 800-sizeR
rY = 300

squareL = pygame.Rect(lX, lY, sizeL, sizeL)
squareR = pygame.Rect(rX, rY, sizeR, sizeR)

squareL.bottomleft=(lX, lY)
squareR.bottomleft=(rX, rY)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill("grey13")

    squareL.x += speedL
    squareR.x += speedR

    if squareL.left <= 0:
        speedL *= -1
        squareL.left = 1
    if squareR.right >= 800:
        speedR *= -1
        squareR.right = 799

    if squareL.right >= squareR.left:
        old_speedL, old_speedR = speedL, speedR
        speedR = (get_v2(m1=massL, m2=massR, u1=old_speedL, u2=old_speedR))
        speedL = (get_v1(m1=massL, m2=massR, u1=old_speedL, u2=old_speedR))

        overlap = squareL.right - squareR.left
        squareL.x -= overlap // 2
        squareR.x += overlap // 2


    pygame.draw.line(screen, (255,255,255), (0,300), (800,300), 2)

    speedL_surface = font.render(f"{round(speedL, 3)}m/s", True, (128, 0 , 255))
    speedR_surface = font.render(f"{round(speedR, 3)}m/s", True, (128, 0 , 255))

    screen.blit(speedL_surface, (20, 20))
    screen.blit(speedR_surface, (700, 20))

    pygame.draw.rect(screen, (255, 0, 0), squareL)  # Draw AFTER
    pygame.draw.rect(screen, (0, 0, 255), squareR)
    
    pygame.display.update()
    clock.tick(60)