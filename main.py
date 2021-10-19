from os import terminal_size
from tkinter.constants import RIGHT
from selenium import webdriver
from threading import Thread
import tkinter as tk
from selenium.webdriver.common.keys import Keys
import time


stop = True

wordlist = open("./web2").read().splitlines()

arrayOfWords = []

driver = webdriver.Chrome("./chromedriver.exe")


def auto_start():
    global stop
    try:
        driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div[1]/div[1]/button").click()
    except:
        is_bot_on.config(fg="red",text="ERROR")
        time.sleep(2)
        is_bot_on.config(fg="red",text="OFF")
        return 
    time.sleep(1)
    stop = False


def bot_loop():
    global stop
    global arrayOfWords
    while not stop:
        try:
            if driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[1]/button").is_displayed():
                arrayOfWords = []
                auto_start()
                time.sleep(0.5)
        except:
            is_bot_on.config(fg="red",text="ERROR")
            time.sleep(2)
            is_bot_on.config(fg="red",text="OFF")

        if driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[2]/form/input").is_displayed() and not stop:
            print("___________________________________________________")
            syllable = driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div[2]/div[2]/div").text
            box = driver.find_element_by_xpath(
                "/html/body/div[2]/div[3]/div[2]/div[2]/form/input")

            for line in wordlist:
                if syllable in line and not line in arrayOfWords:
                    matchingWord = line
                    arrayOfWords.append(line)
                    break

            box.click()
            box.send_keys(matchingWord)
            box.send_keys(Keys.RETURN)
            time.sleep(0.01)


def stop_bot():
    global stop
    is_bot_on.config(fg="red",text="OFF")
    stop = True


def start_bot():
    global stop
    stop = False
    is_bot_on.config(fg="green",text="ON")
    bot_loop()


def start_bot_background():
    t = Thread(target=start_bot)
    t.start()

r = tk.Tk()
is_bot_on = tk.Label(r, text='OFF', bg='#2a2a2a', fg="red")

def join_room_with_name(room_code, name):
    if len(room_code) < 4 or len(name) < 2:
        is_bot_on.config(fg="red",text="INVALID ROOM OR NAME LENGTH < 2")
        time.sleep(2)
        is_bot_on.config(fg="red",text="OFF")
        return

    driver.get("https://www.jklm.fun/%s" % (room_code))
    print(room_code)
    print(name)

    try:
        answerBox = driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/form/div[2]/input")

        time.sleep(0.1)
        answerBox.clear()
        answerBox.send_keys(name)
        answerBox.send_keys(Keys.RETURN)

        time.sleep(1)
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

        time.sleep(0.01)
    except:
        pass

def join_room_with_name_background(room_code,name):
    t = Thread(target=join_room_with_name, args=(room_code,name))
    t.start()

if __name__ == "__main__":
    r.title('JKLM MENU')

    r.minsize(width=230, height=190)
    r.configure(bg='#2a2a2a')
    r.resizable(width=False, height=False)

    room_code_text = tk.Label(r, text='ROOM CODE (NO NEED FOR UPPERCASE)', bg='#2a2a2a', fg="white")
    room_code = tk.Entry(r, bg="#9c9c9c")
    name_text = tk.Label(r, text='NAME FOR GAME', bg='#2a2a2a', fg="white")
    name = tk.Entry(r, bg="#9c9c9c")

    join_game = tk.Button(r, text='Join',bg="#505050", fg="white",
                          command=lambda: join_room_with_name_background(room_code.get().upper(), name.get()))

    start_button = tk.Button(r, text='Start', width=25, bg="#505050", fg="white",
                             command=start_bot_background)
    stop_button = tk.Button(r, text='Stop', width=25, bg="#505050", fg="white",
                             command=stop_bot)

    space = tk.PanedWindow(r, bg='#2a2a2a',height=4)
    space1 = tk.PanedWindow(r, bg='#2a2a2a',height=1)
    space2 = tk.PanedWindow(r, bg='#2a2a2a',height=1)
    space3 = tk.PanedWindow(r, bg='#2a2a2a',height=3)

    space3.pack()
    start_button.pack()
    space.pack()
    stop_button.pack()
    room_code_text.pack()
    room_code.pack()
    name_text.pack()
    name.pack()
    space2.pack()
    is_bot_on.pack()
    space1.pack()
    join_game.pack()
    r.mainloop()
