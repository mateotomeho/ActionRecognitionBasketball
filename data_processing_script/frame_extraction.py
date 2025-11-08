import cv2
import os
import numpy as np

#Declare the input and output directories
VIDEOS_DIR = "processed_dataset"      # Folder containing videos organized by class
OUTPUT_DIR = "frames_dataset"         # Folder where extracted frames will be saved
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create the output directory if it doesn't exist

#Number of frames to extract and target frame size
FRAMES_PER_VIDEO = 16     # Number of frames to sample per video
FRAME_SIZE = (128, 128)   # Target size (width, height) for each extracted frame

#Loop through each label folder in the videos directory
for label in os.listdir(VIDEOS_DIR):
    label_path = os.path.join(VIDEOS_DIR, label)
    
    #Skip if not a folder just in case
    if not os.path.isdir(label_path):
        continue

    # Create a corresponding label folder in the output directory
    output_label_path = os.path.join(OUTPUT_DIR, label)
    os.makedirs(output_label_path, exist_ok=True) #example: frames_dataset/block

    # Loop though each video in the label folder
    for video_name in os.listdir(label_path):
        if not video_name.endswith(".mp4"):
            continue  # skip non-video files

        video_path = os.path.join(label_path, video_name)
        video_id = os.path.splitext(video_name)[0]  # remove .mp4 extension
        
        # Create a subfolder to store frames for this video
        out_dir = os.path.join(output_label_path, video_id)
        os.makedirs(out_dir, exist_ok=True)

        # Open the video file
        cap = cv2.VideoCapture(video_path)  # load video using OpenCV
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # total frames in the video

        # Determine how often to sample a frame
        # Example: if 160 total frames, we take 1 frame every 10 frames → 160/16 = 10
        step = max(frame_count // FRAMES_PER_VIDEO, 1)

        frame_idx = 0   # keep track of current frame index
        saved = 0       # number of frames successfully saved

        #Loop through the video frames
        while cap.isOpened() and saved < FRAMES_PER_VIDEO:
            ret, frame = cap.read()  # read one frame
            if not ret:
                break  # stop if we reach the end of the video or read fails

            # Save a frame every "step" interval
            if frame_idx % step == 0:
                # Convert to grayscale to reduce computational complexity
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Resize to uniform dimensions (128x128)
                resized = cv2.resize(gray, FRAME_SIZE)
                
                # Save the processed frame as an image
                frame_filename = os.path.join(out_dir, f"frame_{saved:03d}.jpg")
                cv2.imwrite(frame_filename, resized)
                
                saved += 1  # increment the number of saved frames
            
            frame_idx += 1  # move to next frame index

        cap.release()  # close the video file to free memory

print(" Frame extraction complete!")
