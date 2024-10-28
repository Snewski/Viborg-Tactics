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


## Setting up dataframe ##
columns = ['Number', 'Position', 'Age', 'Foot', 'Experience', 'Tactic', 'Decision'] # Need columns for the tactical data
logfile = pd.DataFrame(columns = columns)


## GUI ##
# Creating dialogue box
DialogueBox = gui.Dlg(title = "Viborg Tactics")
DialogueBox.addText('Udfyld venligst de nedenstående felter:')
list_of_numbers = list(range(1, 17)) # Options for years of experience
# Adding information fields
DialogueBox.addField('Hvor på banen spiller du?:', choices = ['Fosvarsspiller', 'Midtbanespiller', 'Angriber'], color = "green")
DialogueBox.addField('Dit trøjenummer:', color = "black")
DialogueBox.addField('Hvilken fod er din dominante?:', choices = ['Højre', 'Venstre'],color = "green")
DialogueBox.addField('Din alder:', color = "black")
DialogueBox.addField('Hvor mange år har du spillet fodbold?:', choices = list_of_numbers, color = "green")
# Showing dialogue box
DialogueBox.show()


# Collecting participant information
if DialogueBox.OK:
    Position = DialogueBox.data[0]
    Number = DialogueBox.data[1]
    Foot = DialogueBox.data[2]
    Age = DialogueBox.data[3]
    Experience = DialogueBox.data[4]

    # Create a new entry as a dictionary
    new_entry = {
        'Number': Number,
        'Position': Position,
        'Age': Age,
        'Foot': Foot,
        'Experience': Experience,
        'Tactic': '',  # Placeholder for tactical data
        'Decision': ''  # Placeholder for decision data
    }

    # Append the new entry to the logfile dataframe
    logfile = logfile.append(new_entry, ignore_index=True)

    # Save the logfile as a CSV
    logfile.to_csv("logfiles/tactical_log.csv", index=False)
    
else:
    core.quit()


## All text chunks ##

consent_text = "Kære deltager, du skal til at tage en test, der har til formål at vurdere din viden om fodboldstrategier og beslutningstagning. Testen tager omkring [x minutter], så vær forberedt på at afsætte din tid til dette, da testen skal gennemføres, når først den er startet. Din besvarelse vil blive anonymiseret, og dataen vil udelukkende blive brugt til forsknings- og træningsformål. \n\n Hvis du giver samtykke og gerne vil fortsætte til testen, skal du trykke på mellemrumstasten."

warmup_text1 = "Du vil nu blive præsenteret for 3 opvarmningsøvelser, så du vænner dig til testens struktur. I testen får du vist en kort video som omhandler en specifik spilsituation, hvorefter du skal tage en taktisk beslutning. Efter opvarmningsøvelserne starter testen. \n\n Tryk på mellemrumstasten for at fortsætte."

warmup_text2 = "Før hver spilsituation bliver vist, vil en rød prik indikere hvor bolden er, mens en rød cirkel vil angive, hvor spilleren du skal holde øje med, vil være. \n\n Tryk på mellemrumstasten for at fortsætte."
#display a black image with red dot and red circle example along warmup_text2
warmup_text3 = "Efter hver spilsituation vil 4 figurer blive vist på skærmen, der beskriver mulige beslutninger som den markerede spiller kan træffe igennem pile (pilene repræsenterer ikke spillerens endelige position, kun retningen af ​​hans bevægelse)."
#display example options
warmup_text4 = "Du skal markere den bedste løsningsmulighed for situationen og svare så hurtigt som muligt. Din score vil blive baseret på dit svar og din svartid. \n\n Tryk på mellemrumstasten for at starte opvarmningen."
#intro_text = "Opvarmningen er nu færdig, tryk på mellemrumstasten når du er klar til at starte testen"
task_text = "Hvad burde den markerede spiller gøre?"
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
    # Wait a short moment before closing
    core.wait(2)
    # Close the window after the video ends
    win.close()



## Choosing option ##

def present_text_and_images(text, image_paths, logfile, index):
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
    decision = None  # Initialize decision variable
    
    while not clicked:
        if mouse.getPressed()[0]:  # Check if the left mouse button is pressed
            mouse_x, mouse_y = mouse.getPos()
            if image_stim_left.contains(mouse_x, mouse_y):
                chosen_image = selected_images[0]  # Left image clicked
                clicked = True
            elif image_stim_right.contains(mouse_x, mouse_y):
                chosen_image = selected_images[1]  # Right image clicked
                clicked = True
    
    # Map the chosen image to the decision
    if chosen_image == 'Pictures/option1.png':
        decision = "pass to teammate"
    elif chosen_image == 'Pictures/option2.png':
        decision = "move forward"
    
    # Store the decision in the logfile DataFrame
    logfile.at[index, 'Decision'] = decision
    
    # Start a 3-second countdown (optional)
    for i in range(3, 0, -1):
        countdown_text = visual.TextStim(win, text=str(i), color="black", height=0.1, pos=(0, 0))  # Center countdown
        countdown_text.draw()  # Draw the updated instruction
        win.flip()  # Show the countdown
        core.wait(1)  # Wait for 1 second for each number

    # Display "Next Scene" centered
    next_scene_text = visual.TextStim(win, text="Næste Situation", color="black", height=0.1, pos=(0, 0))  # Center "Next Scene"
    next_scene_text.draw()
    win.flip()
    core.wait(1)  # Wait for 1 second before closing the window

    # Close the window
    win.close()


image_paths = ['Pictures/option1.png', 'Pictures/option2.png']



## the consent and instruction section ##
present_text(consent_text)
present_text(warmup_text1)
present_text_and_image(warmup_text2, "Pictures/warmup_reddot.png")
present_text_and_image("For eksempel", "Pictures/warmup_field.png")
present_text_and_image(warmup_text3, "Pictures/warmup_options.png")
present_text(warmup_text4)

## the warm up section ##
present_video("Videos_Dots/warmup_vid_1.mp4")
present_text_and_images(task_text, image_paths, logfile, index=0)






## Save logfile ##
logfile_name = f"logfiles/logfile_{Number}.csv"
logfile.to_csv(logfile_name)
