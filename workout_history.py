from tkinter import *
import random

def initializeWindowLayout():

    global history_labelFrame
    global flavor_labelFrame
    global scrollBar
    global canvas
    global secondFrame
    
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=0)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=0)
    
    history_labelFrame = LabelFrame(window, text="Workout History")
    history_labelFrame.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")
    
    flavor_labelFrame = LabelFrame(window, text="Message of the Refresh")
    flavor_labelFrame.grid(row=1, column=0, padx=8, pady=(0, 5), sticky="nsew")
    
    
    Label(flavor_labelFrame, text= getRandomFlavor() ).pack(anchor="w", padx=10)
    
    reverseSortButton = Button(history_labelFrame, text="Sort Oldest/Newest", command=reverseSort)
    reverseSortButton.pack()
    
    deleteHistoryButton = Button(history_labelFrame, text="Clear History", command=clearHistory)
    deleteHistoryButton.pack()
    
    canvas = Canvas(history_labelFrame)
    canvas.pack(side = LEFT, fill = BOTH, expand = True)
    
    scrollBar = Scrollbar(history_labelFrame, orient=VERTICAL, command=canvas.yview)
    scrollBar.pack(side = RIGHT, fill = Y)
    
    canvas.configure(yscrollcommand = scrollBar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
    
    secondFrame = Frame(canvas)
    canvas.create_window((0,0), window=secondFrame, anchor="nw")

def readHistoryFile():
    # read workout_history.txt
    file = open("workout_history.txt", "r")
    lines = file.readlines()
    
    global workout_history
    workout_history = []
    workout = {"exercises": [], "duration": 0, "date": 0}
    exercises = []
    for line in lines:
        if line.find("!") >= 0:
            exercises.append(line[1:-1])
        elif line == "\n":
            workout.update( {"exercises": exercises} )
            workout_history.append(workout)
            workout = {}
            exercises = []
        elif line.find("#") >= 0:
            workout["duration"] = int(line[1:-1])
        elif line.find("@") >= 0:
            workout["date"] = line[1:-1]
        else:
            exercise = line.split(",")
            exercise[1] = int(exercise[1])
            exercise[2] = int(exercise[2][0:-1])
            print(exercise)
            exercises.append(exercise)
    file.close()


def populateHistory():
        
    secondFrame.columnconfigure(3, weight=1)
    
    Label(secondFrame, text="Date").grid(row=0, column=0, sticky="EW")
    Label(secondFrame, text="Name").grid(row=0, column=1, sticky="EW")
    Label(secondFrame, text="Duration").grid(row=0, column=2, sticky="EW")
    Label(secondFrame, text="Exercises").grid(row=0, column=3, sticky="EW")
    
    i = 1
    for workout in workout_history:
        Label(secondFrame, text=workout["date"]).grid(row=i, column=0, padx=5, pady=5)
        Label(secondFrame, text=f"{workout['duration']} minutes").grid(row=i, column=2, padx=5, pady=5)
        
        exercises = ""
        for exercise in workout["exercises"]:
            if isinstance(exercise, str):
                Label(secondFrame, text=exercise).grid(row=i, column=1, padx=5, pady=5)
            else:
                exercises += f"{exercise[0]} (Reps: {exercise[1]}, Sets: {exercise[2]})\n"
        else:
            exercises = exercises[0:-1]
        exercisesLabel = Label(secondFrame, text=exercises)
        exercisesLabel.grid(row=i, column=3, padx=5)
        
        i += 1

def reverseSort():
    for widget in window.winfo_children():
        widget.destroy()
        
    initializeWindowLayout()
    workout_history.reverse()
    populateHistory()
    
def getRandomFlavor():
    flavorTexts = [
        "Keep up the good work!",
        "You exercised!",
        "Being healthy is good!",
        "IP: 124.105.6.187",
        "So cool!",
        ]
    
    # SPECIL [[Text Me!]] MESSAGES!!
    
    return random.choice(flavorTexts)

def clearHistory():
    file = open("workout_history.txt", "w")
    file.close()
    
    for widget in window.winfo_children():
        widget.destroy()
    
    readHistoryFile()
    initializeWindowLayout()
    populateHistory()
            
def openHistoryWindow():
    global window
    window = Tk()
    window.geometry("600x400")
    window.title("Workout History")
    
    initializeWindowLayout()
    readHistoryFile()
    populateHistory()
    window.mainloop()