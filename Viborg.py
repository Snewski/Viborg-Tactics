### Viborg-Tactics ###

## Importing modules ##
from psychopy import visual, event, core, gui, data, clock
import pandas as pd, random, os

## Logfile ##
# Making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

list_of_numbers = list(range(1, 17)) # Options for years of experience

## GUI ##
# Creating dialogue box
DialogueBox = gui.Dlg(title = "Viborg Tactics")
DialogueBox.addText('Udfyld venligst de nedenstående felter:')
# Adding information fields
DialogueBox.addField('Position:', choices = ['Fosvarsspiller', 'Midtbanespiller', 'Angriber'], color = "green")
DialogueBox.addField('Trøjenummer:', color = "black")
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

# Setting up dataframe
columns = ['Number', 'Position', 'Age', 'Foot', 'Experience'] # Need columns for the tactical data
logfile = pd.DataFrame(columns = columns)
















# Save logfile
logfile_name = f"logfiles/logfile_{Number}.csv"
logfile.to_csv(logfile_name)
