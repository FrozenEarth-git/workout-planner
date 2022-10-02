from tkinter import *
import random



def initializeWindowLayout():
    window = Tk()
    window.geometry("600x400")
    window.title("Complete Workouts")
    
    global history_labelFrame
    global flavor_labelFrame
    global scrollBar
    global canvas
    global secondFrame
    
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=0)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=0)
    
    history_labelFrame = LabelFrame(window, text="Mark Workouts as Completed")
    history_labelFrame.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")

    canvas = Canvas(history_labelFrame)
    canvas.pack(side = LEFT, fill = BOTH, expand = True)
    
    scrollBar = Scrollbar(history_labelFrame, orient=VERTICAL, command=canvas.yview)
    scrollBar.pack(side = RIGHT, fill = Y)
    
    canvas.configure(yscrollcommand = scrollBar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
    
    secondFrame = Frame(canvas)
    canvas.create_window((0,0), window=secondFrame, anchor="nw")


def populateWorkouts():
    # read file
    f = open("workouts.txt", "r")
    lines = f.readlines()
    
    global workouts
    workouts = []
    workout = []
    for line in lines:
        if line.find("!") >= 0:
            workout.append(line[1:-1])
        elif line == "\n":
            workouts.append(workout)
            workout = []
        else:
            exercise = line.split(",")
            exercise[1] = int(exercise[1])
            exercise[2] = int(exercise[2][0:-1])
            workout.append(exercise)
            
    f.close()
    
    # display workouts
    i = 0
    global buttons
    buttons = []
    for workout in workouts:
        if not workout:
            break
        workoutText = ""
        for exercise in workout:
            if isinstance(exercise, str):
                workoutText += exercise + "\n"
            else:
                workoutText += f"{exercise[0]} (Reps: {exercise[1]}, Sets: {exercise[2]})\n"
        # print(workoutText)
        workoutLabel = Label(secondFrame, text=workoutText)
        workoutLabel.grid(row=i, column=0, padx=5)
        
        completeButton = Button(secondFrame, text="Complete Workout", command=lambda t=str(i): completeWorkout(t))
        completeButton.grid(row=i, column=1, padx=5)
        buttons.append(completeButton)
        i += 1
                
def completeWorkout(index):
    workout = workouts[int(index)]
    print(workout)
    file = open("workout_history.txt", "a")
    
    duration = simpledialog.askinteger("Duration", "How long did you work out? (in minutes)")
    date = simpledialog.askstring("Date", "What day did you work out?")
    
    completedWorkout = ""
    
    # add workout name w/ exercises
    for exercise in workout:
        if isinstance(exercise, str):
            completedWorkout += f"!{workout[0]}\n"
        else:
            completedWorkout += f"{exercise[0]},{exercise[1]},{exercise[2]}\n"
    
    # add workout duration
    completedWorkout += f"#{duration}\n"
    # add workout date
    completedWorkout += f"@{date}\n"
    
    completedWorkout += "\n"
    
    file.write(completedWorkout)
    file.close()

def openCompletionWindow():
    initializeWindowLayout()
    populateWorkouts()
    window.mainloop()