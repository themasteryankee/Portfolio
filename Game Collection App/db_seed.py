import sqlite3

game_list = [
    {"name": "Resident Evil 5",
     "consoles": [("Playstation 3", "images/re5/resident_evil_5_ps3.jpg", 2009, "In this installment of the Resident Evil "
                                                                            "franchise, play as Chris to advert the next "
                                                                            "viral outbreak! Enjoy the action packed "
                                                                            "adventure as Chris and his new partner "
                                                                            "Sheva defeat stronger, meaner, and smarter, enemies!"),
                  ("Xbox 360", "images/re5/resident_evil_5_360.png", 2009, "In this installment of the Resident Evil "
                                                                       "franchise, play as Chris to advert the next "
                                                                       "viral outbreak! Enjoy the action packed "
                                                                       "adventure as Chris and his new partner "
                                                                       "Sheva defeat stronger, meaner, and smarter, enemies!"),
                  ("PC", "images/re5/resident_evil_5_pc.jpg", 2009, "In this installment of the Resident Evil "
                                                                "franchise, play as Chris to advert the next "
                                                                "viral outbreak! Enjoy the action packed "
                                                                "adventure as Chris and his new partner "
                                                                "Sheva defeat stronger, meaner, and smarter, enemies!"),
                  ("Playstation 4", "images/re5/resident_evil_5_ps4.jpg", 2016, "In this installment of the Resident Evil "
                                                                            "franchise, play as Chris to advert the next "
                                                                            "viral outbreak! Enjoy the action packed "
                                                                            "adventure as Chris and his new partner "
                                                                            "Sheva defeat stronger, meaner, and smarter, enemies!"),
                  ("Nintendo Switch", "images/re5/resident_evil_5_switch.jpg", 2019, "In this installment of the Resident Evil "
                                                                            "franchise, play as Chris to advert the next "
                                                                            "viral outbreak! Enjoy the action packed "
                                                                            "adventure as Chris and his new partner "
                                                                            "Sheva defeat stronger, meaner, and smarter, enemies!"),
                  ("Xbox One", "images/re5/resident_evil_5_x1.jpg", 2016, "In this installment of the Resident Evil "
                                                                            "franchise, play as Chris to advert the next "
                                                                            "viral outbreak! Enjoy the action packed "
                                                                            "adventure as Chris and his new partner "
                                                                            "Sheva defeat stronger, meaner, and smarter, enemies!")]},

    {"name": "Resident Evil 4",
     "consoles": [("Playstation 2", "images/re4/resident_evil_4_ps2.png", 2005, "Play through this industry-changing title "
                                                                            "as fan-favorite character Leon S. Kennedy. "
                                                                            "On a mission to save the President's Daughter, "
                                                                            "Leon will face many challenges brought about "
                                                                            "by an infected community. This action-horror "
                                                                            "title is packed to the brim with secrets and "
                                                                            "non-stop thrills! In this version, there "
                                                                            "is an extra unlockable available not seen in "
                                                                            "some other versions of the PyScape."),
                  ("Nintendo Wii", "images/re4/resident_evil_4_wii.jpg", 2007, "This time in HD, play through this industry-changing title "
                                                                           "as fan-favorite character Leon S. Kennedy. "
                                                                           "On a mission to save the President's Daughter, "
                                                                           "Leon will face many challenges brought about "
                                                                           "by an infected community. This action-horror "
                                                                           "title is packed to the brim with secrets and "
                                                                           "non-stop thrills! In this version, there "
                                                                           "is an extra unlockable available not seen in "
                                                                           "some other versions of the PyScape, as well as "
                                                                           "the ability to use motion controls!"),
                  ("PC", "images/re4/resident_evil_4_pc.jpg", 2007, "Play through this industry-changing title "
                                                                "as fan-favorite character Leon S. Kennedy. "
                                                                "On a mission to save the President's Daughter, "
                                                                "Leon will face many challenges brought about "
                                                                "by an infected community. This action-horror "
                                                                "title is packed to the brim with secrets and "
                                                                "non-stop thrills! In this version, there "
                                                                "is an extra unlockable available not seen in "
                                                                "some other versions of the PyScape."),
                  ("Nintendo GameCube", "images/re4/resident_evil_4_gc.jpg", 2005, "Play through this industry-changing title "
                                                                               "as fan-favorite character Leon S. Kennedy. "
                                                                               "On a mission to save the President's Daughter, "
                                                                               "Leon will face many challenges brought about "
                                                                               "by an infected community. This action-horror "
                                                                               "title is packed to the brim with secrets and "
                                                                               "non-stop thrills!"),
                  ("Playstation 4", "images/re4/resident_evil_4_ps4.jpg", 2014, "This time in HD, play through this industry-changing title "
                                                                            "as fan-favorite character Leon S. Kennedy. "
                                                                            "On a mission to save the President's Daughter, "
                                                                            "Leon will face many challenges brought about "
                                                                            "by an infected community. This action-horror "
                                                                            "title is packed to the brim with secrets and "
                                                                            "non-stop thrills!"),
                  ("Xbox One", "images/re4/resident_evil_4_x1.png", 2014,
                   "This time in HD, play through this industry-changing title "
                   "as fan-favorite character Leon S. Kennedy. "
                   "On a mission to save the President's Daughter, "
                   "Leon will face many challenges brought about "
                   "by an infected community. This action-horror "
                   "title is packed to the brim with secrets and "
                   "non-stop thrills!")]},

    {"name": "Resident Evil 4: Ultimate HD Edition",
     "consoles": [("PC", "images/re4/resident_evil_4_hd_pc.jpeg", 2014,
                   "This time in HD, play through this industry-changing title "
                   "as fan-favorite character Leon S. Kennedy. "
                   "On a mission to save the President's Daughter, "
                   "Leon will face many challenges brough about "
                   "by an infected community. This action-horror "
                   "title is packed to the brim with secrets and "
                   "non-stop thrills!")]},

    {"name": "Resident Evil 4 HD",
     "consoles": [("Playstation 3", "images/re4/resident_evil_4_ps3.png", 2011, "This time in HD, play through this industry-changing title "
                                                                            "as fan-favorite character Leon S. Kennedy. "
                                                                            "On a mission to save the President's Daughter, "
                                                                            "Leon will face many challenges brought about "
                                                                            "by an infected community. This action-horror "
                                                                            "title is packed to the brim with secrets and "
                                                                            "non-stop thrills!"),
                  ("Xbox 360", "images/re4/resident_evil_4_360.jpg", 2011,
                   "This time in HD, play through this industry-changing title "
                   "as fan-favorite character Leon S. Kennedy. "
                   "On a mission to save the President's Daughter, "
                   "Leon will face many challenges brought about "
                   "by an infected community. This action-horror "
                   "title is packed to the brim with secrets and "
                   "non-stop thrills!"),
                  ("Nintendo Switch", "images/re4/resident_evil_4_switch.jpg", 2019,
                   "This time in HD and on the go, play through "
                   "this industry-changing title "
                   "as fan-favorite character Leon S. Kennedy. "
                   "On a mission to save the President's Daughter, "
                   "Leon will face many challenges brought about "
                   "by an infected community. This action-horror "
                   "title is packed to the brim with secrets and "
                   "non-stop thrills!")]},
    {"name": "Resident Evil 5: Gold Edition",
     "consoles": [("Playstation 3", "images/re5/resident_evil_5_gold_ps3.jpg", 2010, "In this installment of the Resident Evil "
                                                                            "franchise, play as Chris to advert the next "
                                                                            "viral outbreak! Enjoy the action packed "
                                                                            "adventure as Chris and his new partner "
                                                                            "Sheva defeat stronger, meaner, and smarter, enemies!\n"
                                                                            "Resident Evil 5: Gold Edition also includes "
                                                                            "all downloadable content available. This includes "
                                                                            "costumes, new episodes, and more!"),
                  ("Xbox 360", "images/re5/resident_evil_5_gold_360.jpg", 2010, "In this installment of the Resident Evil "
                                                                            "franchise, play as Chris to advert the next "
                                                                            "viral outbreak! Enjoy the action packed "
                                                                            "adventure as Chris and his new partner "
                                                                            "Sheva defeat stronger, meaner, and smarter, enemies!\n"
                                                                            "Resident Evil 5: Gold Edition also includes "
                                                                            "all downloadable content available. This includes "
                                                                            "costumes, new episodes, and more!"),
                  ("PC", "images/re5/resident_evil_5_gold_pc.png", 2015, "In this installment of the Resident Evil "
                                                                            "franchise, play as Chris to advert the next "
                                                                            "viral outbreak! Enjoy the action packed "
                                                                            "adventure as Chris and his new partner "
                                                                            "Sheva defeat stronger, meaner, and smarter, enemies!\n"
                                                                            "Resident Evil 5: Gold Edition also includes "
                                                                            "all downloadable content available. This includes "
                                                                            "costumes, new episodes, and more!")]},
    {"name": "Resident Evil",
     "consoles": [("Nintendo GameCube", "images/re/resident_evil_gc.jpg", 2002, "During a terrible and horrific epidemic, "
                                                                                "uncover the secrets of whats truly going on. "
                                                                                "This horror experience will introduce you to "
                                                                                "a skin crawling franchise with intense "
                                                                                "moments filled with puzzles, action, and "
                                                                                "intense story-telling!"),
                  ("PC", "images/re/resident_evil_pc.png", 1996, "During a terrible and horrific epidemic, "
                                                                 "uncover the secrets of whats truly going on. "
                                                                 "This horror experience will introduce you to "
                                                                 "a skin crawling franchise with intense "
                                                                 "moments filled with puzzles, action, and "
                                                                 "intense story-telling!"),
                  ("Sega Saturn", "images/re/resident_evil_ss.jpg", 1997, "During a terrible and horrific epidemic, "
                                                                          "uncover the secrets of whats truly going on. "
                                                                          "This horror experience will introduce you to "
                                                                          "a skin crawling franchise with intense "
                                                                          "moments filled with puzzles, action, and "
                                                                          "intense story-telling!"),
                  ("Playstation", "images/re/resident_evil_ps.jpg", 1996, "During a terrible and horrific epidemic, "
                                                                          "uncover the secrets of whats truly going on. "
                                                                          "This horror experience will introduce you to "
                                                                          "a skin crawling franchise with intense "
                                                                          "moments filled with puzzles, action, and "
                                                                          "intense story-telling!"),
                  ("Nintendo GameBoy Color", "images/re/resident_evil_gbc.jpg", 2001,
                   "Now on the go, during a terrible and horrific epidemic, "
                   "you can uncover the secrets of whats truly going on. "
                   "This horror experience will introduce you to "
                   "a skin crawling franchise with intense "
                   "moments filled with puzzles, action, and "
                   "intense story-telling!"),
                  ("Xbox 360", "images/re/resident_evil_360.jpg", 2015, "During a terrible and horrific epidemic, "
                                                                        "uncover the secrets of whats truly going on. "
                                                                        "This horror experience will introduce you to "
                                                                        "a skin crawling franchise with intense "
                                                                        "moments filled with puzzles, action, and "
                                                                        "intense story-telling!")]},
    {"name": "Resident Evil 2",
     "consoles": [("Sega Dreamcast", "images/re2/resident_evil_2_dc.jpg", 1998, "Introducing Leon Kennedy, and Claire Redfield, "
                                                                                "explore the Raccoon City Police Department "
                                                                                "as the city is overrun with the undead. "
                                                                                "Solve puzzles, explore, and strategize while "
                                                                                "surviving through the horrors each room has "
                                                                                "to offer!"),
                  ("Nintendo 64", "images/re2/resident_evil_2_n64.jpg", 1999,
                   "Introducing Leon Kennedy, and Claire Redfield, "
                   "explore the Raccoon City Police Department "
                   "as the city is overrun with the undead. "
                   "Solve puzzles, explore, and strategize while "
                   "surviving through the horrors each room has "
                   "to offer!"),
                  ("Nintendo GameCube", "images/re2/resident_evil_2_gc.jpg", 2003,
                   "Introducing Leon Kennedy, and Claire Redfield, "
                   "explore the Raccoon City Police Department "
                   "as the city is overrun with the undead. "
                   "Solve puzzles, explore, and strategize while "
                   "surviving through the horrors each room has "
                   "to offer!"),
                  ("Playstation", "images/re2/resident_evil_ps.jpg", 1998,
                   "Introducing Leon Kennedy, and Claire Redfield, "
                   "explore the Raccoon City Police Department "
                   "as the city is overrun with the undead. "
                   "Solve puzzles, explore, and strategize while "
                   "surviving through the horrors each room has "
                   "to offer!"),
                  ("PC", "images/re2/resident_evil_2_pc.jpg", 1998, "Introducing Leon Kennedy, and Claire Redfield, "
                                                                    "explore the Raccoon City Police Department "
                                                                    "as the city is overrun with the undead. "
                                                                    "Solve puzzles, explore, and strategize while "
                                                                    "surviving through the horrors each room has "
                                                                    "to offer!")]},
    {"name": "Resident Evil 2: Dual Shock Version",
     "consoles": [("Playstation 2", "images/re2/resident_evil_2_ps_dual.jpg", 1998,
                   "Introducing Leon Kennedy, and Claire Redfield, "
                   "explore the Raccoon City Police Department "
                   "as the city is overrun with the undead. "
                   "Solve puzzles, explore, and strategize while "
                   "surviving through the horrors each room has "
                   "to offer with new Dual Shock support!")]},
    {"name": "Resident Evil 3: Nemesis",
     "consoles": [("PC", "images/re3/resident_evil_3_pc.jpg", 2000, "Tie in the events that have taken place "
                                                                    "in Racoon City in this whole new experience! "
                                                                    "With new enemies and new areas to explore, "
                                                                    "you'll find yourself facing this horror title "
                                                                    "with excitement as you unravel the happenings "
                                                                    "related to the T-Virus!"),
                  ("Playstation", "images/re3/resident_evil_3_ps.jpg", 1998, "Tie in the events that have taken place "
                                                                             "in Racoon City in this whole new experience! "
                                                                             "With new enemies and new areas to explore, "
                                                                             "you'll find yourself facing this horror title "
                                                                             "with excitement as you unravel the happenings "
                                                                             "related to the T-Virus!"),
                  ("Sega Dreamcast", "images/re3/resident_evil_3_dc.jpg", 2000,
                   "Tie in the events that have taken place "
                   "in Racoon City in this whole new experience! "
                   "With new enemies and new areas to explore, "
                   "you'll find yourself facing this horror title "
                   "with excitement as you unravel the happenings "
                   "related to the T-Virus!"),
                  ("Nintendo GameCube", "images/re3/resident_evil_3_gc.jpg", 2003,
                   "Tie in the events that have taken place "
                   "in Racoon City in this whole new experience! "
                   "With new enemies and new areas to explore, "
                   "you'll find yourself facing this horror title "
                   "with excitement as you unravel the happenings "
                   "related to the T-Virus!")]}
    ]

connection = sqlite3.connect("userdata.db")
cursor = connection.cursor()

for game in game_list:
    cursor.execute("INSERT INTO Games (name) VALUES (?)",
                   (game["name"],))
    game_id = cursor.lastrowid

    for console_name, box_art_path, release_year, description in game["consoles"]:
        cursor.execute("SELECT id FROM Consoles WHERE console_name = ?", (console_name,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO Consoles (console_name) VALUES (?)", (console_name,))
            console_id = cursor.lastrowid
        else:
            console_id = result[0]

        cursor.execute("INSERT INTO GameConsoles (game_id, console_id,"
                       "box_art, release_year, description) VALUES (?, ?, ?, ?, ?)",
                       (game_id, console_id, box_art_path, release_year, description))

connection.commit()
connection.close()
print("Finished Seeding")