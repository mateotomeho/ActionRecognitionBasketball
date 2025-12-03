import os
import shutil
import random
import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

TARGET_CLASSES = ["pass", "dribble", "shoot", "defense"]
#Desired cap for all selected classes
MAX_VIDEOS_PER_CLASS = 500 

# Declare the input and output directories
SOURCE_DIR = "frames_dataset"
# Using a new name for the destination folder to clearly indicate it's the balanced version
DEST_DIR = "split_dataset_balanced" 

# Clean up previous destination directory for a fresh split
if os.path.exists(DEST_DIR):
    shutil.rmtree(DEST_DIR) 
os.makedirs(DEST_DIR, exist_ok=True)
# ----------------------------------------------------------------

# Split ratios (Applied to the newly capped source pool)
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

# For reproducibility
random.seed(100)

# To store class frame counts for weight calculation
class_counts = Counter()

## 1. Filter, Cap, and Split Videos

for label in os.listdir(SOURCE_DIR):
    label_path = os.path.join(SOURCE_DIR, label)
    
    # Filter: Skip classes not in the TARGET_CLASSES list
    if label not in TARGET_CLASSES or not os.path.isdir(label_path):
        continue
    
    # Get all video folders for this label
    videos = []
    for v in os.listdir(label_path):
        full_path = os.path.join(label_path, v)
        if os.path.isdir(full_path):
            videos.append(v)
            
    # Cap: Apply the maximum video limit BEFORE splitting
    # Shuffle first to ensure randomness, then cap at MAX_VIDEOS_PER_CLASS
    random.shuffle(videos)
    videos_to_split = videos[:MAX_VIDEOS_PER_CLASS]
    
    n_total = len(videos_to_split) # The new total is the capped/available count
    n_train = int(train_ratio * n_total)
    n_val = int(val_ratio * n_total)
    
    # Split the videos based on the new proportional counts
    train_videos = videos_to_split[:n_train]
    val_videos = videos_to_split[n_train:n_train + n_val]
    test_videos = videos_to_split[n_train + n_val:]

    splits = {
        "train": train_videos,
        "val": val_videos,
        "test": test_videos
    }
    
    # Copy the split videos into their respective folders
    for split_name, split_videos in splits.items():
        split_label_dir = os.path.join(DEST_DIR, split_name, label)
        os.makedirs(split_label_dir, exist_ok=True)

        for vid in split_videos:
            src = os.path.join(label_path, vid)
            dst = os.path.join(split_label_dir, vid)
            
            # Copy the entire directory (video frames)
            shutil.copytree(src, dst)

            # Count frames for weight calculation
            n_frames = len(os.listdir(src))
            class_counts[label] += n_frames

print("Dataset split complete")

## 2. Save Class Weights and Summary

total_frames = sum(class_counts.values())
class_weights = {}

for label, count in class_counts.items():
    # Inverse frequency weighting
    class_weights[label] = round(total_frames / (len(class_counts) * count), 4)

weights_path = os.path.join(DEST_DIR, "class_weights.json")
with open(weights_path, "w") as f:
    json.dump({
        "class_counts": class_counts,
        "class_weights": class_weights
    }, f, indent=4)

print("\nClass counts (New Balanced Split):")
for label, count in class_counts.items():
    print(f"{label:15} {count:6d}")

print("\nClass weights (inverse frequency, New Balanced Split):")
for label, weight in class_weights.items():
    print(f"{label:15} {weight:.4f}")

print(f"\nSaved weights and counts to {weights_path}")

## 3. Print Final Summary Table (Images Count)

split_counts = {"train": 0, "val": 0, "test": 0}

for split_name in ["train", "val", "test"]:
    split_dir = os.path.join(DEST_DIR, split_name)
    # The script now only finds the 4 target labels inside DEST_DIR
    for label in os.listdir(split_dir):
        label_path = os.path.join(split_dir, label)
        if not os.path.isdir(label_path):
            continue
        for vid in os.listdir(label_path):
            vid_path = os.path.join(label_path, vid)
            if os.path.isdir(vid_path):
                split_counts[split_name] += len(os.listdir(vid_path))

split_counts["total"] = sum(split_counts.values())

df_splits = pd.DataFrame({
    "Split": ["Train", "Validation", "Test", "Total"],
    "Number of Images": [
        split_counts["train"],
        split_counts["val"],
        split_counts["test"],
        split_counts["total"]
    ]
})

print("\n=== Dataset Split Summary (Capped at 500 Videos/Class) ===")
print(df_splits.to_string(index=False))

fig, ax = plt.subplots()
ax.axis('off')
table = ax.table(cellText=df_splits.values,
                 colLabels=df_splits.columns,
                 loc='center',
                 cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)
plt.title("Dataset Split Summary (Capped at 500 Videos/Class)", pad=20)
plt.show()

##################################################################################################

# import os
# import shutil
# import random
# import json
# from collections import Counter

# #Declare the intput and output directories
# SOURCE_DIR = "frames_dataset"
# DEST_DIR = "split_dataset"
# os.makedirs(DEST_DIR, exist_ok=True)

# # Split ratios
# train_ratio = 0.8
# val_ratio = 0.1
# test_ratio = 0.1

# # For reproducibility
# random.seed(100)

# # To store class frame counts for weight calculation
# class_counts = Counter()

# #Loop through each label folder in the source directory
# for label in os.listdir(SOURCE_DIR):
#     label_path = os.path.join(SOURCE_DIR, label)
#     if not os.path.isdir(label_path):
#         continue
    
#     # Get all video folders for this label
#     videos = []
#     for v in os.listdir(label_path):
#         full_path = os.path.join(label_path, v)
#         if os.path.isdir(full_path):
#             videos.append(v)
#     random.shuffle(videos) # shuffle for randomness

#     n_total = len(videos)
#     n_train = int(train_ratio * n_total)
#     n_val = int(val_ratio * n_total)
    
#     # Split the videos into train/val/test sets
#     train_videos = videos[:n_train]
#     val_videos = videos[n_train:n_train + n_val]
#     test_videos = videos[n_train + n_val:]

#     splits = {
#         "train": train_videos,
#         "val": val_videos,
#         "test": test_videos
#     }
    

#     # Copy the splits videos into their respective folders
#     for split_name, split_videos in splits.items():
#         split_label_dir = os.path.join(DEST_DIR, split_name, label)
#         os.makedirs(split_label_dir, exist_ok=True)

#         for vid in split_videos:
#             src = os.path.join(label_path, vid)
#             dst = os.path.join(split_label_dir, vid)
#             shutil.copytree(src, dst)

#             # Count frames for weight calculation
#             n_frames = len(os.listdir(src))
#             class_counts[label] += n_frames

# print("Dataset split complete")

# ########################################
# #Save class counts and compute weights
# total_frames = sum(class_counts.values())
# class_weights = {}

# for label, count in class_counts.items():
#     # Inverse frequency weighting
#     class_weights[label] = round(total_frames / (len(class_counts) * count), 4)

# # Save to JSON for later use in Colab
# weights_path = os.path.join(DEST_DIR, "class_weights.json")
# with open(weights_path, "w") as f:
#     json.dump({
#         "class_counts": class_counts,
#         "class_weights": class_weights
#     }, f, indent=4)

# print("\nClass counts:")
# for label, count in class_counts.items():
#     print(f"{label:15} {count:6d}")

# print("\nClass weights (inverse frequency):")
# for label, weight in class_weights.items():
#     print(f"{label:15} {weight:.4f}")

# print(f"\nSaved weights and counts to {weights_path}")

# ########################################
# import pandas as pd
# import matplotlib.pyplot as plt

# # Count total frames per split
# split_counts = {"train": 0, "val": 0, "test": 0}

# for split_name in ["train", "val", "test"]:
#     split_dir = os.path.join(DEST_DIR, split_name)
#     for label in os.listdir(split_dir):
#         label_path = os.path.join(split_dir, label)
#         if not os.path.isdir(label_path):
#             continue
#         for vid in os.listdir(label_path):
#             vid_path = os.path.join(label_path, vid)
#             if os.path.isdir(vid_path):
#                 split_counts[split_name] += len(os.listdir(vid_path))

# # Add total
# split_counts["total"] = sum(split_counts.values())

# # Create a DataFrame for a clean table view
# df_splits = pd.DataFrame({
#     "Split": ["Train", "Validation", "Test", "Total"],
#     "Number of Images": [
#         split_counts["train"],
#         split_counts["val"],
#         split_counts["test"],
#         split_counts["total"]
#     ]
# })

# print("\n=== Dataset Split Summary ===")
# print(df_splits.to_string(index=False))

# #Show the table visually with Matplotlib
# fig, ax = plt.subplots()
# ax.axis('off')
# table = ax.table(cellText=df_splits.values,
#                  colLabels=df_splits.columns,
#                  loc='center',
#                  cellLoc='center')
# table.auto_set_font_size(False)
# table.set_fontsize(10)
# table.scale(1.2, 1.2)
# plt.title("Dataset Split Summary", pad=20)
# plt.show()
