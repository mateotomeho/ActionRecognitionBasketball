import json
import os
from collections import defaultdict
import pandas as pd

# === File paths ===
ANNOTATION_PATH = "spacejam_dataset/annotation.json"
LABELS_PATH = "spacejam_dataset/labels_dict.json"
VIDEOS_DIR = "spacejam_dataset/videos"

# === Load JSON files ===
with open(ANNOTATION_PATH, "r") as f:
    annotations = json.load(f)

with open(LABELS_PATH, "r") as f:
    labels_dict = json.load(f)

# === Get all video files ===
video_files = [v for v in os.listdir(VIDEOS_DIR) if v.endswith(".mp4")]
video_ids = [os.path.splitext(v)[0] for v in video_files]  # keep '_flipped'

# === Check which videos have labels ===
labeled_videos = set(annotations.keys())
all_video_ids = set(video_ids)

videos_with_labels = [vid for vid in all_video_ids if vid in labeled_videos]
videos_without_labels = [vid for vid in all_video_ids if vid not in labeled_videos]

# === Count how many videos per category ===
category_counts = defaultdict(int)
for vid, label_id in annotations.items():
    label_name = labels_dict.get(str(label_id), "unknown")
    category_counts[label_name] += 1

# === Create DataFrame summary ===
summary_df = pd.DataFrame([
    {"Label ID": k, "Label Name": v, "Count": category_counts[v]}
    for k, v in labels_dict.items()
]).sort_values(by="Count", ascending=False)

# === Print results ===
print(f"Total videos found: {len(all_video_ids)}")
print(f"Videos with labels: {len(videos_with_labels)}")
print(f"Videos without labels: {len(videos_without_labels)}\n")

print("=== Videos without labels (first 10) ===")
print(videos_without_labels[:10], "...\n")

print("=== Category counts ===")
print(summary_df)

# === Optional: Save summary to CSV for later ===
summary_df.to_csv("label_summary.csv", index=False)
print("\n Saved summary as label_summary.csv")


# === Optional: Plot category distribution ===
import matplotlib.pyplot as plt

summary_df.plot(kind='bar', x='Label Name', y='Count', legend=False)
plt.title('Video Counts per Label')
plt.ylabel('Count')
plt.xlabel('Label Name')
plt.tight_layout()
plt.show()

# === Save missing videos list ===
missing_videos_path = "missing_videos.txt"

with open(missing_videos_path, "w") as f:
    for vid in sorted(videos_without_labels):
        f.write(vid + "\n")

print(f"\nSaved list of {len(videos_without_labels)} missing videos to {missing_videos_path}")
