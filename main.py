from bot import Bot
import logging

# https://github.com/DaCoolOne/DumbIdeas/tree/main/reddit_ph_compressor
# creates the directories and files the bot uses if they don't already exist
# compressed form because otherwise it would be another 500 lines :3
b = 'E͉͍͐͏͔͓͒̀͊͏͎͉͍ͯ͐͏͔͒̀͏̴͓͉͎̝̜̤̯̣̹̰̥͈͔͍̞̜͈͔͍̞̜͓͔͙̞ͯͯ̈́̀̀̂̂̂́̀͌ͯ͌ͯ͌ͯ͂͘ͅͅ͏͙͈͔͍̈́̌̀͌̀͛ͯ̀̀͆͏̛͎͔͍͉͙͉͓͎͓͓͉͔̍͆́͌̀́͒́͌̌̀́̍͒͆ͯͯ́͂͌̀͛ͯ̀̀͆̚͝ͅͅ͏̛͎͔͍͉͙͉͓͎͓͓͉̍͆́͌̀́͒́͌̌̀́̍͒͆ͯ̀̀͂̚ͅ͏͒̈́͒̍̓ͅ͏͓͌͌́͐̀̓̚ͅ͏̛̛͓͉͔͈͔͔͈͌͌́͐ͯ̀̀͗̈́̀̑̐̐̅ͯͯͯ̈́̌̀̀͛ͯ̀̀͂̚͝ͅ͏͓͒̈́͒̀̑͐̀̚͘ͅ͏̛̛̛͉͔͔͉͇͎͔͉͎͇̘͔͎͔͈͈͉͖͎͇͌̈́̀̃̈́̈́̈́̈́̈́̈́ͯ̀̀̍́͌̀͌͆ͯ̀̀͐́̈́̈́̀͐ͯͯͯ͒̍̓͌̈́̈̉̀͛ͯ̀̀͂́̓͋͒͘̚̚͘̚͝ͅͅͅͅ͏͕͎̈́̍̓͏͌͏̛̛̛͉͎͕͔͍͇͉͎͍͇͉͎̜͓͔͙̞̜͓͉͔̞͕͎͔͉͒̀̃̈́̈́̈́̈́̈́̈́ͯͯͯ͐̀͛ͯ̀̀́͒̀̒͐̀̐ͯͯͯ́̀͛ͯ̀̀́͒̀͐̀̐ͯͯ̏͌ͯ̓͒͐ͯ͆̓̚̚͘̚̕͘͝͝͝ͅ͏͎͓͎͉͔͍͉͓͕͔͖͍͎͔̝̀̈́̿̈̌̀̿̈́͆́͌̉̀͛ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͔͍͔͈͈͔͔̓̎͌̈́̈̉ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚ͅͅͅͅͅͅ͏͈̓́͌͏̡͓͔͕͔͔̟͉͔͍̝͍͎͔͈͉͓͕͔̝͉͓͕͔͈͓͓͓̣̓̐̐̐̏͐̈́́̿̈́́́̂̋̋̂̂̋͌̎̓̓͋̈́̋̂̆̿̈́͆́͌̂̋̿̈́͆́͌̌̀͛̂́̈́͒̂̀͛̂̓̓̍̚̚ͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͔͒͏̡͌̍͌͌͏̛̯͉͇͉͎͕͎͔͉͗̍͒̂̀̂̊̂̉ͯͯͯ͆̓̚͝͝͝͏͎͓͖͔͖͉͎͔͉̝̀́̿̈́́́̈̉̀͛ͯ̀̀̀̀́͒̀̓͌̿̈́̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͎͔͉͖͉͎͔͓͔̝̓̎͌̈́̈̂̓͌̿̈́̂̉ͯ̀̀̀̀́͒̀̓͌̿̓͒̀̀̈́ͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͎͔͓͔͖͈͎͎̝̓̎͌̈́̈̂̓͌̿̓͒̂̉ͯ̀̀̀̀́͒̀̓́͌̀̀̈́ͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎͖͕̝͈͔͔̓̎͌̈́̈̂̓́͌̂̉ͯ̀̀̀̀́͒̀͒͌̀̀̂͐̏̏͌̚ͅͅͅͅͅ͏͈̓́͌͏͓͔͓͔͉͎͔̓̐̐̐̏̿̓͌̿̓̚ͅͅ͏̡̛͎͉͇̟͉͎͔͉̝͉͎͔͉͖͕͉͎͔͓͔̝͉͎͔͓͔͖͕͈͎͎̝͈͎͎͖͕͔͈͕͈͓͓͓̣͆̓͌̿̈́̂̀̋̀̓͌̿̈́̎́͌̀̋̀̂̆̓͌̿̓͒̂̀̋̀̓͌̿̓͒̎́͌̀̋̀̂̆̓́͌̂̀̋̀̓́͌̎́͌ͯ̀̀̀̀͆̓̈͒͌̌̀͛̂́̈́͒̂̀͛̂̓̓̍̚ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͔͒͏̡͌̍͌͌͏̛̯͉͇͉͎͔̣͗̍͒̂̀̂̊̂̉ͯ̀̀̀̀́͌͒̈̂̚͝͝ͅ͏͎͉͇͕͔͓͓͔͔͔͈͆̀͐̈́́̈́̌̀͐͌́̀͒́͒̀̀͂ͅͅͅͅͅ͏͔͔̀͏̛͕͓͕͎͓͓͔͈͉͓͉͓͔͈͉͓͔͕͎͕͎͔͉̀̀̈͌̀̀̀̀͆͒̀͒̉̂̉ͯͯͯ͆̓͝ͅͅͅ͏͎͕͔͔͉͎͇͓͔͉̀͐̈́́̿͒͐́̿̓ͅͅͅͅ͏͎͖͈͉͈̝̈̉̀͛ͯ̀̀̀̀́͒̀͗̓̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͉͈̓̎͌̈́̈̂͗̓̿ͅͅͅͅ͏̛͎͖͕͉͈͉͈̝̝͔͉͎͇̂̉̎́͌ͯ̀̀̀̀͆̀̈͗̓̀̀̂͒͐́̀͐ͅͅͅͅ͏͌͌̂̉̀͛ͯ̀̀̀̀̀̀̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͉͖͈͉͎̝͓͌͌̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇͉͖͈͉͎̝͔͕͓̓̎͌̈́̈̂̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̈́͝ͅͅͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͉͖͈͉͎̝͔͕͌͌̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇͉͖͈͉͎̝͓͕͎͔͉̓̎͌̈́̈̂̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅͅͅͅͅͅ͏͎͈͎͎̀̓́͌̿͐ͅ͏͉͎͔͓̿͏͎͉͖͎̝̓͌̓͋̈̉̀͛ͯ̀̀̀̀́͒̀́͂͌̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͎͈͉͎̿́͂͌̈́̂̉̎̓̓͋̈́ͯ̀̀̀̀͆̀̈́͂͌̈́̉̀͛ͯ̀̀̀̀̀̀̀̀̈́ͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͉͖͈͉͎̝͓͓̿̈́̂̉̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̈́͝ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͉͖͈͉͎̝͔͕͕͎͔͉̿̈́̂̉̎̈́̈́̀̀͒ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅͅ͏͎͉͔͍͖͎̯͔͉̀́̈́̈́̿̈̉̀͛ͯ̀̀̀̀́͒̀͗͐ͅͅ͏͎̝̀̀̈́͏̛͕͍͎͔͔̥͍͎͔͉͎͕͔͎̯͔͉̓̎̓͒́͌̈̂͐̂̉ͯ̀̀̀̀͗͐ͅͅͅͅͅͅ͏͎͓͓̮͍̝̎̓͌́́̀̀̂͐ͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͍͎͔͓̝̂ͯͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͎̯͔͉̂̉ͯ̀̀̀̀͗͐ͅ͏͎͈̎͐͌́̓ͅ͏̝̯͔͉͌̈́͒̀̀̂͐ͅ͏̛͎͍͎͔͓͎͇͔͈̀̂̀̋̀̈͌̎͌̀̋̀̑̉ͯͯ̀̀̀̀̈́ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͌͌̿͏͔͉͐͏͎͓͎̣͈͉͎̯͔͉̂̉̎́͐͐̈́͌̈́̈͗͐ͅͅ͏̛͎͖͎̳̝̉ͯ̀̀̀̀́͒̀͗͐́̓̀̀̈́ͅͅ͏̛͕͍͎͔͔̥͍͎͔͎̳͓͓̮͍̝̓̎̓͒́͌̈̂͂͒̂̉ͯ̀̀̀̀͗͐́̓̎̓͌́́̀̀̂͐ͅͅͅͅͅͅͅͅ͏͓͌͌̿͂͒́͋̂ͯ̀̀̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͎̣͈͉͎̳͕͎͔͉̂̉̎́͐͐̈́͌̈́̈͗͐́̓̉ͯͯͯ͆̓͝ͅͅͅ͏͎͍̀͒ͅ͏͖͉͔͍͖͍͎͔͓̝̿̈̉̀͛ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͉͎͓̝̂̉ͯ̀̀̀̀́͒̀͌͂͒́͋̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏̛͓͉͍͎͔͓͎͇͔͈̞͍͎͔͓̻͍͎͔͓͎͇͔͈͍͌͌̿͂͒́͋̂̉ͯ̀̀̀̀͆̀̈͌̎͌̀̀̒̉̀͛ͯ̀̀̀̀̀̀̀̀͌͌̎͌̀̍̀̑̽̎͒ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͉͎͓̻͉͎͓͎͇͔͈͍̈̉ͯ̀̀̀̀̀̀̀̀͌͂͒́͋͌͂͒́͋̎͌̀̍̀̑̽̎͒ͅͅͅͅͅͅͅ͏̛͖͕͎͔͉̈̉ͯ̀̀̀̀ͯͯͯ͆̓͝͝ͅ͏͎͓͕͍͉͔̀͂̿͐͏͖͕͎͙͖͕̝͌͌̈̉̀͛ͯ̀̀̀̀́͒̀͆͒͑̓̿́͌̀̀̈́ͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͖͕͖͕͎͙͕͎͉͔̝̓̎͌̈́̈̂͆͒͑̓̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿̀̀̈́ͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͕͎͉͔͓͖͕͖͔͉͔̝̓̎͌̈́̈̂͆͒͑̓̿̂̉̎́͌ͯ̀̀̀̀́͒̀͌̀̀̈́ͅͅͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏̛͔͉͔͖͕͖͌͌̿͌̂̉̎́͌ͯ̀̀̀̀́͒̀ͅͅ͏͔͉͐͏͎͓̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂͐ͅͅͅͅͅ͏͌͌̿͏͔͉͐͏̛͎͓͖͈͎͎̂̉ͯ̀̀̀̀́͒̀̓́͌̿͐ͅ͏͉͎͔͓͎̝̿́͂͌̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͎͈͖͈͎͎̿́͂͌̈́̂̉̎̓̓͋̈́ͯ̀̀̀̀́͒̀̓́͌̿͐ͅͅͅͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔̝̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͈͎͎̓̎͌̈́̈̂̓́͌̿͐ͅͅͅͅͅ͏̛͉͎͔͓͍͔͖͕͖͕͔͉̿́̂̉̎́͌ͯ̀̀̀̀́͒̀̈́͒́ͅ͏͎̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂͐ͅͅͅͅ͏͕͔͉͌͌̿̈́͒́͏̛͎͖͕͉͔͉͔̝̝͔̰͓͓͔̂̉̎́͌ͯ̀̀̀̀͆̀̈͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀͐ͅͅͅͅͅͅ͏̛̛͔͉͔͔͕͎͉͕͎͙͖͕̝̝͔̰͓͓͔͌͌̀͌́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈͆͒͑̓̿́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀͐͝ͅͅͅͅͅͅͅͅͅ͏̛̛͕͎͙͔͕͎͉͕͔͉͌͌̀͆͒͑̓́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈̈́͒́͝ͅͅͅ͏̛̛͎̜̝͔̦͕͎͙͍͕͓͔̞͔͕͎͖̀̀̐̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͒͑̓̀̀͂̀̀̐̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀́͒̀̓͝ͅͅͅͅͅ͏̛͕͎͔̝͖͒̀̀̐ͯ̀̀̀̀́͒̀ͅ͏͔͉͐͏̛͎͓͔͔̝̻͈͉̿̀̀̽ͯ̀̀̀̀͗͌̀̈̓͘ͅͅ͏͕͎͔̜͒̀̀ͅ͏͔͉͐͏͎͓͎͇͔͈͉̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀͆̀̈ͅ͏͔͉͐͏͎͓̻̓͏͕͎͔͖͕̝̝͔̥͍͔͙͖͕͒̽̎́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́͌͒̈̂͐̀́͌̀͆ͅͅͅͅ͏͒̀͏͎̀ͅ͏͍͒̀͏͒̀ͅ͏͔͈͆̀̀ͅ͏͔͉͐͏͎͓͓͍̌̀͐͌́̀͒ͅͅͅ͏͖̀ͅ͏̛̛͓͔͖͕͔͕͎͒̀̀́͌̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͝ͅͅͅ͏͔͉͐͏͎͓͔͔̻̿̓͘ͅ͏͕͎͔̝͒̽̀̀ͅ͏͔͉͐͏͎͓̻̓͏̛͕͎͔͖͕͒̽̎́͌ͯ̀̀̀̀̀̀̀̀̓ͅͅ͏̛͕͎͔͔̝͖͕͎͙͖͕͕͎͉͔͓͕͎͙͕͎͉͔͔͉͔͔͉͔͒̋̋ͯ̀̀̀̀ͯ̀̀̀̀̈́́́̀̀͛ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿́͌̂̀͆͒͑̓̿́͌̌ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿̂̀͆͒͑̓̿̌ͯ̀̀̀̀̀̀̀̀̂͌̂̀͌̌ͯ̀̀̀̀̀̀̀̀̂̚̚̚͝ͅͅͅͅͅͅͅͅͅͅ͏͔͉͐͏͎͓̂̀̚͏͔͉͐͏͎͓͔͔̿̌ͯ̀̀̀̀̀̀̀̀̂̓̿͐͘ͅ͏͉͎͔͓͎͈͎͎̿́͂͌̈́̂̀̓́͌̿͐̚ͅͅͅ͏͉͎͔͓͎̿́͂͌̈́̌ͯ̀̀̀̀̀̀̀̀̂̓̿͐ͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔͈͎͎̂̀̓́͌̿͐̚ͅͅ͏͉͎͔͓͖̿͐͒̿ͅ͏͔͕͔͉̌ͯ̀̀̀̀̀̀̀̀̂̈́͒́ͅ͏͎͕͔͉̂̀̈́͒́̚͏͎͔͈͈͔͔ͯ̀̀̀̀ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚͝ͅ͏͈̓́͌͏͓͔̓̐̐̐̏͐̚͏͍͔͈͌͌̂̌̀͛ͯ̀̀̀̀̀̀̀̀ͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͔͖͔͔͓̝͔͙͕͉̈́̀̎͒͆̈̈́́́̉ͯ̀̀̀̀̉ͯͯͯ́͒̀͌͒̀̀̂͑͗͒̚͝͝ͅͅͅ͏̷̴̵̸̶̡̧̨̢̛͓͇͈͚͖͎͍̱̥̲̹̩̯̰̳̤̦̪̫̬̺̣̮̭͓͉͔͕͎͔͉͐́̈́͆͊͋͌̓͂̂̎͐͌̈̂̂̉ͯ͆̓͘͏̛͎͎͔͔͖͕͉̝̀̓͌́̈̉̀͛ͯ̀̀̀̀́͒̀͂͌̈́͒̀̀̂̂ͯ̀̀̀̀͆͘ͅͅͅ͏̛̛̛̛͔͉̝͉̜͔͔͎͇͔͈͉͉͔͔͓͉͎͕͓͔͔̻͉͕͉̝͔͔̻͉͔͕͎͕͉͕͎͔͉͒̀̈͌̀̀̀̐̀̀̀̎͌̀̋̋̉̀͛ͯ̀̀̀̀̀̀̀̀͆̀̈͌͒̎̓͌̈́̈̽̉̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͌̈́͒̀̋̀̽ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀ͯ̀̀̀̀͒͒̀͂͌̈́͒ͯͯͯ͆̓͘͘͘͝͝͝ͅͅͅͅͅͅͅͅͅͅͅ͏͎͓͕͍͉͔͍͓͇͖̀͂̿̈̉̀͛ͯ̀̀̀̀́͒̀̓͏͎͔͎͔̝̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͍͓͇̓̎͌̈́̈̂̿͂ͅͅͅͅ͏̛͙͖͕͖͕͎͙͖͕̝̈́̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿́͌̀̀̈́ͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͖͕͖͕͎͙͕͎͉͔̝̓̎͌̈́̈̂͆͒͑̓̂̉̎́͌ͯ̀̀̀̀́͒̀͆͒͑̓̿̀̀̈́ͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͕͎͙͕͎͉͔͓͖͕͉̓̎͌̈́̈̂͆͒͑̓̿̂̉̎́͌ͯ̀̀̀̀͆̀̈̓ͅͅͅͅͅͅͅ͏͎͔͎͔̝̝͔̰͓͓͔͍͓͓͇̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀̓ͅͅͅͅͅͅͅ͏̛̛̛̛̛̛͎͔͎͔͔͕͎͉͕͎͙͖͕̝̝͔̰͓͓͔͍͓͓͇͕͎͙͔͕͎͉͕͎͙͖͕̜̝͔̦͕͎͙͍͕͓͔̞͔͕͎͔̝͖͕͎͙͖͕͕͎͉͔͓͕͎͙͕͎͉͔͍͓͇́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈͆͒͑̓̿́͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀͆͒͑̓́̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈͆͒͑̓̿́͌̀̀̐̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͒͑̓̀̀͂̀̀̐̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀̈́́́̀̀͛ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿́͌̂̀͆͒͑̓̿́͌̌ͯ̀̀̀̀̀̀̀̀̂͆͒͑̿̂̀͆͒͑̓̿̌ͯ̀̀̀̀̀̀̀̀̂̿͂̚̚͝͝͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͙̈́̂̀̓̚͏͎͔͎͔͔͈͈͔͔ͯ̀̀̀̀ͯ̀̀̀̀͆̓̈̂͐̏̏͌̚͝ͅͅ͏͈̓́͌͏͓͔͍͓͇͍͔͈̓̐̐̐̏̂̌̀͛ͯ̀̀̀̀̀̀̀̀̚ͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͔͓͙͎͕͎͔͉̈́̀̎͒͆̈̈́́́̉ͯ̀̀̀̀̉ͯͯͯ́̓̀͆̓̚͝͝͏͎͇͔͔͉͎͇͖͔͍̝͉͔͔͈͈͔͔̀̿͒͐́̈̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅͅ͏͈̓́͌͏̛͓͔͇͔͔͉͎͇͔͕͎͉͔͔͍͓̓̐̐̐̏̿͒͐́̂̉ͯ̀̀̀̀͒͒̀́͗́̀͐̎͊̚ͅͅͅͅ͏͎͓͙͎͕͎͔͉̈̉ͯͯͯ́̓̀͆̓͝͏͎͍̀͒ͅ͏͖͔͉͎͇͔͓͎͍͖͔͍̝͉͔͔͈͈͔͔̿͒͐́̿́͋̈́̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅͅͅ͏͈̓́͌͏͓͔͍̓̐̐̐̏͒̚ͅ͏͖͔͉͎͇͍͔͈̿͒͐́̂̌̀͛ͯ̀̀̀̀̀̀̀̀ͅͅͅͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏̛͙̪̳̯̮͓͔͉͎͇͉͙͎͍͎͍͔͍̝͉͔͔͍͓̈́̀̎͒͆̈͛̂́̂̀́̉ͯ̀̀̀̀̉ͯ̀̀̀̀͐̀̀́͗́̀͐̎͊̚̚͝͝ͅͅ͏̛͎͉͔͍̻͓͕͓͓͔̦͉͔̈̉ͯ̀̀̀̀͆̀̈́͐̂̓̓̂̽̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂́͌̈́̀ͅͅͅ͏͍̀͒ͅ͏̛̛̛͖͔͉͎͇͔͓̭͓͓͇͔͍̻͍͓͓͇͔͕͎͓͎͍̝͎͍͖͔͍͎͔̝̀͒͐́̀́͋́̀́̀̂̀̋̀͐̂́̂̽̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀́̀̀́̎͒͐͌́̓̈̂̀̂̌̀̂̿̂̉ͯ̀̀̀̀̀̀̀̀́͒̀́͂͌̿͌̀̀̈́̚͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͎͎͍͔͍͎͔͍̓̎͌̈́̈̓͌́̈́̉̉ͯ̀̀̀̀̀̀̀̀́͂͌̿͌̎͒ͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔̲͍̈̉ͯ̀̀̀̀̀̀̀̀́͌͒̈̂ͅͅͅ͏͖͓͕͓͓͕͙͓͙͎͕͎͔͉̈́̀̓̓͆͌͌̂̉ͯ̀̀̀̀ͯͯͯ́̓̀͆̓͝͝ͅͅ͏͎̀́̈́̈́̿͏͍͒̿͒ͅ͏͖͈͎͇͖͉͓̝̿̓́̈́̈̉̀͛ͯ̀̀̀̀́͒̀̿́̈́̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂́̈́̈́̿ͅͅͅͅ͏͍͒̿͒ͅ͏̡̛͖͖͕̝̝͖͉͖̝̂̉̎́͌̀̀̂̈́̈́̂ͯ̀̀̀̀́͒̀́̈́̈́̿̈́̀̀̈́ͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩̓̎͌̈́̈̂́̈́̈́̿ͅͅͅͅ͏͔͉͐͏͎͈̿̓͏̛͓͎͖͍͎͔͓̝̂̉ͯ̀̀̀̀́͒̀́̈́̈́̿͌̀̀̈́ͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͓͙̣͓͓̮͍̓̎͌͌́́̈̂ͅͅͅͅͅ͏̛͎͙͖͍͌̿́̈́̈́̂̉ͯ̀̀̀̀́͒̀͒ͅ͏͖͉͖̝̿̈́̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͍̓̎͌̈́̈̂͒ͅͅͅͅͅ͏͖̿ͅ͏͔͉͐͏͎͈̿̓͏̛͓͎͖͍̂̉ͯ̀̀̀̀́͒̀͒ͅͅ͏͖͔̝̿́͂͌̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͔͉͎͇͔͖͖͙͔͔̝̓̎͌̈́̈̂͒͐́̿́͂͌̂̉ͯ̀̀̀̀́͒̀͒̿̀̀̈́͘ͅͅͅͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͖͙͔͔͕͈͖͓͔͕̝̓̎͌̈́̈̂͒̿̿͂͒̂̉ͯ̀̀̀̀́͒̀͆͆̀̀̈́͘ͅͅͅͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͓͔͕͖̓̎͌̈́̈̂͆͆̂̉ͯ̀̀̀̀́͒̀̓ͅͅͅͅ͏̛̛̛͕͎͔̝͉͉͓͖͙͔͔͓͔͙̝͉͓͙͉͎͉͎͉͖͈͉͎̝͓͍͒̀̀̐ͯ̀̀̀̀͆̀̈̿́̈́̈́̉̀͛ͯ̀̀̀̀̀̀̀̀͒̿̎͌̀̀̂̈́͐͌́͌̂ͯ̀̀̀̀̀̀̀̀́̈́̈́̿̈́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀͒͘̚ͅͅͅͅͅͅͅͅͅ͏̛͖͉͖͈͉͎̝͔͕͈͉̿̈́̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅͅͅ͏͕͎͔̜͍͎͔͓͎͇͔͈͍͎͔͓̻͒̀̀́̈́̈́̿͌̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́̈́̿͌̓ͅͅͅͅͅͅͅͅ͏̛͕͎͔͈͉͎̝͓͒̽̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͓͔͕͓͔͙̝͉͓͙͎͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͆̎͌̀̀̂̈́͐͌́̚͝ͅͅ͏̛̛͎͓͓͔͕͓͔͙̝͉͓͙͉͎͉͎͖͙͔͔͓͔͙̝͉͓͙͎̂ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀͆͆̎͌̀̀̂̈́͐͌́͌̂ͯ̀̀̀̀̀̀̀̀͒̿̎͌̀̀̂̈́͐͌́̚͘̚͝ͅͅͅͅͅͅͅͅͅ͏̛̛͎͉͖͈͉͎̝͔͕͍̂ͯ̀̀̀̀̀̀̀̀́̈́̈́̿̈́̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀͒ͅͅͅͅ͏̛͖͉͖͈͉͎̝͓͈͉̿̈́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅͅͅ͏͕͎͔̜͍͎͔͓͎͇͔͈͍͎͔͓̻͒̀̀́̈́̈́̿͌̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́̈́̿͌̓ͅͅͅͅͅͅͅͅ͏̛͕͎͔͈͉͎̝͔͕͒̽̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͝ͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͍͆̀͒ͅ͏͖͔͈͉͎̞͈͉͍̿́͂͌̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒̚ͅͅͅͅ͏̛̛̛͖͓͔͕͈͉͎̝͓͕͈̝͉͔͇͔͔͉͎͇͖̈̉ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀͆͆̎̈́̈́̀̀͆́͌ͯͯ̀̀̀̀̀̀̀̀͂͒̀̀́͗́̀̿͒͐́̈̉ͯ̀̀̀̀̀̀̀̀́͒̀̓͝ͅͅͅͅͅͅ͏̛͕͎͔̝͈͉͒̀̀̐ͯ̀̀̀̀̀̀̀̀͗͌̀̈̓ͅͅ͏͕͎͔̜͕͈͎͇͔͈͖͉͔͍̝͕͈̻͒̀̀͂͒̎͌̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀́͒̀̀̀͂͒̓ͅͅͅ͏̛͕͎͔͒̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅ͏͎͓͔͔͍̝̀͐̀̀̈́͏̛̛͕͍͎͔͔̥͍͎͔͔͔͍͉̝͎͉͔͍̻͎͍̓̎̓͒́͌̈̂͒̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎̈́̀̀̓͌́̈̂́̂̽̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅͅͅͅ͏͎͓͔͍̀͒ͅ͏͖͔͎̝̿͂̀̀̈́ͅ͏͕͍͎͔͔̥͍͎͔͕͔͔̓̎̓͒́͌̈̂͂ͅͅͅͅͅ͏̛͎̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͏͎͓͔͔͍̝͉͔͍̻͎͍͍̀͐̒̀̀̂́̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒ͅͅͅ͏͖͔͎̿͂̎ͅ͏͎͉̝͕͎͔͉̓͌̓͋̀̀͆̓͏͎͕͈͍̈̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀͂͒̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒̚ͅ͏̛͖͔͉͎͇͔͓͔͍͍̿͒͐́̿́͋̈͐̒̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒͝ͅͅͅͅ͏̴̨͖͔͎͉͎͎̭̬̝̲͍̿͂̎͒̀̀̂ͅͅͅ͏̛͖͔͓̀́͋̂ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅ͏͎͓͔̀̓͏̛͎͔͎͔̝͉͔͍̻͎͍̀̀̂́̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͎͓͔͔͙̝͉͔͍̻͔͙̀͐̀̀̂͐̂̽ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͎͓͔͕͎͙̝͉͔͍̻͖̀͆͒͑̓̀̀̂͆͒͑̿́͌̂̽ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅ͏͎͓͔̀̓͏͎͔͎͔͍͎͔̝̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͔͙͍͎͔̝̀͐̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͕͎͙͍͎͔̝̀͆͒͑̓̿͌̀̀̈́ͅͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏̴̨͎͔͎͔͍͎͔͉͎͎̭̬̝̿͌̎͒̀̀̓ͅͅͅͅͅ͏̴̴̨̨̛̛̛͎͔͎͔͔͙͍͎͔͉͎͎̭̬̝͔͙͕͎͙͍͎͔͉͎͎̭̬̝͕͎͙͔͍͎̣͈͉͍ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̿͌̎͒̀̀͐ͯ̀̀̀̀̀̀̀̀̀̀̀̀͆͒͑̓̿͌̎͒̀̀͆͒͑̓ͯͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͒ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔͎͔͍͎̣͈͉̿͂̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈̓ͅͅ͏̛̛̛͎͔͎͔͍͎͔͔͍͎̣͈͉͔͙͍͎͔͔͍͎̣͈͉͕͎͙͍͎͔͍̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͐̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͆͒͑̓̿͌̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͖͔͎̣͈͉͔͍̿́͂͌̎́͐͐̈́͌̈́̈͐̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓ͅͅͅ͏̛͕͎͔͓͔͕͔͈͉͓͉͓͔͈͒̋̋ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀̏̏̀͆̀̀̀̀͝ͅͅ͏͎͙͙͉͇͌̀͗́̀̀͏͔͉͔͔̀̀͏̀͗͏͉͎͒͋ͯ̀̀̀̀̀̀̀̀̏̏̀̀͋͏͉͔͓͉͍͔͈͔͍͗̀̀͂́̈́ͯ̀̀̀̀̀̀̀̀̏̏̀̀͂́̈́̀́̀͌̀͏͉͕͓͋ͯ̀̀̀̀̀̀̀̀̏̏̀̀̀͒́͌̀͐͒ͅͅ͏͇͍͍͉͎͇͎͇͕͇͓͖͕͕͕͕͕͈̝̻͒́̀͌́́ͯ̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀́͒̀͂͒̀̀̽ͯ̀̀̀̀̀̀̀̀͆̚ͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͍͆̀͒ͅ͏͖͔͈͉͎̞͉͕͕͕͕͕͈͉͎͕͓͈͉͉͈͉͍̿́͂͌̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̏̀̓ͯ̀̀̀̀̀̀̀̀̀̀̀̀͆̀̈͂͒̎̓͌̈́̈̓͌̈́̎̈́̉̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒̚ͅͅͅͅͅ͏̛̛͖͓͕͕͕͕͕͈͕͓͈͈͉͉͓͙͎͕͎͔͉̈̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͂͒̎͐̈̓͌̈́̎̈́̉ͯ̀̀̀̀̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀ͯͯͯ́̓̀͆̓͝͝͝͝͝ͅͅͅ͏͎͇͔͇͉͖͙͖͔͍̝͉͔͔͈͈͔͔̀̿́͗́̈̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅ͏͈̓́͌͏̛͓͔͇͔͇͉͖͙͔͕͎͉͔͔͍͓̓̐̐̐̏̿́͗́̂̉ͯ̀̀̀̀͒͒̀́͗́̀͐̎͊̚ͅͅͅ͏̛͎͓͙͎͕͎͔͉̈̉ͯͯͯ́̓̀͆̓͝͏͎͎͇͉͖͙͖͔͍̝͉͔͔͈͈͔͔̀̓́̓͌̿́͗́̈̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅ͏͈̓́͌͏̛͓͔͎͇͉͖͙͖͓̝͉͔͔͍͓̓̐̐̐̏̓́̓͌̿́͗́̂̉ͯ̀̀̀̀́͒̀͒̀̀́͗́̀͐̎͊̚ͅͅͅ͏̛͎͉͓̻͓͕͓͓̈̉ͯ̀̀̀̀͆̀̈͒̂̓̓̂̽̉̀͛ͯ̀̀̀̀̀̀̀̀͆ͅͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͆̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͔͈͉͎͈͉͍̓̎͌̈́̈̂́͗́̿̈́́́̂̉̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒ͅͅͅͅͅͅͅ͏̧̛̛͖͔͉͖͙͎͓͔̦͉͔̈̉ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀́͌͒̈̂́͗́̀̓́̓͌͌̈́̂̉ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂́͌̈́̀͝͝ͅͅͅͅͅͅͅͅͅ͏̛͎͇͉͖͙͓̻͍͓͇͓͙͎͕͎͔͉̀̈́̀́͗́̀̂̀̋̀͒̂̂̽̉ͯ̀̀̀̀ͯͯͯ́̓̀͆̓̚͝͝ͅͅͅ͏͎͎͇͉͖͙͖͔͍̝͉͔͔͈͈͔͔̀̈́̿́͗́̈̉̀͛ͯ̀̀̀̀́͒̀͐̀̀́͗́̀͆̓̈̂͐̏̏͌̚ͅͅͅ͏͈̓́͌͏̛͓͔͎͇͉͖͙͖͓̝͉͔͔͍͓̓̐̐̐̏̈́̿́͗́̂̉ͯ̀̀̀̀́͒̀͒̀̀́͗́̀͐̎͊̚ͅͅͅ͏̛͎͉͓̻͓͕͓͓̈̉ͯ̀̀̀̀͆̀̈͒̂̓̓̂̽̉̀͛ͯ̀̀̀̀̀̀̀̀͆ͅͅ͏͒̀̈̓͏͎͓͔͈͉̀̓͌̈́̀͏͆̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͔͈͉͎͈͉͍̓̎͌̈́̈̂́͗́̿̈́́́̂̉̎̓͌̈́͒̉̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̓͌̈́̎͒ͅͅͅͅͅͅͅ͏̧̛̛͖͔͉͖͙͉͎͎͓̻͉͎͎͓͔̦͉͔̈̉ͯ̀̀̀̀̀̀̀̀ͯ̀̀̀̀̀̀̀̀́͌͒̈̂́͗́̀͗͒̀̂̀̋̀͒̂͗͒̂̽̉ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂́͌̈́̀̚͝͝ͅͅͅͅͅͅͅͅͅͅ͏̛͎͇͉͖͙͓̻͍͓͇͕͎͔͉̀̈́̀́͗́̀̂̀̋̀͒̂̂̽̉ͯ̀̀̀̀ͯͯͯ͆̓̚͝͝ͅͅͅ͏͎͓͍͓͔͕͎͎̰̀͌͐̈̉̀͛ͯ̀̀̀̀͒͒̀͗̀͒ͅͅͅͅ͏͍͉͓͓̈͒ͅͅ͏̴͖̝̞͓͔͉͍͌̀̀ͅͅͅ͏͕͔͓̈͒ͅ͏̛͖͍͓͓͙͎͕͎͔͉͌̌̀̉̉ͯͯͯ́̓̀͆̓͝ͅ͏͎̀͌͏̛͇͉͖͙͉͔͓͖͉͇͉͖͙̝́̈́̿́͗́̈̉̀͛ͯ̀̀̀̀́͗́̀͌͐̈̉ͯ̀̀̀̀́͒̀͆̿́͗́̀̀̈́̕ͅͅͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͉͇͉͖͙͖͉͎̓̎͌̈́̈̂͆̿́͗́̂̉ͯ̀̀̀̀́͒̀͆̿ͅͅͅͅͅ͏͔͇͉͖͙̝̿́͗́̀̀̈́ͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͉͎̓̎͌̈́̈̂͆̿ͅͅͅͅ͏̛̛͔͇͉͖͙͔͙͇͉͖͙̝͉͔͇͔͇͉͖͙͔͈̿́͗́̂̉ͯ̀̀̀̀͒̀͛ͯ̀̀̀̀̀̀̀̀́͗́̀̀́͗́̀̿́͗́̈̉ͯ̀̀̀̀̀̓́̓̀̈͒͒͝ͅͅͅͅͅ͏͒̉̀͛ͯ̀̀̀̀̀̀̀̀̓͏͎͓͏͌̎͌ͅ͏͇͎͔̈̂͗ͅ͏͒͋̀͒͒ͅ͏̛̛̛͔͕͎͉͇͉͖͙̻͔͉͖͉͇͉͖͙͈͉͎̝͓͉͎͒̀̓̂̉ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈́͗́̂́̓̂̽̉͛ͯ̀̀̀̀̀̀̀̀͆̿́͗́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀̀̀̀̀͆̿̚͝ͅͅͅͅͅͅ͏̛͔͇͉͖͙͈͉͎̝͔͕̿́͗́̎̈́̈́̀̀͒ͯͯ̀̀̀̀̀̀̀̀̓ͅͅͅ͏͎͓͔͔͍̝̀͐̀̀̈́͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂͒̂̉ͯ̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͎͕͔͔̀̓́̓͌̿͂ͅ͏͎̝̀̀̈́͏͕͍͎͔͔̥͍͎͔͕͔͔̓̎̓͒́͌̈̂͂ͅͅͅͅͅ͏̛͎̂̉ͯ̀̀̀̀̀̀̀̀̓͏͎͓͔͎͕͔͔̀̈́̿͂ͅ͏͎̝̀̀̈́͏͕͍͎͔͔̥͍͎͔͕͔͔̓̎̓͒́͌̈̂͂ͅͅͅͅͅ͏̛͎͎͕͔͔̂̉ͯ̀̀̀̀̀̀̀̀̓́̓͌̿͂ͅ͏͎̎͏̛͎͉̝͎͇͉͖͙͎͕͔͔̓͌̓͋̀̀̓́̓͌̿́͗́ͯ̀̀̀̀̀̀̀̀̓́̓͌̿͂ͅͅͅ͏̴̨̛͎͉͎͎̭̬̝̣͎͇͉͖͙͎͕͔͔̎͒̀̀̂́̓͌̀́͗́̂ͯ̀̀̀̀̀̀̀̀̈́̿͂ͅͅͅͅ͏͎̎͏̛͎͉̝͎͇͉͖͙͎͕͔͔̓͌̓͋̀̀̈́̿́͗́ͯ̀̀̀̀̀̀̀̀̈́̿͂ͅͅͅ͏̴̨̛͎͉͎͎̭̬̝̥͎͇͉͖͙̎͒̀̀̂̈́̀́͗́̂ͯͯ̀̀̀̀̀̀̀̀̓ͅͅ͏͎͓͔͔͉͔͍͎͔̝̀͌̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͓͉͔͉̀̈́̓͒͐ͅ͏͎͍͎͔̝̿͌̀̀̈́ͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͎͔͎͔͓͍͎͔̝̀͒́̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͎͍͎͔̝̀̓́̓͌̿͌̀̀̈́ͅͅͅͅ͏̛͕͍͎͔͔̥͍͎͔͔̓̎̓͒́͌̈̂̈́̂̉ͯ̀̀̀̀̀̀̀̀̓ͅͅͅͅͅ͏͎͓͔͎͍͎͔̝̀̈́̿͌̀̀̈́ͅͅͅͅ͏̴̨̛̛͕͍͎͔͔̥͍͎͔͔͔͉͔͍͎͔͉͎͎̭̬̝͇͉͖͙̻͔͉͔͓͉͔͉̓̎̓͒́͌̈̂̈́̂̉ͯͯ̀̀̀̀̀̀̀̀͌̿͌̎͒̀̀́͗́̂͌̂̽ͯ̀̀̀̀̀̀̀̀̈́̓͒͐ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̴̨͎͍͎͔͉͎͎̭̬̝͇͉͖͙̻͓͉͔͉̿͌̎͒̀̀́͗́̂̈́̓͒͐ͅͅͅͅͅͅ͏̴̨̛̛͎͎͔͎͔͓͍͎͔͉͎͎̭̬̝͇͉͖͙̻͎͔͎͔͓͎͍͎͔͎̣͈͉͎͕͔͔̂̽ͯ̀̀̀̀̀̀̀̀͒́̿͌̎͒̀̀́͗́̂͒́̂̽ͯ̀̀̀̀̀̀̀̀̓́̓͌̿͌̎́͐͐̈́͌̈́̈̓́̓͌̿͂ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͎͎͍͎͔͎̣͈͉͎͕͔͔̉ͯ̀̀̀̀̀̀̀̀̈́̿͌̎́͐͐̈́͌̈́̈̈́̿͂ͅͅͅͅͅͅ͏̛̛͎͔͍͎̣͈͉͔͉͔͍͎͔͔͍͎̣͈͉͓͉͔͉̉ͯͯ̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͌̿͌̉ͯ̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈̈́̓͒͐ͅͅͅͅͅͅͅ͏̛̛̛̛͎͍͎͔͔͍͎̣͈͉͎͔͎͔͓͍͎͔͔͍͎̣͈͉͎͍͎͔͔͍͎̣͈͉͎͍͎͔̿͌̉ͯ̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈͒́̿͌̉ͯ̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈̓́̓͌̿͌̉ͯ̀̀̀̀̀̀̀̀͐̎́͐͐̈́͌̈́̈̈́̿͌̉ͯͯ̀̀̀̀̀̀̀̀̈́ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏̢̛̛͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͔͎̣͈͉͔͍͓͓͙͉͇͉͖͙͈͉͎̝͔͕͉͎̓̎͌̈́̈̂́͗́̿̈́́́̂̉̎́͐͐̈́͌̈́̈͐̉ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̏̏̀́ͯ̀̀̀̀̀̀̀̀͆̿́͗́̎̈́̈́̀̀͒ͯ̀̀̀̀̀̀̀̀͆̿͝ͅͅͅͅͅͅͅͅͅͅͅͅ͏̛͔͇͉͖͙͈͉͎̝͓͓͙͎͕͎͔͉̿́͗́̎̈́̈́̀̀͆́͌ͯ̀̀̀̀ͯͯͯ́̓̀͆̓͝͝ͅͅͅ͏͎͓͕͍͉͔͇͉͖͙͔͉͔̝̀͂̿́͗́̈̉̀͛ͯ̀̀̀̀͌̀̀̈́ͅͅ͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͔͉͔͖͕͓͉͔͉̓̎͌̈́̈̂́͗́̿͌̂̉̎́͌ͯ̀̀̀̀̈́̓͒͐ͅͅͅͅͅͅͅͅ͏͎̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͓͉͔͉̓̎͌̈́̈̂́͗́̿̈́̓͒͐ͅͅͅͅͅͅ͏̛͎͖͕͔͉͔̂̉̎́͌ͯ̀̀̀̀̓͋̿̓ͅͅ͏͓͔̝̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͔͉͔̓̎͌̈́̈̂̓͋̿̓ͅͅͅͅͅ͏̛̛͓͔͖͕͉͔͉͔̝̝͔̰͓͓͔͔͉͔̂̉̎́͌ͯ̀̀̀̀͆̀̈͌̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀͌̂̉ͯ̀̀̀̀̀̀̀̀̈́ͅͅͅͅͅͅͅ͏̢͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͓͕͍͉͔͔͔͔͓͔͙̝͉͓͙͎̓̎͌̈́̈̂́͗́̿͂̈́̿̂̉̎͌̀̀̂̈́͐͌́͘̚ͅͅͅͅͅͅͅͅ͏̛̛͎͔͕͎͉͓͉͔͉̂ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈̈́̓͒͐͝ͅͅͅ͏͎̝̝͔̰͓͓͔͓͉͔͉̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀̈́̓͒͐ͅͅͅͅͅ͏̛͎̂̉ͯ̀̀̀̀̀̀̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͓͕͍͉͔͔͔͔͓͔͙̝͉͓͙͎̓̎͌̈́̈̂́͗́̿͂̈́̿̂̉̎͌̀̀̂̈́͐͌́͘̚ͅͅͅͅͅͅͅͅ͏̛̛͎͔͕͎͉͔͉͔̂ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯ̀̀̀̀͆̀̈̓͋̿̓͝ͅͅͅ͏͓͔̝̝͔̰͓͓͔͔͉͔̀̀̂̂̉̀͛ͯ̀̀̀̀̀̀̀̀́͌͒̈̂͌́̀̀́̀̓͋̀̓ͅͅͅͅͅ͏̛͓͔̂̉ͯ̀̀̀̀̀̀̀̀̈́͏̢͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͓͕͍͉͔͔͔͔͓͔͙̝͉͓͙͎̓̎͌̈́̈̂́͗́̿͂̈́̿̂̉̎͌̀̀̂̈́͐͌́͘̚ͅͅͅͅͅͅͅͅ͏̛̛͎͔͕͎͖͓̝͉͔͔͈͈͔͔̂ͯ̀̀̀̀̀̀̀̀͒͒ͯ̀̀̀̀ͯͯ̀̀̀̀́͒̀͒̀̀́͗́̀͆̓̈̂͐̏̏͌̚͝ͅͅͅͅ͏͈̓́͌͏͓͔͇͉͖͙͍͔͈̓̐̐̐̏́̈́̈́̿́͗́̂̌̀͛ͯ̀̀̀̀̀̀̀̀̚ͅͅ͏̴̰̯̳͈͓̣̈́̀̂̂̌ͯ̀̀̀̀̀̀̀̀̂́̈́͒̂̀͛ͯ̀̀̀̀̀̀̀̀̀̀̀̀̂̚̚ͅͅ͏̴͎͔͎͔͙͉͔͉̍͐̂̀̂́͐͐͌̓́̚ͅͅ͏͎͓̏͊͏͎̂ͯ̀̀̀̀̀̀̀̀̌ͯ̀̀̀̀̀̀̀̀͂͝͏͙̪̳̯̮͓͔͉͎͇͉͙͔͉͔͔͉͔͓͉͔͉̈́̀̎͒͆̈͛̂͌̂̀͌̌̀̂̈́̓͒͐̚̚ͅͅͅ͏͎͓͉͔͉̂̀̈́̓͒͐̚ͅ͏͎͔͉͔̌̀̂̓͋̿̓ͅ͏͓͔͔͉͔̂̀̓͋̿̓̚ͅ͏̛͓͔͓̝͉͔͓͓̉ͯ̀̀̀̀̉ͯ̀̀̀̀͒̀̀́͗́̀͒̎͊͝͝ͅͅ͏̛͎͉͓̻͓͕͓͓̈̉ͯ̀̀̀̀͆̀̈́͒̂̓̓̂̽̉̀͛ͯ̀̀̀̀̀̀̀̀̈́ͅͅ͏̴̢̨͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͓͕͍͉͔͔͔͔͉͎͎̭̬̝̥̓̎͌̈́̈̂́͗́̿͂̈́̿̂̉̎͒̀̀̂͒͒͘ͅͅͅͅͅͅͅͅ͏̛͓͕͍͉͔͔͉͎͇͇͉͖͙͓̻͍͓͇͓͒̀͂̀́͗́̀̂̀̋̀͒̂̂̽ͯ̀̀̀̀̀͌̀͛ͯ̀̀̀̀̀̀̀̀̈́̚͝ͅͅͅͅ͏̴̢̨̧̛͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͓͕͍͉͔͔͔͔͉͎͎̭̬̝͉͖͙͓͕͍͉͔͔͉͎̓̎͌̈́̈̂́͗́̿͂̈́̿̂̉̎͒̀̀̂́͗́̀͂̈́̂ͯ̀̀̀̀ͯͯͯ͗̈́͘͝͝ͅͅͅͅͅͅͅͅͅͅ͏͗̎͏͎͌͏̝́̈́̀̀͌͏̡̧̢̢̛͇͉͖͙̜͓͉͔̞̜͈̞̜͔͉͔̞̹̣́̈́̿́͗́̈̉ͯ̏̓͒͐ͯ́̈́ͯ͌̀̓ͅͅͅ͏͎͉͇͇̜͔͉͔̞̜͈̞̜͆̀͐́̏͌ͯ̏́̈́ͯ͂ͅͅͅ͏̡̧̢͙̞̜͈̞̹̰̣̈́ͯͯ̑̀̓͏͎͉͇̜͈̞̜͈̝͆̏̑ͯ́̀͒͆̂̏͌ͅ͏̶͇̞͉̂͗̀͌ͅ͏͇͉̜̞̜̞̜͉͖͉̝̀͆͌̏́͂͒ͯ̈́̀̈́̂̓ͅ͏͎͉͇̞̜͈̞̣͉͎͔͆̂ͯ̀̀̀̀̓͌̀̓ͅ͏͎͉͇̜͈̞̣͉͎͔̩̤̜͉͎͕͔͉̝͉͎͔͉͖͕̝͉͎͔͉̞̜̞̣͉͎͔̳͔̜͉͎͕͔͉̝͉͎͔͓͔͖͕̝͉͎͔͓͔̞̜̞̣͈͎͎͎͍̜͉͎͕͔͉̝͈͎͎͖͕̝͈͎͎̞̜̞̜͕͔͔͆̏̓ͯ̀̀̀̀͌̀̀͐̀̈́̂̓͌̿̈́̂̀́͌̂͛͛̓͌̿̈́̂͂͒ͯ̀̀̀̀͌̀̓͒̀͐̀̈́̂̓͌̿̓͒̂̀́͌̂͛͛̓͌̿̓͒̂͂͒ͯ̀̀̀̀́͌̀́̀͐̀̈́̂̓́͌̂̀́͌̂͛͛̓́͌̂͂͒ͯ̀̀̀̀͂̚̚̚͝͝͝͝͝͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͉̝͓͔̀̈́̂̿̓ͅ͏͎͉͇͆̂̀͏͎͉̝͓͖͔̞̳͖̜͕͔͔̓͌̓͋̂́̿̈́́́̈̉̂́̏͂ͅͅ͏̴͎̞̜͉͖̞̜͉͖͉̝͇͉͖͙͉͖̞̜͈̞̭͎͇͇͉͖͙̜͈̞̜͉͖͉̝͉͇͉͖͙͈͉͎̝̞̜͔͉̝͇͉͖͙͔̞̜͔͈̞̜͔̞̜͔̞͉͔̜͔̞̜͔̞̤͓͉͔͉ͯ̏̈́ͯ̈́̀̈́̂́͗́̿̈́̂ͯ̀̀̀̀̓́́̀́͗́̏̓ͯ̀̀̀̀̈́̀̈́̂͆̿́͗́̂̀̈́̈́̂̂ͯ̀̀̀̀̀̀̀̀́͂͌̀̈́̂́͗́̿́͂͌̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̈́͌̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̈́̓͒͐ͅͅͅͅͅͅͅͅͅͅͅ͏͎̜͔̞̜͔̞̥͎͔͎͔͓̜͔̞̜͔̞̣͎̜͔̞̜͔̞̥͎͈̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̈́͒́̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̈́́̓͌̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̈́̈́̀̆̀̓ͅ͏͏͓͉͎͎̜͔̞̜͔̞̜͔͈̞̜͔̀͗͒̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅͅͅ͏͙͉̝͇͉͖͙͔̞̜͙͎͍͉̈́̀̈́̂́͗́̿̈́́́̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̍̍̀̈́́̓̀͐ͅ͏͕͔͉͐͌́͏͎̞̜͔̀̍̍ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏͂͏͙̞̜͔̞̜͉͖̞̜͉͖͉̝͉͎̈́ͯ̀̀̀̀̀̀̀̀̏́͂͌ͯ̀̀̀̀̏̈́ͯ̀̀̀̀̈́̀̈́̂͆̿ͅ͏͔͇͉͖͙̞̜͓͔͙̝̿́͗́̂ͯ̀̀̀̀̀̀̀̀͐̀͌̂͆ͅͅ͏̴͎͔͓͉͚̖̞̣͔͇͉͖͙̜̞͉͔̜͉͎͕͔͉̝͇͉͖͙͔͉͔͈̍̑͐̂͒́̀́̀́͗́̏͐ͯ̀̀̀̀̀̀̀̀͌ͯ̀̀̀̀̀̀̀̀͐̀̈́̂́͗́̿͌̂̀͐͌́̓̚͘̚ͅͅͅͅͅͅͅͅ͏̝̳͔͍͌̈́͒̂́̀̓ͅͅ͏͇͉͖͙̞̜̞̤͓͉͔͉̈́̀́͗́̂͂͒ͯ̀̀̀̀̀̀̀̀̓͒͐ͅͅͅ͏͎̜͉͎͕͔͉̝͇͉͖͙͓͉͔͉ͯ̀̀̀̀̀̀̀̀͐̀̈́̂́͗́̿̈́̓͒͐̚ͅͅ͏͎͈̂̀͐͌́̓ͅ͏̷̝͉͎̳͔͍͌̈́͒̂̀́̀́̀̓ͅͅ͏̈́̀͆ͅ͏̴̞̜̞͉͔͒̎̎̎̂͂͒ͯ̀̀̀̀̀̀̀̀̓͋̀̓ͅ͏͓͔̀̈͐͏͉͎͔͓̜͉͎͕͔͉̝͔͉͔̉ͯ̀̀̀̀̀̀̀̀͐̀̈́̂̓͋̿̓̚ͅ͏͓͔͔͙̝͎͕͍͓͉͚̝̘͈̂̀͐̂͂͒̂̀̂̂̀͐͌́̓ͅͅͅͅ͏̝̞̜̞̜͕͔͔͌̈́͒̂̐̂ͯ̀̀̀̀̀̀̀̀͂͒ͯ̀̀̀̀̀̀̀̀͂̕ͅ͏͎͉̝͓͕͍͉͔͇͉͖͙̀̈́̂͂̿́͗́̂̀ͅ͏͎͉̝̓͌̓͋̇̈́͏̢̛͕͍͎͔͇͔̥͍͎͔͙̩͇͉͖͙͓͕͍͉͔͔͔͔͓͔͙̝͓͕͍͉͔͇͉͖͙̞̳͕͍͉͔̜͕͔͔̓̎͌̈́̈̂́͗́̿͂̈́̿̂̉̎͌̂̂͂̿́͗́̈̉̇͂̏͂͘ͅͅͅͅͅͅͅͅͅ͏͎̞̜͉̝͇͉͖͙͓͕͍͉͔͔͔͔͓͔͙̝͉͓͙͎ͯ̀̀̀̀̀̀̀̀͐̀̈́̂́͗́̿͂̈́̿̂̀͌̂̈́͐͌́͘̚ͅͅͅͅ͏͎̞̳͕͍͉͔͔͉͎͇̜̞̜͉͖̞̜͉͖̞̜͉͖͉̝͔͉͎͇͔͓͓̞̜͎͓͕͔̻͍̂͂̎̎̎̏͐ͯ̀̀̀̀̏̈́ͯ̏̈́ͯ̈́̀̈́̂́̈́̈́̿͒͐́̿́͋̂ͯ́̍̍̀̀̀̀̈́̀͒͌̀́̈́̈́̏͒̚ͅͅͅͅͅͅ͏͖̻͔͉͎͇̽̀́̀͒͐́̀͐ͅͅͅ͏͍͓͓͇͖͙̻͉͎͕͔̻͍͉͎͕͔͓͈͌͌̏́̽̀͒̀͐̽̀̏ͅͅͅͅͅ͏̡͕͓̞̜͈̞͔͉͎͇͔͓͓̜͈̞̜͓͔͉̝͒̽̍̍ͯ̀̀̀̀̓̈́̈́̀͒͐́̀́͋̏̓ͯ̀̀̀̀͌̓̀̈́̂́̈́̈́̿ͅͅͅͅ͏͍͒̿͒ͅ͏͖̂̀ͅ͏͎͈͎͇̝̓́̂́̈́̈́̿ͅ͏͍͒̿͒ͅ͏͖͈͎͇̞̜̿̓́̈́̈̉̂ͯ̀̀̀̀̀̀̀̀ͅͅ͏͔͉͐͏̡͎͉̝̞̜̀̈́̂́̈́̈́̂̈́̈́̏͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍̀̈́̂͒ͅ͏͖̞̲͍̂ͅͅ͏͖̜̏ͅ͏͔͉͐͏͎̞̜͓͔̞̜͉̝͓͔͕͓͔͙̝͉͓͙͎ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀́̀͐̀̈́̂͆͆̂̀͌̂̈́͐͌́̚ͅͅͅ͏͎̞͔͉͎͇͔͓̜̞̜͓͔͉̝͈͉͈̂͒͐́̀́͋̏͐ͯ̀̀̀̀͌̓̀̈́̂͗̓̿ͅͅͅͅͅ͏͎̂̀ͅ͏͎͈͎͇̝͕͔͔͉͎͇͓͔͉̓́̂͐̈́́̿͒͐́̿̓ͅͅͅͅͅ͏͎͓͓̝̈̉̂̀̓͌́̂͏͎͙̞̜͌̿́̈́̈́̂ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝̀̈́̂͐͏̞͔͉͎͇͌͌̂͒͐́̀͐ͅͅ͏̜͌͌̏͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍͓͓͇̞͔͉͎͇͍͓͓͇̜̀̈́̂́̂͒͐́̀́̏ͅͅͅͅͅͅ͏͔͉͐͏͎̞̜͓͔̞̜͓͔͙̝͉͓͙͉͎͉͎͉̝͖͙͔͔͕͈̞͔͈͔͔͓͖͙̜̞̜͉͎͕͔͉̝͕͎͙͓͓̝ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀͐̀͌̂̈́͐͌́͌̂̀̈́̂͒̿̿͂͒̂́̀͒͐́̀͒̀̏͐ͯ̀̀̀̀͐̀̈́̂͆͒͑̓̂̀̓͌́̂̚͘ͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎͙͔͙̝͎͕͍͈͌̿́̈́̈́̂̀͐̂͂͒̂̀͐͌́̓ͅͅͅ͏̝͓͉͚̝̖͍͉͎̝͍̝̙̞̜͓͔͉̝͕͎͙͕͎͉͔͓͓͓̝͌̈́͒̂̂̀̀̂̐̂̀́̂̂ͯ̀̀̀̀͌̓̀̈́̂͆͒͑̓̿̂̀̓͌́̂̕͘̕ͅͅͅͅͅͅ͏͎͙̞̜͌̿́̈́̈́̂ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͍͉͎͕͔͓̞͍͉͎͕͔͓̜̀̈́̂̂̏ͅͅ͏͔͉͐͏͎̞̜ͯ̀̀̀̀̀̀̀̀͏͔͉͐͏͎͉̝͈̀̈́̂͏͕͓̞͈͒̂͏͕͓̜͒̏͏͔͉͐͏͎̞̜͓͔̞̜͉͖͉̝ͯ̀̀̀̀̏͌̓ͯ̀̀̀̀̈́̀̈́̂́̈́̈́̿ͅͅ͏͔͉͐͏͎͈̿̓͏͓͎̞̜͉͖͉̝̂ͯ̀̀̀̀̀̀̀̀̈́̀̈́̂͐ͅ͏͉͖̞̰͌͌̿̈́̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀͏͔͉͔̜͉͎͕͔͉̝͌͌̀͌ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̀̈́̂͐̚ͅ͏͔͉͔͈͌͌̿͌̂̀͐͌́̓ͅͅ͏̨̝͓͔͉͓̟̞̜̞̯͔͉͌̈́͒̂́̈́̏́͌̂͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐ͅͅ͏͎͓̜̞̜͉͖͉̝͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̈́̀̈́̂͐̚͏͌͌̿͏͔͉͐͏͎͓̞̜͉͎͕͔͓͓̝̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̀̓͌́̂͐͏͌͌̿͏͔͉͐͏͎͓͈̂̀͐͌́̓ͅ͏̝͈͓̞̜͓͓̝͌̈́͒̂́̈́̂͂͒̀̓͌́̂͐ͅͅ͏͓̞̜͉͎͕͔͓͓̝͌͌̿͂͒́͋̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̀̓͌́̂͐ͅ͏͌͌̿͏͔͉͐͏͎͓͈̂̀͐͌́̓ͅ͏̝͔͉͓̞̜͓͓̝͌̈́͒̂́͌̂͂͒̀̓͌́̂͐ͅ͏͓̞̜͉͖̞̜͕͔͔͌͌̿͂͒́͋̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅ͏͎͉̝͉͔͍̀̈́̂́̈́̈́̿̂̀ͅ͏͎͉̝͉͔͍̞̜͕͔͔̓͌̓͋̂́̈́̈́̿̈̉̂́̈́̈́̏͂ͅ͏͎̞̜͕͔͔ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͏͎͉̝͍̀̈́̂͒ͅ͏͖͉͔͍̿̂̀ͅͅ͏͎͉̝͍̓͌̓͋̂͒ͅ͏͖͉͔͍̞͍̿̈̉̂͒ͅͅͅ͏͖̜͕͔͔̏͂ͅ͏͎̞̜̞̜͉͎͕͔͔͙̝͈ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͐̀͐̂̓̓͋͂ͅͅ͏͉̝͈͎͎̂̀̈́̂̓́͌̿͐͘ͅ͏͉͎͔͓͎̿́͂͌̈́̂̀ͅͅ͏͎͉̝͈͎͎̓͌̓͋̂̓́͌̿͐ͅ͏͉͎͔͓̿͏͎͉̞̓͌̓͋̈̉̂̀̀́͌͌͏͈͔͔͓͔͗̀̓́͒̀ͅ͏͖̀͏͔͉͔͈͈͎͎̀͗̀̓́͌̀͐ͅͅ͏͉͎͔͓̜̞̜͉͖͉̝͈͎͎͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̈́̀̈́̂̓́͌̿͐ͅ͏͉͎͔͓͉͖͈͉͎̞͈͖̿̈́̂̀̈́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̓̀ͅͅ͏͔̀̓ͅ͏͓͔͓̜͉͎͕͔͉̝͈͎͎̀͐̀̈́̂̓́͌̿͐ͅ͏͉͎͔͓͍͔͔͙̝͎͕͍͓͉͚̝̖͈̿́̂̀͐̂͂͒̂̀̀͐͌́̓ͅͅͅͅ͏̝̞͈͎͎͌̈́͒̂̑̐̐̂̀̓́͌̀͐ͅͅ͏͉͎͔͓̜͉͖̞̤͕͔͉ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͒́͏͎͓̀̈̓ͅ͏͎͓̜͉͎͕͔͉̝̈́̉̀͐̀̈́̂͐̚͏͕͔͉͌͌̿̈́͒́͏͎͔͙̝͎͕͍͓͉͚̝̖͈̂̀͐̂͂͒̂̀̂̂̀͐͌́̓ͅͅͅͅ͏̝̞̜̞̜͕͔͔͌̈́͒̂̑̒̐̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅ͏͎͉̝͓͕͍͉͔̀̈́̂͂̿͐͏͌͌̂̀͏͎͉̝͓͕͍͉͔̓͌̓͋̂͂̿͐͏̞͌͌̈̉̂́̈́̈́̀͐͏̜͕͔͔͌͌̏͂͏͎̞̜͉͖̞̜͉͖͉̝͍͓͇͉͖͈͉͎̝̞̭͓͓͇̜͉͎͕͔͉̝͍͓͇ͯ̀̀̀̀̀̀̀̀̏̈́ͯͯ̀̀̀̀̀̀̀̀̈́̀̈́̂̿̈́̂̀̈́̈́̂̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̀͐̀̈́̂̿͂̚ͅͅͅ͏͙͈̈́̂̀͐͌́̓ͅ͏̝̳͕͓͉͔͌̈́͒̂͂̓͒͂̀ͅͅ͏͍̀͒ͅ͏͖͓͓͔͙̝͍͇͉͎̞̜̞̜͕͔͔̀́̈́́̂̀͌̂́͒̀͐̀̐͐̂͂͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂̚̕͘͘ͅͅ͏͎͉̝͓͕͍͉͔͍͓͇̀̈́̂͂̿̂̀͏͎͉̝͓͕͍͉͔͍͓͇̞͍͓͓͇̜͕͔͔̓͌̓͋̂͂̿̈̉̂́̈́̈́̀́̏͂ͅͅ͏͎̞̜͉͖̞̜͉͖̞̜͉͖͉̝͍ͯ̀̀̀̀̀̀̀̀̏̈́ͯ̀̀̀̀̏̈́ͯ̀̀̀̀̈́̀̈́̂͒ͅ͏͖̿ͅ͏͔͉͐͏͎͈̿̓͏͓͎͈͉͎̝̞̜͔͉̝͕͎͔͔͉͎͇̞̜͔͈̞̜͔̞̜͔͈̞̲͍̂̀̈́̈́̂̂ͯ̀̀̀̀̀̀̀̀́͂͌̀̈́̂̓͒͒̿͒͐́̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀ͅͅͅͅͅͅͅͅ͏͖̜͔͈̞̜͔͈̞̭͓͓͇̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̀̓ͅͅͅ͏͎͔͎͔̏͐ͅ͏̴͔͉͔̜͔͈̞̜͔͈̞͙̜͔͈̞̜͔͈̞̦͕͎͙͍͉͎͕͔͓̜͔͈̞̜͔̞̜͔͈̞̜͔͌͌̀͌̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͐̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀͒͑̓̀̈̉̏ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏́̈́ͯ̀̀̀̀̀̀̀̀̀̀̀̀͂ͅͅͅͅͅͅ͏͙͉̝͔͉͎͇͔̞̜̈́̀̈́̂͒͐́̿́͂͌̂ͯ̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀̀́̍̍̀͐ͅͅͅ͏͕͔͙͎͍͉͙̞̜͔͐͌́̈́̀̈́́̓́͌͌̀̓̀̍̍ͯ̀̀̀̀̀̀̀̀̀̀̀̀̏͂̚ͅ͏͙̞̜͔̞̜͉͖̞̜͉͖̞̜͉͖͉̝̈́ͯ̀̀̀̀̀̀̀̀̏́͂͌ͯ̀̀̀̀̏̈́ͯ̏̈́ͯͯ̈́̀̈́̂̓ͅ͏͍͍͎͓̞̜͈̞̣́̈́̂ͯ̀̀̀̀̓͏͍͍͎̣́̈́̀͏͎͉͇͕͔͉͆͒́͏͎̜͈̞̜̞̤͕͔̏̓ͯ̀̀̀̀͐͆́͌̀̓ͅ͏͍͍͎͓̜̞̜͔̞̜͔͈̞̜͔̞̜͔͈̞̥͎̜͔͈̞̜͔͈̞̣́̈́̏͐ͯ̀̀̀̀́͂͌ͯ̀̀̀̀́̈́ͯ̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀́͂͌̈́̏ͯ̀̀̀̀̀̀̀̀ͅͅͅ͏͍͍͎̜͔͈̞̜͔͈̞̤͓͉͔͉́̈́̏ͯ̀̀̀̀̀̀̀̀̓͒͐ͅ͏͎̜͔͈̞̜͔̞̜͔͈̞̜͔̏ͯ̀̀̀̀̀̀̏͒ͯ̀̀̀̀̏́̈́ͯ̀̀̀̀͂ͅ͏͙̞̈́ͯ̀̀̀̀͛̅̀͆͏͒̀͒͏͉͎͕͔͗̀̀̈́͆́͌̿̓ͅ͏͍͍͎͓̜͔̞̜͔̞́̈́̀̅ͯ̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͏̻͈͗̇̓̓͋͂ͅ͏͓̜͔̞̜͔̞̇̽́͆̀̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͘͜͝͝ͅ͏̻͎͍̜͔̞̜͔̞͗̇́̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͝ͅ͏̻͓͉͔͉͗̇̈́̓͒͐ͅ͏͎͓̜͔̞̜͔̞͎̇̽́͆̀̏̈́ͯ̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀͛̅̀̈́͆͜͝͝ͅͅ͏̜͔͒̀̅ͯ̀̀̀̀̏͂͝͏͙̞̜͔̞̜̞̣͕͓͔̈́ͯ̀̀̀̀̏́͂͌ͯ̀̀̀̀͐ͅ͏͍̀̓͏͍͍͎͓̜̞̜̞̣͕͓͔́̈́̏͐ͯ̀̀̀̀͐͏͍̀̓͏͍͍͎͓́̈́̀͏͖͉͕͔͒͒̈́̀̈́͆́͌̀̓ͅͅͅ͏͍͍͎͓͇͉͎͇͓͉͔͈͔͕͎̳͕͓͉͔́̈́̀̈̎̎̀́̈́̈́̀́́̈́̀͗̀͒͒̀̂͂̓͒͂̀ͅͅͅ͏͔͈͈͎͎͔̀̀̓́͌̀ͅͅ͏͍̀͒ͅ͏͖͓̀́̈́̂̀͗ͅ͏͕͌̈́̀͏͖͉͔͈͕͔͔͕͎͒͒̈́̀̀̈́͆́͌̀͒͒̀ͅͅͅͅͅ͏̜͈̝͈͔͔͓͇͉͔͈͕͆̀̂́̀͒͆̂͐̏̏͂̎̓̚ͅ͏̴̡͍͉͔͉͓͉͔͈̳̏͐͌͒̏͗̓̈́͘ͅ͏͕͔͉͌͏͎͓̞͈͔͔͓͇͉͔͈͕̂͐̏̏͂̎̓̚͏̴̡͍͉͔͉͓͉͔͈̳̏͐͌͒̏͗̓̈́͘ͅ͏͕͔͉͌͏͎͓̜̞̜̞̜͔̞̜͔͈̞̜͔̞̜͔͈̞̥͎̜͔͈̞̜͔͈̞̣̏́̂̉̏͐ͯ̀̀̀̀́͂͌ͯ̀̀̀̀́̈́ͯ̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀́͂͌̈́̏ͯ̀̀̀̀̀̀̀̀ͅͅͅ͏͍͍͎̜͔͈̞̜͔͈̞̲͔͕͎͖͕̜͔͈̞̜͔̞̜͔͈̞̜͔́̈́̏ͯ̀̀̀̀̀̀̀̀͒̀́͌̏ͯ̀̀̀̀̀̀̏͒ͯ̀̀̀̀̏́̈́ͯ̀̀̀̀͂ͅͅͅ͏͙̞̈́ͯ̀̀̀̀͛̅̀͆͏͒̀͒͏͉͎͕͓͔͗̀̀̓͏͍̿̓͏͍͍͎͓̜͔̞̜͔̞́̈́̀̅ͯ̀̀̀̀̀̀̀̀͒ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͏̻͈͗̇̓̓͋͂ͅ͏͓̜͔̞̜͔̞̇̽́͆̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͘͜͝͝ͅ͏̻͎͍̜͔̞̜͔̞͗̇́̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̀̀̈́͛͛̀͒͝͝ͅ͏̻͔͕͎̜͔̞̜͔̞͎͗̇͒͒̇̽̀̏̈́ͯ̀̀̀̀̀̀̀̀̏͒ͯ̀̀̀̀͛̅̀̈́͆͝͝ͅͅ͏̜͔͒̀̅ͯ̀̀̀̀̏͂͝͏͙̞̜͔̞̜͉͖̞̜̈́ͯ̀̀̀̀̏́͂͌ͯ̏̈́ͯ̏͂ͅ͏͙̞̜͈͔͍̞͔̈́ͯ̏͌ͯ̂̂̂ͯ͏͎̝͉͎͔̝͈͎͎͉͎͔͉͉͎͔͓͔͍͉͓̝͕͓͔͋̀̀͛ͯ̓͌̀̀͛̂̓́͌̂̀̂̂̌̀̂̓͌̿̈́̂̀̂̂̌̀̂̓͌̿̓͒̂̀̂̂ͯ̓̀̀͛ͯ̀̀̂̓̚̚̚͝͝ͅͅͅͅͅͅͅ͏͍̿̓͏͍͍͎͓̻͕͔́̈́̂̀̽̌ͯ̀̀̂̈́͆́͌̿̓̚ͅ͏͍͍͎͓̻͎͍͕́̈́̂̀ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂́̈́̈́͑̚̚ͅ͏̴͔͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅͅ͏̡͎͓͕̂̀̂̈́̈́̀́̀͑̚͏͔͔̀ͅ͏͔͈͔͓͍̀̀̈́́́͂́̀̈ͅͅ͏͓̈́̀͏͎͙͎͍͕͌̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͑̚͝ͅ͏̴͔͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅͅ͏͎̲͔͕͎͓͉͔͈͕̂̀̂͒̀͒̀͑̚ͅͅͅ͏͔͎͕͍̻͎͕͍͇͕͍͎͔̀͂͒̀̽̀̈́͒̀̑̉̀ͅͅͅ͏͎͒̀́̀͒́̈́͏͍͕̀͑͏͔͎͍͈̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͌͌̚͝ͅͅͅ͏̴͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̳͙͓͈̂̀̂́̀͌͌̚ͅ͏͔̀͂́̓͋̀͏̴͔͈͕͓͎͍͉͎͇͎͕͓͉͔͉̀̀͒̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͐̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅ͏͎̲͓̂̀̂͐̚ͅ͏͎͓͉͔͈̰̈́̀͗̀̇͏͎͇͎͍͓͈́̇̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂̚͝ͅ͏͕͔͏̴͕͔͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̳͈̂̀̂̚͏͕͔͓̀͏͕͔͔͈͓͉͉͕͓͍̀̀͐̓͆̈́̀͒̀̈ͅͅͅͅ͏͓̈́̀͏̴͎͙͎͍͔͉͔͎͕͓͉͔͉͌̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͌̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅ͏͎̣͈͎͇͓͔͈͔͉͔̂̀̂́̀̀͌̀̚ͅͅͅ͏͔͈͓͔͍͍͆̀̀͒́̀̈ͅͅ͏͓̈́̀͏̴͎͙͎͍͇͍͎͕͓͉͔͉͌̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂́̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅ͏͎̣͈͎͇͓͔͈͇͍͔͇̂̀̂́̀̀́̀̓́̚ͅͅͅͅ͏͙͔͒̀͏͔͈͓͉͉͇͍͍̀̀͐̓͆̈́̀́̀̈ͅͅͅͅ͏͓̈́̀͏͎͙͎͍͌̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂́̈́̈́̿̓̚͝ͅ͏̴͍͍͎͎͕͓͉͔͉́̈́̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏̡͎͓̻̂̀̂̈́̈́̀̓̚͏͍͍͎͇͕͍͎͔͔͈͔͉͕͔̻͔͔͇͕͍͎͔͉͎͈͔͈͎͍́̈́̽̀̈́͒̀̑̉̀́̀͗͌͌̀͐̀̽̀̈́͒̀̒̉̀̀̓́̀͗̀̓́͌͌̈́̀̈͘ͅͅͅͅͅ͏͓̈́̀͏͎͙̳͙͎͔͌̉̎̀́̀́́̈́̈́̿̓͘̚͏͍͍͎͔͉͔͔̦́̈́̀͗͒̀ͅ͏͌͌͏͍͗̀̀ͅ͏͎͔͉͔͔͈͔͔͓͔͉͔͔̀͗͒̀͐̏̏͗͒̎̓̚̚ͅͅ͏͍͕͎͎̏̈́͏͎͍͍̔̓̒̑̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͒̚͝ͅͅ͏͖̿̓ͅ͏̴͍͍͎͎͕͓͉͔͉́̈́̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̲͍̂̀̂̚ͅ͏͖͓̻̀̓ͅ͏͍͍͎͇͕͍͎͔́̈́̽̀̈́͒̀̑̉̀͆͒ͅ͏͍͔͈͕͓͔̀̀̓ͅ͏͍̀̓͏͍͍͎͓͉͓͔͍́̈́̀͌̀̈͏͓̈́̀͏̴͎͙͎͍͔͈͔͉͍͎͕͓͉͔͉͌̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͗́̓̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅ͏͎̲͔͕͎͓͉͔͈͔͈͍̂̀̂͒̀͗̀̀́̚ͅͅ͏͕͎͔̀͏͔͉͍͔͈͕͓͈͓͓͎͔͈͉͎͇͔͈͈͎͎͓͉͎͔͈͉͓͆̀̀̀͒̀́̀͐̈́̀͗́̓̀̀̓́͌̀̓̀̀͂ͅͅͅͅͅͅͅ͏͔͓͉͍͍͎͔͎͍̀͗́̀͐͌̈́̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͌̚͝ͅͅͅͅ͏̴͖͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅͅ͏͎̲͔͕͎͓͔͈͕͔̂̀̂͒̀̀̓́͌̓͌́̈́̀͌̚ͅͅͅ͏̴͖͔͎͔͈͈͔͔͎͔͈͓͉͉͉͔͍͎͍̘͎͕͓͉͔͉̀͂͗̀̀̓́͒̀́̈́̀̀͐̓͆̈́̀̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͂́͌͌̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ͏͎̣̂̀̂̚͏̴͎͓͕͔͔͈̘͎͍͓͙͎͔͎͕͓͉͔͉͌̀̀͂́͌͌́̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂́̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚͘̚͝ͅͅͅͅͅͅ͏̧͎͉͖͓͓͙͎͔̂̀̂̀́̀̚͘ͅ͏͎͈̀͏͔͗̀͏͎͖͎͕͓͔̀́̈́̈́̀́̀́̈́́̓̈́̀̓ͅ͏͍̀̓͏͍͍͎͎͍́̈́̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͐̚͝ͅ͏̴͉͎͔͓͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̲͔͕͎͓͔͈̂̀̂͒̀̀͐̚ͅͅ͏͉͎͔͓̀͆͏͔͈͉͎͕͉͉͎͇͈͔͔͒̀̀͑͒̀̓́͒̀ͅͅ͏͓͉͉͈͔͔͎͍͇͉͖͒̀͐̓͆̈́̀̓́͒̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͐̚͝ͅͅͅͅͅ͏̴͉͎͔͓͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏̧͎͉͖͓̂̀̂̀͐̚ͅ͏͉͎͔͓͔̀͏͓͉͉͕͓͎͍͍̀́̀͐̓͆̈́̀͒̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂̚͝ͅͅͅͅ͏͇͉͖̈́͐ͅ͏̴͉͎͔͓͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎͍̂̀̂̈̚͏͓̈́̀͏̧͎͙͉͖͓͌̉̀̀͐ͅ͏͉͎͔͓͔̀͏͓͉͉͕͓̀́̀͐̓͆̈́̀͒̀͆͒ͅͅͅ͏͍͔͈̭̀̀ͅ͏̢͎͔͍͎͉͎͇͎͍͔̈́̀́͋̀̈͒́̈́́͒͋̀͐̈́̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂́͋͐̚͝ͅͅͅͅ͏̴͉͎͔͓͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎͍̂̀̂̈̚͏͓̈́̀͏̴͎͙͓͌̉̀́͋̀͐ͅ͏͉͎͔͓̀͆͒͏̴͍͕͓͎͍͇͍͎͕͓͉͔͉̀́̀͒̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂́͂͌̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅ͏̧͎͍͓͓̂̀̂́͂͌̀̚ͅ͏͍̀͐ͅ͏͉͎͔͓͉͔͈͔͈͈͎̀͗̀̀̓́̓̀ͅͅ͏͉͎͎͉͎͇͕͔͆̀͗̀͐̀͏͔͈͍̀̀̀́̕͘ͅ͏͕͎͔͇͍̀́͂͌̈́̀ͅ͏͒̀͌͏͓͉͎͇͉͔͎͍̀̀́͌͌̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂̓̚͝ͅ͏̴͉͎͉͎͕͓͉͔͉͆͌͐̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏̧͎͍͓͓̂̀̂́͂͌̀̚ͅ͏͍̀͐ͅ͏͉͎͔͓̀͏͎͈͎͓͉͓͎͍̀́̀̐̏̐̀̓́̓̀͂́̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͌́̈́͒͂̕̕̚͝ͅͅͅͅ͏̴͎͕͓͉͔͉́͒̈́̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̳͈̂̀̂̚͏͓͔͈͗̀̀͐ͅ͏͉͎͔͓̀͏͔͈͔͆̀̀ͅ͏̴͈͔͔͓͎͍͎͕͓͉͔͉͐̀̀̓́͒̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͒́͆͆͌̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̕̚̚͝ͅͅͅͅͅͅͅ͏͎̳͔͔͓̂̀̂́͒̀́̀͒́͆͆͌̀͆̚ͅ͏͒̀̐̐̐̀͐̕͏͉͎͔͓͉͔͈͕͔̀͗̀͐̀͏͉͎͎͓͍͔̀̀͗͒̀̈́̀͗̕ͅ͏͎͍͉͎͎͓͔̋́̀͗͒̀͘ͅ͏̴͈͎͇͉͎͔͈͕͔͕͎͍͎͎͕͓͉͔͉̀͂̀̓́́͂͌̀̀̀͆͒̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂̓́̓͌͒́͆͆͌̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅͅͅͅͅͅ͏̴͎̣͎͓͔͈͕͎͔͎͍͓͎͕͓͉͔͉̂̀̂́̓͌̀̀̓͒͒̀͒́͆͆͌̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͒́͆͆͌̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚̚͝ͅͅͅͅͅͅͅͅͅͅ͏͎̳͔͔͓̂̀̂́͒̀́̀͒́͆͆͌̀͆̚ͅ͏͒̀̐̐̐̀͐̕͏͉͎͔͓͉͔͈̀͗̀͏͎͉͎͎͍͔̀͗͒̀̈́̀͗ͅͅ͏͎͔̀͏͈͎͇͉͎͔͈͕͔͕͎͍̀͂̀̓́́͂͌̀̀̀͆͒̉̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͊̚͝ͅͅͅͅͅͅ͏̴͉͎͎͕͓͉͔͉̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚ͅͅͅͅ͏͎̪̂̀̂̚͏̴͉͎͓͔͈͕͎͔͎͍͇͉͖͙͎͕͓͉͔͉̀̀̓͒͒̀͒́͆͆͌̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂́͗́̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅͅͅ͏͎̳͈̂̀̂̚͏͓͉͎͗̀͆͏̀́͂͏̴͕͔͔͈͕͎͔͇͉͖͙͎͍͎͔͎͕͓͉͔͉̀̀̓͒͒̀́͗́̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͒̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚͝ͅͅͅͅͅͅͅͅͅͅ͏̴͎̥͎͔͓͔͈͕͎͔͇͉͖͙͎͍͔͉͍͎͕͓͉͔͉̂̀̂͒̀̀̓͒͒̀́͗́̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂͒̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚̚͝ͅͅͅͅͅͅͅͅͅͅ͏̴͎̳͔͔͓͔͉͍͎͍͎͔͉͍͓͎͕͓͉͔͉̂̀̂́͒̀́̀͒̂ͯ̀̀̀̀̌ͯ̀̀̀̀͛ͯ̀̀̀̀̀̀̂́̂̀̂̓́̓͌͒̂̌ͯ̀̀̀̀̀̀̂́͂͌̈́̂̀͒̌ͯ̀̀̀̀̀̀̂̈́̓͒͐̚̚̚͝ͅͅͅͅͅͅͅͅ͏͎̣͎͓͔͉͍͓͔͉͎͇͔͓͓̻͕̂̀̂́̓͌̀́͌͌̀͒̂ͯ̀̀̀̀ͯ̀̀̽̌ͯ̀̀̂͒͐́̿́͋̂̀̽ͯͯ͑̚̚͝͝ͅͅͅͅ͏͔͓̝̻͉͎̀̀̽ͯͯ͆̀ͅ͏͔̀͏͓͔͈͉͓͉͓͓͔͓̎͐́̎̈́͒̈̂̎̏́̂̉ͯ̀̀̀̀̚ͅ͏͓͍͉͓͓͔͓͉͎̎͋̈́͒̈̂̎̏́̂̉ͯ͆̀ͅ͏͔̀͏͓͔͈͉͓͉͔͍͔͓̎͐́̎̈́͒̈̂̎̏͐͌́̂̉ͯ̀̀̀̀̚ͅͅ͏͓͍͉͔͍͔͓͉͎̎͋̈́͒̈̂̎̏͐͌́̂̉ͯͯ͆̀ͅͅ͏͔̀͏͓͔͈͉͓͔͓͔͍͔͓͉͎͈͔͍͉͔͈̎͐́̎̈̂̎̏͐͌́̏̈́̎͌̂̉ͯ̀̀̀̀͗̀͘͘̚ͅͅͅͅ͏͎͔͍͔͓͉͎͈͔͍͓͉͉͉͔͉͎͉͎͐̈̂̎̏͐͌́̏̈́̎͌̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͆͌̎͗͒̈̈́̉ͯ͆̀͘̚͘ͅͅͅͅͅͅͅͅ͏͔̀͏͓͔͈͉͓͔͓͓͓͔͓̎͐́̎̈̂̎̏́̏̓͘ͅͅ͏͎͉͇͓͆̎͊͏͎͉͔͈̂̉ͯ̀̀̀̀͗̀̚͏͎͓͓͔͓͐̈̂̎̏́̏̓ͅͅ͏͎͉͇͓͆̎͊͏͎͓͉͓̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͊̚ͅ͏͎͕͍͉͎͔͉͉͎̎̈́͐̈̓͌̌̀͆͌̉ͯ͆̀ͅͅ͏͔̀͏͓͔͈͉͓͔͓͓͓͔͓͕̎͐́̎̈̂̎̏́̏͑͘ͅͅ͏͔͓͓̎͊ͅ͏͎͉͔͈̂̉ͯ̀̀̀̀͗̀̚͏͎͓͓͔͓͕͐̈̂̎̏́̏͑ͅͅ͏͔͓͓̎͊ͅ͏͎͓͉͓̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͊̚ͅ͏͎͕͍͕̎̈́͐̈͑͏͔͓͉͉͎̌̀͆͌̉ͯ͆̀ͅͅ͏͔̀͏͓͔͈͉͓͔͓͓͓͔͓͔̎͐́̎̈̂̎̏́̏͘ͅͅ͏͎͓͋̎͊ͅ͏͎͉͔͈̂̉ͯ̀̀̀̀͗̀̚͏͎͓͓͔͓͔͐̈̂̎̏́̏ͅͅ͏͎͓͋̎͊ͅ͏͎͓͉͓̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͊̚ͅ͏͎͕͍͔̎̈́͐̈͏͎͉͉͎͋̌̀͆͌̉ͯ͆̀ͅͅ͏͔̀͏͓͔͈͉͓͔͓͓͓͔͓͔͓̎͐́̎̈̂̎̏́̏̈́́́̎͊͘ͅͅ͏͎͉͔͈̂̉ͯ̀̀̀̀͗̀̚͏͎͓͓͔͓͔͓͐̈̂̎̏́̏̈́́́̎͊ͅͅ͏͎͓͉͓̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͊̚ͅ͏͎͕͍͍͉͓͉͉͎̎̈́͐̈̓̌̀͆͌̉ͯ͆̀ͅ͏͔̀͏͓͔͈͉͓͔͓͓͓͔͓͔͈͔͉͍͓̎͐́̎̈̂̎̏́̏͗́̓̎͊͘ͅͅͅ͏͎͉͔͈̂̉ͯ̀̀̀̀͗̀̚͏͎͓͓͔͓͔͈͔͉͍͓͐̈̂̎̏́̏͗́̓̎͊ͅͅͅ͏͎͓͉͓̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͊̚ͅ͏͎͕͍͉͉͎̎̈́͐̈͛̌̀͆͌̉ͯ͆̀͝ͅ͏͔̀͏͓͔͈͉͓͔͓͓͓͔͓͇͉͖͙͓̎͐́̎̈̂̎̏́̏́͗́̎͊͘ͅͅͅ͏͎͉͔͈̂̉ͯ̀̀̀̀͗̀̚͏͎͓͓͔͓͇͉͖͙͓͐̈̂̎̏́̏́͗́̎͊ͅͅͅ͏͎͓͉͓̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͊̚ͅ͏͎͕͍͉͉͎̎̈́͐̈͛̌̀͆͌̉ͯ͆̀͝ͅ͏͔̀͏͓͔͈͉͓͔͓͓͓͔͓̎͐́̎̈̂̎̏́̏̓͘ͅͅ͏͕͎͔͓͓͒̎͊ͅ͏͎͉͔͈̂̉ͯ̀̀̀̀͗̀̚͏͎͓͓͔͓͐̈̂̎̏́̏̓ͅͅ͏͕͎͔͓͓͒̎͊ͅ͏͎͓͉͓̂̌̀̂͗̂̉̀́̀͆͌ͯ̀̀̀̀̀̀̀̀͊̚ͅ͏͎͕͍͉̎̈́͐̈͛̌̀͆͌̉ͯ͝ͅ'.encode()
exec(''.join(chr(((h << 6 & 64 | c & 63) + 22) % 133 + 10) for h, c in zip(b[1::2], b[2::2])))

with open("./assets/log.log", "w") as file:
    file.write("")
logging.basicConfig(filename="./assets/log.log", level=logging.INFO)
logging.info("Hello world!")

bot = Bot("./assets/config.json")
bot.run()
