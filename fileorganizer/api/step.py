import os
import json
from operator import itemgetter

from fileorganizer.api.project import ProjectAPI


class StepAPI:

    @staticmethod
    def all_names(project_name: str) -> [str]:
        metadatas = list()
        project_root = ProjectAPI.make_foldername(project_name)
        for folder in os.listdir(project_root):
            step_folderpath = os.path.join(project_root, folder)
            if not os.path.isdir(step_folderpath):
                continue

            metadata_filepath = StepAPI._make_metadata_filepath(project_name, folder)
            if not os.path.exists(metadata_filepath):
                continue

            with open(metadata_filepath, "r") as metadata_file:
                metadata = json.load(metadata_file)

            if metadata['type'] == "step":
                metadatas.append(metadata)

        return [metadata['name'] for metadata in sorted(metadatas, key=itemgetter('order'))]

    @staticmethod
    def exists(project_name: str, step_name: str) -> bool:
        """Return True of False regarding if a project exists (case-insensitive)"""
        return os.path.exists(StepAPI.make_foldername(project_name, step_name))

    @staticmethod
    def new(project_name: str, step_name: str) -> bool:
        step_foldername = StepAPI.make_foldername(project_name, step_name)
        documentation_foldername = StepAPI._make_documentation_foldername(project_name, step_name)
        os.makedirs(step_foldername)
        os.makedirs(documentation_foldername)

        step_count = len(StepAPI.all_names(project_name))

        metadata = {
            "type": "step",
            "name": step_name,
            "order": step_count
        }
        with open(StepAPI._make_metadata_filepath(project_name, step_name), "w+") as metadata_file:
            json.dump(metadata, metadata_file, indent=2)

        return True

    @staticmethod
    def open_folder(project_name: str, step_name: str) -> None:
        os.startfile(StepAPI.make_foldername(project_name, step_name))

    @staticmethod
    def _make_documentation_foldername(project_name: str, step_name: str) -> str:
        foldername = StepAPI.make_foldername(project_name, step_name)
        return os.path.join(foldername, "_documentation")

    @staticmethod
    def _make_metadata_filepath(project_name: str, step_name: str) -> str:
        return os.path.join(StepAPI.make_foldername(project_name, step_name), ".fileorganizer")

    @staticmethod
    def make_foldername(project_name: str, step_name: str) -> str:
        return os.path.join(ProjectAPI.make_foldername(project_name), StepAPI._sanitize(step_name))

    @staticmethod
    def _sanitize(name: str) -> str:
        return name.lower().replace(" ", "").replace("'", "")
