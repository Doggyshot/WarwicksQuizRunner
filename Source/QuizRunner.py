import tkinter
from tkinter import messagebox
import json
import threading
import sys
import os
import time
import math
import QuizScript

def getMainPath(relativePath):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)+"\\"+relativePath
    else:
        return os.path.dirname(__file__)+"\\"+relativePath

BASE_DIR = getMainPath("")
BIN_FOLDER = BASE_DIR+"bin"
QUIZ_COOLDOWN = 72060 # Quizzes on the website take 20 hours to be completable again.

MainGUI = tkinter.Tk()
creditsEarnedInSession = tkinter.IntVar()
creditsEarnedInSession.set(0)

with open(getMainPath("Configs.json"), "r") as f:
    data = json.load(f)

currentQuizCooldown = data['GlobalConfigs']['NextCompletionTime']

def saveSettings():
    data['GlobalConfigs']['Username'] = usernameField.get()
    data['GlobalConfigs']['Password'] = passwordField.get()
    data['GlobalConfigs']['HidePassword'] = hidePassword.get()
    data['GlobalConfigs']['DisablePopup'] = disablePopup.get()
    data['GlobalConfigs']['EarnedCredits'] += creditsEarnedInSession.get()
    data['GlobalConfigs']['NextCompletionTime'] = currentQuizCooldown

    with open(getMainPath("Configs.json"), "w") as f:
        json.dump(data, f)

def startAutoFarm():
    saveSettings()
    if (not disablePopup.get()):
        confirmMessageBox = messagebox
        confirmMessageBox.showinfo("Success", "Quiz farmer started (click to proceed)")
     
    MainGUI.withdraw()
    openRunningMenu()

def bindToClose():
    saveSettings()
    MainGUI.destroy()

def bindToCloseRunning():
    if (not disablePopup.get()):
        confirmMessageBox = messagebox
        response = confirmMessageBox.askquestion("Exit Application", "Are you sure you want to end the quiz farmer early?")
        if response == "yes":
            saveSettings()
            MainGUI.destroy()
    else:
        saveSettings()
        MainGUI.destroy()

def openSettingsMenu():
    SettingsGUI = tkinter.Toplevel(MainGUI)
    SettingsGUI.geometry("250x100+"+str(MainGUI.winfo_x()+300)+"+"+str(MainGUI.winfo_y()+50))
    SettingsGUI.title("Settings")
    SettingsGUI.configure(bg="#C2B280")
    SettingsGUI.resizable(False, False)
    SettingsGUI.grab_set()

    hidePasswordButton = tkinter.Checkbutton(SettingsGUI, text = "Hide password", onvalue = tkinter.TRUE, offvalue = tkinter.FALSE, variable = hidePassword, bg="#C2B280", fg="#553F2E", font=('Comic Sans MS', 12), activebackground="#C2B280", activeforeground="#553F2E", command=togglePasswordHide)
    hidePasswordButton.pack(anchor="nw")

    disablePopupButton = tkinter.Checkbutton(SettingsGUI, text = "Disable confirmation popups", onvalue = tkinter.TRUE, offvalue = tkinter.FALSE, variable = disablePopup, bg="#C2B280", fg="#553F2E", font=('Comic Sans MS', 12), activebackground="#C2B280", activeforeground="#553F2E")
    disablePopupButton.pack(anchor="nw")

dotcount = 3 
statusText = tkinter.StringVar() # for quizscript.py to be able to interact with
statusText.set("Starting quiz runner...")

def openRunningMenu():
    RunningGUI = tkinter.Toplevel(MainGUI)
    RunningGUI.geometry("440x120+"+str(MainGUI.winfo_x())+"+"+str(MainGUI.winfo_y()))
    RunningGUI.title("Running Quizzes (Credits earned: 0)")
    RunningGUI.configure(bg="#C2B280")
    RunningGUI.resizable(False, False)
    RunningGUI.grab_set()
    RunningGUI.protocol("WM_DELETE_WINDOW", bindToCloseRunning)

    runningText = tkinter.StringVar()
    runningText.set("Running Quizzes...")

    creditsFarmed = tkinter.Label(RunningGUI, fg="#553F2E", bg="#C2B280", font=('Comic Sans MS', 16), textvariable=runningText)
    creditsFarmed.pack(pady=1)

    def closeSuccessfulRun(a, b, c):
        if statusText.get() == "Quizzes completed! (Closing menu in 0)":
            saveSettings()
            MainGUI.destroy()

    def repeatDots():
        global dotcount
        match dotcount:
            case 1:
                runningText.set("Running Quizzes.")
                dotcount = 2
            case 2:
                runningText.set("Running Quizzes..")
                dotcount = 3
            case 3:
                runningText.set("Running Quizzes...")
                dotcount = 1
        RunningGUI.after(500, repeatDots)

    RunningGUI.after(0, repeatDots)

    statusText.trace("w", closeSuccessfulRun)

    def updateTitleCreditCount(a, b, c):
        RunningGUI.title("Running Quizzes (Credits earned: "+str(creditsEarnedInSession.get())+")")

    def updateNextQuizRunTime(a, b, c):
        global currentQuizCooldown
        currentQuizCooldown = math.floor(time.time())+QUIZ_COOLDOWN

    creditsEarnedInSession.trace("w", updateTitleCreditCount)
    creditsEarnedInSession.trace("w", updateNextQuizRunTime)
    
    with open(BIN_FOLDER+r"\answers.json", "r") as f:
        answerKey = json.load(f)

    def startQuizFarmer():
        thread = threading.Thread(target=QuizScript.runQuizzes, args=(usernameField.get(), passwordField.get(), answerKey, statusText, creditsEarnedInSession), daemon=True)
        thread.start()

    statusLabel = tkinter.Label(RunningGUI, fg="#272524", bg="#C2B280", font=('Comic Sans MS', 13), textvariable=statusText)
    statusLabel.pack(pady=1)

    leaveInBGText = tkinter.Label(RunningGUI, fg="#272524", bg="#C2B280", font=('Comic Sans MS', 12), text="(You may leave this in the background.)")
    leaveInBGText.pack(pady=12)

    RunningGUI.after(200, startQuizFarmer)


def togglePasswordHide():
    if hidePassword.get():
        passwordField.configure(show="*")
    else:
        passwordField.configure(show="")

MainGUI.geometry("470x220")
MainGUI.title("Warwick's Quiz Runner")
MainGUI.configure(bg="#C2B280")
MainGUI.resizable(False, False)
MainGUI.iconbitmap(True, BIN_FOLDER+r"\Warwick32x32.ico")


programHeader = tkinter.Label(MainGUI, text="Warwick's Quiz Runner", fg="#553F2E", bg="#C2B280", font=('Comic Sans MS', 18))
programHeader.pack()

userString = tkinter.StringVar()
usernameField = tkinter.Entry(MainGUI, fg="#553F2E", font=('Comic Sans MS', 18), textvariable=userString)
usernameField.insert(tkinter.END, data['GlobalConfigs']['Username'])
usernameField.pack(pady=3)

passwordString = tkinter.StringVar()
passwordField = tkinter.Entry(MainGUI, fg="#553F2E", font=('Comic Sans MS', 18), textvariable=passwordString)
passwordField.insert(tkinter.END, data['GlobalConfigs']['Password'])
passwordField.pack()

nextTimeToQuiz = tkinter.StringVar()
def updateTimeToNextQuiz():
    currentTime = time.time()
    timeDifference = math.floor(currentTime - currentQuizCooldown)

    if (timeDifference >= 0): # Are the next quizzes ready
        nextTimeToQuiz.set("Quizzes are ready!")
    else:
        timeDifference = abs(timeDifference)
        hours = math.floor(timeDifference / 3600)
        minutes = math.floor((timeDifference % 3600) / 60)
        seconds = math.floor(timeDifference - (hours * 3600 + minutes * 60))

        timeText = "Quizzes ready in: "
        timeTextParts = []
        if hours > 0:
            timeTextParts.append(f"{hours} hour"+("s" if hours != 1 else ""))
        if minutes > 0:
            timeTextParts.append(f"{minutes} minute"+("s" if minutes != 1 else ""))
        if seconds > 0:
            timeTextParts.append(f"{seconds} second"+("s" if seconds != 1 else ""))

        timeText = timeText+", ".join(timeTextParts)+"."
        nextTimeToQuiz.set(timeText)
        nextTimeToCompletionText.after(1000, updateTimeToNextQuiz)


nextTimeToCompletionText = tkinter.Label(MainGUI, fg="#553F2E", bg="#C2B280", font=('Comic Sans MS', 12), textvariable=nextTimeToQuiz)
nextTimeToCompletionText.pack()
nextTimeToCompletionText.after(0, updateTimeToNextQuiz)

creditsEarned = data['GlobalConfigs']['EarnedCredits']
creditsText = tkinter.StringVar()
creditsText.set("Total credits farmed: "+str(creditsEarned))

creditsFarmed = tkinter.Label(MainGUI, fg="#553F2E", bg="#C2B280", font=('Comic Sans MS', 10), textvariable=creditsText)
creditsFarmed.pack()

buttonContainer = tkinter.Frame(MainGUI, bg="#C2B280")
buttonContainer.pack()

startButton = tkinter.Button(buttonContainer, text="Start Farm", fg="#FFFFFF", bg="#A67B5B", font=('Comic Sans MS', 8), command=startAutoFarm) 
startButton.pack(side="left", padx="5")   

SettingsButton = tkinter.Button(buttonContainer, text="Settings", fg="#FFFFFF", bg="#A67B5B", font=('Comic Sans MS', 8), command=openSettingsMenu) 
SettingsButton.pack(side="right", padx="5") 

creatorCredits = tkinter.Label(MainGUI, text="Made by Doggyshot, contact me on Discord or Twitter for any issues.", fg="#553F2E", bg="#C2B280", font=('Comic Sans MS', 10))
creatorCredits.pack()

hidePassword = tkinter.BooleanVar(value = data['GlobalConfigs']['HidePassword'])
disablePopup = tkinter.BooleanVar(value = data['GlobalConfigs']['DisablePopup'])
togglePasswordHide()

MainGUI.protocol("WM_DELETE_WINDOW", bindToClose)
MainGUI.mainloop()