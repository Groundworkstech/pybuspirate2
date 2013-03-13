#!/usr/bin/env python
# encoding: utf-8
"""
This file is part of pyBusPirate2
Download at http://code.google.com/p/pybuspirate2/

Copyright (c) 2010 Sebastian Muniz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
__version__ = "0.1"
__author__  = "Sebastian 'topo' Muniz"

__all__     = [ "Banners", "randomBanner"]

from random import randint, seed

Banners = [
r"""
                 ____             ____  _             __      ___ 
    ____  __  __/ __ )__  _______/ __ \(_)_________ _/ /____ |__ \
   / __ \/ / / / __  / / / / ___/ /_/ / // ___/ __ `/ __/ _ \__/ /
  / /_/ / /_/ / /_/ / /_/ (__  ) ____/ // /  / /_/ / /_/  __/ __/ 
 / .___/\__, /_____/\__,_/____/_/   /_//_/   \__,_/\__/\___/____/ 
/_/    /____/                                                     
""",

r"""
 \,___, ,    .  /   \  ,   .   ____ /   \ ` .___    ___  _/_     ___  /   \
 |    \ |    `  |,_-<  |   |  (     |,_-' | /   \  /   `  |    .'   `   _-'
 |    | |    |  |    ` |   |  `--.  |     | |   ' |    |  |    |----'  /   
 |`---'  `---|. `----' `._/| \___.' /     / /     `.__/|  \__/ `.___, /___,
 \       \___/                                                             
""",

r"""
             ____            _____ _           _       ___  
            |  _ \          |  __ (_)         | |     |__ \ 
 _ __  _   _| |_) |_   _ ___| |__) | _ __ __ _| |_ ___   ) |
| '_ \| | | |  _ <| | | / __|  ___/ | '__/ _` | __/ _ \ / / 
| |_) | |_| | |_) | |_| \__ \ |   | | | | (_| | ||  __// /_ 
| .__/ \__, |____/ \__,_|___/_|   |_|_|  \__,_|\__\___|____|
| |     __/ |                                               
|_|    |___/                                                

""",

r"""
  _   _   _   _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( p | y | B | u | s | P | i | r | a | t | e | 2 )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
""",

r"""
              ______               ______ __              __          ______ 
.-----.--.--.|   __ \.--.--.-----.|   __ \__|.----.---.-.|  |_.-----.|__    |
|  _  |  |  ||   __ <|  |  |__ --||    __/  ||   _|  _  ||   _|  -__||    __|
|   __|___  ||______/|_____|_____||___|  |__||__| |___._||____|_____||______|
|__|  |_____|                                                                
""",

"""
             8\"\"\"\"8               8\"\"\"\"8                            eeee 
eeeee e    e 8    8   e   e eeeee 8    8 e  eeeee  eeeee eeeee eeee    8 
8   8 8    8 8eeee8ee 8   8 8   " 8eeee8 8  8   8  8   8   8   8       8 
8eee8 8eeee8 88     8 8e  8 8eeee 88     8e 8eee8e 8eee8   8e  8eee eee8 
88      88   88     8 88  8    88 88     88 88   8 88  8   88  88   8    
88      88   88eeeee8 88ee8 8ee88 88     88 88   8 88  8   88  88ee 8eee 
""",

r"""
            .---.             .---.  _             .-.      .---. 
            : .; :            : .; ::_;           .' `.     `--. :
.---. .-..-.:   .'.-..-. .--. :  _.'.-..--.  .--. `. .'.--.   ,','
: .; `: :; :: .; :: :; :`._-.': :   : :: ..'' .; ; : :' '_.'.'.'_ 
: ._.'`._. ;:___.'`.__.'`.__.':_;   :_;:_;  `.__,_;:_;`.__.':____;
: :    .-. :                                                      
:_;    `._.'                                                      
""",

r"""                                                                           
             _-_ _,,               -__ /\\                   ,         /\  
                -/  )                ||  \\  '         _    ||        (  ) 
-_-_  '\\/\\   ~||_<   \\ \\  _-_,  /||__|| \\ ,._-_  < \, =||=  _-_    // 
|| \\  || ;'    || \\  || || ||_.   \||__|| ||  ||    /-||  ||  || \\  //  
|| ||  ||/      ,/--|| || ||  ~ ||   ||  |, ||  ||   (( ||  ||  ||/   /(   
||-'   |/      _--_-'  \\/\\ ,-_-  _-||-_/  \\  \\,   \/\\  \\, \\,/  {___ 
|/    (       (                      ||                                    
'      -_-                                                                 
""",

r"""
              ______         _____                      _   
             (, /    )      (, /   ) ,                 '  ) 
    __         /---(      _  _/__ /    __  _  _/_  _  ,--'  
    /_)_(_/_) / ____)(_(_/_)_/     _(_/ (_(_(_(___(/_/___   
 .-/   .-/ (_/ (          ) /                               
(_/   (_/                (_/                                
""",

r"""                                                                               
               .oPYo.                .oPYo.  o                o         .oPYo. 
               8   `8                8    8                   8             `8 
.oPYo. o    o o8YooP' o    o .oPYo. o8YooP' o8 oPYo. .oPYo.  o8P .oPYo.    oP' 
8    8 8    8  8   `b 8    8 Yb..    8       8 8  `' .oooo8   8  8oooo8 .oP'   
8    8 8    8  8    8 8    8   'Yb.  8       8 8     8    8   8  8.     8'     
8YooP' `YooP8  8oooP' `YooP' `YooP'  8       8 8     `YooP8   8  `Yooo' 8ooooo 
8 ....::....8 :......::.....::.....::..::::::....:::::.....:::..::.....:.......
8 :::::::ooP'.:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
..:::::::...:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
""",

r"""
      _        _             _  
._   |_)    _ |_)o._ _._|_ _  ) 
|_)\/|_)|_|_> |  || (_| |_(/_/_ 
|  /                            
""",

r"""
         _____         _____ _         _       ___ 
 ___ _ _| __  |_ _ ___|  _  |_|___ ___| |_ ___|_  |
| . | | | __ -| | |_ -|   __| |  _| .'|  _| -_|  _|
|  _|_  |_____|___|___|__|  |_|_| |__,|_| |___|___|
|_| |___|                                          
""",

r"""
              (  _`\              (  _`\  _             ( )_         /'__`\ 
 _ _    _   _ | (_) ) _   _   ___ | |_) )(_) _ __   _ _ | ,_)   __  (_)  ) )
( '_`\ ( ) ( )|  _ <'( ) ( )/',__)| ,__/'| |( '__)/'_` )| |   /'__`\   /' / 
| (_) )| (_) || (_) )| (_) |\__, \| |    | || |  ( (_| || |_ (  ___/ /' /( )
| ,__/'`\__, |(____/'`\___/'(____/(_)    (_)(_)  `\__,_)`\__)`\____)(_____/'
| |    ( )_| |                                                              
(_)    `\___/'                                                              
""",

r"""
             ______             ______ _                         ______  
            (____  \           (_____ (_)              _        (_____ \ 
 ____  _   _ ____)  )_   _  ___ _____) )  ____ _____ _| |_ _____  ____) )
|  _ \| | | |  __  (| | | |/___)  ____/ |/ ___|____ (_   _) ___ |/ ____/ 
| |_| | |_| | |__)  ) |_| |___ | |    | | |   / ___ | | |_| ____| (_____ 
|  __/ \__  |______/|____/(___/|_|    |_|_|   \_____|  \__)_____)_______)
|_|   (____/                                                             

""",

r"""
            , __            , __                        __ 
           /|/  \          /|/  \o                     /  )
   _        | __/        ,  |___/    ,_    __, _|_  _    / 
 |/ \_|   | |   \|   |  / \_|    |  /  |  /  |  |  |/   /  
 |__/  \_/|/|(__/ \_/|_/ \/ |    |_/   |_/\_/|_/|_/|__//___
/|       /|                                                
\|       \|                                                
""",

r"""
            __             __                         __ 
          |/  |           /  | /           /         /  )
 ___      |___|      ___ (___|   ___  ___ (___  ___ (  / 
|   )\   )|   )|   )|___ |    | |   )|   )|    |___)  / )
|__/  \_/ |__/ |__/  __/ |    | |    |__/||__  |__   /_/ 
|      /                                                 
"""
]

def randomBanner():
    seed()
    banner_num = randint(0, len(Banners) - 1)
    return Banners[banner_num]

