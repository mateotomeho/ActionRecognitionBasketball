import os
import json
import shutil

#File paths
BASE_DIR = "spacejam_dataset"
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
ANNOTATION_PATH = os.path.join(BASE_DIR, "annotation.json")
LABELS_PATH = os.path.join(BASE_DIR, "labels_dict.json")

#Output folder
OUTPUT_DIR = "processed_dataset"
os.makedirs(OUTPUT_DIR, exist_ok=True)

#Load JSON files
with open(ANNOTATION_PATH, "r") as f:
    annotations = json.load(f)

with open(LABELS_PATH, "r") as f:
    labels_dict = json.load(f)

#Reverse the labels dict: map ID -> name directly
id_to_label = {int(k): v for k, v in labels_dict.items()}

#Track stats
moved_count = 0
skipped_count = 0
missing_files = []

#Create subfolders for each valid label (except 'discard') -found in the previous code that there isn't a 'discard' video
for label_name in set(id_to_label.values()):
    if label_name == "discard":
        continue
    os.makedirs(os.path.join(OUTPUT_DIR, label_name), exist_ok=True)

#Process each labeled video
for video_id, label_id in annotations.items():
    label_name = id_to_label.get(label_id, "unknown")

    # Skip discard and unknown
    if label_name in ["discard", "unknown"]:
        skipped_count += 1
        continue

    src_video = os.path.join(VIDEOS_DIR, f"{video_id}.mp4")
    dst_video = os.path.join(OUTPUT_DIR, label_name, f"{video_id}.mp4")

    # Check file existence
    if not os.path.exists(src_video):
        missing_files.append(video_id)
        skipped_count += 1
        continue

    # Copy (or move if you prefer to save space)
    shutil.copy2(src_video, dst_video)
    # shutil.move(src_video, dst_video)  # use this instead if you want to MOVE, not COPY

    moved_count += 1

print(f"Organized {moved_count} videos into {OUTPUT_DIR}/")
print(f"Skipped {skipped_count} videos (missing or discarded)")
if missing_files:
    print(f"Missing video files saved to missing_videos_organized.txt")

    with open("missing_videos_organized.txt", "w") as f:
        for vid in missing_files:
            f.write(vid + "\n")
