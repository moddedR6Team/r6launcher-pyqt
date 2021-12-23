def folder_to_string(folder_name):
    folder_to_string_dict = {
        "Vanilla": "Vanilla",
        "BlackIce": "Black Ice",
        "SkullRain": "Skull Rain",
        "RedCrow": "Red Crow",
        "VelvetShell": "Velvet Shell",
        "Health": "Health",
        "BloodOrchid": "Blood Orchid",
        "WhiteNoise": "White Noise",
        "Chimera": "Chimera",
        "Parabellum": "Parabellum",
        "GrimSky": "Grim Sky",
        "WindBastion": "Wind Bastion",
        "BurntHorizon": "Burnt Horizon",
        "PhantomSight": "Phantom Sight",
        "EmberRise": "Ember Rise",
        "ShiftingTides": "Shifting Tides",
        "VoidEdge": "Void Edge",
        "SteelWave": "Steel Wave",
        "ShadowLegacy": "Shadow Legacy",
        "NeonDawn": "Neon Dawn",
        "CrimsonHeist": "Crimson Heist",
        "NorthStar": "North Star",
        "CrystalGuard": "Crystal Guard",
        "HighCalibre": "High Calibre"
    }
    if folder_name in folder_to_string_dict.keys():
        return folder_to_string_dict[folder_name]
    else:
        return ""