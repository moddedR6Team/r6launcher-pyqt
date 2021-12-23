from PyQt5 import QtWidgets as qtWidgets, QtCore as qtCore

from r6launcher import Profile


class SettingsDialog(qtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.resize(850, 600)
        self.setWindowTitle("Settings")

        q_btn = qtWidgets.QDialogButtonBox.Apply | qtWidgets.QDialogButtonBox.Discard

        self.buttonBox = qtWidgets.QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.parent_layout = qtWidgets.QVBoxLayout()

        self.layout = qtWidgets.QFormLayout()

        self.darkModeCheckbox = qtWidgets.QCheckBox()
        self.darkModeCheckbox.setChecked(True)
        self.darkModeCheckbox.stateChanged.connect(self.set_light_mode)

        self.layout.addRow("", qtWidgets.QLabel("<h1><b>WIP</b></h1><br>Coming soon"))
        # self.layout.addRow("Dark mode", self.darkModeCheckbox)
        # self.layout.addRow("Setting 2", qtWidgets.QRadioButton())
        # self.layout.addRow("Setting 3", qtWidgets.QDial())

        self.parent_layout.addLayout(self.layout)
        self.parent_layout.addWidget(self.buttonBox)

        self.setLayout(self.parent_layout)

    def set_light_mode(self):
        pass


class NewProfileDialog(qtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.resize(850, 600)
        self.setWindowTitle("Add new profile...")

        q_btn = qtWidgets.QDialogButtonBox.Ok | qtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = qtWidgets.QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

        self.parent_layout = qtWidgets.QVBoxLayout()

        self.layout = qtWidgets.QFormLayout()

        self.profile_name_line_edit = qtWidgets.QLineEdit()
        self.profile_name_line_edit.textChanged.connect(self.change_profile_name)

        self.select_file_button = qtWidgets.QPushButton("Select file...")
        self.select_file_button.clicked.connect(self.open_file)

        self.layout.addRow("Profile Name", self.profile_name_line_edit)
        self.layout.addRow("Startup File", self.select_file_button)

        self.parent_layout.addLayout(self.layout)
        self.parent_layout.addWidget(self.buttonBox)

        self.setLayout(self.parent_layout)

        self.profile_name = ""
        self.exe_path = ""

    def save(self):
        self.accept()
        return_profile = Profile(self.profile_name, self.exe_path)
        return return_profile

    def change_profile_name(self):
        self.profile_name = self.profile_name_line_edit.text()

    @qtCore.pyqtSlot()
    def open_file(self):
        options = qtWidgets.QFileDialog.Options()
        files, _ = qtWidgets.QFileDialog.getOpenFileNames(self, "Select version boot file", "",
                                                          "Siege startup file (*.exe *.bat)", options=options)
        if files:
            print(files)
            self.select_file_button.setText(files[0])
            self.exe_path = files[0]