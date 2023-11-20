import math
import threading
import tkinter as tk
from tkinter import messagebox

key = ''


def ensize():

    with open('candidate/choice.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 去除空行
    lines = [line.strip() for line in lines if line.strip()]

    with open('candidate/choice.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))
    with open('candidate/choice.txt', 'r') as file:
        lines = file.readlines()
    if len(lines) < 2:
        size = 0
    else:
        size = int(math.log(len(lines), 2))
    return size


def bianma():
    n = ensize()
    if n != 0:
        binary_numbers = [bin(i)[2:].zfill(n) for i in range(2**n)]
        return binary_numbers


def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
        mid = (high + low) // 2
 
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
 
    return -1


def extract():
    n = ensize()
    if not n:
        return 0
    else:
        global key
        value = key
        while len(value) < n:
            value += '0'
        target = value[:n]
        binary_numbers = bianma()
        result = binary_search(binary_numbers, target)
        key = value[n:]
        if not key:
            def show_message():
                root = tk.Tk()
                root.withdraw()  # hide the main window
                messagebox.showinfo("Notification", "Key has been completely used.")
                root.destroy()  # destroy the main window

            threading.Thread(target=show_message).start()
        return result
