import json, os


class Setting:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def update(self, new_value):
        self.value = new_value

    def read(self):
        return self.value

    def get_json(self):
        return [self.name, self.value]


class BooleanSetting(Setting):
    def __init__(self, name, value):
        super().__init__(name, value)

    def update(self, value):
        if type(value) == bool:
            self.value = value

    def get_json(self):
        return [self.name, "True" if self.value else "False"]


class IntSetting(Setting):
    def __init__(self, name, value):
        super().__init__(name, value)

    def update(self, new_value):
        self.value = new_value

    def get_json(self):
        return [self.name, str(self.value)]


class StringSetting(Setting):
    def __init__(self, name, value):
        super().__init__(name, value)

    def get_json(self):
        return [self.name, self.value]


class SetStringSetting(Setting):
    def __init__(self, name, value, possible_values):
        super().__init__(name, value)

        self.possible_values = possible_values

    def update(self, new_value):
        if new_value in self.possible_values:
            self.value = new_value

    def get_json(self):
        return [self.name, self.value]


class SettingsManager:
    def __init__(self):
        self.default_settings = []

        dark_mode_setting = BooleanSetting("dark_mode", True)

        self.default_settings.append(["Boolean", dark_mode_setting])

        self.settings_list = []

        if not os.path.isfile("settings.json") or open("settings.json", 'r').read() == "{}":
            self.write_settings_first_time()

        self.read_settings_file()

    def write_settings_first_time(self):
        settings_dict = {}

        for setting in self.default_settings:
            setting_type = setting[0]
            setting_instance = setting[1]
            settings_dict[setting_instance.get_json()[0]] = {"type": setting_type,
                                                             "value": setting_instance.get_json()[1]}

        with open("settings.json", 'w+') as f:
            f.write(json.dumps(settings_dict))

    def read_settings_file(self):
        self.settings_list = {}
        switch_case_type = {
            "Boolean": BooleanSetting,
            "String": StringSetting,
            "SetString": SetStringSetting,
            "Int": IntSetting
        }
        with open("settings.json", 'r') as f:
            json_sett = json.loads(f.read())
            for setting in json_sett:
                setting_type = json_sett[setting]["type"]
                if setting_type == "Boolean":
                    self.settings_list[setting] = [json_sett[setting]["type"],
                                                   BooleanSetting(setting, json_sett[setting]["value"])]
                elif setting_type == "String":
                    self.settings_list[setting] = [json_sett[setting]["type"],
                                                   StringSetting(setting, json_sett[setting]["value"])]
                elif setting_type == "SetString":
                    self.settings_list[setting] = [json_sett[setting]["type"],
                                                   SetStringSetting(setting, json_sett[setting]["value"])]
                elif setting_type == "Int":
                    self.settings_list[setting] = [json_sett[setting]["type"],
                                                   IntSetting(setting, json_sett[setting]["value"])]
                else:
                    self.settings_list[setting] = [json_sett[setting]["type"],
                                                   Setting(setting, json_sett[setting]["value"])]

    def update_setting(self, index, new_value):
        print(self.settings_list)
        self.settings_list[index][1].update(new_value)

        settings_dict = {}
        for setting in self.settings_list:
            settings_dict[self.settings_list[setting][1].name] = {"type": self.settings_list[setting][0],
                                                                  "value": self.settings_list[setting][1].value}

        with open("settings.json", 'w+') as f:
            f.write(json.dumps(settings_dict, indent=4))

    def read_setting(self, index):
        return self.settings_list[index][1].value
