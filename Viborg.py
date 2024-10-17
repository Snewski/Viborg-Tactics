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

consent_text = "Dear participant, you are going to take part in a test aiming to asses your knowledge of football strategies and decision making. The test will take approximately [time duration]. Please reserve this time for the full test, as it must be completed once it has started. The responses will be anonymized, and the data will be solely used for research and training purposes. If you consent and would like to proceed to the test, press the space bar."

warmup_text1 = "You will be presented with 3 warm up scenes so that you get used to the task. After the warm up scenes, we will start the test. Press the space bar to continue."

warmup_text2 = "Before each scene starts a red dot will point where the ball is, while a red circle will indicate where the player that you need to watch will be. Press the space bar to continue."
#display a black image with red dot and red circle example along warmup_text2
warmup_text3 = "After each scene, 4 figures will show up on the screen describing the watched player movement through arrows (the arrow doesn't represents the player's final position, only the direction of his movement.)"
#display example options
warmup_text4 = "You must mark the best solution option for the play and ﻿﻿﻿answer as fast as possible. Your score will be based on your answer and response time. Press space to begin the warm up."
#intro_text = "Warm up is completed, press space if you are ready to begin the test"
#task_text = "What should the featured player do?"
#next_text = "Next scene"

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

## Presenting example with image ##

def present_text_and_image(text, image_path):  # Added an image_path parameter
    # Create a full-screen PsychoPy window
    win = visual.Window(fullscr=True)
    # Create the text stimulus
    instruction = visual.TextStim(win, text=text, color="black", height=0.08, pos=(0, 0.6))  # Position text higher
    # Create the image stimulus
    image_stim = visual.ImageStim(win, image=image_path, pos=(0, -0.3), size=(1, 1))  # Position image below text
    
    # Draw the text and image, and flip the window to display them
    instruction.draw()
    image_stim.draw()
    win.flip()
    
    # Wait for the spacebar to be pressed
    event.waitKeys(keyList=['space'])
    
    # Close the window
    win.close()


# Example usage
#example_text = "This is an example. Press the spacebar to continue."
#present_text(example_text)
# Alternatively you can also just write the string into the function as below
#present_text("This is an example. Press the spacebar to continue.")

## the consent and instruction section ##
present_text(consent_text)
present_text(warmup_text1)
present_text_and_image(warmup_text2, "Pictures/warmup_reddot.png")
present_text_and_image("Example", "Pictures/warmup_field.png")
present_text_and_image(warmup_text3, "Pictures/warmup_options.png")
present_text(warmup_text4)







## Save logfile ##
logfile_name = f"logfiles/logfile_{Number}.csv"
logfile.to_csv(logfile_name)
