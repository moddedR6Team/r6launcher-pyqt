import json
import sys
import os
import subprocess
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtGui as qtGui
import PyQt5.QtCore as qtCore
import qdarkstyle

import settings_manager
import misc_util
import custom_dialogs
import custom_log


class Profile:
    def __init__(self, name, exe_path):
        self.name = name
        self.exe_path = exe_path
        self.arguments = str

    def to_string(self):
        return f"Profile '{self.name}' - Path: '{self.exe_path}'"

class MainWindow(qtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.logger = custom_log.Logger(".\\logs\\", False)
        self.logger.log(self.logger.INFO, "R6 Launcher started")

        self.logger.log(self.logger.INFO, f"Qt version: {qtCore.QT_VERSION_STR}")

        self.is_siege_running = False

        self.check_if_siege_running_timer = qtCore.QTimer()
        self.check_if_siege_running_timer.timeout.connect(self.on_timer_update)
        self.check_if_siege_running_timer.setInterval(500)
        self.check_if_siege_running_timer.start()

        self.auto_refresh_timer = qtCore.QTimer()
        self.auto_refresh_timer.timeout.connect(self.button_update_pages)
        self.auto_refresh_timer.setInterval(10000)
        self.auto_refresh_timer.start()

        self.resize(650, 400)
        self.setWindowTitle("R6 Launcher Alpha")

        # If profiles json file doesnt exist, makes a new blank one
        if not os.path.isfile("profiles.json"):
            self.logger.log(self.logger.INFO, "Can't find 'profile.json', creating new one")
            with open("profiles.json", 'w+') as f:
                f.write("{}")

        self.read_json_profiles()

        self.game_running = False

        self.update_app()

        self.showNormal()

    def on_timer_update(self):
        new_status = misc_util.is_siege_running()
        if not new_status == self.is_siege_running:
            self.is_siege_running = misc_util.is_siege_running()
            self.button_update_pages()

    def __del__(self):
        self.logger.log(self.logger.INFO, "Closing R6 Launcher")

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
            self.logger.log(self.logger.INFO, "Cleared layout")
        else:
            self.logger.log(self.logger.INFO, "Layout empty, skipped clearing")

    def read_json_profiles(self):
        self.profile_list = []
        self.logger.log(self.logger.INFO, "Reading profiles from 'profile.json'")
        with open("profiles.json", 'r') as f:
            profiles_json_content = json.loads(f.read())
            for profile in profiles_json_content:
                p_content = profiles_json_content[profile]
                new_profile = Profile(profile, p_content["exe_path"])
                self.profile_list.append(new_profile)
                self.logger.log(self.logger.INFO, f"Loaded {new_profile.to_string()}")

    def update_app(self):
        layout = qtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.page_combo = qtWidgets.QComboBox()
        self.update_check_box()
        self.page_combo.activated.connect(self.switch_page)

        self.addprofile_button = qtWidgets.QPushButton()
        self.addprofile_button.setIcon(qtGui.QIcon(os.path.join("assets", "add_icon_w")))
        self.addprofile_button.clicked.connect(self.button_new_profile)

        self.editprofile_button = qtWidgets.QPushButton()
        self.editprofile_button.setIcon(qtGui.QIcon(os.path.join("assets", "edit_icon_w")))
        self.editprofile_button.clicked.connect(self.button_wip_function)

        self.deleteprofile_button = qtWidgets.QPushButton()
        self.deleteprofile_button.setIcon(qtGui.QIcon(os.path.join("assets", "delete_icon_w")))
        self.deleteprofile_button.clicked.connect(self.button_delete_profile)

        self.settings_button = qtWidgets.QPushButton()
        self.settings_button.setIcon(qtGui.QIcon(os.path.join("assets", "settings_icon_w")))
        self.settings_button.clicked.connect(self.button_open_settings)

        self.refresh_button = qtWidgets.QPushButton()
        self.refresh_button.setIcon(qtGui.QIcon(os.path.join("assets", "refresh_icon_w")))
        self.refresh_button.clicked.connect(self.button_update_pages)

        self.stackedLayout = qtWidgets.QStackedLayout()

        self.pages_list = []
        self.update_page_list()

        self.top_layout = qtWidgets.QHBoxLayout()

        self.top_layout.addWidget(self.page_combo, 2)
        self.top_layout.addWidget(self.addprofile_button)
        # self.top_layout.addWidget(self.editprofile_button)
        self.top_layout.addWidget(self.deleteprofile_button)
        self.top_layout.addWidget(self.refresh_button)
        self.top_layout.addWidget(self.settings_button)

        layout.addLayout(self.top_layout)
        layout.addLayout(self.stackedLayout)

    def update_check_box(self):
        self.page_combo.clear()
        if not self.profile_list:
            self.page_combo.addItem("<Add a new profile to start>")
            self.logger.log(self.logger.INFO, "No profile found, showing '<Add a new profile to start>'")
        for profile in self.profile_list:
            self.page_combo.addItem(profile.name)
            self.logger.log(self.logger.INFO, f"Added profile {profile.to_string()} to combo box")

    def update_page_list(self):
        self.pages_list = []
        self.clear_layout(self.stackedLayout)
        for profile in self.profile_list:
            page = qtWidgets.QWidget()

            page_layout_top = qtWidgets.QVBoxLayout()

            self.test_label = qtWidgets.QLabel("Test")
            page_layout_top.addWidget(self.test_label)

            # page_layout_top.addWidget(qtWidgets.QLabel(f"Profile index: {self.page_combo.currentIndex()}"))
            # page_layout_top.addWidget(qtWidgets.QLabel("<b>*image of the season here*</b>"))
            page_layout_top.addWidget(qtWidgets.QLabel(f"Profile Name: {profile.name}"))
            siege_folder = os.path.dirname(os.path.realpath(profile.exe_path))
            page_layout_top.addWidget(qtWidgets.QLabel(f"Path: {siege_folder}"))
            size = 0
            for element in os.scandir(siege_folder):
                size += os.path.getsize(element)
            page_layout_top.addWidget(qtWidgets.QLabel(f"Size: {misc_util.pretty_string_size(size)}"))

            self.logger.log(self.logger.INFO, f"Showing profile {profile.to_string()}")

            # self.stackedLayout.setCurrentIndex(self.page_combo.currentIndex())
            page_layout_parent = qtWidgets.QVBoxLayout()
            page_layout_parent.addStretch(1)

            play_button = qtWidgets.QPushButton("Stop" if self.is_siege_running else "Play")
            if self.is_siege_running:
                play_button.clicked.connect(misc_util.kill_r6)
            else:
                play_button.clicked.connect(self.on_click_play_siege)

            page_layout_parent.addLayout(page_layout_top)
            page_layout_parent.addWidget(play_button)

            page.setLayout(page_layout_parent)

            self.pages_list.append(page)
            self.stackedLayout.addWidget(page)

            self.switch_page()

    def switch_page(self):
        self.stackedLayout.setCurrentIndex(self.page_combo.currentIndex())

    def add_profile_json(self, _new_profile):
        self.profile_list = []

        with open("profiles.json", 'r') as f:
            profiles_json_content = json.loads(f.read())
            for profile in profiles_json_content:
                p_content = profiles_json_content[profile]
                new_profile = Profile(profile, p_content["exe_path"])
                self.profile_list.append(new_profile)
        self.profile_list.append(_new_profile)
        self.logger.log(self.logger.INFO, f"Added new profile {_new_profile.to_string()}")

        serializable_profile_dict = {}
        for profile in self.profile_list:
            serializable_profile_dict[profile.name] = {"exe_path": profile.exe_path}

        with open("profiles.json", 'w+') as f:
            f.write(json.dumps(serializable_profile_dict, indent=4))

        self.button_update_pages()

    @qtCore.pyqtSlot()
    def button_update_pages(self):
        self.read_json_profiles()
        self.update_check_box()
        self.update_page_list()
        self.logger.log(self.logger.INFO, "Refreshed launcher")

    @qtCore.pyqtSlot()
    def on_click_play_siege(self):
        current_profile = self.profile_list[self.page_combo.currentIndex()]
        self.logger.log(self.logger.INFO, f"Playing Siege, profile {current_profile.to_string()}")
        subprocess.Popen([current_profile.exe_path, "/belaunch"], creationflags=subprocess.CREATE_NEW_CONSOLE)

    @qtCore.pyqtSlot()
    def button_new_profile(self):
        dlg = custom_dialogs.NewProfileDialog()
        if dlg.exec():
            new_profile = dlg.save()
            if new_profile.name and new_profile.exe_path:
                self.add_profile_json(new_profile)
            else:
                self.logger.log(self.logger.ERROR, "Given wrong information, new profile not added")

    @qtCore.pyqtSlot()
    def button_open_settings(self):
        dlg = custom_dialogs.SettingsDialog()
        if dlg.exec():
            self.logger.log(self.logger.ERROR, "Settings opened")
        else:
            self.logger.log(self.logger.ERROR, "Settings opened")

    @qtCore.pyqtSlot()
    def button_delete_profile(self):
        if self.profile_list:
            selected_profile = self.profile_list[self.page_combo.currentIndex()]

            messagebox = qtWidgets.QMessageBox.question(self, 'Are you sure',
                                                        f"Delete profile \"{selected_profile.name}\"?",
                                                        qtWidgets.QMessageBox.Yes | qtWidgets.QMessageBox.No,
                                                        qtWidgets.QMessageBox.No)
            if messagebox == qtWidgets.QMessageBox.Yes:
                self.profile_list.remove(selected_profile)
                self.logger.log(self.logger.ERROR, f"Removed profile {selected_profile.to_string()}")

                serializable_profile_dict = {}
                for profile in self.profile_list:
                    serializable_profile_dict[profile.name] = {"exe_path": profile.exe_path}

                with open("profiles.json", 'w+') as f:
                    f.write(json.dumps(serializable_profile_dict, indent=4))

                self.button_update_pages()

    @qtCore.pyqtSlot()
    def button_wip_function(self):
        dlg = qtWidgets.QDialog(self)
        dlg.setWindowTitle("WIP")
        dlg.resize(300, 300)
        layout = qtWidgets.QVBoxLayout()
        layout.addWidget(qtWidgets.QLabel("<b>WIP</b><br>This button still isn't working"))
        dlg.setLayout(layout)
        dlg.exec()


SETTINGS_MANAGER = settings_manager.SettingsManager()


class R6Launcher(qtWidgets.QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        ex = MainWindow()
        ex.show()
        sys.exit(self.exec_())


def main():
    os.environ['QT_API'] = 'pyqt5'
    app = R6Launcher()


if __name__ == '__main__':
    main()
