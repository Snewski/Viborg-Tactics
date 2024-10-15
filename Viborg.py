### Viborg-Tactics ###


## To-Do ##

## Script-Related ##
# Write text chunks for the different parts (consent, instructions, etc.)
# Make windows for stimuli and tactical decisions
# Make sure data is collected in a desired format
# Randomize stimuli order, while keeping video and related red dot together
# Make 2-3 practice trials to familiarize participants
## Non-Script ##
# Find video stimuli and group with red dots
# Make pictures and text for tactical decisions


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
def present_text(text): # Function to present text: the only parameter is a (str) with the text to display
    # Create a full-screen PsychoPy window
    win = visual.Window(fullscr=True)
    # Create the text stimulus
    instruction = visual.TextStim(win, text=text, color="black", height=0.08) # The height parameter might need to be adjusted
    # Draw the text and flip the window to display it
    instruction.draw()
    win.flip()
    # Wait for the spacebar to be pressed
    event.waitKeys(keyList=['space'])
    # Close the window
    win.close()


# Example usage
example_text = "This is an example. Press the spacebar to continue."
present_text(example_text)
# Alternatively you can also just write the string into the function as below
#present_text("This is an example. Press the spacebar to continue.")










## Save logfile ##
logfile_name = f"logfiles/logfile_{Number}.csv"
logfile.to_csv(logfile_name)
