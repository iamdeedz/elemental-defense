from constants import screen_width, screen_height

base_waypoints = [(1145, 62),
                  (1136, 77),
                  (1117, 99),
                  (1087, 119),
                  (1050, 147),
                  (1024, 159),
                  (1002, 164),
                  (923, 182),
                  (645, 179),
                  (606, 175),
                  (578, 178),
                  (545, 190),
                  (530, 207),
                  (512, 238),
                  (521, 362),
                  (542, 395),
                  (564, 406),
                  (596, 417),
                  (617, 425),
                  (647, 433),
                  (675, 434),
                  (1027, 453),
                  (1152, 483),
                  (1241, 527),
                  (1297, 573),
                  (1310, 611),
                  (1319, 676),
                  (1310, 726),
                  (1283, 756),
                  (1245, 776),
                  (1213, 801),
                  (1164, 822),
                  (1116, 834),
                  (1084, 844),
                  (1059, 846),
                  (922, 859),
                  (856, 867),
                  (668, 875),
                  (514, 900),
                  (377, 994),
                  (331, 1072)]

percentages = []
for waypoint in base_waypoints:
    percentages.append((waypoint[0] / 1920, waypoint[1] / 1080))

waypoints = []
for percentage in percentages:
    waypoints.append((percentage[0] * screen_width, percentage[1] * screen_height))
