# Define monitor regions for camera 2
camera2_monitor_regions = [
    (415, 495, 205, 365),  # Monitor 1
    (420, 448, 800, 913),  # Monitor 2
    (330, 346, 481, 561),  # Monitor 3
    (376, 397, 738, 824),  # Monitor 4
    (350, 365, 683, 765),  # Monitor 5
    (329, 341, 653, 722),  # Monitor 6
    (366, 401, 298, 419)   # Monitor 2 For Camera 1
]

# Define workstation regions for camera 2
camera2_workstation_regions = [
    (409, 537, 212, 387),  # Workstation 1
    (419, 538, 802, 954),  # Workstation 2
    (324, 349, 486, 572),  # Workstation 3
    (369, 435, 728, 863),  # Workstation 4
    (349, 377, 700, 778),  # Workstation 5
    (327, 353, 664, 733)   # Workstation 6
]

# Define monitor regions for camera 1
camera1_monitor_regions = [
    (431, 485, 340, 425),  # Monitor 1
    (386, 420, 495, 586),  # Monitor 3
    (350, 378, 495, 560),  # Monitor 4
    (364, 400, 587, 670),  # Monitor 5
    (340, 360, 565, 626)   # Monitor 6
]

# Define workstation regions for camera 1
camera1_workstation_regions = [
    (410, 539, 311, 440),  # Workstation 1
    (346, 426, 346, 460),  # Workstation 2
    (374, 539, 474, 582),  # Workstation 3
    (337, 382, 484, 559),  # Workstation 4
    (360, 418, 579, 673),  # Workstation 5
    (334, 362, 559, 623)   # Workstation 6
]

# Define the workstation coordinates for camera 1
workstation_coordinates_camera1 = [
    [311, 410, 440, 539],
    [346, 346, 460, 426],
    [474, 374, 582, 539],
    [484, 337, 559, 382],
    [579, 360, 673, 418],
    [559, 334, 623, 362]
]

# Define the workstation coordinates for camera 2
workstation_coordinates_camera2 = [
    [212, 409, 387, 537],
    [802, 419, 954, 538],
    [486, 324, 572, 349],
    [728, 369, 863, 435],
    [700, 349, 778, 377],
    [664, 327, 733, 353]
]

# Define the camera and monitor variables as dictionaries
camera1_monitor_variables = {
    "Monitor 1": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 2": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 3": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 4": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 5": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 6": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0}
}

camera2_monitor_variables = {
    "Monitor 1": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 2": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 3": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 4": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 5": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0},
    "Monitor 6": {"On - Person": 0, "On - No Person": 0, "Off - Person": 0}
}

camera1_monitor_isBusy = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}
camera2_monitor_isBusy = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False}