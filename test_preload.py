from psychopy import visual, event, core
import glob
import random
from multiprocessing import Process, Manager

## Text for consent ##
consent_text = "Kære deltager, du skal til at tage en test, der har til formål at vurdere din viden om fodboldstrategier og beslutningstagning. Testen tager omkring [x minutter], så vær forberedt på at afsætte din tid til dette, da testen skal gennemføres, når først den er startet. Din besvarelse vil blive anonymiseret, og dataen vil udelukkende blive brugt til forsknings- og træningsformål. \n\n Hvis du giver samtykke og gerne vil fortsætte til testen, skal du trykke på mellemrumstasten."

## Create a function for preloading stimuli ##
def preload_stimuli(base_path, num_folders, stimuli_dict):
    folder_names = [f"Klip_{i}" for i in range(1, num_folders + 1)]
    random.shuffle(folder_names)

    for folder_name in folder_names:
        # Add a placeholder entry to signal loading progress
        stimuli_dict[folder_name] = "loading"

        # Simulate preloading videos
        video_path = f"{base_path}/{folder_name}/{folder_name}.mp4"
        stimuli_dict[folder_name] = {
            "video": video_path,  # Replace with actual loading logic if needed
            "images": []
        }

        # Simulate preloading images
        image_paths = glob.glob(f"{base_path}/{folder_name}/*.png")
        if len(image_paths) > 4:
            image_paths = random.sample(image_paths, 4)  # Ensure only 4 images are used
        stimuli_dict[folder_name]["images"] = image_paths

    print("Preloading complete.")

## Main execution ##
if __name__ == '__main__':
    base_path = "Pictures"
    num_folders = 5

    # Use a manager dictionary to share preloading status between processes
    manager = Manager()
    stimuli_dict = manager.dict()

    # Start the preloading process
    preloading_process = Process(target=preload_stimuli, args=(base_path, num_folders, stimuli_dict))
    preloading_process.start()

    # Create a PsychoPy window for consent display
    win = visual.Window(fullscr=True)
    instruction = visual.TextStim(win, text=consent_text, color="black", height=0.08)

    # Display the consent text while waiting for spacebar
    while True:
        # Draw and display the consent text
        instruction.draw()
        win.flip()

        # Check for spacebar press to proceed
        keys = event.getKeys(keyList=['space'])
        if 'space' in keys:
            print("Spacebar pressed. Exiting consent.")
            break

        # Optionally display preloading progress (debugging)
        print(f"Preloading status: {len(stimuli_dict)} folders loaded")

    # Ensure the preloading process finishes if not already done
    if preloading_process.is_alive():
        print("Waiting for preloading to finish...")
        preloading_process.join()

    print("Consent given and preloading completed. Proceeding to the experiment.")
    win.flip()
    core.wait(0.5)
