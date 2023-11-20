from pathlib import Path
import pandas as pd
from src import config

# Constants
SUBFOLDERS = ["resources", "code", "data", "results"]
ADDITIONAL_FOLDERS = ["src", "resources", "data"]
WEEK_FOLDER_FORMAT = "Week_{:02d}_{}"  # Format for week folder names

class ScheduleManager:
    def __init__(self):
        self.schedule_df = None
        self.topics = None
        self.load_schedule()
        self.week_folders = {}
        self.set_week_folder_names()

    def load_schedule(self):
        schedule_path = config.DOCS_DIR / 'schedule.csv'
        self.schedule_df = pd.read_csv(schedule_path)
        self.set_topics()

    def set_topics(self):
        if self.schedule_df is not None:
            self.topics = {int(row['Week']): row['Topic'] for _, row in self.schedule_df.iterrows()}

    def set_week_dir(self, week_num):
        if self.topics:
            topic_name = self.topics.get(week_num, "TopicName")
            week_folder = config.BASE_DIR / WEEK_FOLDER_FORMAT.format(week_num, topic_name)
            self.week_folders[week_num] = week_folder

    def set_week_folder_names(self):
        if self.schedule_df is not None:
            weeks = len(self.schedule_df)
            for week_num in range(1, weeks + 1):
                self.set_week_dir(week_num)

    def create_week_directories(self):
        self.set_week_folder_names()  # Ensure week folder names are set
        for week_num, week_folder in self.week_folders.items():
            week_folder.mkdir(parents=True, exist_ok=True)
            for subfolder in SUBFOLDERS:
                (week_folder / subfolder).mkdir(exist_ok=True)

    def create_week_subdirectory(self, week_num):
        self.set_week_dir(week_num)  # Ensure the week directory is set
        week_folder = self.week_folders.get(week_num)
        if week_folder:
            week_folder.mkdir(parents=True, exist_ok=True)
            subfolders = ["resources/resources.md", "code/code.md", "data/data.md", "results/results.md"]
            for subfolder in subfolders:
                (week_folder / subfolder).touch()
            print(f"Week {week_num} activated successfully!")

    def create_additional_folders(self):
        for folder in ADDITIONAL_FOLDERS:
            (config.BASE_DIR / folder).mkdir(exist_ok=True)
        print(f"Folder structure for {config.BASE_DIR} created successfully!")

def get_baseio():
    sch = ScheduleManager()
    return sch

# Example usage
def main():
    schedule_manager = ScheduleManager()
    schedule_manager.set_weeks()
    schedule_manager.create_additional_folders()

