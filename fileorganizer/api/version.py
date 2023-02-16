import os
import json
from operator import itemgetter

from fileorganizer.python_extensions import sanitize
from fileorganizer.api.step import StepAPI


class VersionAPI:

    @staticmethod
    def all_names(project_name: str, step_name: str) -> [str]:
        metadatas = list()
        step_root = StepAPI.make_foldername(project_name, step_name)
        for folder in os.listdir(step_root):
            version_folderpath = os.path.join(step_root, folder)
            if not os.path.isdir(version_folderpath):
                continue

            metadata_filepath = VersionAPI._make_metadata_filepath(project_name, step_name, folder)
            if not os.path.exists(metadata_filepath):
                continue

            with open(metadata_filepath, "r") as metadata_file:
                metadata = json.load(metadata_file)

            if metadata['type'] == "version":
                metadatas.append(metadata)

        return [metadata['name'] for metadata in sorted(metadatas, key=itemgetter('order'))]

    @staticmethod
    def exists(project_name: str, step_name: str, version_name: str) -> bool:
        """Return True of False regarding if a project exists (case-insensitive)"""
        return os.path.exists(VersionAPI.make_foldername(project_name, step_name, version_name))

    @staticmethod
    def new(project_name: str, step_name: str, version_name: str) -> bool:
        version_foldername = VersionAPI.make_foldername(project_name, step_name, version_name)
        documentation_foldername = VersionAPI._make_documentation_foldername(project_name, step_name, version_name)
        os.makedirs(version_foldername)
        os.makedirs(documentation_foldername)

        version_count = len(VersionAPI.all_names(project_name, step_name))

        metadata = {
            "type": "version",
            "name": version_name,
            "order": version_count
        }
        with open(VersionAPI._make_metadata_filepath(project_name, step_name, version_name), "w+") as metadata_file:
            json.dump(metadata, metadata_file, indent=2)

        return True

    @staticmethod
    def open_folder(project_name: str, step_name: str, version_name: str) -> None:
        os.startfile(VersionAPI.make_foldername(project_name, step_name, version_name))

    @staticmethod
    def _make_documentation_foldername(project_name: str, step_name: str, version_name: str) -> str:
        foldername = VersionAPI.make_foldername(project_name, step_name, version_name)
        return os.path.join(foldername, "_documentation")

    @staticmethod
    def _make_metadata_filepath(project_name: str, step_name: str, version_name: str) -> str:
        return os.path.join(VersionAPI.make_foldername(project_name, step_name, version_name), ".fileorganizer")

    @staticmethod
    def make_filepath(project_name: str, step_name: str, version_name: str) -> str:
        return os.path.join(
            VersionAPI.make_foldername(project_name, step_name, version_name),
            f"{sanitize(step_name)}_{sanitize(version_name)}"
        )

    @staticmethod
    def make_foldername(project_name: str, step_name: str, version_name: str) -> str:
        return os.path.join(StepAPI.make_foldername(project_name, step_name), sanitize(version_name))
