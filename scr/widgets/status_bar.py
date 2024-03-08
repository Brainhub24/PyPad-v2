from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy

from scr.scripts.tools.file import FileLoader
from scr.scripts.utils import Path
from scr.project import ProjectConfig


class StatusBar(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setStyleSheet(FileLoader.load_style("scr/widgets/styles/status_bar.css"))
        self.setObjectName("status-bar")
        self.setMinimumHeight(30)

        self.mainLayout = QHBoxLayout()

        self.current_file_status = QLabel()
        self.current_position = QLabel()
        # self.current_encoding = QLabel("utf-8")

        self.mainLayout.addWidget(self.current_file_status)
        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored))
        self.mainLayout.addWidget(self.current_position)
        self.mainLayout.addWidget(QLabel("Version: Pre-release v0.2.2"))
        # self.mainLayout.addWidget(self.current_encoding)

        self.setLayout(self.mainLayout)

    def set_current_file_status(self, __path: str) -> None:
        text = Path.to_relative_path(ProjectConfig.get_directory(), __path).replace("\\", "  >  ")
        self.current_file_status.setText(text)

    def set_current_position(self, line: int, char: int) -> None:
        self.current_position.setText(f"Line: {line + 1}{" " * 3}Column: {char + 1}")

    def text_file(self, visible: bool) -> None:
        self.current_position.setVisible(visible)
        # self.current_encoding.setVisible(visible)

    def change_file_status(self, tab) -> None:
        if tab is None: return

        if tab.path is not None:
            self.set_current_file_status(tab.path)

        else:
            self.set_current_file_status(tab.title)

    def update_status_bar(self, tab) -> None:
        if tab is None: return

        if tab.is_readable(): self.text_file(True)
        else: self.text_file(False)
