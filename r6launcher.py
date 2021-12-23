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
import useful_funcs


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

        self.launcher_version = "0.0.2"

        self.logger = custom_log.Logger(".\\logs\\", False)
        self.logger.log(self.logger.INFO, f"R6 Launcher v{self.launcher_version} started")

        self.logger.log(self.logger.INFO, f"Qt version: {qtCore.QT_VERSION_STR}")

        self.is_siege_running = False

        self.check_if_siege_running_timer = qtCore.QTimer()
        self.check_if_siege_running_timer.timeout.connect(self.on_timer_update)
        self.check_if_siege_running_timer.setInterval(500)
        self.check_if_siege_running_timer.start()

        self.resize(650, 400)
        self.setWindowTitle(f"R6 Launcher {self.launcher_version}")

        # If profiles json file doesnt exist, makes a new blank one
        if not os.path.isfile("profiles.json"):
            self.logger.log(self.logger.INFO, "Can't find 'profile.json', creating new one")
            with open("profiles.json", 'w+') as f:
                f.write("{}")

        self.read_json_profiles()

        self.update_app()

        self.showNormal()

    def on_timer_update(self):
        new_status = misc_util.is_siege_running()
        if not new_status == self.is_siege_running:
            self.is_siege_running = misc_util.is_siege_running()
            old_index = self.launcher_page_combo.currentIndex()
            self.button_update_pages()
            self.launcher_page_combo.setCurrentIndex(old_index)

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

        parent_layout = qtWidgets.QHBoxLayout()

        self.left_column_layout = qtWidgets.QVBoxLayout()
        self.left_column_layout.setAlignment(qtCore.Qt.AlignTop)

        self.go_launcher_button = qtWidgets.QPushButton("Launcher")
        self.go_launcher_button.setIcon(qtGui.QIcon(os.path.join("assets", "play_arrow_icon_w.png")))
        self.go_launcher_button.clicked.connect(self.parent_switch_page_launcher)
        self.go_launcher_button.setStyleSheet("QPushButton {text-align:left;}");

        self.go_downloader_button = qtWidgets.QPushButton("Downloader")
        self.go_downloader_button.setIcon(qtGui.QIcon(os.path.join("assets", "download_icon_w.png")))
        self.go_downloader_button.clicked.connect(self.parent_switch_page_downloader)
        self.go_launcher_button.setStyleSheet("QPushButton {text-align:left;}");

        self.go_marketplace_button = qtWidgets.QPushButton("Marketplace")
        self.go_marketplace_button.setIcon(qtGui.QIcon(os.path.join("assets", "shop_icon_w.png")))
        self.go_marketplace_button.clicked.connect(self.parent_switch_page_marketplace)
        self.go_marketplace_button.setStyleSheet("QPushButton {text-align:left;}");

        self.go_settings_button = qtWidgets.QPushButton("Settings")
        self.go_settings_button.setIcon(qtGui.QIcon(os.path.join("assets", "settings_icon_w.png")))
        self.go_settings_button.clicked.connect(self.parent_switch_page_settings)
        self.go_settings_button.setStyleSheet("QPushButton {text-align:left;}");

        self.go_about_button = qtWidgets.QPushButton("About")
        self.go_about_button.setIcon(qtGui.QIcon(os.path.join("assets", "info_icon_w.png")))
        self.go_about_button.clicked.connect(self.parent_switch_page_about)
        self.go_about_button.setStyleSheet("QPushButton {text-align:left;}");

        self.left_column_layout.addWidget(self.go_launcher_button)
        self.left_column_layout.addWidget(self.go_downloader_button)
        self.left_column_layout.addWidget(self.go_marketplace_button)
        self.left_column_layout.addWidget(self.go_settings_button)
        self.left_column_layout.addWidget(self.go_about_button)

        self.parent_stacked_layout = qtWidgets.QStackedLayout()
        parent_layout.addLayout(self.left_column_layout)
        parent_layout.addLayout(self.parent_stacked_layout)
        self.setLayout(parent_layout)

        launcher_layout_page = qtWidgets.QVBoxLayout()

        launcher_page = qtWidgets.QWidget()
        downloader_page = qtWidgets.QWidget()
        marketplace_page = qtWidgets.QWidget()
        settings_page = qtWidgets.QWidget()
        about_page = qtWidgets.QWidget()

        ## LAUCHER SECTION
        self.launcher_page_combo = qtWidgets.QComboBox()
        self.update_check_box()
        self.launcher_page_combo.activated.connect(self.launcher_switch_page)
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
        self.launcher_stackedLayout = qtWidgets.QStackedLayout()
        self.update_page_list()
        self.top_layout = qtWidgets.QHBoxLayout()
        self.top_layout.addWidget(self.launcher_page_combo, 2)
        self.top_layout.addWidget(self.addprofile_button)
        # self.top_layout.addWidget(self.editprofile_button)
        self.top_layout.addWidget(self.deleteprofile_button)
        self.top_layout.addWidget(self.refresh_button)
        # self.top_layout.addWidget(self.settings_button)
        launcher_layout_page.addLayout(self.top_layout)
        launcher_layout_page.addLayout(self.launcher_stackedLayout)
        launcher_page.setLayout(launcher_layout_page)

        # DOWNLOADER SECTION
        downloader_layout_page = qtWidgets.QVBoxLayout()
        downloader_layout_page.addWidget(qtWidgets.QLabel("Downloader Placeholder"))
        downloader_page.setLayout(downloader_layout_page)

        # MARKETPLACE SECTION
        marketplace_layout_page = qtWidgets.QVBoxLayout()
        marketplace_layout_page.addWidget(qtWidgets.QLabel("Marketplace Placeholder"))
        marketplace_page.setLayout(marketplace_layout_page)

        # SETTINGS SECTION
        settings_layout_page = qtWidgets.QVBoxLayout()
        settings_layout_page.addWidget(qtWidgets.QLabel("Settings Placeholders"))
        settings_page.setLayout(settings_layout_page)

        # ABOUT SECTION
        about_layout_page = qtWidgets.QVBoxLayout()
        about_sublayout = qtWidgets.QVBoxLayout()
        about_sublayout.setAlignment(qtCore.Qt.AlignCenter)
        about_label_content = f"""
            <font face=verdana color=white>
            <h1>R6Launcher version version {self.launcher_version}</h1>
            <br>
            <h3>Made by Lungu</h3>
            <h3>Checkout the <a href='https://discord.com/invite/9KByVQXFck'>Modded R6 discord server!<a/></h3>
            </font>
        """
        about_label = qtWidgets.QLabel(about_label_content)
        about_label.setOpenExternalLinks(True)
        about_sublayout.addWidget(about_label)
        about_layout_page.addLayout(about_sublayout)
        about_page.setLayout(about_layout_page)

        self.parent_stacked_layout.addWidget(launcher_page)
        self.parent_stacked_layout.addWidget(downloader_page)
        self.parent_stacked_layout.addWidget(marketplace_page)
        self.parent_stacked_layout.addWidget(settings_page)
        self.parent_stacked_layout.addWidget(about_page)
        self.parent_stacked_layout.setAlignment(qtCore.Qt.AlignLeft | qtCore.Qt.AlignTop)

    @qtCore.pyqtSlot()
    def parent_switch_page_launcher(self):
        self.parent_stacked_layout.setCurrentIndex(0)

    @qtCore.pyqtSlot()
    def parent_switch_page_downloader(self):
        self.parent_stacked_layout.setCurrentIndex(1)

    @qtCore.pyqtSlot()
    def parent_switch_page_marketplace(self):
        self.parent_stacked_layout.setCurrentIndex(2)

    @qtCore.pyqtSlot()
    def parent_switch_page_settings(self):
        self.parent_stacked_layout.setCurrentIndex(3)

    @qtCore.pyqtSlot()
    def parent_switch_page_about(self):
        self.parent_stacked_layout.setCurrentIndex(4)

    def update_check_box(self):
        self.launcher_page_combo.clear()
        if not self.profile_list:
            self.launcher_page_combo.addItem("<Add a new profile to start>")
            self.logger.log(self.logger.INFO, "No profile found, showing '<Add a new profile to start>'")
        for profile in self.profile_list:
            self.launcher_page_combo.addItem(profile.name)
            self.logger.log(self.logger.INFO, f"Added profile {profile.to_string()} to combo box")

    def update_page_list(self):
        self.clear_layout(self.launcher_stackedLayout)
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
            self.launcher_stackedLayout.addWidget(page)

            self.launcher_switch_page()

    def launcher_switch_page(self):
        self.launcher_stackedLayout.setCurrentIndex(self.launcher_page_combo.currentIndex())

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
        current_profile = self.profile_list[self.launcher_page_combo.currentIndex()]
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
            selected_profile = self.profile_list[self.launcher_page_combo.currentIndex()]

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
