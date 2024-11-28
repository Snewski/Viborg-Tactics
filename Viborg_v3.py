### Viborg-Tactics ###

from psychopy import prefs
prefs.general['videoBackend'] = 'opencv'

## To-Do ##

## Script-Related ##
# Optimize the loading of the videos and images
# Save the inputs in logfiles
# Make sure data is collected in a desired format
# Make 2-3 practice trials to familiarize participants
# Check if the text is good on all the instructions
# Add a function: if 'q' is pressed then escape experiment at any time


## Non-Script ##
# Find video stimuli
# Make pictures and text for tactical decisions
# delete some folders to make the right ratio
# delete the warm up scenarios from the pictures folder
# probably update the loop after that


## Importing modules ##
from psychopy import visual, event, core, gui, data, clock
import pandas as pd, random, os, glob


## Logfile ##
# Making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")


## Setting up dataframe ##
columns = ['Number', 'Position', 'Team', 'Age', 'Foot', 'Experience', 'Experience_VFF' , 'Video', 'Decision', 'RT'] # Need columns for the tactical data
logfile = pd.DataFrame(columns = columns)


## GUI ##
# Creating dialogue box
DialogueBox = gui.Dlg(title = "Viborg Tactics")
DialogueBox.addText('Udfyld venligst de nedenstående felter:')
list_of_numbers = list(range(0, 20)) # Options for years of experience
# Adding information fields
DialogueBox.addField('Hvor på banen spiller du?:', choices = ['Fosvarsspiller', 'Midtbanespiller', 'Angriber'], color = "green")
DialogueBox.addField('Hvad er dit trøjenummer:', color = "black")
DialogueBox.addField('Hvilket hold spiller du for?', choices = ['U13', 'U14', 'U15', 'U16', 'U17', 'U18', 'U19', 'Førsteholdet'], color = 'green')
DialogueBox.addField('Hvilken fod er din dominante?:', choices = ['Højre', 'Venstre'],color = "black")
DialogueBox.addField('Hvad er din alder:', color = "green")
DialogueBox.addField('Hvor mange år har du spillet fodbold?:', choices = list_of_numbers, color = "black")
DialogueBox.addField('Hvor mange år har du spillet fodbold hos VFF?:', choices = list_of_numbers, color = "green")



## All text chunks ##

consent_text = "Kære deltager, du skal til at tage en test, der har til formål at vurdere din viden om fodboldstrategier og beslutningstagning. Testen tager omkring [x minutter], så vær forberedt på at afsætte din tid til dette, da testen skal gennemføres, når først den er startet. Din besvarelse vil blive anonymiseret, og dataen vil udelukkende blive brugt til forsknings- og træningsformål. \n\n Hvis du giver samtykke og gerne vil fortsætte til testen, skal du trykke på mellemrumstasten."

warmup_text1 = "Du vil nu blive præsenteret for 3 opvarmningsøvelser, så du vænner dig til testens struktur. I testen får du vist en kort video som omhandler en specifik spilsituation, hvorefter du skal tage en taktisk beslutning. Konteksten for hver spilsituation i testen er neutral, hvilket vil sige at du skal forestille dig at stillingen er 0-0 efter omtrent 20 minutters spilletid. Efter opvarmningsøvelserne starter testen. \n\n Tryk på mellemrumstasten for at fortsætte."

#warmup_text2 = "Før hver spilsituation bliver vist, vil en rød prik indikere hvor bolden er, mens en rød cirkel vil angive, hvor spilleren du skal holde øje med, vil være. \n\n Tryk på mellemrumstasten for at fortsætte."
#display a black image with red dot and red circle example along warmup_text2
warmup_text3 = "Efter hver spilsituation vil 4 figurer blive vist på skærmen, der beskriver mulige beslutninger som den markerede spiller kan træffe igennem pile."
warmup_text4 = "Du skal markere den bedste løsningsmulighed for situationen. Din score vil blive baseret på dit svar. \n\n Tryk på mellemrumstasten for at starte opvarmningen."
intro_text = "Opvarmningen er nu færdig, tryk på mellemrumstasten når du er klar til at starte testen."
task_text = "Hvad burde den markerede spiller gøre?"
#next_text = "Next scene"

# Modified quitting function
def check_for_quit():
    keys = event.getKeys(keyList=['q'])
    if 'q' in keys:
        print("Exiting experiment")
        
        # Save the logfile before exiting
        logfile_name = f"logfiles/logfile_{Number}_{Team}.csv"
        logfile.to_csv(logfile_name)
        print(f"Logfile saved to {logfile_name}")
        
        win.close()
        core.quit()


## Presenting text function ##
def present_text(text): # Function to present text: the only parameter is a (str) with the text to display
    # Create a full-screen PsychoPy window
    #win = visual.Window(fullscr=True)
    # Create the text stimulus
    instruction = visual.TextStim(win, text=text, color="black", height=0.08) # The height parameter might need to be adjusted
    # Draw the text and flip the window to display it
    instruction.draw()
    win.flip()
    # Wait for the spacebar to be pressed
    event.waitKeys(keyList=['space'])
    # Close the window
    #win.close()

## Preload question##
def preload_question(text):
    """
    Function to present a question and wait for 'y' or 'n' key input.
    - If 'y' is pressed, the program continues.
    - If 'n' is pressed, the program quits.
    """
    # Create a not full-screen PsychoPy window
    win = visual.Window(fullscr=False)
    # Create the text stimulus
    instruction = visual.TextStim(win, text=text, color="black", height=0.08)  # Adjust height if needed
    while True:
        # Draw the text and flip the window to display it
        instruction.draw()
        win.flip()
        
        # Wait for a key press and handle response
        keys = event.waitKeys(keyList=['y', 'n'])
        if keys:
            if 'y' in keys:
                break  # Proceed if 'y' is pressed
            elif 'n' in keys:
                win.close()  # Close the window
                core.quit()  # Quit the program
    
    # Close the window before continuing
    win.close()

## Create a full-screen window once at the start ##
win = visual.Window(fullscr=False)

## Start preloading? ##
preload_question("Start preloading the experiment? \n\n Press 'y' to preload, or press 'n' to quit.")

## Preload videos and images ##
base_path = "Pictures"
num_folders = 3
folder_names = [f"Klip_{i}" for i in range(1, num_folders + 1)]
random.shuffle(folder_names)

video_stimuli = {}
image_stimuli = {}

for folder_name in folder_names:
    check_for_quit()  # Call this at the start or during the loop
    # Preload videos
    video_files = glob.glob(f"{base_path}/{folder_name}/*.mp4")
    if video_files:  # Ensure video files exist
        video_stimuli[folder_name] = visual.MovieStim3(
            win, video_files[0], size=(1600, 900)  # Assumes one video per folder
        )
    else:
        print(f"No video files found in {folder_path}")

    
    # Preload images
    image_paths = glob.glob(f"{base_path}/{folder_name}/*.png")
    if len(image_paths) > 4:
        image_paths = random.sample(image_paths, 4)  # Ensure only 4 images are used
    image_stimuli[folder_name] = [visual.ImageStim(win, img_path, size=(0.7, 0.7)) for img_path in image_paths]

## Presenting example with image ##
def present_text_and_image(text, image_path):  # Added an image_path parameter
    # Create a full-screen PsychoPy window
    #win = visual.Window(fullscr=True)
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
    #win.close()

## Presenting Video ##
def present_video(video_path):
    # Create a full-screen PsychoPy window
    #win = visual.Window(fullscr=True)
    # Create the video stimulus
    video_stim = visual.MovieStim3(win, video_path, size=(1600, 900))  # Adjust the size as needed, (1920, 1080) is fullscreen
    # Play the video until it finishes
    while video_stim.status != visual.FINISHED:
        video_stim.draw()
        win.flip()
    # Wait a short moment before closing
    #core.wait(1)
    # Close the window after the video ends
    #win.close()
    # Save video path for logfile
    return video_path

## Presenting Decision ##
def present_text_and_images(text, image_paths, logfile, index, folder_label):
    # Create a full-screen PsychoPy window
    #win = visual.Window(fullscr=True)
    
    # Create the text stimulus
    instruction = visual.TextStim(win, text=text, color="black", height=0.08, pos=(0, 0.8))
    
    # Display the folder label in the bottom-right corner
    folder_text = visual.TextStim(win, text=folder_label, pos=(0.9, -0.8), height=0.05, color='black', alignHoriz='right')
    
    # Randomly shuffle the selected images
    random.shuffle(image_paths)
    
    # Adjust the spacing and position for a balanced 2x2 grid
    horizontal_offset = 0.4   # Distance between columns
    vertical_offset = 0.4     # Distance between rows
    grid_offset = -0.2        # Lower the entire grid (adjust as needed)

    # Create the image stimuli in a balanced 2x2 grid with the grid moved lower
    image_stim_top_left = visual.ImageStim(win, image=image_paths[0], pos=(-horizontal_offset, vertical_offset + grid_offset), size=(0.7, 0.7))
    image_stim_top_right = visual.ImageStim(win, image=image_paths[1], pos=(horizontal_offset, vertical_offset + grid_offset), size=(0.7, 0.7))
    image_stim_bottom_left = visual.ImageStim(win, image=image_paths[2], pos=(-horizontal_offset, -vertical_offset + grid_offset), size=(0.7, 0.7))
    image_stim_bottom_right = visual.ImageStim(win, image=image_paths[3], pos=(horizontal_offset, -vertical_offset + grid_offset), size=(0.7, 0.7))
    
    # Draw the text, images, and folder label, and flip the window to display them
    instruction.draw()
    folder_text.draw()  # Draw folder label
    image_stim_top_left.draw()
    image_stim_top_right.draw()
    image_stim_bottom_left.draw()
    image_stim_bottom_right.draw()
    win.flip()
    
    # Initialize and start the timer
    timer = core.Clock()
    
    # Wait for mouse click on any image
    mouse = event.Mouse(win=win)
    clicked = False
    chosen_image = None
    Response_time = None  # To store the time taken to make a selection
    
    while not clicked:
        if mouse.getPressed()[0]:  # Check if the left mouse button is pressed
            mouse_x, mouse_y = mouse.getPos()
            if image_stim_top_left.contains(mouse_x, mouse_y):
                chosen_image = image_paths[0]  # Top left image clicked
                clicked = True
            elif image_stim_top_right.contains(mouse_x, mouse_y):
                chosen_image = image_paths[1]  # Top right image clicked
                clicked = True
            elif image_stim_bottom_left.contains(mouse_x, mouse_y):
                chosen_image = image_paths[2]  # Bottom left image clicked
                clicked = True
            elif image_stim_bottom_right.contains(mouse_x, mouse_y):
                chosen_image = image_paths[3]  # Bottom right image clicked
                clicked = True
    
    # Record the response time when an image is clicked
    Response_time = timer.getTime()
    
    # Retrieve the decision from the decision_map using the chosen image
    Decision = decision_map.get(chosen_image, None)
    
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
    #win.close()
    # Save the decision
    return Decision, Response_time


# Showing dialogue box
DialogueBox.show()

# Collecting participant information
if DialogueBox.OK:
    Position = DialogueBox.data[0]
    Number = DialogueBox.data[1]
    Team = DialogueBox.data[2]
    Foot = DialogueBox.data[3]
    Age = DialogueBox.data[4]
    Experience = DialogueBox.data[5]
    Experience_VFF = DialogueBox.data[6]
else:
    core.quit()


## Create a full-screen window once at the start ##
win = visual.Window(fullscr=True)

## the consent and instruction section ##
present_text(consent_text)
present_text(warmup_text1)
#present_text_and_image(warmup_text2, "Pictures/warmup_reddot.png")
#present_text_and_image("For eksempel", "Pictures/warmup_field.png")
present_text_and_image(warmup_text3, "Pictures/warmup_options.png")
present_text(warmup_text4)

## Warm up loop ##
# Define the base path and number of folders
warmup_path = "Warmup"
warmup_folders = 3

# Generate the folder names and shuffle them for a random order
folder_names = [f"Klip_{i}" for i in range(1, warmup_folders + 1)]
random.shuffle(folder_names)

# Loop through each folder in the randomized order
for index, folder_name in enumerate(folder_names):
    check_for_quit()  # Call this at the start or during the loop
    # Get the .png images in the current folder
    image_paths = glob.glob(f"{warmup_path}/{folder_name}/*.png")
    
    # Ensure only four images are selected; pick four at random if there are more
    if len(image_paths) > 4:
        image_paths = random.sample(image_paths, 4)
    
    # Map the chosen image to a decision using its filename
    decision_map = {img_path: os.path.splitext(os.path.basename(img_path))[0] for img_path in image_paths}
    
    # Find the MP4 file in the current folder
    mp4_files = glob.glob(f"{warmup_path}/{folder_name}/*.mp4")
    if len(mp4_files) != 1:
        raise ValueError(f"Expected exactly one MP4 file in folder '{folder_name}', found {len(mp4_files)}.")
    video_path = mp4_files[0]
    
    # Present the video and the images
    Video_path = present_video(video_path)
    Decision, Response_time = present_text_and_images(
        task_text, 
        image_paths, 
        logfile, 
        index=index, 
        folder_label=folder_name  # Pass the folder name to the function
    )
    
    # Append the new entry to the logfile dataframe
    logfile = logfile.append({
        'Number': Number,
        'Position': Position,
        'Team': Team,
        'Age': Age,
        'Foot': Foot,
        'Experience': Experience,
        'Experience_VFF': Experience_VFF,
        'Video': Video_path,
        'Decision': Decision,
        'RT': Response_time
    }, ignore_index=True)


## start the experiment ##
present_text(intro_text)

## Experiment loop ##
# Define the base path and number of folders
base_path = "Pictures"
num_folders = 3

# Generate the folder names and shuffle them for a random order
folder_names = [f"Klip_{i}" for i in range(1, num_folders + 1)]
random.shuffle(folder_names)

# Loop through each folder in the randomized order
for index, folder_name in enumerate(folder_names):
    check_for_quit()  # Call this at the start or during the loop
    # Get the .png images in the current folder
    image_paths = glob.glob(f"{base_path}/{folder_name}/*.png")
    
    # Ensure only four images are selected; pick four at random if there are more
    if len(image_paths) > 4:
        image_paths = random.sample(image_paths, 4)
    
    # Map the chosen image to a decision using its filename
    decision_map = {img_path: os.path.splitext(os.path.basename(img_path))[0] for img_path in image_paths}
    
    # Find the MP4 file in the current folder
    mp4_files = glob.glob(f"{base_path}/{folder_name}/*.mp4")
    if len(mp4_files) != 1:
        raise ValueError(f"Expected exactly one MP4 file in folder '{folder_name}', found {len(mp4_files)}.")
    video_path = mp4_files[0]
    
    # Present the video and the images
    Video_path = present_video(video_path)
    Decision, Response_time = present_text_and_images(
        task_text, 
        image_paths, 
        logfile, 
        index=index, 
        folder_label=folder_name  # Pass the folder name to the function
    )
    
    # Append the new entry to the logfile dataframe
    logfile = logfile.append({
        'Number': Number,
        'Position': Position,
        'Team': Team,
        'Age': Age,
        'Foot': Foot,
        'Experience': Experience,
        'Experience_VFF': Experience_VFF,
        'Video': Video_path,
        'Decision': Decision,
        'RT': Response_time
    }, ignore_index=True)


win = visual.Window(fullscr=True)
thank_you_text = visual.TextStim(win, text="Tak", color="black", height=0.1, pos=(0, 0))
thank_you_text.draw()
win.flip()
core.wait(2)
win.close()

## Save logfile ##
logfile_name = f"logfiles/logfile_{Number}_{Team}.csv"
logfile.to_csv(logfile_name)