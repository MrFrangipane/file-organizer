import os
import json


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

        return os.path.exists(ProjectAPI.make_project_foldername(project_name))

    @staticmethod
    def new(project_name) -> bool:
        project_foldername = ProjectAPI.make_project_foldername(project_name)
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
    def open_documentation(project_name):
        os.startfile(ProjectAPI._make_documentation_foldername(project_name))

    @staticmethod
    def _make_documentation_foldername(project_name):
        project_foldername = ProjectAPI.make_project_foldername(project_name)
        return os.path.join(project_foldername, "_documentation")

    @staticmethod
    def _make_metadata_filepath(project_name):
        return os.path.join(ProjectAPI.make_project_foldername(project_name), ".fileorganizer")

    @staticmethod
    def make_project_foldername(project_name):
        return os.path.join(ProjectAPI.root_folder, ProjectAPI._sanitize(project_name))

    @staticmethod
    def _sanitize(name):
        return name.lower().replace(" ", "").replace("'", "")
