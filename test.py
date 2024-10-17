from psychopy import visual, core, event

# Create a window
win = visual.Window(size=(800, 600))

# Load the movie
movie = visual.MovieStim3(win, 'Videos_Dots/warmup_vid_1.mp4', size=(640, 480))

# Play the movie
while movie.status != visual.FINISHED:
    movie.draw()
    win.flip()

    # Optional: Break the video with a keypress
    if event.getKeys():
        break

# Clean up
movie.stop()
win.close()
core.quit()