import logging
import json
import os

bot = None

if not os.path.isdir("./assets"):
    os.mkdir("./assets")
if not os.path.isdir("./templates"):
    os.mkdir("./templates")
# creating files. made with
# https://github.com/DaCoolOne/DumbIdeas/tree/main/reddit_ph_compressor
# so as not to make 98210742197421984 lines of stuff
b = 'E͉͔͈͗̀͏̴͎͔͍͔͓͉͎͈͔͍͓͉͉͉͔̜̤̯̣̹̰̥͈͔͍̞̜͈͔͍̞̜͓͔͙̞͐̈̂̎̏͐͌́̏̈́̎͌̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀͆͌̎͗͒̈̂̂̂́̀͌ͯ͌ͯ͌ͯ͂͘̚ͅͅͅͅͅͅͅͅ͏͙͈͔͍̈́̌̀͌̀͛ͯ̀̀͆͏̛͎͔͍͉͙͉͓͎͓͓͉͔̍͆́͌̀́͒́͌̌̀́̍͒͆ͯͯ́͂͌̀͛ͯ̀̀͆̚͝ͅͅ͏̛͎͔͍͉͙͉͓͎͓͓͉̍͆́͌̀́͒́͌̌̀́̍͒͆ͯ̀̀͂̚ͅ͏͒̈́͒̍̓ͅ͏͓͌͌́͐̀̓̚ͅ͏̛̛͓͉͔͈͔͔͈͌͌́͐ͯ̀̀͗̈́̀̑̐̐̅ͯͯͯ̈́̌̀̀͛ͯ̀̀͂̚͝ͅ͏͓͒̈́͒̀̑͐̀̚͘ͅ͏̛̛̛͉͔͔͉͇͎͔͉͎͇̘͔͎͔͈͈͉͖͎͇͌̈́̀̃̈́̈́̈́̈́̈́̈́ͯ̀̀̍́͌̀͌͆ͯ̀̀͐́̈́̈́̀͐ͯͯͯ͒̍̓͌̈́̈̉̀͛ͯ̀̀͂́̓͋͒͘̚̚͘̚͝ͅͅͅͅ͏͕͎̈́̍̓͏͌͏̛̛̛͉͎͕͔͍͇͉͎͍͇͉͎̜͓͔͙̞̜͓͉͔̞͕͎͔͉͒̀̃̈́̈́̈́̈́̈́̈́ͯͯͯ͐̀͛ͯ̀̀́͒̀̒͐̀̐ͯͯͯ́̀͛ͯ̀̀́͒̀͐̀̐ͯͯ̏͌ͯ̓͒͐ͯ͆̓̚̚͘̚̕͘͝͝͝ͅ͏͎͓͎͉͔͍͖͍͎͔̝̀̈́̿̈̉̀͛ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͔͍͔͈͈͔͔̓̎͌̈́̈̉ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚ͅͅͅͅͅͅ͏͈̓́͌͏̡͓͔͕͔͔̟͉͔͍̝͍͎͔͈͈͓͓͓̣̓̐̐̐̏͐̈́́̿̈́́́̂̋̋̂̂̋͌̎̓̓͋̈́̌̀͛̂́̈́͒̂̀͛̂̓̓̍̚̚ͅͅͅͅͅͅͅͅͅͅ͏͎͔͒͏̡͌̍͌͌͏̛̯͉͇͉͎͕͎͔͉͗̍͒̂̀̂̊̂̉ͯͯͯ͆̓̚͝͝͝͏͎͓͖͔͖͉͎͔͉̝̀́̿̈́́́̈̉̀͛ͯ̀̀̀̀́͒̀̓͌̿̈́̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͎͔͉͖͉͎͔͓͔̝̓̎͌̈́̈̂̓͌̿̈́̂̉ͯ̀̀̀̀́͒̀̓͌̿̓͒̀̀̈́ͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͎͔͓͔͖͈͎͎̝̓̎͌̈́̈̂̓͌̿̓͒̂̉ͯ̀̀̀̀́͒̀̓́͌̀̀̈́ͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎͖͕̝͈͔͔̓̎͌̈́̈̂̓́͌̂̉ͯ̀̀̀̀́͒̀͒͌̀̀̂͐̏̏͌̚ͅͅͅͅͅ͏͈̓́͌͏͓͔͓͔͉͎͔̓̐̐̐̏̿̓͌̿̓̚ͅͅ͏̡̛͎͉͇̟͉͎͔͉̝͉͎͔͉͖͕͉͎͔͓͔̝͉͎͔͓͔͖͕͈͎͎̝͈͎͎͖͕͔͈͕͈͓͓͓̣͆̓͌̿̈́̂̀̋̀̓͌̿̈́̎́͌̀̋̀̂̆̓͌̿̓͒̂̀̋̀̓͌̿̓͒̎́͌̀̋̀̂̆̓́͌̂̀̋̀̓́͌̎́͌ͯ̀̀̀̀͆̓̈͒͌̌̀͛̂́̈́͒̂̀͛̂̓̓̍̚ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͔͒͏̡͌̍͌͌͏̛̯͉͇͉͎͔̣͗̍͒̂̀̂̊̂̉ͯ̀̀̀̀́͌͒̈̂̚͝͝ͅ͏͎͉͇͕͔͓͓͔͔͔͈͆̀͐̈́́̈́̌̀͐͌́̀͒́͒̀̀͂ͅͅͅͅͅ͏͔͔̀͏̛͕͓͕͎͔͉̀̂̉ͯͯͯ͆̓͝ͅ͏͎͕͔͔͉͎͇͓͔͉̀͐̈́́̿͒͐́̿̓ͅͅͅͅ͏͎͖͈͉͈̝̈̉̀͛ͯ̀̀̀̀́͒̀͗̓̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͉͈̓̎͌̈́̈̂͗̓̿ͅͅͅͅ͏̛͎͖͕͉͈͉͈̝̝͔͉͎͇̂̉̎́͌ͯ̀̀̀̀͆̀̈͗̓̀̀̂͒͐́̀͐ͅͅͅͅ͏͌͌̂̉̀͛ͯ̀̀̀̀̀̀̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͉͖͈͉͎̝͓͌͌̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇͉͖͈͉͎̝͔͕͓̓̎͌̈́̈̂̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̈́͝ͅͅͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͉͖͈͉͎̝͔͕͌͌̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇͉͖͈͉͎̝͓͕͎͔͉̓̎͌̈́̈̂̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅͅͅͅͅͅ͏͎͈͎͎̀̓́͌̿͐ͅ͏͉͎͔͓̿͏͎͉͖͎̝̓͌̓͋̈̉̀͛ͯ̀̀̀̀́͒̀́͂͌̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͎͈͉͎̿́͂͌̈́̂̉̎̓̓͋̈́ͯ̀̀̀̀͆̀̈́͂͌̈́̉̀͛ͯ̀̀̀̀̀̀̀̀̈́ͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͉͖͈͉͎̝͓͓̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̈́͝ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͉͖͈͉͎̝͔͕͕͎͔͉̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅͅ͏͎͉͔͍͖͎̯͔͉̀́̈́̈́̿̈̉̀͛ͯ̀̀̀̀́͒̀͗͐ͅͅ͏͎̝̀̀̈́͏̛͕͍͎͔͔̥͍͎͔͉͎͕͔͎̯͔͉̓̎̓͒́͌̈̂͐̂̉ͯ̀̀̀̀͗͐ͅͅͅͅͅͅ͏͎͓͓̮͍̝̎̓͌́́̀̀̂͐ͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͍͎͔͓̝̂ͯͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͎̯͔͉̂̉ͯ̀̀̀̀͗͐ͅ͏͎͈̎͐͌́̓ͅ͏̝̯͔͉͌̈́͒̀̀̂͐ͅ͏̛͎͍͎͔͓͎͇͔͈̀̂̀̋̀̈͌̎͌̀̋̀̑̉ͯͯ̀̀̀̀̈́ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͌͌̿͏͔͉͐͏͎͓͎̣͈͉͎̯͔͉̂̉̎́͐͐̈́͌̈́̈͗͐ͅͅ͏̛͎͖͎̳̝̉ͯ̀̀̀̀́͒̀͗͐́̓̀̀̈́ͅͅ͏̛͕͍͎͔͔̥͍͎͔͎̳͓͓̮͍̝̓̎̓͒́͌̈̂͂͒̂̉ͯ̀̀̀̀͗͐́̓̎̓͌́́̀̀̂͐ͅͅͅͅͅͅͅͅ͏͓͌͌̿͂͒́͋̂ͯ̀̀̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͎̣͈͉͎̳͕͎͔͉̂̉̎́͐͐̈́͌̈́̈͗͐́̓̉ͯͯͯ͆̓͝ͅͅͅ͏͎͍̀͒ͅ͏͖͉͔͍͖͍͎͔͓̝̿̈̉̀͛ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͉͎͓̝̂̉ͯ̀̀̀̀́͒̀͌͂͒́͋̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏̛͓͉͍͎͔͓͎͇͔͈̞͍͎͔͓̻͍͎͔͓͎͇͔͈͍͌͌̿͂͒́͋̂̉ͯ̀̀̀̀͆̀̈͌̎͌̀̀̒̉̀͛ͯ̀̀̀̀̀̀̀̀͌͌̎͌̀̍̀̑̽̎͒ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͉͎͓̻͉͎͓͎͇͔͈͍̈̉ͯ̀̀̀̀̀̀̀̀͌͂͒́͋͌͂͒́͋̎͌̀̍̀̑̽̎͒ͅͅͅͅͅͅͅ͏̛͖͕͎͔͉̈̉ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅ͏͎͓͕͍͉͔̀͂̿͐͏͖͕͎͙͖͕̝͌͌̈̉̀͛ͯ̀̀̀̀́͒̀͆͒͑̓̿́͌̀̀̈́ͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͖͕͖͕͎͙͕͎͉͔̝̓̎͌̈́̈̂͆͒͑̓̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿̀̀̈́ͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͕͎͉͔͓͖͕͖͔͉͔̝̓̎͌̈́̈̂͆͒͑̓̿̂̉̎́͌ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͔͉͔͖͕͖͌͌̿͌̂̉̎́͌ͯ̀̀̀̀́͒̀ͅͅ͏͔͉͐͏͎͓̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͈͎͎̂̉ͯ̀̀̀̀́͒̀̓́͌̿͐ͅ͏͉͎͔͓͎̝̿́͂͌̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͎͈͖͈͎͎̿́͂͌̈́̂̉̎̓̓͋̈́ͯ̀̀̀̀́͒̀̓́͌̿͐ͅͅͅͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔̝̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͍͔͖͕͖͕͔͉̿́̂̉̎́͌ͯ̀̀̀̀́͒̀̈́͒́ͅ͏͎̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͕͔͉͌͌̿̈́͒́͏̛͎͖͕͉͔͉͔̝̝͔̰͓͓͔̂̉̎́͌ͯ̀̀̀̀͆̀̈͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀͐ͅͅͅͅͅͅ͏̛̛͔͉͔͔͕͎͉͕͎͙͖͕̝̝͔̰͓͓͔͌͌̀͌́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈͆͒͑̓̿́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀͐͝ͅͅͅͅͅͅͅͅͅ͏̛̛͕͎͙͔͕͎͖͌͌̀͆͒͑̓́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀́͒̀̓͝ͅͅͅ͏̛͕͎͔̝͖͒̀̀̐ͯ̀̀̀̀́͒̀ͅ͏͔͉͐͏̛͎͓͔͔̝̻͈͉̿̀̀̽ͯ̀̀̀̀͗͌̀̈̓͘ͅͅ͏͕͎͔̜͒̀̀ͅ͏͔͉͐͏͎͓͎͇͔͈͉̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀͆̀̈ͅ͏͔͉͐͏͎͓̻̓͏͕͎͔͖͕̝̝͔̥͍͔͙͖͕͒̽̎́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́͌͒̈̂͐̀́͌̀͆ͅͅͅͅ͏͒̀͏͎̀ͅ͏͍͒̀͏͒̀ͅ͏͔͈͆̀̀ͅ͏͔͉͐͏͎͓͓͍̌̀͐͌́̀͒ͅͅͅ͏͖̀ͅ͏̛̛͓͔͖͕͔͕͎͒̀̀́͌̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͝ͅͅͅ͏͔͉͐͏͎͓͔͔̻̿̓͘ͅ͏͕͎͔̝͒̽̀̀ͅ͏͔͉͐͏͎͓̻̓͏̛͕͎͔͖͕͒̽̎́͌ͯ̀̀̀̀̀̀̀̀̓ͅͅ͏̛͕͎͔͔̝͖͕͎͙͖͕͕͎͉͔͓͕͎͙͕͎͉͔͔͉͔͔͉͔͒̋̋ͯ̀̀̀̀ͯ̀̀̀̀̈́́́̀̀͛ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿́͌̂̀͆͒͑̓̿́͌̌ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿̂̀͆͒͑̓̿̌ͯ̀̀̀̀̀̀̀̀̂͌̂̀͌̌ͯ̀̀̀̀̀̀̀̀̂̚̚̚͝ͅͅͅͅͅͅͅͅͅͅ͏͔͉͐͏͎͓̂̀̚͏͔͉͐͏͎͓͔͔̿̌ͯ̀̀̀̀̀̀̀̀̂̓̿͐͘ͅ͏͉͎͔͓͎͈͎͎̿́͂͌̈́̂̀̓́͌̿͐̚ͅͅͅ͏͉͎͔͓͎̿́͂͌̈́̌ͯ̀̀̀̀̀̀̀̀̂̓̿͐ͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔͈͎͎̂̀̓́͌̿͐̚ͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔͕͔͉̌ͯ̀̀̀̀̀̀̀̀̂̈́͒́ͅ͏͎͕͔͉̂̀̈́͒́̚͏͎͔͈͈͔͔ͯ̀̀̀̀ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚͝ͅ͏͈̓́͌͏͓͔̓̐̐̐̏͐̚͏͍͔͈͌͌̂̌̀͛ͯ̀̀̀̀̀̀̀̀ͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͔͖͔͔͓̝͔͙͕͉̈́̀̎͒͆̈̈́́́̉ͯ̀̀̀̀̉ͯͯͯ́͒̀͌͒̀̀̂͑͗͒̚͝͝ͅͅͅ͏̷̴̵̸̶̡̧̨̢̛͓͇͈͚͖͎͍̱̥̲̹̩̯̰̳̤̦̪̫̬̺̣̮̭͓͉͔͕͎͔͉͐́̈́͆͊͋͌̓͂̂̎͐͌̈̂̂̉ͯ͆̓͘͏̛͎͎͔͔͖͕͉̝̀̓͌́̈̉̀͛ͯ̀̀̀̀́͒̀͂͌̈́͒̀̀̂̂ͯ̀̀̀̀͆͘ͅͅͅ͏̛̛̛̛͔͉̝͉̜͔͔͎͇͔͈͉͉͔͔͓͉͎͕͓͔͔̻͉͕͉̝͔͔̻͉͔͕͎͕͉͕͎͔͉͒̀̈͌̀̀̀̐̀̀̀̎͌̀̋̋̉̀͛ͯ̀̀̀̀̀̀̀̀͆̀̈͌͒̎̓͌̈́̈̽̉̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͌̈́͒̀̋̀̽ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀ͯ̀̀̀̀͒͒̀͂͌̈́͒ͯͯͯ͆̓͘͘͘͝͝͝ͅͅͅͅͅͅͅͅͅͅͅ͏͎͓͕͍͉͔͍͓͇͖̀͂̿̈̉̀͛ͯ̀̀̀̀́͒̀̓͏͎͔͎͔̝̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇̓̎͌̈́̈̂̿͂ͅͅͅͅ͏̛͙͖͕͖͕͎͙͖͕̝̈́̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿́͌̀̀̈́ͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͖͕͖͕͎͙͕͎͉͔̝̓̎͌̈́̈̂͆͒͑̓̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿̀̀̈́ͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͕͎͉͔͓͖͕͉̓̎͌̈́̈̂͆͒͑̓̿̂̉̎́͌ͯ̀̀̀̀͆̀̈̓ͅͅͅͅͅͅͅ͏͎͔͎͔̝̝͔̰͓͓͔͍͓͓͇̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀̓ͅͅͅͅͅͅͅ͏̛̛̛̛͎͔͎͔͔͕͎͉͕͎͙͖͕̝̝͔̰͓͓͔͍͓͓͇͕͎͙͔͕͎͔̝͖͕͎͙͖͕͕͎͉͔͓͕͎͙͕͎͉͔͍͓͇́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈͆͒͑̓̿́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀͆͒͑̓́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀̈́́́̀̀͛ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿́͌̂̀͆͒͑̓̿́͌̌ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿̂̀͆͒͑̓̿̌ͯ̀̀̀̀̀̀̀̀̂̿͂̚̚͝͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͙̈́̂̀̓̚͏͎͔͎͔͔͈͈͔͔ͯ̀̀̀̀ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚͝ͅͅ͏͈̓́͌͏͓͔͍͓͇͍͔͈̓̐̐̐̏̂̌̀͛ͯ̀̀̀̀̀̀̀̀̚ͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͔͓͙͎͕͎͔͉̈́̀̎͒͆̈̈́́́̉ͯ̀̀̀̀̉ͯͯͯ́̓̀͆̓̚͝͝͏͎͇͔͔͉͎͇͖͔͍̝͉͔͔͈͈͔͔̀̿͒͐́̈̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅͅ͏͈̓́͌͏̛͓͔͇͔͔͉͎͇͔͕͎͉͔͔͍͓̓̐̐̐̏̿͒͐́̂̉ͯ̀̀̀̀͒͒̀́͗́̀͐̎͊̚ͅͅͅͅ͏͎͓͙͎͕͎͔͉̈̉ͯͯͯ́̓̀͆̓͝͏͎͍̀͒ͅ͏͖͔͉͎͇͔͓͎͍͖͔͍̝͉͔͔͈͈͔͔̿͒͐́̿́͋̈́̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅͅͅ͏͈̓́͌͏͓͔͍̓̐̐̐̏͒̚ͅ͏͖͔͉͎͇͍͔͈̿͒͐́̂̌̀͛ͯ̀̀̀̀̀̀̀̀ͅͅͅͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͎͍͎͍͔͍̝͉͔͔͍͓̈́̀̎͒͆̈͛̂́̂̀́̉ͯ̀̀̀̀̉ͯ̀̀̀̀͐̀̀́͗́̀͐̎͊̚̚͝͝ͅͅ͏̛͎͉͔͍̻͓͕͓͓͔̦͉͔̈̉ͯ̀̀̀̀͆̀̈́͐̂̓̓̂̽̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂́͌̈́̀ͅͅͅ͏͍̀͒ͅ͏̛̛̛͖͔͉͎͇͔͓̭͓͓͇͔͍̻͍͓͓͇͔͕͎͓͎͍̝͎͍͖͔͍͎͔̝̀͒͐́̀́͋́̀́̀̂̀̋̀͐̂́̂̽̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀́̀̀́̎͒͐͌́̓̈̂̀̂̌̀̂̿̂̉ͯ̀̀̀̀̀̀̀̀́͒̀́͂͌̿͌̀̀̈́̚͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͎͎͍͔͍͎͔͍̓̎͌̈́̈̓͌́̈́̉̉ͯ̀̀̀̀̀̀̀̀́͂͌̿͌̎͒ͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔̲͍̈̉ͯ̀̀̀̀̀̀̀̀́͌͒̈̂ͅͅͅ͏͖͓͕͓͓͕͙͓͙͎͕͎͔͉̈́̀̓̓͆͌͌̂̉ͯ̀̀̀̀ͯͯͯ́̓̀͆̓͝͝ͅͅ͏͎̀́̈́̈́̿͏͍͒̿͒ͅ͏͖͈͎͇͖͉͓̝̿̓́̈́̈̉̀͛ͯ̀̀̀̀́͒̀̿́̈́̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂́̈́̈́̿ͅͅͅͅ͏͍͒̿͒ͅ͏̡̛͖͖͕̝̝͖͉͖̝̂̉̎́͌̀̀̂̈́̈́̂ͯ̀̀̀̀́͒̀́̈́̈́̿̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂́̈́̈́̿ͅͅͅͅ͏͔͉͐͏͎͈̿̓͏̛͓͎͖͍͎͔͓̝̂̉ͯ̀̀̀̀́͒̀́̈́̈́̿͌̀̀̈́ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂ͅͅͅͅͅ͏̛͎͙͖͍͌̿́̈́̈́̂̉ͯ̀̀̀̀́͒̀͒ͅ͏͖͉͖̝̿̈́̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͍̓̎͌̈́̈̂͒ͅͅͅͅͅ͏͖̿ͅ͏͔͉͐͏͎͈̿̓͏̛͓͎͖͍̂̉ͯ̀̀̀̀́͒̀͒ͅͅ͏͖͔̝̿́͂͌̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͔͉͎͇͔͖͖͙͔͔̝̓̎͌̈́̈̂͒͐́̿́͂͌̂̉ͯ̀̀̀̀́͒̀͒̿̀̀̈́͘ͅͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͖͙͔͔͕͈͖͓͔͕̝̓̎͌̈́̈̂͒̿̿͂͒̂̉ͯ̀̀̀̀́͒̀͆͆̀̀̈́͘ͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͓͔͕͖̓̎͌̈́̈̂͆͆̂̉ͯ̀̀̀̀́͒̀̓ͅͅͅͅ͏̛̛̛͕͎͔̝͉͉͓͖͙͔͔͓͔͙̝͉͓͙͉͎͉͎͉͖͈͉͎̝͓͍͒̀̀̐ͯ̀̀̀̀͆̀̈̿́̈́̈́̉̀͛ͯ̀̀̀̀̀̀̀̀͒̿̎͌̀̀̂̈́͐͌́͌̂ͯ̀̀̀̀̀̀̀̀́̈́̈́̿̈́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀͒͘̚ͅͅͅͅͅͅͅͅͅ͏̛͖͉͖͈͉͎̝͔͕͈͉̿̈́̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅͅͅ͏͕͎͔̜͍͎͔͓͎͇͔͈͍͎͔͓̻͒̀̀́̈́̈́̿͌̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́̈́̿͌̓ͅͅͅͅͅͅͅͅ͏̛͕͎͔͈͉͎̝͓͒̽̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͓͔͕͓͔͙̝͉͓͙͎͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͆̎͌̀̀̂̈́͐͌́̚͝ͅͅ͏̛̛͎͓͓͔͕͓͔͙̝͉͓͙͉͎͉͎͖͙͔͔͓͔͙̝͉͓͙͎̂ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀͆͆̎͌̀̀̂̈́͐͌́͌̂ͯ̀̀̀̀̀̀̀̀͒̿̎͌̀̀̂̈́͐͌́̚͘̚͝ͅͅͅͅͅͅͅͅͅ͏̛̛͎͉͖͈͉͎̝͔͕͍̂ͯ̀̀̀̀̀̀̀̀́̈́̈́̿̈́̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀͒ͅͅͅͅ͏̛͖͉͖͈͉͎̝͓͈͉̿̈́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅͅͅ͏͕͎͔̜͍͎͔͓͎͇͔͈͍͎͔͓̻͒̀̀́̈́̈́̿͌̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́̈́̿͌̓ͅͅͅͅͅͅͅͅ͏̛͕͎͔͈͉͎̝͔͕͒̽̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͝ͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͍͆̀͒ͅ͏͖͔͈͉͎̞͈͉͍̿́͂͌̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒̚ͅͅͅͅ͏̛̛̛͖͓͔͕͈͉͎̝͓͕͈̝͉͔͇͔͔͉͎͇͖̈̉ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͆̎̈́̈́̀̀͆́͌ͯͯ̀̀̀̀̀̀̀̀͂͒̀̀́͗́̀̿͒͐́̈̉ͯ̀̀̀̀̀̀̀̀́͒̀̓͝ͅͅͅͅͅͅ͏̛͕͎͔̝͈͉͒̀̀̐ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅ͏͕͎͔̜͕͈͎͇͔͈͖͉͔͍̝͕͈̻͒̀̀͂͒̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́͒̀̀̀͂͒̓ͅͅͅ͏̛͕͎͔͒̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅ͏͎͓͔͔͍̝̀͐̀̀̈́͏̛̛͕͍͎͔͔̥͍͎͔͔͔͍͉̝͎͉͔͍̻͎͍̓̎̓͒́͌̈̂͒̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎̈́̀̀̓͌́̈̂́̂̽̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅͅͅͅ͏͎͓͔͍̀͒ͅ͏͖͔͎̝̿͂̀̀̈́ͅ͏͕͍͎͔͔̥͍͎͔͕͔͔̓̎̓͒́͌̈̂͂ͅͅͅͅͅ͏̛͎̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͏͎͓͔͔͍̝͉͔͍̻͎͍͍̀͐̒̀̀̂́̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒ͅͅͅ͏͖͔͎̿͂̎ͅ͏͎͉̝͕͎͔͉̓͌̓͋̀̀͆̓͏͎͕͈͍̈̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀͂͒̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒̚ͅ͏̛͖͔͉͎͇͔͓͔͍͍̿͒͐́̿́͋̈͐̒̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒͝ͅͅͅͅ͏̴̨͖͔͎͉͎͎̭̬̝̲͍̿͂̎͒̀̀̂ͅͅͅ͏̛͖͔͓̀́͋̂ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅ͏͎͓͔̀̓͏̛͎͔͎͔̝͉͔͍̻͎͍̀̀̂́̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͎͓͔͔͙̝͉͔͍̻͔͙̀͐̀̀̂͐̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͎͓͔͕͎͙̝͉͔͍̻͔̻͖̀͆͒͑̓̀̀̂̈́́́̂̽̂͆͒͑̿́͌̂̽ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅ͏͎͓͔̀̓͏͎͔͎͔͍͎͔̝̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͔͙͍͎͔̝̀͐̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͕͎͙͍͎͔̝̀͆͒͑̓̿͌̀̀̈́ͅͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏̴̨͎͔͎͔͍͎͔͉͎͎̭̬̝̿͌̎͒̀̀̓ͅͅͅͅͅ͏̴̴̨̨̛̛̛͎͔͎͔͔͙͍͎͔͉͎͎̭̬̝͔͙͕͎͙͍͎͔͉͎͎̭̬̝͕͎͙͔͍͎̣͈͉͍ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̿͌̎͒̀̀͐ͯ̀̀̀̀̀̀̀̀̀̀̀̀͆͒͑̓̿͌̎͒̀̀͆͒͑̓ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͒ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔͎͔͍͎̣͈͉̿͂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈̓ͅͅ͏̛̛̛͎͔͎͔͍͎͔͔͍͎̣͈͉͔͙͍͎͔͔͍͎̣͈͉͕͎͙͍͎͔͍̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͐̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͆͒͑̓̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔͎̣͈͉͔͍̿́͂͌̎́͐͐̈́͌̈́̈͐̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͓͔͕͔͈͉͓͉͓͔͈͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀̏̏̀͆̀̀̀̀͝ͅͅ͏͎͙͙͉͇͌̀͗́̀̀͏͔͉͔͔̀̀͏̀͗͏͉͎͒͋ͯ̀̀̀̀̀̀̀̀̏̏̀̀͋͏͉͔͓͉͍͔͈͔͍͗̀̀͂́̈́ͯ̀̀̀̀̀̀̀̀̏̏̀̀͂́̈́̀́̀͌̀͏͉͕͓͋ͯ̀̀̀̀̀̀̀̀̏̏̀̀̀͒́͌̀͐͒ͅͅ͏͇͍͍͉͎͇͎͇͕͇͓͖͕͕͕͕͕͈̝̻͒́̀͌́́ͯ̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀́͒̀͂͒̀̀̽ͯ̀̀̀̀̀̀̀̀͆̚ͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͍͆̀͒ͅ͏͖͔͈͉͎̞͉͕͈͉͎͕͓͈͉͉͈͉͍̿́͂͌̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀͆̀̈͂͒̎̓͌̈́̈̓͌̈́̎̈́̉̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒̚ͅͅͅͅͅ͏̡̧̢̢̛̛͖͓͕͈͕͓͈͈͉͉̜͓͉͔̞̜͈̞̜͔͉͔̞̹̣̈̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͂͒̎͐̈̓͌̈́̎̈́̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀ͯͯ̏̓͒͐ͯ́̈́ͯ͌̀̓͝͝͝͝͝ͅͅͅͅͅ͏͎͉͇͇̜͔͉͔̞̜͈̞̜͆̀͐́̏͌ͯ̏́̈́ͯ͂ͅͅͅ͏̡̧̢͙̞̜͈̞̹̰̣̈́ͯͯ̑̀̓͏͎͉͇̜͈̞̜͈̝͆̏̑ͯ́̀͒͆̂̏͌ͅ͏̶͇̞͉̂͗̀͌ͅ͏͇͉̜̞̜̞̜͉͖͉̝̀͆͌̏́͂͒ͯ̈́̀̈́̂̓ͅ͏͎͉͇̞̜͈̞̣͉͎͔͆̂ͯ̀̀̀̀̓͌̀̓ͅ͏͎͉͇̜͈̞̣͉͎͔̩̤̜͉͎͕͔͉̝͉͎͔͉͖͕̝͉͎͔͉̞̜̞̣͉͎͔̳͔̜͉͎͕͔͉̝͉͎͔͓͔͖͕̝͉͎͔͓͔̞̜̞̣͈͎͎͎͍̜͉͎͕͔͉̝͈͎͎͖͕̝͈͎͎̞̜̞̜͕͔͔͆̏̓ͯ̀̀̀̀͌̀̀͐̀̈́̂̓͌̿̈́̂̀́͌̂͛͛̓͌̿̈́̂͂͒ͯ̀̀̀̀͌̀̓͒̀͐̀̈́̂̓͌̿̓͒̂̀́͌̂͛͛̓͌̿̓͒̂͂͒ͯ̀̀̀̀́͌̀́̀͐̀̈́̂̓́͌̂̀́͌̂͛͛̓́͌̂͂͒ͯ̀̀̀̀͂̚̚̚͝͝͝͝͝͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͉̝͓͔̀̈́̂̿̓ͅ͏͎͉͇͆̂̀͏͎͉̝͓͖͔̞̳͖̜͕͔͔̓͌̓͋̂́̿̈́́́̈̉̂́̏͂ͅͅ͏͎̞̜͉͖̞̜͉͖͉̝͔͉͎͇͔͓͓̞̜͎͓͕͔̻͍ͯ̏̈́ͯͯ̈́̀̈́̂́̈́̈́̿͒͐́̿́͋̂ͯ́̍̍̀̀̀̀̈́̀͒͌̀́̈́̈́̏͒̚ͅͅͅͅͅ͏͖̻͔͉͎͇̽̀́̀͒͐́̀͐ͅͅͅ͏͔͉͎͇͍͓͓͇͖͙̻͉͎͕͔̻͍͉͎͕͔͓͈͌͌̏͒͐́̏́̽̀͒̀͐̽̀̏ͅͅͅͅͅͅͅ͏̡͕͓̞̜͈̞͔͉͎͇͔͓͓̜͈̞̜͓͔͉̝͒̽̍̍ͯ̀̀̀̀̓̈́̈́̀͒͐́̀́͋̏̓ͯ̀̀̀̀͌̓̀̈́̂́̈́̈́̿ͅͅͅͅ͏͍͒̿͒ͅ͏͖̂̀ͅ͏͎͈͎͇̝̓́̂́̈́̈́̿ͅ͏͍͒̿͒ͅ͏͖͈͎͇̞̜̿̓́̈́̈̉̂ͯ̀̀̀̀̀̀̀̀ͅͅ͏͔͉͐͏̡͎͉̝̞̜̀̈́̂́̈́̈́̂̈́̈́̏͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍̀̈́̂͒ͅ͏͖̞̲͍̂ͅͅ͏͖̜̏ͅ͏͔͉͐͏͎̞̜͓͔̞̜͉̝͓͔͕͓͔͙̝͉͓͙͎ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀́̀͐̀̈́̂͆͆̂̀͌̂̈́͐͌́̚ͅͅͅ͏͎̞͔͉͎͇͔͓̜̞̜͓͔͉̝͈͉͈̂͒͐́̀́͋̏͐ͯ̀̀̀̀͌̓̀̈́̂͗̓̿ͅͅͅͅͅ͏͎̂̀ͅ͏͎͈͎͇̝͕͔͔͉͎͇͓͔͉̓́̂͐̈́́̿͒͐́̿̓ͅͅͅͅͅ͏͎͓͓̝̈̉̂̀̓͌́̂͏͎͙̞̜͌̿́̈́̈́̂ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝̀̈́̂͐͏̞͔͉͎͇͌͌̂͒͐́̀͐ͅͅ͏̜͌͌̏͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍͓͓͇̞͔͉͎͇͍͓͓͇̜̀̈́̂́̂͒͐́̀́̏ͅͅͅͅͅͅ͏͔͉͐͏͎̞̜͓͔̞̜͓͔͙̝͉͓͙͉͎͉͎͉̝͖͙͔͔͕͈̞͔͈͔͔͓͖͙̜̞̜͉͎͕͔͉̝͕͎͙͓͓̝ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀͐̀͌̂̈́͐͌́͌̂̀̈́̂͒̿̿͂͒̂́̀͒͐́̀͒̀̏͐ͯ̀̀̀̀͐̀̈́̂͆͒͑̓̂̀̓͌́̂̚͘ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͙͔͙̝͎͕͍͈͌̿́̈́̈́̂̀͐̂͂͒̂̀͐͌́̓ͅͅͅ͏̝͓͉͚̝̖͍͉͎̝͍̝̙̞̜͓͔͉̝͕͎͙͕͎͉͔͓͓͓̝͌̈́͒̂̂̀̀̂̐̂̀́̂̂ͯ̀̀̀̀͌̓̀̈́̂͆͒͑̓̿̂̀̓͌́̂̕͘̕ͅͅͅͅͅͅ͏͎͙̞̜͌̿́̈́̈́̂ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍͉͎͕͔͓̞͍͉͎͕͔͓̜̀̈́̂̂̏ͅͅ͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͈̀̈́̂͏͕͓̞͈͒̂͏͕͓̜͒̏͏͔͉͐͏͎̞̜͓͔̞̜͉͖͉̝ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀̈́̀̈́̂́̈́̈́̿ͅͅ͏͔͉͐͏͎͈̿̓͏͓͎̞̜͉͖͉̝̂ͯ̀̀̀̀̀̀̀̀̈́̀̈́̂͐ͅ͏͉͖̞̰͌͌̿̈́̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀͏͔͉͔̜͉͎͕͔͉̝͌͌̀͌ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̀̈́̂͐̚ͅ͏͔͉͔͈͌͌̿͌̂̀͐͌́̓ͅͅ͏̨̝͓͔͉͓̟̞̜̞̯͔͉͌̈́͒̂́̈́̏́͌̂͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐ͅͅ͏͎͓̜̞̜͉͖͉̝͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̈́̀̈́̂͐̚͏͌͌̿͏͔͉͐͏͎͓̞̜͉͎͕͔͓͓̝̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̀̓͌́̂͐͏͌͌̿͏͔͉͐͏͎͓͈̂̀͐͌́̓ͅ͏̝͈͓̞̜͓͓̝͌̈́͒̂́̈́̂͂͒̀̓͌́̂͐ͅͅ͏͓̞̜͉͎͕͔͓͓̝͌͌̿͂͒́͋̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̀̓͌́̂͐ͅ͏͌͌̿͏͔͉͐͏͎͓͈̂̀͐͌́̓ͅ͏̝͔͉͓̞̜͓͓̝͌̈́͒̂́͌̂͂͒̀̓͌́̂͐ͅ͏͓̞̜͉͖̞̜͕͔͔͌͌̿͂͒́͋̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅ͏͎͉̝͉͔͍̀̈́̂́̈́̈́̿̂̀ͅ͏͎͉̝͉͔͍̞̜͕͔͔̓͌̓͋̂́̈́̈́̿̈̉̂́̈́̈́̏͂ͅ͏͎̞̜͕͔͔ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͏͎͉̝͍̀̈́̂͒ͅ͏͖͉͔͍̿̂̀ͅͅ͏͎͉̝͍̓͌̓͋̂͒ͅ͏͖͉͔͍̞͍̿̈̉̂͒ͅͅͅ͏͖̜͕͔͔̏͂ͅ͏͎̞̜̞̜͉͎͕͔͔͙̝͈ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̀͐̂̓̓͋͂ͅͅ͏͉̝͈͎͎̂̀̈́̂̓́͌̿͐͘ͅ͏͉͎͔͓͎̿́͂͌̈́̂̀ͅͅ͏͎͉̝͈͎͎̓͌̓͋̂̓́͌̿͐ͅ͏͉͎͔͓̿͏͎͉̞̓͌̓͋̈̉̂̀̀́͌͌͏͈͔͔͓͔͗̀̓́͒̀ͅ͏͖̀͏͔͉͔͈͈͎͎̀͗̀̓́͌̀͐ͅͅ͏͉͎͔͓̜̞̜͉͖͉̝͈͎͎͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̈́̀̈́̂̓́͌̿͐ͅ͏͉͎͔͓͉͖͈͉͎̞͈͖̿̈́̂̀̈́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̓̀ͅͅ͏͔̀̓ͅ͏͓͔͓̜͉͎͕͔͉̝͈͎͎̀͐̀̈́̂̓́͌̿͐ͅ͏͉͎͔͓͍͔͔͙̝͎͕͍͓͉͚̝̖͈̿́̂̀͐̂͂͒̂̀̀͐͌́̓ͅͅͅͅ͏̝̞͈͎͎͌̈́͒̂̑̐̐̂̀̓́͌̀͐ͅͅ͏͉͎͔͓̜͉͖̞̤͕͔͉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒́͏͎͓̀̈̓ͅ͏͎͓̜͉͎͕͔͉̝̈́̉̀͐̀̈́̂͐̚͏͕͔͉͌͌̿̈́͒́͏͎͔͙̝͎͕͍͓͉͚̝̖͈̂̀͐̂͂͒̂̀̂̂̀͐͌́̓ͅͅͅͅ͏̝̞̜̞̜͕͔͔͌̈́͒̂̑̒̐̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅ͏͎͉̝͓͕͍͉͔̀̈́̂͂̿͐͏͌͌̂̀͏͎͉̝͓͕͍͉͔̓͌̓͋̂͂̿͐͏̞͌͌̈̉̂́̈́̈́̀͐͏̜͕͔͔͌͌̏͂͏͎̞̜͉͖̞̜͉͖͉̝͍͓͇͉͖͈͉͎̝̞̭͓͓͇̜͉͎͕͔͉̝͍͓͇ͯ̀̀̀̀̀̀̀̀̏̈́ͯͯ̀̀̀̀̀̀̀̀̈́̀̈́̂̿̈́̂̀̈́̈́̂̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̀͐̀̈́̂̿͂̚ͅͅͅ͏͙͈̈́̂̀͐͌́̓ͅ͏̝̳͕͓͉͔͌̈́͒̂͂̓͒͂̀ͅͅ͏͍̀͒ͅ͏͖͓͓͔͙̝͍͇͉͎̞̜̞̜͕͔͔̀́̈́́̂̀͌̂́͒̀͐̀̐͐̂͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂̚̕͘͘ͅͅ͏͎͉̝͓͕͍͉͔͍͓͇̀̈́̂͂̿̂̀͏͎͉̝͓͕͍͉͔͍͓͇̞͍͓͓͇̜͕͔͔̓͌̓͋̂͂̿̈̉̂́̈́̈́̀́̏͂ͅͅ͏͎̞̜͉͖̞̜͉͖̞̜͉͖͉̝͍ͯ̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̏̈́ͯ̀̀̀̀̈́̀̈́̂͒ͅ͏͖̿ͅ͏͔͉͐͏͎͈̿̓͏͓͎͈͉͎̝̞̜͔͉̝͕͎͔͔͉͎͇̞̜͔͈̞̜͔̞̜͔͈̞̲͍̂̀̈́̈́̂̂ͯ̀̀̀̀̀̀̀̀́͂͌̀̈́̂̓͒͒̿͒͐́̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀ͅͅͅͅͅͅͅͅ͏͖̜͔͈̞̜͔͈̞̭͓͓͇̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̀̓ͅͅͅ͏͎͔͎͔̏͐ͅ͏̴͔͉͔̜͔͈̞̜͔͈̞͙̜͔͈̞̜͔͈̞̦͕͎͙͍͉͎͕͔͓̜͔͈̞̜͔̞̜͔͈̞̜͔͌͌̀͌̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒͑̓̀̈̉̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅͅͅͅͅͅ͏͙͉̝͔͉͎͇͔̞̜̈́̀̈́̂͒͐́̿́͂͌̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̍̍̀͐ͅͅͅ͏͕͔͙͎͍͉͙̞̜͔͐͌́̈́̀̈́́̓́͌͌̀̓̀̍̍ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏͂̚ͅ͏͙̞̜͔̞̜͉͖̞̜͉͖̞̜͉͖͉̝̈́ͯ̀̀̀̀̀̀̀̀̏́͂͌ͯ̀̀̀̀̏̈́ͯ̏̈́ͯͯ̈́̀̈́̂̓ͅ͏͍͍͎͓̞̜͈̞̣́̈́̂ͯ̀̀̀̀̓͏͍͍͎̣́̈́̀͏͎͉͇͕͔͉͆͒́͏͎̜͈̞̜̞̤͕͔̏̓ͯ̀̀̀̀͐͆́͌̀̓ͅ͏͍͍͎͓̜̞̜͔̞̜͔͈̞̜͔̞̜͔͈̞̥͎̜͔͈̞̜͔͈̞̣́̈́̏͐ͯ̀̀̀̀́͂͌ͯ̀̀̀̀́̈́ͯ̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀́͂͌̈́̏ͯ̀̀̀̀̀̀̀̀ͅͅͅ͏͍͍͎̜͔͈̞̜͔͈̞̤͓͉͔͉́̈́̏ͯ̀̀̀̀̀̀̀̀̓͒͐ͅ͏͎̜͔͈̞̜͔̞̜͔͈̞̜͔̏ͯ̀̀̀̀̀̀̏͒ͯ̀̀̀̀̏́̈́ͯ̀̀̀̀͂ͅ͏͙̞̈́ͯ̀̀̀̀͛̅̀͆͏͒̀͒͏͉͎͕͔͗̀̀̈́͆́͌̿̓ͅ͏͍͍͎͓̜͔̞̜͔̞́̈́̀̅ͯ̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͏̻͈͗̇̓̓͋͂ͅ͏͓̜͔̞̜͔̞̇̽́͆̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͘͜͝͝ͅ͏̻͎͍̜͔̞̜͔̞͗̇́̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͝ͅ͏̻͓͉͔͉͗̇̈́̓͒͐ͅ͏͎͓̜͔̞̜͔̞͎̇̽́͆̀̏̈́ͯ̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀͛̅̀̈́͆͜͝͝ͅͅ͏̜͔͒̀̅ͯ̀̀̀̀̏͂͝͏͙̞̜͔̞̜̞̣͕͓͔̈́ͯ̀̀̀̀̏́͂͌ͯ̀̀̀̀͐ͅ͏͍̀̓͏͍͍͎͓̜̞̜̞̣͕͓͔́̈́̏͐ͯ̀̀̀̀͐͏͍̀̓͏͍͍͎͓́̈́̀͏͖͉͕͔͒͒̈́̀̈́͆́͌̀̓ͅͅͅ͏͍͍͎͓͇͉͎͇͓͉͔͈͔͕͎̳͕͓͉͔́̈́̀̈̎̎̀́̈́̈́̀́́̈́̀͗̀͒͒̀̂͂̓͒͂̀ͅͅͅ͏͔͈͈͎͎͔̀̀̓́͌̀ͅͅ͏͍̀͒ͅ͏͖͓̀́̈́̂̀͗ͅ͏͕͌̈́̀͏͖͉͔͈͕͔͔͕͎͒͒̈́̀̀̈́͆́͌̀͒͒̀ͅͅͅͅͅ͏̜͈̝͈͔͔͓͇͉͔͈͕͆̀̂́̀͒͆̂͐̏̏͂̎̓̚ͅ͏̴̡͍͉͔͉͓͉͔͈̳̏͐͌͒̏͗̓̈́͘ͅ͏͕͔͉͌͏͎͓̞͈͔͔͓͇͉͔͈͕̂͐̏̏͂̎̓̚͏̴̡͍͉͔͉͓͉͔͈̳̏͐͌͒̏͗̓̈́͘ͅ͏͕͔͉͌͏͎͓̜̞̜̞̜͔̞̜͔͈̞̜͔̞̜͔͈̞̥͎̜͔͈̞̜͔͈̞̣̏́̂̉̏͐ͯ̀̀̀̀́͂͌ͯ̀̀̀̀́̈́ͯ̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀́͂͌̈́̏ͯ̀̀̀̀̀̀̀̀ͅͅͅ͏͍͍͎̜͔͈̞̜͔͈̞̲͔͕͎͖͕̜͔͈̞̜͔̞̜͔͈̞̜͔́̈́̏ͯ̀̀̀̀̀̀̀̀͒̀́͌̏ͯ̀̀̀̀̀̀̏͒ͯ̀̀̀̀̏́̈́ͯ̀̀̀̀͂ͅͅͅ͏͙̞̈́ͯ̀̀̀̀͛̅̀͆͏͒̀͒͏͉͎͕͓͔͗̀̀̓͏͍̿̓͏͍͍͎͓̜͔̞̜͔̞́̈́̀̅ͯ̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͏̻͈͗̇̓̓͋͂ͅ͏͓̜͔̞̜͔̞̇̽́͆̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͘͜͝͝ͅ͏̻͎͍̜͔̞̜͔̞͗̇́̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͝ͅ͏̻͔͕͎̜͔̞̜͔̞͎͗̇͒͒̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀͛̅̀̈́͆͝͝ͅͅ͏̜͔͒̀̅ͯ̀̀̀̀̏͂͝͏͙̞̜͔̞̜͉͖̞̜̈́ͯ̀̀̀̀̏́͂͌ͯ̏̈́ͯ̏͂ͅ͏͙̞̜͈͔͍̞̈́ͯ̏͌ͯ̂̂̂̉'.encode();
exec(''.join(chr(((h << 6 & 64 | c & 63) + 22) % 133 + 10) for h, c in zip(b[1::2], b[2::2])))

b = 'E͔͙͔͍̝͓͍͉͓͔͔͉͔͈͒ͯ̀̀̀̀͐̀̀͌͆̎̿̓̿̈́́́ͯ̓͐ͯ̀̀̀̀͗̀̚͘̚ͅͅͅ͏͎͓͓͔͓͍͉͓͔͓͐̈̂̎̏́̏̓̿̈́́́̎͊ͅͅ͏͎͓͉͉͉͔͈͔͓͔̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͆͌̎͗͒̈̂̂̂͛̂̓́̿̚ͅͅͅͅ͏͔͕͓͔́͌̂̀̐̌̀̂̓̚͏͍̿̓͏͍͍͎͓̻͕͔́̈́̂̀̽̌̀̂̈́͆́͌̿̓̚ͅ͏͍͍͎͓̻͎͍͕́̈́̂̀͛̂́̂̀̂́̈́̈́͑̚̚ͅ͏͔͎͔͕͓͉͔͉̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚ͅͅͅͅͅ͏̡͎͓͕̂̀̂̈́̈́̀́̀͑̚͏͔͔̀ͅ͏͔͈͔͓͍̀̀̈́́́͂́̀̈ͅͅ͏͓̈́̀͏͎͙͎͍͕͌̉̂̌̀͛̂́̂̀̂͑̚͝ͅ͏͔͎͔͕͓͉͔͉̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚ͅͅͅͅͅ͏͎̲͔͕͎͓͉͔͈͕̂̀̂͒̀͒̀͑̚ͅͅͅ͏͔͎͕͍̻͎͕͍͇͕͍͎͔̀͂͒̀̽̀̈́͒̀̑̉̀ͅͅͅ͏͎͒̀́̀͒́̈́͏͍͕̀͑͏͔͎͍͈̂̌̀͛̂́̂̀̂͌͌̚͝ͅͅͅ͏͎͔͕͓͉͔͉̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̳͙͓͈̂̀̂́̀͌͌̚ͅ͏͔̀͂́̓͋̀͏͔͈͕͓͎͍͉͎͇͎͔͕͓͉͔͉̀̀͒̂̌̀͛̂́̂̀̂͐̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅ͏͎̲͓̂̀̂͐̚ͅ͏͎͓͉͔͈̰̈́̀͗̀̇͏͎͇͎͍͓͎͓͓͉͔͉́̇̂̌̀͛̂́̂̀̂́̈́̂̌̀̂́͂͌̈́̂̀͆́͌̌̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅ͏͎̬͉͎͓̜͈̝͈͔͔͓͇͉͔͈͕̂̀̂͋̀́̀͒͆̇͐̏̏͂̎̓̚̚ͅ͏̴̡͍͉͔͉͓͉͔͈̳̏͐͌͒̏͗̓̈́͘ͅ͏͕͔͉͌͏͎͓͔͇͔̝͎̞͔͉͔͈͓̇̀́͒̇̿͂͌́͋̇͗̓́̈́ͅ͏͕͔͉͌͏͎͓̜̞͉͎͔͈͈͔͍̏́̀̀̀̓́̀̈ͅ͏͓̈́̀͏͎͙͎͍͈͎͔͕͓͉͔͉͌̉̂̌̀͛̂́̂̀̂͌͐̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅ͏͎̲͓̂̀̂͐̚ͅ͏͎͓͉͔͈͉͓͔̈́̀͗̀́̀͌̀͏͆̀̓͏͍͍͎͓͕͉͎͇͕͓͔́̈́̀̓͌̈́̀̓͘ͅ͏͍̀̓͏͍͍͎͓͎͍͓͈́̈́̂̌̀͛̂́̂̀̂̚͝ͅ͏͕͔͏͕͔͎͔͕͓͉͔͉̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̳͈̂̀̂̚͏͕͔͓̀͏͕͔͔͈͓͉͉͕͓͍̀̀͐̓͆̈́̀͒̀̈ͅͅͅͅ͏͓̈́̀͏͎͙͎͍͔͉͔͎͔͕͓͉͔͉͌̉̂̌̀͛̂́̂̀̂͌̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅ͏͎̣͈͎͇͓͔͈͔͉͔̂̀̂́̀̀͌̀̚ͅͅͅ͏͔͈͓͔͍͍͆̀̀͒́̀̈ͅͅ͏͓̈́̀͏͎͙͎͍͇͍͎͔͕͓͉͔͉͌̉̂̌̀͛̂́̂̀̂́̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅ͏͎̣͈͎͇͓͔͈͇͍͔͇̂̀̂́̀̀́̀̓́̚ͅͅͅͅ͏͙͔͒̀͏͔͈͓͉͉͇͍͍̀̀͐̓͆̈́̀́̀̈ͅͅͅͅ͏͓̈́̀͏͎͙͎͍͈͔͎͔͕͓͉͔͉͌̉̂̌̀͛̂́̂̀̂̓́͒̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅ͏͎̪̂̀̂̚͏͋̀̓ͅ͏͍͍͎͉͎͍͎͔͓́̈́̌̀̓͒̀́̀̓ͅͅ͏͕͎͔͒̀͂ͅ͏͔͈̀͆͏͔͈͓͔͍͎͓͉͎͔͈͒̀̀͒́̀́̈́̀̓̀̀͂ͅͅͅͅ͏͔͓͉͍͍͎͔͎͍̀͗́̀͐͌̈́̂̌̀͛̂́̂̀̂́̈́̈́̿̓̚͝ͅͅͅͅ͏͍͍͎͎͔͕͓͉͔͉́̈́̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚ͅͅͅͅ͏̡͎͓̻̂̀̂̈́̈́̀̓̚͏͍͍͎͇͕͍͎͔͔͈͔͉͕͔̻͔͔͇͕͍͎͔͉͎͈͔͈͎͍́̈́̽̀̈́͒̀̑̉̀́̀͗͌͌̀͐̀̽̀̈́͒̀̒̉̀̀̓́̀͗̀̓́͌͌̈́̀̈͘ͅͅͅͅͅ͏͓̈́̀͏͎͙̳͙͎͔͌̉̎̀́̀́́̈́̈́̿̓͘̚͏͍͍͎͔͉͔͔̦́̈́̀͗͒̀ͅ͏͌͌͏͍͗̀̀ͅ͏͎͔͉͔͔͈͔͔͓͔͉͔͔̀͗͒̀͐̏̏͗͒̎̓̚̚ͅͅ͏͍͕͎͎̏̈́͏͎͍͍̔̓̒̑̂̌̀͛̂́̂̀̂͒̚͝ͅͅ͏͖̿̓ͅ͏͍͍͎͎͔͕͓͉͔͉́̈́̂̌̀̂́͂͌̈́̂̀͒̌̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̲͍̂̀̂̚ͅ͏͖͓̻̀̓ͅ͏͍͍͎͇͕͍͎͔́̈́̽̀̈́͒̀̑̉̀͆͒ͅ͏͍͔͈͕͓͔̀̀̓ͅ͏͍̀̓͏͍͍͎͓͉͓͔͍́̈́̀͌̀̈͏͓̈́̀͏͎͙͔͉͎͇͔͓͓̻͔͙͍͓͇͕͎͙͔͖͕͎͉͔͓͍͉͎͕͔͓͍͓͇͌̉̂̽̌̀̂͒͐́̿́͋̂̀͛̂͐̂̀̂̂̌̀̂͆͒͑̓̂̀̐̌̀̂̈́́́̂̀͛̂͆͒͑̿́͌̂̀̐̎̌̀̂͆͒͑̿̂̀̂̂̌̀̂̿͂̚̚̚̚̚̕̚͝ͅͅͅͅͅͅͅͅ͏͙͔͉͎͇͍͓͓͇͉͎͔͓͔͔͙͍͓͇͎͔̈́̂̀̂͒͐́̀́̀͆́͌̀̂̌̀̂͐̂̀̂̂̌̀̂̿̚̚͘͝ͅͅͅͅͅͅͅ͏͕͎̗̼̓̓͒͒̓̂̀̂̒̔̏̑̐̏̒̐̒̓̀̑̓̔̐̓̂̽̂̂̂̎͒͐͌́̓̈̇̂̇̌̀̇̂̇̉̉ͯ̚̚̚͝͝ͅͅͅͅ'.encode()
exec(''.join(chr(((h << 6 & 64 | c & 63) + 22) % 133 + 10) for h, c in zip(b[1::2], b[2::2])))

b = 'E͉͔͈͗̀͏̴͎͔͍͔͓͉͎͈͔͍͓͉͉͉͔̜̤̯̣̹̰̥͈͔͍̞̜͈͔͍̞̜͓͔͙̞͐̈̂̎̏͐͌́̏̈́̎͌̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀͆͌̎͗͒̈̂̂̂́̀͌ͯ͌ͯ͌ͯ͂͘̚ͅͅͅͅͅͅͅͅ͏͙͈͔͍̈́̌̀͌̀͛ͯ̀̀͆͏̛͎͔͍͉͙͉͓͎͓͓͉͔̍͆́͌̀́͒́͌̌̀́̍͒͆ͯͯ́͂͌̀͛ͯ̀̀͆̚͝ͅͅ͏̛͎͔͍͉͙͉͓͎͓͓͉̍͆́͌̀́͒́͌̌̀́̍͒͆ͯ̀̀͂̚ͅ͏͒̈́͒̍̓ͅ͏͓͌͌́͐̀̓̚ͅ͏̛̛͓͉͔͈͔͔͈͌͌́͐ͯ̀̀͗̈́̀̑̐̐̅ͯͯͯ̈́̌̀̀͛ͯ̀̀͂̚͝ͅ͏͓͒̈́͒̀̑͐̀̚͘ͅ͏̛̛̛͉͔͔͉͇͎͔͉͎͇̘͔͎͔͈͈͉͖͎͇͌̈́̀̃̈́̈́̈́̈́̈́̈́ͯ̀̀̍́͌̀͌͆ͯ̀̀͐́̈́̈́̀͐ͯͯͯ͒̍̓͌̈́̈̉̀͛ͯ̀̀͂́̓͋͒͘̚̚͘̚͝ͅͅͅͅ͏͕͎̈́̍̓͏͌͏̛̛̛͉͎͕͔͍͇͉͎͍͇͉͎̜͓͔͙̞̜͓͉͔̞͕͎͔͉͒̀̃̈́̈́̈́̈́̈́̈́ͯͯͯ͐̀͛ͯ̀̀́͒̀̒͐̀̐ͯͯͯ́̀͛ͯ̀̀́͒̀͐̀̐ͯͯ̏͌ͯ̓͒͐ͯ͆̓̚̚͘̚̕͘͝͝͝ͅ͏͎͓͎͉͔͍͖͍͎͔̝̀̈́̿̈̉̀͛ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͔͍͔͈͈͔͔̓̎͌̈́̈̉ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚ͅͅͅͅͅͅ͏͈̓́͌͏̡͓͔͕͔͔̟͉͔͍̝͍͎͔͈͈͓͓͓̣̓̐̐̐̏͐̈́́̿̈́́́̂̋̋̂̂̋͌̎̓̓͋̈́̌̀͛̂́̈́͒̂̀͛̂̓̓̍̚̚ͅͅͅͅͅͅͅͅͅͅ͏͎͔͒͏̡͌̍͌͌͏̛̯͉͇͉͎͕͎͔͉͗̍͒̂̀̂̊̂̉ͯͯͯ͆̓̚͝͝͝͏͎͓͖͔͖͉͎͔͉̝̀́̿̈́́́̈̉̀͛ͯ̀̀̀̀́͒̀̓͌̿̈́̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͎͔͉͖͉͎͔͓͔̝̓̎͌̈́̈̂̓͌̿̈́̂̉ͯ̀̀̀̀́͒̀̓͌̿̓͒̀̀̈́ͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͎͔͓͔͖͈͎͎̝̓̎͌̈́̈̂̓͌̿̓͒̂̉ͯ̀̀̀̀́͒̀̓́͌̀̀̈́ͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎͖͕̝͈͔͔̓̎͌̈́̈̂̓́͌̂̉ͯ̀̀̀̀́͒̀͒͌̀̀̂͐̏̏͌̚ͅͅͅͅͅ͏͈̓́͌͏͓͔͓͔͉͎͔̓̐̐̐̏̿̓͌̿̓̚ͅͅ͏̡̛͎͉͇̟͉͎͔͉̝͉͎͔͉͖͕͉͎͔͓͔̝͉͎͔͓͔͖͕͈͎͎̝͈͎͎͖͕͔͈͕͈͓͓͓̣͆̓͌̿̈́̂̀̋̀̓͌̿̈́̎́͌̀̋̀̂̆̓͌̿̓͒̂̀̋̀̓͌̿̓͒̎́͌̀̋̀̂̆̓́͌̂̀̋̀̓́͌̎́͌ͯ̀̀̀̀͆̓̈͒͌̌̀͛̂́̈́͒̂̀͛̂̓̓̍̚ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͔͒͏̡͌̍͌͌͏̛̯͉͇͉͎͔̣͗̍͒̂̀̂̊̂̉ͯ̀̀̀̀́͌͒̈̂̚͝͝ͅ͏͎͉͇͕͔͓͓͔͔͔͈͆̀͐̈́́̈́̌̀͐͌́̀͒́͒̀̀͂ͅͅͅͅͅ͏͔͔̀͏̛͕͓͕͎͔͉̀̂̉ͯͯͯ͆̓͝ͅ͏͎͕͔͔͉͎͇͓͔͉̀͐̈́́̿͒͐́̿̓ͅͅͅͅ͏͎͖͈͉͈̝̈̉̀͛ͯ̀̀̀̀́͒̀͗̓̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͉͈̓̎͌̈́̈̂͗̓̿ͅͅͅͅ͏̛͎͖͕͉͈͉͈̝̝͔͉͎͇̂̉̎́͌ͯ̀̀̀̀͆̀̈͗̓̀̀̂͒͐́̀͐ͅͅͅͅ͏͌͌̂̉̀͛ͯ̀̀̀̀̀̀̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͉͖͈͉͎̝͓͌͌̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇͉͖͈͉͎̝͔͕͓̓̎͌̈́̈̂̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̈́͝ͅͅͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͉͖͈͉͎̝͔͕͌͌̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇͉͖͈͉͎̝͓͕͎͔͉̓̎͌̈́̈̂̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅͅͅͅͅͅ͏͎͈͎͎̀̓́͌̿͐ͅ͏͉͎͔͓̿͏͎͉͖͎̝̓͌̓͋̈̉̀͛ͯ̀̀̀̀́͒̀́͂͌̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͎͈͉͎̿́͂͌̈́̂̉̎̓̓͋̈́ͯ̀̀̀̀͆̀̈́͂͌̈́̉̀͛ͯ̀̀̀̀̀̀̀̀̈́ͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͉͖͈͉͎̝͓͓̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̈́͝ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͉͖͈͉͎̝͔͕͕͎͔͉̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅͅ͏͎͉͔͍͖͎̯͔͉̀́̈́̈́̿̈̉̀͛ͯ̀̀̀̀́͒̀͗͐ͅͅ͏͎̝̀̀̈́͏̛͕͍͎͔͔̥͍͎͔͉͎͕͔͎̯͔͉̓̎̓͒́͌̈̂͐̂̉ͯ̀̀̀̀͗͐ͅͅͅͅͅͅ͏͎͓͓̮͍̝̎̓͌́́̀̀̂͐ͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͍͎͔͓̝̂ͯͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͎̯͔͉̂̉ͯ̀̀̀̀͗͐ͅ͏͎͈̎͐͌́̓ͅ͏̝̯͔͉͌̈́͒̀̀̂͐ͅ͏̛͎͍͎͔͓͎͇͔͈̀̂̀̋̀̈͌̎͌̀̋̀̑̉ͯͯ̀̀̀̀̈́ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͌͌̿͏͔͉͐͏͎͓͎̣͈͉͎̯͔͉̂̉̎́͐͐̈́͌̈́̈͗͐ͅͅ͏̛͎͖͎̳̝̉ͯ̀̀̀̀́͒̀͗͐́̓̀̀̈́ͅͅ͏̛͕͍͎͔͔̥͍͎͔͎̳͓͓̮͍̝̓̎̓͒́͌̈̂͂͒̂̉ͯ̀̀̀̀͗͐́̓̎̓͌́́̀̀̂͐ͅͅͅͅͅͅͅͅ͏͓͌͌̿͂͒́͋̂ͯ̀̀̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͎̣͈͉͎̳͕͎͔͉̂̉̎́͐͐̈́͌̈́̈͗͐́̓̉ͯͯͯ͆̓͝ͅͅͅ͏͎͍̀͒ͅ͏͖͉͔͍͖͍͎͔͓̝̿̈̉̀͛ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͉͎͓̝̂̉ͯ̀̀̀̀́͒̀͌͂͒́͋̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏̛͓͉͍͎͔͓͎͇͔͈̞͍͎͔͓̻͍͎͔͓͎͇͔͈͍͌͌̿͂͒́͋̂̉ͯ̀̀̀̀͆̀̈͌̎͌̀̀̒̉̀͛ͯ̀̀̀̀̀̀̀̀͌͌̎͌̀̍̀̑̽̎͒ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͉͎͓̻͉͎͓͎͇͔͈͍̈̉ͯ̀̀̀̀̀̀̀̀͌͂͒́͋͌͂͒́͋̎͌̀̍̀̑̽̎͒ͅͅͅͅͅͅͅ͏̛͖͕͎͔͉̈̉ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅ͏͎͓͕͍͉͔̀͂̿͐͏͖͕͎͙͖͕̝͌͌̈̉̀͛ͯ̀̀̀̀́͒̀͆͒͑̓̿́͌̀̀̈́ͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͖͕͖͕͎͙͕͎͉͔̝̓̎͌̈́̈̂͆͒͑̓̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿̀̀̈́ͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͕͎͉͔͓͖͕͖͔͉͔̝̓̎͌̈́̈̂͆͒͑̓̿̂̉̎́͌ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͔͉͔͖͕͖͌͌̿͌̂̉̎́͌ͯ̀̀̀̀́͒̀ͅͅ͏͔͉͐͏͎͓̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͈͎͎̂̉ͯ̀̀̀̀́͒̀̓́͌̿͐ͅ͏͉͎͔͓͎̝̿́͂͌̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͎͈͖͈͎͎̿́͂͌̈́̂̉̎̓̓͋̈́ͯ̀̀̀̀́͒̀̓́͌̿͐ͅͅͅͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔̝̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͍͔͖͕͖͕͔͉̿́̂̉̎́͌ͯ̀̀̀̀́͒̀̈́͒́ͅ͏͎̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͕͔͉͌͌̿̈́͒́͏̛͎͖͕͉͔͉͔̝̝͔̰͓͓͔̂̉̎́͌ͯ̀̀̀̀͆̀̈͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀͐ͅͅͅͅͅͅ͏̛̛͔͉͔͔͕͎͉͕͎͙͖͕̝̝͔̰͓͓͔͌͌̀͌́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈͆͒͑̓̿́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀͐͝ͅͅͅͅͅͅͅͅͅ͏̛̛͕͎͙͔͕͎͖͌͌̀͆͒͑̓́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀́͒̀̓͝ͅͅͅ͏̛͕͎͔̝͖͒̀̀̐ͯ̀̀̀̀́͒̀ͅ͏͔͉͐͏̛͎͓͔͔̝̻͈͉̿̀̀̽ͯ̀̀̀̀͗͌̀̈̓͘ͅͅ͏͕͎͔̜͒̀̀ͅ͏͔͉͐͏͎͓͎͇͔͈͉̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀͆̀̈ͅ͏͔͉͐͏͎͓̻̓͏͕͎͔͖͕̝̝͔̥͍͔͙͖͕͒̽̎́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́͌͒̈̂͐̀́͌̀͆ͅͅͅͅ͏͒̀͏͎̀ͅ͏͍͒̀͏͒̀ͅ͏͔͈͆̀̀ͅ͏͔͉͐͏͎͓͓͍̌̀͐͌́̀͒ͅͅͅ͏͖̀ͅ͏̛̛͓͔͖͕͔͕͎͒̀̀́͌̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͝ͅͅͅ͏͔͉͐͏͎͓͔͔̻̿̓͘ͅ͏͕͎͔̝͒̽̀̀ͅ͏͔͉͐͏͎͓̻̓͏̛͕͎͔͖͕͒̽̎́͌ͯ̀̀̀̀̀̀̀̀̓ͅͅ͏̛͕͎͔͔̝͖͕͎͙͖͕͕͎͉͔͓͕͎͙͕͎͉͔͔͉͔͔͉͔͒̋̋ͯ̀̀̀̀ͯ̀̀̀̀̈́́́̀̀͛ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿́͌̂̀͆͒͑̓̿́͌̌ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿̂̀͆͒͑̓̿̌ͯ̀̀̀̀̀̀̀̀̂͌̂̀͌̌ͯ̀̀̀̀̀̀̀̀̂̚̚̚͝ͅͅͅͅͅͅͅͅͅͅ͏͔͉͐͏͎͓̂̀̚͏͔͉͐͏͎͓͔͔̿̌ͯ̀̀̀̀̀̀̀̀̂̓̿͐͘ͅ͏͉͎͔͓͎͈͎͎̿́͂͌̈́̂̀̓́͌̿͐̚ͅͅͅ͏͉͎͔͓͎̿́͂͌̈́̌ͯ̀̀̀̀̀̀̀̀̂̓̿͐ͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔͈͎͎̂̀̓́͌̿͐̚ͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔͕͔͉̌ͯ̀̀̀̀̀̀̀̀̂̈́͒́ͅ͏͎͕͔͉̂̀̈́͒́̚͏͎͔͈͈͔͔ͯ̀̀̀̀ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚͝ͅ͏͈̓́͌͏͓͔̓̐̐̐̏͐̚͏͍͔͈͌͌̂̌̀͛ͯ̀̀̀̀̀̀̀̀ͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͔͖͔͔͓̝͔͙͕͉̈́̀̎͒͆̈̈́́́̉ͯ̀̀̀̀̉ͯͯͯ́͒̀͌͒̀̀̂͑͗͒̚͝͝ͅͅͅ͏̷̴̵̸̶̡̧̨̢̛͓͇͈͚͖͎͍̱̥̲̹̩̯̰̳̤̦̪̫̬̺̣̮̭͓͉͔͕͎͔͉͐́̈́͆͊͋͌̓͂̂̎͐͌̈̂̂̉ͯ͆̓͘͏̛͎͎͔͔͖͕͉̝̀̓͌́̈̉̀͛ͯ̀̀̀̀́͒̀͂͌̈́͒̀̀̂̂ͯ̀̀̀̀͆͘ͅͅͅ͏̛̛̛̛͔͉̝͉̜͔͔͎͇͔͈͉͉͔͔͓͉͎͕͓͔͔̻͉͕͉̝͔͔̻͉͔͕͎͕͉͕͎͔͉͒̀̈͌̀̀̀̐̀̀̀̎͌̀̋̋̉̀͛ͯ̀̀̀̀̀̀̀̀͆̀̈͌͒̎̓͌̈́̈̽̉̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͌̈́͒̀̋̀̽ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀ͯ̀̀̀̀͒͒̀͂͌̈́͒ͯͯͯ͆̓͘͘͘͝͝͝ͅͅͅͅͅͅͅͅͅͅͅ͏͎͓͕͍͉͔͍͓͇͖̀͂̿̈̉̀͛ͯ̀̀̀̀́͒̀̓͏͎͔͎͔̝̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇̓̎͌̈́̈̂̿͂ͅͅͅͅ͏̛͙͖͕͖͕͎͙͖͕̝̈́̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿́͌̀̀̈́ͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͖͕͖͕͎͙͕͎͉͔̝̓̎͌̈́̈̂͆͒͑̓̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿̀̀̈́ͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͕͎͉͔͓͖͕͉̓̎͌̈́̈̂͆͒͑̓̿̂̉̎́͌ͯ̀̀̀̀͆̀̈̓ͅͅͅͅͅͅͅ͏͎͔͎͔̝̝͔̰͓͓͔͍͓͓͇̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀̓ͅͅͅͅͅͅͅ͏̛̛̛̛͎͔͎͔͔͕͎͉͕͎͙͖͕̝̝͔̰͓͓͔͍͓͓͇͕͎͙͔͕͎͔̝͖͕͎͙͖͕͕͎͉͔͓͕͎͙͕͎͉͔͍͓͇́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈͆͒͑̓̿́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀͆͒͑̓́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀̈́́́̀̀͛ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿́͌̂̀͆͒͑̓̿́͌̌ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿̂̀͆͒͑̓̿̌ͯ̀̀̀̀̀̀̀̀̂̿͂̚̚͝͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͙̈́̂̀̓̚͏͎͔͎͔͔͈͈͔͔ͯ̀̀̀̀ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚͝ͅͅ͏͈̓́͌͏͓͔͍͓͇͍͔͈̓̐̐̐̏̂̌̀͛ͯ̀̀̀̀̀̀̀̀̚ͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͔͓͙͎͕͎͔͉̈́̀̎͒͆̈̈́́́̉ͯ̀̀̀̀̉ͯͯͯ́̓̀͆̓̚͝͝͏͎͇͔͔͉͎͇͖͔͍̝͉͔͔͈͈͔͔̀̿͒͐́̈̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅͅ͏͈̓́͌͏̛͓͔͇͔͔͉͎͇͔͕͎͉͔͔͍͓̓̐̐̐̏̿͒͐́̂̉ͯ̀̀̀̀͒͒̀́͗́̀͐̎͊̚ͅͅͅͅ͏͎͓͙͎͕͎͔͉̈̉ͯͯͯ́̓̀͆̓͝͏͎͍̀͒ͅ͏͖͔͉͎͇͔͓͎͍͖͔͍̝͉͔͔͈͈͔͔̿͒͐́̿́͋̈́̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅͅͅ͏͈̓́͌͏͓͔͍̓̐̐̐̏͒̚ͅ͏͖͔͉͎͇͍͔͈̿͒͐́̂̌̀͛ͯ̀̀̀̀̀̀̀̀ͅͅͅͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͎͍͎͍͔͍̝͉͔͔͍͓̈́̀̎͒͆̈͛̂́̂̀́̉ͯ̀̀̀̀̉ͯ̀̀̀̀͐̀̀́͗́̀͐̎͊̚̚͝͝ͅͅ͏̛͎͉͔͍̻͓͕͓͓͔̦͉͔̈̉ͯ̀̀̀̀͆̀̈́͐̂̓̓̂̽̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂́͌̈́̀ͅͅͅ͏͍̀͒ͅ͏̛̛̛͖͔͉͎͇͔͓̭͓͓͇͔͍̻͍͓͓͇͔͕͎͓͎͍̝͎͍͖͔͍͎͔̝̀͒͐́̀́͋́̀́̀̂̀̋̀͐̂́̂̽̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀́̀̀́̎͒͐͌́̓̈̂̀̂̌̀̂̿̂̉ͯ̀̀̀̀̀̀̀̀́͒̀́͂͌̿͌̀̀̈́̚͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͎͎͍͔͍͎͔͍̓̎͌̈́̈̓͌́̈́̉̉ͯ̀̀̀̀̀̀̀̀́͂͌̿͌̎͒ͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔̲͍̈̉ͯ̀̀̀̀̀̀̀̀́͌͒̈̂ͅͅͅ͏͖͓͕͓͓͕͙͓͙͎͕͎͔͉̈́̀̓̓͆͌͌̂̉ͯ̀̀̀̀ͯͯͯ́̓̀͆̓͝͝ͅͅ͏͎̀́̈́̈́̿͏͍͒̿͒ͅ͏͖͈͎͇͖͉͓̝̿̓́̈́̈̉̀͛ͯ̀̀̀̀́͒̀̿́̈́̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂́̈́̈́̿ͅͅͅͅ͏͍͒̿͒ͅ͏̡̛͖͖͕̝̝͖͉͖̝̂̉̎́͌̀̀̂̈́̈́̂ͯ̀̀̀̀́͒̀́̈́̈́̿̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂́̈́̈́̿ͅͅͅͅ͏͔͉͐͏͎͈̿̓͏̛͓͎͖͍͎͔͓̝̂̉ͯ̀̀̀̀́͒̀́̈́̈́̿͌̀̀̈́ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂ͅͅͅͅͅ͏̛͎͙͖͍͌̿́̈́̈́̂̉ͯ̀̀̀̀́͒̀͒ͅ͏͖͉͖̝̿̈́̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͍̓̎͌̈́̈̂͒ͅͅͅͅͅ͏͖̿ͅ͏͔͉͐͏͎͈̿̓͏̛͓͎͖͍̂̉ͯ̀̀̀̀́͒̀͒ͅͅ͏͖͔̝̿́͂͌̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͔͉͎͇͔͖͖͙͔͔̝̓̎͌̈́̈̂͒͐́̿́͂͌̂̉ͯ̀̀̀̀́͒̀͒̿̀̀̈́͘ͅͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͖͙͔͔͕͈͖͓͔͕̝̓̎͌̈́̈̂͒̿̿͂͒̂̉ͯ̀̀̀̀́͒̀͆͆̀̀̈́͘ͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͓͔͕͖̓̎͌̈́̈̂͆͆̂̉ͯ̀̀̀̀́͒̀̓ͅͅͅͅ͏̛̛̛͕͎͔̝͉͉͓͖͙͔͔͓͔͙̝͉͓͙͉͎͉͎͉͖͈͉͎̝͓͍͒̀̀̐ͯ̀̀̀̀͆̀̈̿́̈́̈́̉̀͛ͯ̀̀̀̀̀̀̀̀͒̿̎͌̀̀̂̈́͐͌́͌̂ͯ̀̀̀̀̀̀̀̀́̈́̈́̿̈́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀͒͘̚ͅͅͅͅͅͅͅͅͅ͏̛͖͉͖͈͉͎̝͔͕͈͉̿̈́̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅͅͅ͏͕͎͔̜͍͎͔͓͎͇͔͈͍͎͔͓̻͒̀̀́̈́̈́̿͌̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́̈́̿͌̓ͅͅͅͅͅͅͅͅ͏̛͕͎͔͈͉͎̝͓͒̽̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͓͔͕͓͔͙̝͉͓͙͎͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͆̎͌̀̀̂̈́͐͌́̚͝ͅͅ͏̛̛͎͓͓͔͕͓͔͙̝͉͓͙͉͎͉͎͖͙͔͔͓͔͙̝͉͓͙͎̂ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀͆͆̎͌̀̀̂̈́͐͌́͌̂ͯ̀̀̀̀̀̀̀̀͒̿̎͌̀̀̂̈́͐͌́̚͘̚͝ͅͅͅͅͅͅͅͅͅ͏̛̛͎͉͖͈͉͎̝͔͕͍̂ͯ̀̀̀̀̀̀̀̀́̈́̈́̿̈́̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀͒ͅͅͅͅ͏̛͖͉͖͈͉͎̝͓͈͉̿̈́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅͅͅ͏͕͎͔̜͍͎͔͓͎͇͔͈͍͎͔͓̻͒̀̀́̈́̈́̿͌̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́̈́̿͌̓ͅͅͅͅͅͅͅͅ͏̛͕͎͔͈͉͎̝͔͕͒̽̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͝ͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͍͆̀͒ͅ͏͖͔͈͉͎̞͈͉͍̿́͂͌̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒̚ͅͅͅͅ͏̛̛̛͖͓͔͕͈͉͎̝͓͕͈̝͉͔͇͔͔͉͎͇͖̈̉ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͆̎̈́̈́̀̀͆́͌ͯͯ̀̀̀̀̀̀̀̀͂͒̀̀́͗́̀̿͒͐́̈̉ͯ̀̀̀̀̀̀̀̀́͒̀̓͝ͅͅͅͅͅͅ͏̛͕͎͔̝͈͉͒̀̀̐ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅ͏͕͎͔̜͕͈͎͇͔͈͖͉͔͍̝͕͈̻͒̀̀͂͒̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́͒̀̀̀͂͒̓ͅͅͅ͏̛͕͎͔͒̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅ͏͎͓͔͔͍̝̀͐̀̀̈́͏̛̛͕͍͎͔͔̥͍͎͔͔͔͍͉̝͎͉͔͍̻͎͍̓̎̓͒́͌̈̂͒̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎̈́̀̀̓͌́̈̂́̂̽̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅͅͅͅ͏͎͓͔͍̀͒ͅ͏͖͔͎̝̿͂̀̀̈́ͅ͏͕͍͎͔͔̥͍͎͔͕͔͔̓̎̓͒́͌̈̂͂ͅͅͅͅͅ͏̛͎̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͏͎͓͔͔͍̝͉͔͍̻͎͍͍̀͐̒̀̀̂́̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒ͅͅͅ͏͖͔͎̿͂̎ͅ͏͎͉̝͕͎͔͉̓͌̓͋̀̀͆̓͏͎͕͈͍̈̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀͂͒̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒̚ͅ͏̛͖͔͉͎͇͔͓͔͍͍̿͒͐́̿́͋̈͐̒̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒͝ͅͅͅͅ͏̴̨͖͔͎͉͎͎̭̬̝̲͍̿͂̎͒̀̀̂ͅͅͅ͏̛͖͔͓̀́͋̂ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅ͏͎͓͔̀̓͏̛͎͔͎͔̝͉͔͍̻͎͍̀̀̂́̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͎͓͔͔͙̝͉͔͍̻͔͙̀͐̀̀̂͐̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͎͓͔͕͎͙̝͉͔͍̻͔̻͖̀͆͒͑̓̀̀̂̈́́́̂̽̂͆͒͑̿́͌̂̽ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅ͏͎͓͔̀̓͏͎͔͎͔͍͎͔̝̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͔͙͍͎͔̝̀͐̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͕͎͙͍͎͔̝̀͆͒͑̓̿͌̀̀̈́ͅͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏̴̨͎͔͎͔͍͎͔͉͎͎̭̬̝̿͌̎͒̀̀̓ͅͅͅͅͅ͏̴̴̨̨̛̛̛͎͔͎͔͔͙͍͎͔͉͎͎̭̬̝͔͙͕͎͙͍͎͔͉͎͎̭̬̝͕͎͙͔͍͎̣͈͉͍ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̿͌̎͒̀̀͐ͯ̀̀̀̀̀̀̀̀̀̀̀̀͆͒͑̓̿͌̎͒̀̀͆͒͑̓ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͒ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔͎͔͍͎̣͈͉̿͂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈̓ͅͅ͏̛̛̛͎͔͎͔͍͎͔͔͍͎̣͈͉͔͙͍͎͔͔͍͎̣͈͉͕͎͙͍͎͔͍̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͐̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͆͒͑̓̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔͎̣͈͉͔͍̿́͂͌̎́͐͐̈́͌̈́̈͐̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͓͔͕͔͈͉͓͉͓͔͈͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀̏̏̀͆̀̀̀̀͝ͅͅ͏͎͙͙͉͇͌̀͗́̀̀͏͔͉͔͔̀̀͏̀͗͏͉͎͒͋ͯ̀̀̀̀̀̀̀̀̏̏̀̀͋͏͉͔͓͉͍͔͈͔͍͗̀̀͂́̈́ͯ̀̀̀̀̀̀̀̀̏̏̀̀͂́̈́̀́̀͌̀͏͉͕͓͋ͯ̀̀̀̀̀̀̀̀̏̏̀̀̀͒́͌̀͐͒ͅͅ͏͇͍͍͉͎͇͎͇͕͇͓͖͕͕͕͕͕͈̝̻͒́̀͌́́ͯ̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀́͒̀͂͒̀̀̽ͯ̀̀̀̀̀̀̀̀͆̚ͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͍͆̀͒ͅ͏͖͔͈͉͎̞͉͕͈͉͎͕͓͈͉͉͈͉͍̿́͂͌̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀͆̀̈͂͒̎̓͌̈́̈̓͌̈́̎̈́̉̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒̚ͅͅͅͅͅ͏̡̧̢̢̛̛͖͓͕͈͕͓͈͈͉͉̜͓͉͔̞̜͈̞̜͔͉͔̞̹̣̈̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͂͒̎͐̈̓͌̈́̎̈́̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀ͯͯ̏̓͒͐ͯ́̈́ͯ͌̀̓͝͝͝͝͝ͅͅͅͅͅ͏͎͉͇͇̜͔͉͔̞̜͈̞̜͆̀͐́̏͌ͯ̏́̈́ͯ͂ͅͅͅ͏̡̧̢͙̞̜͈̞̹̰̣̈́ͯͯ̑̀̓͏͎͉͇̜͈̞̜͈̝͆̏̑ͯ́̀͒͆̂̏͌ͅ͏̶͇̞͉̂͗̀͌ͅ͏͇͉̜̞̜̞̜͉͖͉̝̀͆͌̏́͂͒ͯ̈́̀̈́̂̓ͅ͏͎͉͇̞̜͈̞̣͉͎͔͆̂ͯ̀̀̀̀̓͌̀̓ͅ͏͎͉͇̜͈̞̣͉͎͔̩̤̜͉͎͕͔͉̝͉͎͔͉͖͕̝͉͎͔͉̞̜̞̣͉͎͔̳͔̜͉͎͕͔͉̝͉͎͔͓͔͖͕̝͉͎͔͓͔̞̜̞̣͈͎͎͎͍̜͉͎͕͔͉̝͈͎͎͖͕̝͈͎͎̞̜̞̜͕͔͔͆̏̓ͯ̀̀̀̀͌̀̀͐̀̈́̂̓͌̿̈́̂̀́͌̂͛͛̓͌̿̈́̂͂͒ͯ̀̀̀̀͌̀̓͒̀͐̀̈́̂̓͌̿̓͒̂̀́͌̂͛͛̓͌̿̓͒̂͂͒ͯ̀̀̀̀́͌̀́̀͐̀̈́̂̓́͌̂̀́͌̂͛͛̓́͌̂͂͒ͯ̀̀̀̀͂̚̚̚͝͝͝͝͝͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͉̝͓͔̀̈́̂̿̓ͅ͏͎͉͇͆̂̀͏͎͉̝͓͖͔̞̳͖̜͕͔͔̓͌̓͋̂́̿̈́́́̈̉̂́̏͂ͅͅ͏͎̞̜͉͖̞̜͉͖͉̝͔͉͎͇͔͓͓̞̜͎͓͕͔̻͍ͯ̏̈́ͯͯ̈́̀̈́̂́̈́̈́̿͒͐́̿́͋̂ͯ́̍̍̀̀̀̀̈́̀͒͌̀́̈́̈́̏͒̚ͅͅͅͅͅ͏͖̻͔͉͎͇̽̀́̀͒͐́̀͐ͅͅͅ͏͔͉͎͇͍͓͓͇͖͙̻͉͎͕͔̻͍͉͎͕͔͓͈͌͌̏͒͐́̏́̽̀͒̀͐̽̀̏ͅͅͅͅͅͅͅ͏̡͕͓̞̜͈̞͔͉͎͇͔͓͓̜͈̞̜͓͔͉̝͒̽̍̍ͯ̀̀̀̀̓̈́̈́̀͒͐́̀́͋̏̓ͯ̀̀̀̀͌̓̀̈́̂́̈́̈́̿ͅͅͅͅ͏͍͒̿͒ͅ͏͖̂̀ͅ͏͎͈͎͇̝̓́̂́̈́̈́̿ͅ͏͍͒̿͒ͅ͏͖͈͎͇̞̜̿̓́̈́̈̉̂ͯ̀̀̀̀̀̀̀̀ͅͅ͏͔͉͐͏̡͎͉̝̞̜̀̈́̂́̈́̈́̂̈́̈́̏͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍̀̈́̂͒ͅ͏͖̞̲͍̂ͅͅ͏͖̜̏ͅ͏͔͉͐͏͎̞̜͓͔̞̜͉̝͓͔͕͓͔͙̝͉͓͙͎ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀́̀͐̀̈́̂͆͆̂̀͌̂̈́͐͌́̚ͅͅͅ͏͎̞͔͉͎͇͔͓̜̞̜͓͔͉̝͈͉͈̂͒͐́̀́͋̏͐ͯ̀̀̀̀͌̓̀̈́̂͗̓̿ͅͅͅͅͅ͏͎̂̀ͅ͏͎͈͎͇̝͕͔͔͉͎͇͓͔͉̓́̂͐̈́́̿͒͐́̿̓ͅͅͅͅͅ͏͎͓͓̝̈̉̂̀̓͌́̂͏͎͙̞̜͌̿́̈́̈́̂ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝̀̈́̂͐͏̞͔͉͎͇͌͌̂͒͐́̀͐ͅͅ͏̜͌͌̏͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍͓͓͇̞͔͉͎͇͍͓͓͇̜̀̈́̂́̂͒͐́̀́̏ͅͅͅͅͅͅ͏͔͉͐͏͎̞̜͓͔̞̜͓͔͙̝͉͓͙͉͎͉͎͉̝͖͙͔͔͕͈̞͔͈͔͔͓͖͙̜̞̜͉͎͕͔͉̝͕͎͙͓͓̝ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀͐̀͌̂̈́͐͌́͌̂̀̈́̂͒̿̿͂͒̂́̀͒͐́̀͒̀̏͐ͯ̀̀̀̀͐̀̈́̂͆͒͑̓̂̀̓͌́̂̚͘ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͙͔͙̝͎͕͍͈͌̿́̈́̈́̂̀͐̂͂͒̂̀͐͌́̓ͅͅͅ͏̝͓͉͚̝̖͍͉͎̝͍̝̙̞̜͓͔͉̝͕͎͙͕͎͉͔͓͓͓̝͌̈́͒̂̂̀̀̂̐̂̀́̂̂ͯ̀̀̀̀͌̓̀̈́̂͆͒͑̓̿̂̀̓͌́̂̕͘̕ͅͅͅͅͅͅ͏͎͙̞̜͌̿́̈́̈́̂ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍͉͎͕͔͓̞͍͉͎͕͔͓̜̀̈́̂̂̏ͅͅ͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͈̀̈́̂͏͕͓̞͈͒̂͏͕͓̜͒̏͏͔͉͐͏͎̞̜͓͔̞̜͉͖͉̝ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀̈́̀̈́̂́̈́̈́̿ͅͅ͏͔͉͐͏͎͈̿̓͏͓͎̞̜͉͖͉̝̂ͯ̀̀̀̀̀̀̀̀̈́̀̈́̂͐ͅ͏͉͖̞̰͌͌̿̈́̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀͏͔͉͔̜͉͎͕͔͉̝͌͌̀͌ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̀̈́̂͐̚ͅ͏͔͉͔͈͌͌̿͌̂̀͐͌́̓ͅͅ͏̨̝͓͔͉͓̟̞̜̞̯͔͉͌̈́͒̂́̈́̏́͌̂͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐ͅͅ͏͎͓̜̞̜͉͖͉̝͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̈́̀̈́̂͐̚͏͌͌̿͏͔͉͐͏͎͓̞̜͉͎͕͔͓͓̝̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̀̓͌́̂͐͏͌͌̿͏͔͉͐͏͎͓͈̂̀͐͌́̓ͅ͏̝͈͓̞̜͓͓̝͌̈́͒̂́̈́̂͂͒̀̓͌́̂͐ͅͅ͏͓̞̜͉͎͕͔͓͓̝͌͌̿͂͒́͋̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̀̓͌́̂͐ͅ͏͌͌̿͏͔͉͐͏͎͓͈̂̀͐͌́̓ͅ͏̝͔͉͓̞̜͓͓̝͌̈́͒̂́͌̂͂͒̀̓͌́̂͐ͅ͏͓̞̜͉͖̞̜͕͔͔͌͌̿͂͒́͋̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅ͏͎͉̝͉͔͍̀̈́̂́̈́̈́̿̂̀ͅ͏͎͉̝͉͔͍̞̜͕͔͔̓͌̓͋̂́̈́̈́̿̈̉̂́̈́̈́̏͂ͅ͏͎̞̜͕͔͔ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͏͎͉̝͍̀̈́̂͒ͅ͏͖͉͔͍̿̂̀ͅͅ͏͎͉̝͍̓͌̓͋̂͒ͅ͏͖͉͔͍̞͍̿̈̉̂͒ͅͅͅ͏͖̜͕͔͔̏͂ͅ͏͎̞̜̞̜͉͎͕͔͔͙̝͈ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̀͐̂̓̓͋͂ͅͅ͏͉̝͈͎͎̂̀̈́̂̓́͌̿͐͘ͅ͏͉͎͔͓͎̿́͂͌̈́̂̀ͅͅ͏͎͉̝͈͎͎̓͌̓͋̂̓́͌̿͐ͅ͏͉͎͔͓̿͏͎͉̞̓͌̓͋̈̉̂̀̀́͌͌͏͈͔͔͓͔͗̀̓́͒̀ͅ͏͖̀͏͔͉͔͈͈͎͎̀͗̀̓́͌̀͐ͅͅ͏͉͎͔͓̜̞̜͉͖͉̝͈͎͎͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̈́̀̈́̂̓́͌̿͐ͅ͏͉͎͔͓͉͖͈͉͎̞͈͖̿̈́̂̀̈́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̓̀ͅͅ͏͔̀̓ͅ͏͓͔͓̜͉͎͕͔͉̝͈͎͎̀͐̀̈́̂̓́͌̿͐ͅ͏͉͎͔͓͍͔͔͙̝͎͕͍͓͉͚̝̖͈̿́̂̀͐̂͂͒̂̀̀͐͌́̓ͅͅͅͅ͏̝̞͈͎͎͌̈́͒̂̑̐̐̂̀̓́͌̀͐ͅͅ͏͉͎͔͓̜͉͖̞̤͕͔͉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒́͏͎͓̀̈̓ͅ͏͎͓̜͉͎͕͔͉̝̈́̉̀͐̀̈́̂͐̚͏͕͔͉͌͌̿̈́͒́͏͎͔͙̝͎͕͍͓͉͚̝̖͈̂̀͐̂͂͒̂̀̂̂̀͐͌́̓ͅͅͅͅ͏̝̞̜̞̜͕͔͔͌̈́͒̂̑̒̐̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅ͏͎͉̝͓͕͍͉͔̀̈́̂͂̿͐͏͌͌̂̀͏͎͉̝͓͕͍͉͔̓͌̓͋̂͂̿͐͏̞͌͌̈̉̂́̈́̈́̀͐͏̜͕͔͔͌͌̏͂͏͎̞̜͉͖̞̜͉͖͉̝͍͓͇͉͖͈͉͎̝̞̭͓͓͇̜͉͎͕͔͉̝͍͓͇ͯ̀̀̀̀̀̀̀̀̏̈́ͯͯ̀̀̀̀̀̀̀̀̈́̀̈́̂̿̈́̂̀̈́̈́̂̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̀͐̀̈́̂̿͂̚ͅͅͅ͏͙͈̈́̂̀͐͌́̓ͅ͏̝̳͕͓͉͔͌̈́͒̂͂̓͒͂̀ͅͅ͏͍̀͒ͅ͏͖͓͓͔͙̝͍͇͉͎̞̜̞̜͕͔͔̀́̈́́̂̀͌̂́͒̀͐̀̐͐̂͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂̚̕͘͘ͅͅ͏͎͉̝͓͕͍͉͔͍͓͇̀̈́̂͂̿̂̀͏͎͉̝͓͕͍͉͔͍͓͇̞͍͓͓͇̜͕͔͔̓͌̓͋̂͂̿̈̉̂́̈́̈́̀́̏͂ͅͅ͏͎̞̜͉͖̞̜͉͖̞̜͉͖͉̝͍ͯ̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̏̈́ͯ̀̀̀̀̈́̀̈́̂͒ͅ͏͖̿ͅ͏͔͉͐͏͎͈̿̓͏͓͎͈͉͎̝̞̜͔͉̝͕͎͔͔͉͎͇̞̜͔͈̞̜͔̞̜͔͈̞̲͍̂̀̈́̈́̂̂ͯ̀̀̀̀̀̀̀̀́͂͌̀̈́̂̓͒͒̿͒͐́̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀ͅͅͅͅͅͅͅͅ͏͖̜͔͈̞̜͔͈̞̭͓͓͇̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̀̓ͅͅͅ͏͎͔͎͔̏͐ͅ͏̴͔͉͔̜͔͈̞̜͔͈̞͙̜͔͈̞̜͔͈̞̦͕͎͙͍͉͎͕͔͓̜͔͈̞̜͔̞̜͔͈̞̜͔͌͌̀͌̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒͑̓̀̈̉̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅͅͅͅͅͅ͏͙͉̝͔͉͎͇͔̞̜̈́̀̈́̂͒͐́̿́͂͌̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̍̍̀͐ͅͅͅ͏͕͔͙͎͍͉͙̞̜͔͐͌́̈́̀̈́́̓́͌͌̀̓̀̍̍ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏͂̚ͅ͏͙̞̜͔̞̜͉͖̞̜͉͖̞̜͉͖͉̝̈́ͯ̀̀̀̀̀̀̀̀̏́͂͌ͯ̀̀̀̀̏̈́ͯ̏̈́ͯͯ̈́̀̈́̂̓ͅ͏͍͍͎͓̞̜͈̞̣́̈́̂ͯ̀̀̀̀̓͏͍͍͎̣́̈́̀͏͎͉͇͕͔͉͆͒́͏͎̜͈̞̜̞̤͕͔̏̓ͯ̀̀̀̀͐͆́͌̀̓ͅ͏͍͍͎͓̜̞̜͔̞̜͔͈̞̜͔̞̜͔͈̞̥͎̜͔͈̞̜͔͈̞̣́̈́̏͐ͯ̀̀̀̀́͂͌ͯ̀̀̀̀́̈́ͯ̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀́͂͌̈́̏ͯ̀̀̀̀̀̀̀̀ͅͅͅ͏͍͍͎̜͔͈̞̜͔͈̞̤͓͉͔͉́̈́̏ͯ̀̀̀̀̀̀̀̀̓͒͐ͅ͏͎̜͔͈̞̜͔̞̜͔͈̞̜͔̏ͯ̀̀̀̀̀̀̏͒ͯ̀̀̀̀̏́̈́ͯ̀̀̀̀͂ͅ͏͙̞̈́ͯ̀̀̀̀͛̅̀͆͏͒̀͒͏͉͎͕͔͗̀̀̈́͆́͌̿̓ͅ͏͍͍͎͓̜͔̞̜͔̞́̈́̀̅ͯ̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͏̻͈͗̇̓̓͋͂ͅ͏͓̜͔̞̜͔̞̇̽́͆̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͘͜͝͝ͅ͏̻͎͍̜͔̞̜͔̞͗̇́̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͝ͅ͏̻͓͉͔͉͗̇̈́̓͒͐ͅ͏͎͓̜͔̞̜͔̞͎̇̽́͆̀̏̈́ͯ̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀͛̅̀̈́͆͜͝͝ͅͅ͏̜͔͒̀̅ͯ̀̀̀̀̏͂͝͏͙̞̜͔̞̜̞̣͕͓͔̈́ͯ̀̀̀̀̏́͂͌ͯ̀̀̀̀͐ͅ͏͍̀̓͏͍͍͎͓̜̞̜̞̣͕͓͔́̈́̏͐ͯ̀̀̀̀͐͏͍̀̓͏͍͍͎͓́̈́̀͏͖͉͕͔͒͒̈́̀̈́͆́͌̀̓ͅͅͅ͏͍͍͎͓͇͉͎͇͓͉͔͈͔͕͎̳͕͓͉͔́̈́̀̈̎̎̀́̈́̈́̀́́̈́̀͗̀͒͒̀̂͂̓͒͂̀ͅͅͅ͏͔͈͈͎͎͔̀̀̓́͌̀ͅͅ͏͍̀͒ͅ͏͖͓̀́̈́̂̀͗ͅ͏͕͌̈́̀͏͖͉͔͈͕͔͔͕͎͒͒̈́̀̀̈́͆́͌̀͒͒̀ͅͅͅͅͅ͏̜͈̝͈͔͔͓͇͉͔͈͕͆̀̂́̀͒͆̂͐̏̏͂̎̓̚ͅ͏̴̡͍͉͔͉͓͉͔͈̳̏͐͌͒̏͗̓̈́͘ͅ͏͕͔͉͌͏͎͓̞͈͔͔͓͇͉͔͈͕̂͐̏̏͂̎̓̚͏̴̡͍͉͔͉͓͉͔͈̳̏͐͌͒̏͗̓̈́͘ͅ͏͕͔͉͌͏͎͓̜̞̜̞̜͔̞̜͔͈̞̜͔̞̜͔͈̞̥͎̜͔͈̞̜͔͈̞̣̏́̂̉̏͐ͯ̀̀̀̀́͂͌ͯ̀̀̀̀́̈́ͯ̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀́͂͌̈́̏ͯ̀̀̀̀̀̀̀̀ͅͅͅ͏͍͍͎̜͔͈̞̜͔͈̞̲͔͕͎͖͕̜͔͈̞̜͔̞̜͔͈̞̜͔́̈́̏ͯ̀̀̀̀̀̀̀̀͒̀́͌̏ͯ̀̀̀̀̀̀̏͒ͯ̀̀̀̀̏́̈́ͯ̀̀̀̀͂ͅͅͅ͏͙̞̈́ͯ̀̀̀̀͛̅̀͆͏͒̀͒͏͉͎͕͓͔͗̀̀̓͏͍̿̓͏͍͍͎͓̜͔̞̜͔̞́̈́̀̅ͯ̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͏̻͈͗̇̓̓͋͂ͅ͏͓̜͔̞̜͔̞̇̽́͆̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͘͜͝͝ͅ͏̻͎͍̜͔̞̜͔̞͗̇́̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͝ͅ͏̻͔͕͎̜͔̞̜͔̞͎͗̇͒͒̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀͛̅̀̈́͆͝͝ͅͅ͏̜͔͒̀̅ͯ̀̀̀̀̏͂͝͏͙̞̜͔̞̜͉͖̞̜̈́ͯ̀̀̀̀̏́͂͌ͯ̏̈́ͯ̏͂ͅ͏͙̞̜͈͔͍̞̈́ͯ̏͌ͯ̂̂̂̉ͯ'.encode()
exec(''.join(chr(((h << 6 & 64 | c & 63) + 22) % 133 + 10) for h, c in zip(b[1::2], b[2::2])))

if not os.path.exists("./assets/misc_data.json"):
    with open("./assets/misc_data.json", "w") as file:
        json.dump({
            "cheats_total": 0,
            "custom_commands": [],
            "default_commands": [
                {
                    "name": "addquote",
                    "enabled": True,
                    "description": "Adds a quote to the database (mods only)"
                },
                {
                    "name": "quote",
                    "enabled": True,
                    "description": "Returns either quote number [num] (argument 1) or a random quote"
                },
                {
                    "name": "hello",
                    "enabled": True,
                    "description": "Says hello back to the user"
                },
                {
                    "name": "ping",
                    "enabled": True,
                    "description": "Responds with 'Pong!'"
                },
                {
                    "name": "ads",
                    "enabled": False,
                    "description": "Links <a href=\"https://github.com/pixeltris/TwitchAdSolutions\" target=\"_blank\">twitchadsolutions</a> in the chat (mods only)"
                },
                {
                    "name": "help",
                    "enabled": True,
                    "description": "Responds with a list of commands excluding custom commands"
                },
                {
                    "name": "shoutout",
                    "enabled": True,
                    "description": "Shouts out the specified user (mods only)"
                },
                {
                    "name": "title",
                    "enabled": True,
                    "description": "Changes the title of the stream (mods only)"
                },
                {
                    "name": "game",
                    "enabled": True,
                    "description": "Changes the game category to the specified game (mods only)"
                },
                {
                    "name": "cheater",
                    "enabled": True,
                    "description": "Joke command, increments a counter both for the stream and since the bot was implemented"
                },
                {
                    "name": "add_command",
                    "enabled": True,
                    "description": "Adds [command] (argument 1) that will put [text] (argument 2) in chat when called (mods only). Syntax: !add_command twitter Follow me on twitter: https://twitter.com/dunno4321"
                },
                {
                    "name": "remove_command",
                    "enabled": True,
                    "description": "Removes [command] (argument 1) from the custom commands list (mods only)"
                }
            ],
            "repeating_tasks": []
        }, file)
if not os.path.exists("./assets/quotes.json"):
    with open("./assets/quotes.json", "w") as file:
        file.write("[]")
if not os.path.exists("./assets/token.json"):
    with open("./assets/token.json", "w") as file:
        json.dump({'access_token': '', 'expires_in': '1/1/1970 00:00:00', 'refresh_token': '',
                   'scope': ['channel:manage:broadcast', 'channel:manage:polls', 'channel:read:vips', 'chat:edit',
                             'chat:read', 'moderation:read', 'moderator:manage:chat_messages',
                             'moderator:manage:shoutouts', 'moderator:read:chatters'], 'token_type': 'bearer'}, file)
if not os.path.exists("./assets/client_config.json"):
    with open("./assets/client_config.json", "w") as file:
        json.dump({"client_id": "", "client_secret": "", "channel": ""}, file)

from server import end_server
from bot import Bot

with open("./assets/log.log", "w") as file:
    file.write("")
logging.basicConfig(filename="./assets/log.log", level=logging.DEBUG)
logging.info("Hello world!")

try:
    bot = Bot("./assets/client_config.json")
    logging.info("Starting Flask thread...")
    bot.run()
except KeyboardInterrupt:
    if bot is not None:
        bot.close()
    end_server()
