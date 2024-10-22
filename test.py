from psychopy import visual, core, event

# Create a full-screen PsychoPy window
win = visual.Window(fullscr=False, color=(0, 0, 0), units='pix')

# Specify the path to your video file
video_path = 'Videos_Dots/warmup_vid_1.mp4'

# Create the video stimulus
video_stim = visual.MovieStim(win, video_path, size=(1600, 900))

# Set autoDraw to True to automatically draw the video stimulus
video_stim.autoDraw = True

# Start the video playback
while True:
    if video_stim.status == visual.FINISHED:
        break  # Exit the loop if the video has finished

    win.flip()  # Update the window

    # Check for quit (pressing 'q' will close the window)
    if event.getKeys(['q']):
        break

# Cleanup
video_stim.autoDraw = False
win.close()


# Test the function with the path to your video
#present_video('Videos_Dots/warmup_vid_1.mp4')





