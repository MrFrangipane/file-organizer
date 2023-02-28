import os
import json

from fileorganizer.python_extensions import sanitize


class ProjectAPI:

    root_folder = None

    @staticmethod
    def all_names():
        for folder in sorted(os.listdir(ProjectAPI.root_folder)):
            project_folderpath = os.path.join(ProjectAPI.root_folder, folder)
            if not os.path.isdir(project_folderpath):
                continue

            metadata_filepath = ProjectAPI._make_metadata_filepath(folder)
            if not os.path.exists(metadata_filepath):
                continue

            with open(metadata_filepath, "r") as metadata_file:
                metadata = json.load(metadata_file)

            if metadata['type'] == "project":
                yield metadata['name']

    @staticmethod
    def exists(project_name) -> bool:
        """Return True of False regarding if a project exists (case-insensitive)"""
        if ProjectAPI.root_folder is None:
            raise RuntimeError("ProjectAPI has no root folder")

        return os.path.exists(ProjectAPI.make_foldername(project_name))

    @staticmethod
    def new(project_name) -> bool:
        project_foldername = ProjectAPI.make_foldername(project_name)
        documentation_foldername = ProjectAPI._make_documentation_foldername(project_name)
        os.makedirs(project_foldername)
        os.makedirs(documentation_foldername)

        metadata = {
            "type": "project",
            "name": project_name,
        }
        with open(ProjectAPI._make_metadata_filepath(project_name), "w+") as metadata_file:
            json.dump(metadata, metadata_file, indent=2)

        return True

    @staticmethod
    def open_folder(project_name):
        os.startfile(ProjectAPI.make_foldername(project_name))

    @staticmethod
    def set_notes(project_name: str, notes: str) -> None:
        filepath = ProjectAPI._make_notes_filepath(project_name)
        with open(filepath, 'w+') as notes_file:
            notes_file.write(notes)

    @staticmethod
    def get_notes(project_name: str) -> str:
        filepath = ProjectAPI._make_notes_filepath(project_name)
        if not os.path.exists(filepath):
            return ""

        with open(filepath, 'r') as notes_file:
            return notes_file.read()

    @staticmethod
    def _make_notes_filepath(project_name: str) -> str:
        return os.path.join(ProjectAPI.make_foldername(project_name), '.notes.txt')

    @staticmethod
    def _make_documentation_foldername(project_name):
        foldername = ProjectAPI.make_foldername(project_name)
        return os.path.join(foldername, "_documentation")

    @staticmethod
    def _make_metadata_filepath(project_name):
        return os.path.join(ProjectAPI.make_foldername(project_name), ".fileorganizer")

    @staticmethod
    def make_foldername(project_name):
        return os.path.join(ProjectAPI.root_folder, sanitize(project_name))
