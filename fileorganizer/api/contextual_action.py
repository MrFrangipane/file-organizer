import os.path

from PySide6.QtWidgets import QWidget, QLabel

from fileorganizer.qt_extensions import make_icon_button

from fileorganizer.api.version import VersionAPI


class ContextualActionAPI:

    @staticmethod
    def get_all_widgets(project_name: str, step_name: str, version_name: str) -> [QWidget]:
        version_filepath = VersionAPI.make_filepath(project_name, step_name, version_name)

        # KiCad 6
        kicad_6_filepath = os.path.join(
            version_filepath,
            os.path.basename(version_filepath) + '.kicad_pro'
        )
        if os.path.exists(kicad_6_filepath):
            def open_in_kicad_6():
                os.startfile(kicad_6_filepath)

            return [make_icon_button(
                "Open KiCad 6 project", "kicad.png", open_in_kicad_6, "Open..."
            )]

        return list()
