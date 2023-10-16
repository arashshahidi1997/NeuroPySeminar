from pathlib import Path
import pandas as pd
from config_paths import BASE_DIR

base_path = Path(BASE_DIR)

# Load topics from schedule.csv using pandas
schedule_path = base_path / 'schedule.csv'
df = pd.read_csv(schedule_path)
topics = {int(row['Week']): row['Topic'] for _, row in df.iterrows()}

# Determine the number of weeks from the schedule.csv
weeks = len(df)

# Create subfolders for each week
for week_num in range(1, weeks + 1):
    topic_name = topics.get(week_num, "TopicName")  # Use 'TopicName' as default if the week doesn't have a specified topic
    week_folder = base_path / f"Week_{week_num:02d}_{topic_name}"
    week_folder.mkdir(parents=True, exist_ok=True)
    
    subfolders = ["Lecture_Notes", "Jupyter_Notebooks", "Data_Samples"]
    for subfolder in subfolders:
        (week_folder / subfolder).mkdir(exist_ok=True)

# Create additional folders
additional_folders = ["Reference_Texts", "Additional_Resources", "Utils"]
for folder in additional_folders:
    (base_path / folder).mkdir(exist_ok=True)

print(f"Folder structure for {BASE_DIR} created successfully!")
