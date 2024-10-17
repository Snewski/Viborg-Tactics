### Viborg-Tactics ###


## To-Do ##

## Script-Related ##
# Translate (if needed) text chunks for the different parts (consent, instructions, etc.)
# Make windows for stimuli and tactical decisions
# Save the inputs in logfiles
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
task_text = "What should the featured player do?"
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

## Presenting video ##
def present_video(video_path):
    # Create a full-screen PsychoPy window
    win = visual.Window(fullscr=True)
    
    # Create the video stimulus
    video_stim = visual.MovieStim3(win, video_path, size=(1600, 900))  # Adjust the size as needed, (1920, 1080) is fullscreen
    
    # Play the video until it finishes
    while video_stim.status != visual.FINISHED:
        video_stim.draw()
        win.flip()
        
    # Close the window after the video ends
    win.close()



## Choosing option ##
from psychopy import visual, event, core
import random

def present_text_and_images(text, image_paths):
    # Create a full-screen PsychoPy window
    win = visual.Window(fullscr=True)
    
    # Create the text stimulus
    instruction = visual.TextStim(win, text=text, color="black", height=0.08, pos=(0, 0.6))
    
    # Randomly select two images from the list and shuffle their order
    selected_images = random.sample(image_paths, 2)
    random.shuffle(selected_images)
    
    # Create the image stimuli
    image_stim_left = visual.ImageStim(win, image=selected_images[0], pos=(-0.5, -0.3), size=(0.9, 0.9))
    image_stim_right = visual.ImageStim(win, image=selected_images[1], pos=(0.5, -0.3), size=(0.9, 0.9))
    
    # Draw the text and images, and flip the window to display them
    instruction.draw()
    image_stim_left.draw()
    image_stim_right.draw()
    win.flip()
    
    # Wait for mouse click on either image
    mouse = event.Mouse(win=win)
    clicked = False
    chosen_image = None

    while not clicked:
        if mouse.getPressed()[0]:  # Check if the left mouse button is pressed
            mouse_x, mouse_y = mouse.getPos()
            if image_stim_left.contains(mouse_x, mouse_y):
                chosen_image = selected_images[0]  # Left image clicked
                clicked = True
            elif image_stim_right.contains(mouse_x, mouse_y):
                chosen_image = selected_images[1]  # Right image clicked
                clicked = True
    
    #idk if we need it but added a countdown and "next scene" (just like in tactic up)
    # Start a 3-second countdown
    for i in range(3, 0, -1):
        countdown_text = visual.TextStim(win, text=str(i), color="black", height=0.1, pos=(0, 0))  # Center countdown
        countdown_text.draw()  # Draw the updated instruction
        win.flip()  # Show the countdown
        core.wait(1)  # Wait for 1 second for each number

    # Display "Next Scene" centered
    next_scene_text = visual.TextStim(win, text="Next Scene", color="black", height=0.1, pos=(0, 0))  # Center "Next Scene"
    next_scene_text.draw()
    win.flip()
    core.wait(1)  # Wait for 1 second before closing the window

    # Close the window
    win.close()


# Example usage
image_paths = ['Pictures/option1.png', 'Pictures/option2.png']
#present_text_and_images(task_text, image_paths)



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

## the warm up section ##
present_video("Videos_Dots/warmup_vid_1.mp4")
present_text_and_images(task_text, image_paths)






## Save logfile ##
logfile_name = f"logfiles/logfile_{Number}.csv"
logfile.to_csv(logfile_name)
