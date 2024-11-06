## Importing modules ##
from psychopy import visual, event, core, gui, data, clock
import pandas as pd, random, os, glob

## Logfile ##
# Making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

# Define the logfile name
logfile_name = "logfiles/logfile.csv"

## Setting up dataframe ##
columns = ['Number', 'Position', 'Age', 'Foot', 'Experience', 'Experience_VFF', 'Tactic', 'Decision', 'RT']  # Columns for the tactical data
logfile = pd.DataFrame(columns=columns)

## GUI ##
# Creating dialogue box
DialogueBox = gui.Dlg(title="Viborg Tactics")
DialogueBox.addText('Udfyld venligst de nedenstående felter:')
list_of_numbers = list(range(0, 20))  # Options for years of experience
DialogueBox.addField('Hvor på banen spiller du?:', choices=['Fosvarsspiller', 'Midtbanespiller', 'Angriber'], color="green")
DialogueBox.addField('Hvad er dit trøjenummer:', color="black")
DialogueBox.addField('Hvilken fod er din dominante?:', choices=['Højre', 'Venstre'], color="green")
DialogueBox.addField('Hvad er din alder:', color="black")
DialogueBox.addField('Hvor mange år har du spillet fodbold?:', choices=list_of_numbers, color="green")
DialogueBox.addField('Hvor mange år har du spillet fodbold hos VFF?:', choices=list_of_numbers, color="black")
DialogueBox.show()

# Collecting participant information
if DialogueBox.OK:
    Position, Number, Foot, Age, Experience, Experience_VFF = DialogueBox.data
else:
    core.quit()

# Consent and instruction texts
consent_text = "Kære deltager, du skal til at tage en test, der har til formål at vurdere din viden om fodboldstrategier..."
warmup_text1 = "Du vil nu blive præsenteret for 3 opvarmningsøvelser..."
task_text = "Hvad burde den markerede spiller gøre?"

## Create a full-screen window once at the start ##
win = visual.Window(fullscr=True)

# Preload videos and images
base_path = "Pictures"
num_folders = 5
folder_names = [f"Klip_{i}" for i in range(1, num_folders + 1)]
random.shuffle(folder_names)

video_stimuli = {}
image_stimuli = {}

for folder_name in folder_names:
    # Preload videos
    video_path = f"{base_path}/{folder_name}/{folder_name}.mp4"
    video_stimuli[folder_name] = visual.MovieStim3(win, video_path, size=(1600, 900))
    
    # Preload images
    image_paths = glob.glob(f"{base_path}/{folder_name}/*.png")
    if len(image_paths) > 4:
        image_paths = random.sample(image_paths, 4)  # Ensure only 4 images are used
    image_stimuli[folder_name] = [visual.ImageStim(win, img_path, size=(0.7, 0.7)) for img_path in image_paths]

## Present text ##
def present_text(text):
    instruction = visual.TextStim(win, text=text, color="black", height=0.08)
    instruction.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

## Present video ##
def present_video(folder_name):
    video_stim = video_stimuli[folder_name]
    while video_stim.status != visual.FINISHED:
        video_stim.draw()
        win.flip()
    core.wait(2)  # Short wait before moving on

## Present images in 2x2 layout with response collection ##
def present_text_and_images(folder_name, text):
    images = image_stimuli[folder_name]
    random.shuffle(images)
    
    # Define positions for 2x2 layout
    positions = [(-0.4, 0.4), (0.4, 0.4), (-0.4, -0.4), (0.4, -0.4)]
    instruction = visual.TextStim(win, text=text, color="black", height=0.08, pos=(0, 0.8))
    
    # Draw instruction and images in grid
    instruction.draw()
    for img, pos in zip(images, positions):
        img.pos = pos
        img.draw()
    win.flip()

    # Capture response and reaction time
    timer = core.Clock()
    mouse = event.Mouse(win=win)
    chosen_image, response_time = None, None
    
    while not chosen_image:
        if mouse.getPressed()[0]:  # Check left mouse click
            mouse_x, mouse_y = mouse.getPos()
            for img, pos in zip(images, positions):
                if img.contains(mouse_x, mouse_y):
                    chosen_image = img.image
                    response_time = timer.getTime()
                    break

    # Map chosen image to decision label based on filename
    decision_map = {img.image: os.path.splitext(os.path.basename(img.image))[0] for img in images}
    return decision_map.get(chosen_image), response_time

## Run Consent ##
present_text(consent_text)

# Loop through each folder and present stimuli
for index, folder_name in enumerate(folder_names):
    present_video(folder_name)
    Decision, Response_time = present_text_and_images(folder_name, task_text)

    # Append trial data to logfile
    logfile = logfile.append({
        'Number': Number,
        'Position': Position,
        'Age': Age,
        'Foot': Foot,
        'Experience': Experience,
        'Experience_VFF': Experience_VFF,
        'Tactic': folder_name,
        'Decision': Decision,
        'RT': Response_time
    }, ignore_index=True)

    # Save incrementally
    logfile.to_csv(logfile_name, index=False)

# End of experiment message
thank_you_text = visual.TextStim(win, text="Tak", color="black", height=0.1, pos=(0, 0))
thank_you_text.draw()
win.flip()
core.wait(2)
win.close()
