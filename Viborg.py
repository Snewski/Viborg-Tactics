### Viborg-Tactics ###


## To-Do ##

# Write text chunks for the different parts (consent, instructions, etc.)
# Make windows to show stimuli
# Find video stimuli and group with red dots
# Make pictures for tactical decisions and make sure data is collected in the desired format
# Make 2-3 practice trials to familiarize participants


## Importing modules ##
from psychopy import visual, event, core, gui, data, clock
import pandas as pd, random, os


## Logfile ##
# Making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")


## GUI ##
# Creating dialogue box
DialogueBox = gui.Dlg(title = "Viborg Tactics")
DialogueBox.addText('Udfyld venligst de nedenstående felter:')
list_of_numbers = list(range(1, 17)) # Options for years of experience
# Adding information fields
DialogueBox.addField('Position:', choices = ['Fosvarsspiller', 'Midtbanespiller', 'Angriber'], color = "green")
DialogueBox.addField('Dit trøjenummer:', color = "black")
DialogueBox.addField('Hvilken fod er din dominante?:', choices = ['Højre', 'Venstre'],color = "green")
DialogueBox.addField('Alder:', color = "black")
DialogueBox.addField('Hvor mange år har du spillet fodboldt?:', choices = list_of_numbers, color = "green")
# Showing dialogue box
DialogueBox.show()


# Collecting participant information
if DialogueBox.OK:
    Position = DialogueBox.data[0]
    Number = DialogueBox.data[1]
    Foot = DialogueBox.data[2]
    Age = DialogueBox.data[3]
    Experience = DialogueBox.data[4]
else:
    core.quit()


## Setting up dataframe ##
columns = ['Number', 'Position', 'Age', 'Foot', 'Experience'] # Need columns for the tactical data
logfile = pd.DataFrame(columns = columns)


## All text chunks ##




## Presenting introduction/consent ##
win = visual.Window(fullscr = True)
instruction = visual.TextStim(win,text = ?, color="black", height=0.08) # needs consent form/introduction
instruction.draw()
win.flip()
event.waitKeys()
# Close the window
win.close()












## Save logfile ##
logfile_name = f"logfiles/logfile_{Number}.csv"
logfile.to_csv(logfile_name)
