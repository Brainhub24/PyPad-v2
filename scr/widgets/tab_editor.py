from scr.scripts import FileLoader, FileChecker
from scr.config import IconPaths
from .welcome_screen import WelcomeScreen

from PySide6.QtWidgets import QTabWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt

from typing import Any, Optional, Union

from dataclasses import dataclass


@dataclass
class Tab:
    title: str
    widget: Any
    icon: Union[QIcon, str, None] = None
    path: Optional[str] = None
    index: Optional[int] = None

    def is_file(self) -> bool:
        return self.path is not None

    def __post_init__(self) -> None:
        if isinstance(self.icon, str):
            self.icon = QIcon(self.icon)

    def __repr__(self) -> str:
        return f"Tab(title={self.title}, widget={self.widget}, icon={self.icon}, path={self.path}, index={self.index})"


class TabEditor(QTabWidget):
    def __init__(self) -> None:
        super().__init__()

        self.__tabs: list[Tab] = []

        self.setStyleSheet(FileLoader.load_style("scr/widgets/styles/tab_editor.css"))
        self.setObjectName("tab-editor")
        self.setMinimumSize(1040, 480)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setMouseTracking(True)
        self.setIconSize(QSize(16, 16))
        self.tabCloseRequested.connect(self.removeTab)
        self.currentChanged.connect(self.__update_indexes)

    def get_tabs(self) -> list[Tab]:
        return self.__tabs

    def __get_json_info(self) -> dict:
        res = {}

        for i, tab in enumerate(self.__tabs):
            res[str(i)] = {
                "title": tab.title,
                "widget": tab.widget,
                "icon": tab.icon,
                "path": tab.path,
                "index": tab.index
            }

        return res

    def get_info_tabs(self, key: str, only_files: bool = False) -> list:
        res = []
        jsn = self.__get_json_info()

        for tab in jsn.keys():
            if not only_files:
                res.append(jsn[tab][key])

            elif only_files and jsn[tab]["path"] is not None:
                res.append(jsn[tab][key])

        return res

    def check_tab_paths_exist(self) -> None:
        # return self.get_all_info_tabs(True, key="path")

        for i, widget in enumerate(self.get_all_widgets()):
            if hasattr(widget, "get_full_path"):
                if not FileChecker.check_exist(widget.get_full_path()):
                    del self.__tabs[i]
                    self.removeTab(i)

    def update_all_tabs_font(self) -> None:
        for widget in self.get_all_widgets():
            if hasattr(widget, "update_font"):
                widget.update_font()

    def update_all_tabs_settings(self) -> None:
        for widget in self.get_all_widgets():
            if hasattr(widget, "update_settings"):
                widget.update_settings()

    def find_by_path(self, __path: str):
        for widget in self.get_info_tabs(key="widget", only_files=True):
            if widget.get_full_path() == __path:
                return widget

    def get_all_widgets(self) -> list[Any]:
        return [self.widget(i) for i in range(self.count())]

    def get_all_paths(self):
        return self.get_info_tabs(key="path", only_files=True)

    def get_current_path(self) -> str:
        if hasattr(self.currentWidget(), "get_full_path"):
            return self.currentWidget().get_full_path()
        else:
            return ""  # it's need to remove exception

    def __update_indexes(self) -> None:
        for tab in self.__tabs:
            tab.index = self.indexOf(tab.widget)

        self.__tabs.sort(key=lambda t: t.index)

    def removeTab(self, __index: int):
        super().removeTab(__index)
        del self.__tabs[__index]

        if self.count() == 0:
            self.add_tab(Tab("Welcome!", WelcomeScreen(), IconPaths.SystemIcons.WELCOME))

    def add_tab(self, tab: Tab):

        if tab.path is None and hasattr(tab.widget, "get_full_path"):
            tab.path = tab.widget.get_full_path()

        tab.index = len(self.__tabs)

        if tab.path not in self.get_all_paths():
            super().addTab(tab.widget, tab.title)
            self.__tabs.append(tab)
        else:
            self.setCurrentWidget(self.find_by_path(tab.path))

        if tab.icon is not None:
            self.setTabIcon(self.indexOf(tab.widget), tab.icon)
