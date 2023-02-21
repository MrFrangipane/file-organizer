import os.path
from glob import glob

from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QPoint

from fileorganizer.qt_extensions import make_icon, make_icon_button

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

        # FreeCAD 0.20
        freecad_files = sorted(glob(version_filepath + "-*.FCStd") + glob(version_filepath + "-*.step"))
        if freecad_files:

            button = make_icon_button("Select a FreeCAD file to open", "freecad.png", None, "Open...")

            actions = list()
            for freecad_file in freecad_files:
                def open_in_freecad():
                    os.startfile(freecad_file)
                action = QAction(
                    make_icon("freecad.png"),
                    os.path.basename(freecad_file)
                )
                action.triggered.connect(open_in_freecad)
                actions.append(action)

            def open_freecad():
                menu = QMenu()

                for action in actions:
                    menu.addAction(action)

                menu.setFixedWidth(button.width())
                menu.exec(button.mapToGlobal(QPoint(0, button.height())))

            button.clicked.connect(open_freecad)
            return [button]

        # Unknown
        return list()
