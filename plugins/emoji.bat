@echo off
chcp 65001 > nul
title Emoji Library v1.5 [WinTool's 2026 EDITION]
color 0F
mode con: cols=122 lines=60

set "sound=ON"
:: Ustawienie tła startowego ikon na BIAŁE (F0)
set "t_code=F0"

:: Włączenie ANSI
for /f "tokens=2 delims=: " %%a in ('reg query HKCU\Console /v VirtualTerminalLevel 2^>nul') do set vt=%%a
if not defined vt (
    reg add HKCU\Console /f /v VirtualTerminalLevel /t REG_DWORD /d 1 >nul
)

set "R=[38;5;196m"
set "Y=[38;5;226m"
set "G=[38;5;34m"
set "B=[38;5;21m"
set "N=[0m"

:language_setup
cls
echo.
echo                  [31m:                                   :            [32mEt
echo                 [31mt#,                            .    t#,           [32mE#t                                        ;;[0m
echo     [31mt          ;##W.              i          ;W    ;##W.          [32mE##t               t                      ;W[0m
echo    [31m ED.        :#L:WE            LE         f#E   :#L:WE:         [32mE#W#t  GEEEEEEEL   Ej   GEEEEEEEL        f#E[0m
echo     [31mE#K:      .KG  ,#D          L#E       .E#f   .KG   ,#D        [32mE#tfLt    L#K      E#,     L#K         .E#f[0m
echo    [31m E##W;     EE    ;#f        G#W.       iWW;    EE    ;#f       [32mE#t.      t#E      E#t     t#E        iWW;[0m
echo     [31mE#E##t   f#.     t#i      D#K.       L##Lffi f#.     t#i  [32mffW#Dffj.     t#E      E#t     t#E       L##Lffi[0m
echo     [31mE#ti##f :#G      GK      E#K.       tLLG##L  :#G      GK    [32m;LW#ELLLf.  t#E      E#t     t#E      tLLG##L[0m
echo     [31mE#t ;##D.;#L    LW.     .E#E.         ,W#i    ;#L    LW.      [32mE#t       t#E      E#t     t#E        ,W#i[0m
echo     [31mE#ELLE##K:t#f f#:      .K#E          j#E.       t#f f#:       [32mE#t       t#E      E#t     t#E       j#E.[0m
echo     [31mE#L;;;;;;, f#D#;      .K#D          .D#j         f#D#;        [32mE#t       t#E      E#t     t#E     .D#j[0m
echo     [31mE#t          G#t     .W#G          ,WK,           G#t         [32mE#t       t#E      E#t     t#E    ,WK,[0m
echo     [31mE#t           t      :W##########Wt EG.            t          [32mE#t        fE  ##  E#t      fE    EG.[0m
echo                         [2m:,,,,,,,,,,,,,.;;                         ;#t        ::  ## .,;.      ::   ;;[0m
echo.
echo                                                     [34mt#,     L.          [33m,E E#Wi            t#,      L.[0m
echo                                                [34mi   ;##W.    EW[33m:        [33m,ft E###G.         ;##W.     EW:        ,ft[0m
echo        [34m┌─────────----──────┐                   LE :#L:WE    E##[33m;       t#E E#fD#W;        :#L:WE    E##;       t#E[0m
echo        [34m│  [37mSelect language  [34m│                 L#E .KG  ,#D   E##[33m#t      t#E E#t t##L      .KG  ,#D   E###t      t#E[0m
echo        [34m├────────----───────┤                G#W. EE    ;#f  E#f[33mE#f     t#E E#t  .E#K,    EE    ;#f  E#fE#f     t#E[0m
echo        [34m│ [37m[1]  English      [34m│               D#K. f#.     t#i E#t [33mD#G    t#E E#t    j##f f#.     t#i  E#t D#G    t#E[0m
echo        [34m├───────----────────┤              E#K.  :#G      GK E#t [33m f#E.  t#E E#t    :E#K::#G      GK  E#t  f#E.  t#E[0m
echo        [34m│ [37m[2]  Polski      [34m │            .E#E.    ;#L    LW. E#t  [33m t#K: t#E E#t   t##L   ;#L    LW.  E#t   t#K: t#E[0m
echo        [34m├───────----────────┤           .K#E       t#f f#:   E#t  [33m  ;#W,t#E E#t .D#W;      t#f f#:   E#t    ;#W,t#E[0m
echo        [34m│ [37m[3]  Help / Pomoc [34m│          .K#D         f#D#;    E#t   [33m  :K#D#E E#tiW#G.        f#D#;    E#t     :K#D#E[0m
echo        [34m└───────--─--───────┘         .W#G           G#t     E#t   [33m   .E##E E#K##i           G#t     E#t      .E##E[0m
echo                                     [34m:W##########Wt   t                [33m G#E E##D.            ..      G#E        .#E[0m

choice /c 123 /n
set "lang_choice=%errorlevel%"

if %lang_choice%==1 (set "lang=EN" & goto main_menu_en)
if %lang_choice%==2 (set "lang=PL" & goto main_menu_pl)
if %lang_choice%==3 (
    if exist "help.html" (start "" "help.html")
    goto language_setup
)

:main_menu_en
set "lang=EN"
set "L_SEL_CAT=Select category"
set "L_ERR_HTML=ERROR: help.html file not found."
set "L_SEL_MODE=SELECTION MODE"
set "L_IDX=INDEX"
set "L_COL_W=White" & set "L_COL_B=Blue" & set "L_COL_K=Black" & set "L_COL_S=Silver"
set "L_MAIN=Main Menu" & set "L_INPUT=Icon number or Color" & set "L_COPIED=COPIED" 
set "L_ERR_SEL=ERROR: Invalid selection." & set "L_ERR_CAT=ERROR: Invalid category."
color 0F
cls    
echo.
echo          [2m▄▄▄▄▄▄▄▄                          ██         ██[0m                                    [2;3mWindows support by[0m   
echo          ██▀▀▀▀▀▀                          ▀▀         ▀▀                                %R%████████████  %Y%████████████%N%
echo          ██         ████▄██▄   ▄████▄     ████       ████                               %R%████████████  %Y%████████████%N%
echo          ███████    ██ ██ ██  ██▀  ▀██     ██         ██                                %R%████████████  %Y%████████████%N%
echo          ██         ██ ██ ██  ██    ██     ██         ██                                %R%████████████  %Y%████████████%N%
echo          ██▄▄▄▄▄▄   ██ ██ ██  ▀██▄▄██▀     ██       ▄▄▄██▄▄▄     
echo          [2m▀▀▀▀▀▀▀▀   ▀▀ ▀▀ ▀▀    ▀▀▀▀        ██▀▀    ▀▀▀▀▀▀▀▀[0m                            %G%████████████  %B%████████████%N%
echo.                                                                                        %G%████████████  %B%████████████%N%
echo          [2m▄▄             ██     ▄▄[0m                                                       %G%████████████  %B%████████████%N%
echo          ██             ▀▀     ██                                                       %G%████████████  %B%████████████%N%
echo          ██           ████     ██▄███▄    [2m██▄████     ▄█████▄   ██▄████    ▀██  ███[0m            [2;3mpolsdoft.ITS™[0m 
echo          ██             ██     ██▀  ▀██   ██▀         ▀ ▄▄▄██   ██▀         ██▄ ██  
echo          ██             ██     ██    ██   ██         ▄██▀▀▀██   ██          ████▀  
echo          ██▄▄▄▄▄▄   ▄▄▄██▄▄▄   ███▄▄██▀   ██         ██▄▄▄███   ██           ███   
echo          [2m▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀   ▀▀ ▀▀▀     ▀▀          ▀▀▀▀ ▀▀   ▀▀            ██[0m
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo                                      🚀 Emoji Library v1.5 [WinTool's 2026 EDITION]
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo.
echo    [1]  💻 Computers              [2]  📱 Mobile                [3]  💾 Memory/Office       [4]  ⚡ Energy/Industry
echo    [5]  🛠️ Tools/Build            [6]  💠 Shapes/Symbols        [7]  😃 Faces/ASCII         [8]  🌿 Nature/Animals
echo    [9]  ☁️ Weather/Time           [10] ⚽ Sport/Entertain       [11] 🎮 Games               [12] 🎬 Movies
echo    [13] 🎵 Music                  [14] 🎨 Art                   [15] 🍕 Food                [16] ✈️ Travel/Vehicles
echo    [17] 💊 Medicine/Health        [18] 👕 Clothes/Style         [19] 🪐 Space/Astro         [20] 🎲 Random/Mix
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo               [S]  🔉 Sound: [%sound%]      [R]  🔄 Refresh      [i]  💡 Info      [H]  ❔ Help      [X]  ❌ Exit
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
set /p wybor="  » %L_SEL_CAT% [1;3m%username%[0m: "
goto process_choice

:main_menu_pl
set "lang=PL"
set "L_SEL_CAT=Wybierz kategorię"
set "L_ERR_HTML=BŁĄD: Nie znaleziono pliku help.html."
set "L_SEL_MODE=TRYB WYBORU"
set "L_IDX=INDEKS"
set "L_COL_W=Białe" & set "L_COL_B=Niebieskie" & set "L_COL_K=Czarne" & set "L_COL_S=Srebrne"
set "L_MAIN=Menu Główne" & set "L_INPUT=Numer ikony lub kolor" & set "L_COPIED=SKOPIOWANO"
set "L_ERR_SEL=BŁĄD: Nieprawidłowy wybór." & set "L_ERR_CAT=BŁĄD: Nieprawidłowa kategoria."
color 0F
cls    
echo.
echo          [2m▄▄▄▄▄▄▄▄                          ██         ██[0m                                    [2;3mWindows support by[0m   
echo          ██▀▀▀▀▀▀                          ▀▀         ▀▀                                %R%████████████  %Y%████████████%N%
echo          ██         ████▄██▄   ▄████▄     ████       ████                               %R%████████████  %Y%████████████%N%
echo          ███████    ██ ██ ██  ██▀  ▀██     ██         ██                                %R%████████████  %Y%████████████%N%
echo          ██         ██ ██ ██  ██    ██     ██         ██                                %R%████████████  %Y%████████████%N%
echo          ██▄▄▄▄▄▄   ██ ██ ██  ▀██▄▄██▀     ██       ▄▄▄██▄▄▄     
echo          [2m▀▀▀▀▀▀▀▀   ▀▀ ▀▀ ▀▀    ▀▀▀▀        ██▀▀    ▀▀▀▀▀▀▀▀[0m                            %G%████████████  %B%████████████%N%
echo.                                                                                        %G%████████████  %B%████████████%N%
echo          [2m▄▄             ██     ▄▄[0m                                                       %G%████████████  %B%████████████%N%
echo          ██             ▀▀     ██                                                       %G%████████████  %B%████████████%N%
echo          ██           ████     ██▄███▄    [2m██▄████     ▄█████▄   ██▄████    ▀██  ███[0m            [2;3mpolsdoft.ITS™[0m 
echo          ██             ██     ██▀  ▀██   ██▀         ▀ ▄▄▄██   ██▀         ██▄ ██  
echo          ██             ██     ██    ██   ██         ▄██▀▀▀██   ██          ████▀  
echo          ██▄▄▄▄▄▄   ▄▄▄██▄▄▄   ███▄▄██▀   ██         ██▄▄▄███   ██           ███   
echo          [2m▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀   ▀▀ ▀▀▀     ▀▀          ▀▀▀▀ ▀▀   ▀▀            ██[0m
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo                                      🚀 Biblioteka Emoji v1.5 [WinTool's 2026]
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo.
echo         [1]  💻 Komputery             [2]  📱 Mobile               [3]  💾 Pamięć/Biuro       [4]  ⚡ Energia/Przemysł
echo         [5]  🛠️ Narzędzia/Budowa      [6]  💠 Kształty/Symbole     [7]  😃 Buźki/ASCII        [8]  🌿 Przyroda/Zwierzęta
echo         [9]  ☁️ Pogoda/Czas           [10] ⚽ Sport/Rozrywka       [11] 🎮 Gry                [12] 🎬 Filmy
echo         [13] 🎵 Muzyka                [14] 🎨 Sztuka               [15] 🍕 Jedzenie           [16] ✈️ Podróże/Pojazdy
echo         [17] 💊 Medycyna/Zdrowie      [18] 👕 Ubrania/Styl         [19] 🪐 Kosmos/Astro       [20] 🎲 Losowe/Mix
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo               [S]  🔉 Dźwięk: [%sound%]      [R]  🔄 Odśwież      [i]  💡 Info      [H]  ❔ Pomoc      [X]  ❌ Wyjście
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
set /p wybor="  » %L_SEL_CAT% [1;3m%username%[0m: "
goto process_choice

:process_choice
if /i "%wybor%"=="i" (
    if "%lang%"=="EN" goto info_en
    goto info_pl
)
if /i "%wybor%"=="h" (
    if exist "help.html" (
        start "" "help.html"
    ) else (
        echo.
        echo    [!] %L_ERR_HTML%
        if "%sound%"=="ON" powershell -c "[console]::beep(400,250)" >nul
        timeout /t 2 > nul
    )
    if "%lang%"=="EN" goto main_menu_en
    goto main_menu_pl
)
if /i "%wybor%"=="r" (
    if "%lang%"=="EN" goto main_menu_en
    goto main_menu_pl
)
if /i "%wybor%"=="x" exit
if /i "%wybor%"=="s" (
    if "%sound%"=="ON" (set "sound=OFF") else (set "sound=ON")
    if "%lang%"=="EN" goto main_menu_en
    goto main_menu_pl
)

set "isValid="
for /L %%i in (1,1,20) do if "%wybor%"=="%%i" set isValid=1
if not defined isValid goto input_error

:: DATABASE
if "%wybor%"=="1"  set "list=💻_Laptop 🖥️_Monitor ⌨️_Key 🖱️_Mouse 🖲️_Trackball 🕹️_Joystick 🖨️_Printer 💾_Floppy 💿_Disc 🔌_Plug 📡_Antenna 🔋_Battery 🎛️_Knobs 🎚️_Slider 📱_Smartphone 📽️_Projector 🎞️_Film 🎧_Headphones 🔊_Speaker 📺_TV 📟_Pager 📠_Fax 🧭_Compass ⏱️_Stopwatch ⏲️_Timer 🕰️_Clock 💡_Idea 🔦_flashlight 🕯️_Candle 🛰️_Satellite"
if "%wybor%"=="2"  set "list=📱_Phone 📲_Arrow ☎️_Tel 📞_Handset 📶_Signal 📡_Antenna 💬_Bubble 📧_Email 🔍_Search 🔔_Bell 📵_Prohibited 📳_Vibrate 📴_Off 🔇_Mute 🔈_Quiet 🔉_Medium 🔊_Loud 📢_Megaphone 📣_Info 📯_Horn 📪_Mail1 📫_Mail2 📬_Mail3 📭_Mail4 📮_Mailbox 🎙️_Micro 📻_Radio 🎧_Audio 📸_Camera 🤳_Selfie"
if "%wybor%"=="3"  set "list=💾_Disk 💿_CD 📁_Folder 📂_Open 📄_File 📃_List 📜_Scrolls 📋_Board 📅_Date 📆_Calendar 📈_Growth 📉_Drop 📊_Chart 📁_Cat1 📂_Cat2 🗂️_Index 🗃️_Box 🗄️_Cabinet 📝_Note 📑_Bookmarks 🖇️_Clips 📎_Clip 📏_Ruler 📐_SetSquare 📌_Pushpin 📍_Pin2 📎_Hook 🔒_Lock 🔑_Key 🏷️_Tag"
if "%wybor%"=="4"  set "list=⚡_Lightning 🔋_Battery 🔌_Plug 💡_Bulb ⚙️_Gear 🔧_Wrench 🔨_Hammer 🏭_Factory 🧪_Vial ☢️_Atom ⚒️_Pickaxe 🛠️_Tools ⛏️_Blade 🔩_Screw ⚙️_Wheel 🧱_Bricks 🏗️_Crane 🏢_Office 🏭_Chimney 🧨_Dynamite 💣_bomb 🌋_Volcano 🚒_FireTruck 🔦_Flashlight 🏮_Lantern ⛓️_Chain 🧯_Extinguisher 🛡️_Shield 🏹_Bow 🔧_Workshop"
if "%wybor%"=="5"  set "list=🛠️_Set ⚒️_Hammers ⛏️_Pick 🪚_Saw 🪛_Screwdriver 🔩_Screw 🧱_Wall 🏗️_Construct 🏠_House 🚧_Barrier 🏘️_Estate 🏚️_Ruin 🏛️_Hall ⛪_Church 🕌_Mosque ⛩️_Gate 🕍_Synagogue 🏛️_Museum 🏗️_Works 🏢_Skyscraper 🏨_Hotel 🏬_Store 🏗️_Skeleton 🏘️_Houses ⛲_Fountain 🧱_Block 🏗️_Arm 🪜_Ladder 🪟_Window 🛗_Elevator"
if "%wybor%"=="6"  set "list=💠_Gem 🌀_Swirl ♾️_Infinity 🔴_RedSphere 🔵_BlueSphere ⬛_BlackSq ⬜_WhiteSq ✨_Sparkle 💎_Diamond ⭕_Circle 🟥_RedSq 🟦_BlueSq 🟧_Orange 🟨_Yellow 🟩_Green 🟪_Purple 🟫_Brown 🖤_BlackHeart 🤍_WhiteHeart 🤎_BrownHeart 💔_Broken ❣️_Exclaim 💕_Hearts 💞_Spinning 💓_Beating 💗_Growing 💖_Shining 💘_Arrow 💝_Gift 💟_Decor"
if "%wybor%"=="7"  set "list=😀_Smile 😂_Laugh 😍_Heart 😎_Cool 🤔_Think 😭_Cry 👍_OK 🔥_Fire 💀_Skull 🚀_Rocket 🥳_Party 🤩_Wow 🤪_Crazy 🤫_Shh 🫠_Melting 🫡_Salute 🫣_Peeking 🥵_Hot 🥶_Cold 🤯_Explode 🤥_Liar 🤢_Nausea 🤮_Vomit 🤧_Sneeze 😵_Dizzy 🧐_Monocle 🤠_Cowboy  clowns_Clown 👹_Monster 👻_Ghost"
if "%wybor%"=="8"  set "list=🌿_Herb 🐶_Dog 🐱_Cat 🐭_Mouse 🐹_Hamster 🐰_Rabbit 🦊_Fox 🐻_Bear 🐼_Panda 🐨_Koala 🐯_Tiger 🦁_Lion 🐮_Cow 🐷_Pig 🐸_Frog 🐵_Monkey 🐔_Chicken 🐧_Pingwin 🐦_Bird 🐤_Chick 🦆_Duck 🦅_Eagle 🦉_Owl 🦇_Bat 🐺_Wolf 🐗_Boar 🐴_Horse 🦄_Unicorn 🐝_Bee 🌵_Cactus"
if "%wybor%"=="9"  set "list=☀️_Sun ☁️_Cloud ⛈️_Storm ❄️_Snow 🌈_Rainbow 🌊_Wave 🌪️_Tornado ⌛_Hourglass ⏰_Alarm 📅_Date 🌤️_SunCloud 🌦️_RainSun 🌥️_Cloudy 🌧_Rain 🌨_Snowing 🌩_Bolt 🌫_Fog 🌬️_Wind 🌅_Sunrise 🌇_Sunset 🌉_Bridge 🌃_Night 🌌_MilkyWay ⏱️_Stopwatch ⏲️_Timer 🕰️_Clock ⌛_Time ⏳_Sand 📅_Year 🌙_Moon"
if "%wybor%"=="10" set "list=⚽_Soccer 🏀_Basket 🎾_Tennis 🥊_Boxing 🚴_Bike 🏊_swimmer 🏆_Cup 🥇_Gold 🎯_Target 🏁_Finish 🏈_Football 🏉_Rugby 🏐_Volley 🏒_Hockey 🏸_Badminton 🏏_Cricket ⛳_Golf 🏹_Bow 🎣_Fish 🎿_Skis ⛸️_Skates 🪁_Kite 🎱_8Ball 🎲_Dice 🧩_Puzzle ♟️_Chess 🧗_Climber 🏇_Horse 🥋_Karate 🚣_Rower"
if "%wybor%"=="11" set "list=🎮_Pad 🕹️_Stick 👾_Alien 🎲_Dice 🃏_Joker 🀄_Mahjong 🧩_Puzzle ♟️_Chess 🎰_Casino 🎯_Darts 🏎️_F1 🛹_skateboard 🏹_Shooting 🎭_Mask 🥊_Gloves 🪄_Wand 🧿_Eye 🔮_Ball 🧸_Bear 🪀_YoYo 🪁_Kite 🏏_Paddle 🏐_BallV 🏈_BallA 🏀_BallK 🎾_BallT 🎮_Game 🕹️_Retro 👾_Pixel 🎮_Play"
if "%wybor%"=="12" set "list=🎬_Clapper 🎞️_Film 📽️_Projector 🎥_Camera 🍿_Popcorn 🧟_Zombie 🧛_Vampire 👻_Ghost 🎭_Theater 🎟️_Ticket 📼_VHS 📀_DVD 📺_TV 🎞️_Movie 🎬_Action 🎬_Scene 🎞️_Frame 🎭_Drama 📽️_Cinema 🎟️_Entry 🍿_Snack 📺_Screen 🎥_Record 🎬_Start 🎟️_Coupon 🎞️_Tape 🎭_Comedy 🎟️_Seats 📼_Tape 📽️_Screening"
if "%wybor%"=="13" set "list=🎵_Note 🎶_Notes 🎹_Keys 🎸_Guitar 🎻_Violin 🎷_Sax 🎺_Trumpet 🥁_Drums 🎧_Headphones 📻_Radio 🎙️_Mic 🎚️_Slider 🎛️_Knobs 🎤_Voc 🔊_Speaker 🔉_Lower 🔈_Mute 🎼_Clef 🎶_Melody 🎹_Piano 🎸_Electric 🎻_Bow 🎺_Trombone 🥁_Percussion 🎙️_Studio 📻_Receiver 🎧_DJ 🎤_Show 🎵_Sing 🎶_Song"
if "%wybor%"=="14" set "list=🎨_Palette 🖌️_Brush 🖼️_Painting 🗿_Statue 🏛️_Antique ✏️_Pencil 🏰_Castle ⛩️_Shinto 🕋_Kaaba ⛲_Fountain 🖋️_Pen 🖊️_Pen2 🖍️_Crayon 📝_Sketch 📓_Notebook 📔_Diary 📕_Book 📖_Read 📜_Parchment 🏺_Vase 🏛️_Column 🎨_Art 🖌️_Paint 🖼️_Gallery 🗿_Moai 🎨_Design 🏰_Fortress 🖋️_Ink 🖍️_Draw 🎭_Mask"
if "%wybor%"=="15" set "list=🍕_Pizza 🍔_Burger 🍟_Fries 🌭_Hotdog Sushi_Sushi 🍦_IceCream 🍺_Beer ☕_Coffee 🍰_Cake 🍎_Apple 🌮_Taco 🌯_burrito 🥗_Salad 🍲_Soup 🍱_Lunch 🥟_Dumplings 🦞_Lobster 🥩_Steak 🥨_Pretzel 🥞_Pancake  bagel_bagels 🧀_Cheese 🥦_Broccoli 🥑_avocado 🥓_Bacon 🍩_Donut 🍪_Cookie 🍹_Drink 🍷_Wine 🥣_Bowl"
if "%wybor%"=="16" set "list=✈️_Plane 🚀_Rocket 🚗_Car 🚆_Train 🚢_Ship 🚲_Bike 🗺️_Map 🗽_Statue 🗼_Tower ⛽_Fuel 🚜_Tractor 🚛_Truck 🚐_Bus 🚑_Ambulance 🚒_Fire 🏎️_Race 🏍️_Motor ⛵_Sail 🛶_Canoe 🛳️_Liner 🛸_UFO 🚁_Copter 🚠_CableCar 🛰️_Satellite ⚓_Anchor 🚧_Works 🚥_Lights 🚦_Signal 🗺️_Globe 🧭_Compass"
if "%wybor%"=="17" set "list=💊_Meds 💉_Syringe 🩺_Stethoscope 🧬_DNA 🌡️_Termometr 🩹_Bandage 🚑_Ambulance 🏥_Hospital 🧠_Brain 🦷_Tooth 🦴_Bone 🧬_Genes 🔬_Microscope 🔭_Telescope 🩸_Blood 🦠_Virus 🩺_Exam 💊_Pill 🌡️_Fever 🩹_Dressing 🚑_Help 🏥_Clinic 🧠_Mind 🦷_Dentist 🦴_Szkielet 🧪_Test 🔬_Lab 🧬_Helix 🩺_Doctor 💊_Vitamins"
if "%wybor%"=="18" set "list=👕_Tshirt 👖_Pants 👗_Sukienka 👟_Shoes 🕶️_Okulary 💍_Ring 💼_Briefcase 👜_Handbag ⌚_Watch 💄_Szminka 🎒_Backpack 👠_Heels 👢_Boots 🧤_gloves 🧣_Scarf 🎩_Cylinder 🧢_Cap 🧣_Shawl 💍_Diamond 💎_Gem 💼_Case 👜_Bag 👛_Purse 🧥_Coat 🥼_LabCoat 🦺_Vest 👚_Blouse 👙_Bikini 👗_Outfit"
if "%wybor%"=="19" set "list=🌍_Earth 🌙_Moon ☀️_Sun 🪐_Saturn 🚀_Rocket 🛸_UFO 🛰️_Satellite 🔭_telescope ☄️_Comet 🌌_MilkyWay 🌑_NewMoon 🌒_Crescent 🌓_Quarter 🌔_Gibbous 🌕_Full 🌖_Waning 🌗_Quarter2 🌘_Crescent2 🌙_Luna 🌚_Night 🌠_Meteor 🌡️_Atmos 👽_Alien 👾_Pixel 🤖_Robot 👨‍🚀_Astronaut 🛰️_Orbit 📡_Dish 🔭_Space 💥_Explosion"
if "%wybor%"=="20" set "list=🍀_Luck 💎_Diamond 🔥_Fire 👑_Korona 🌈_Tęcza 🦄_Unicorn 🧨_Firecracker 🧿_Eye 🎭_Masks 🧠_Brain 🛸_Saucer 🌋_Lawa 🛸_Ship 🧨_Fuse 🍺_Mug 🍕_Slice 🛹_Skate 🎸_Gitara 💰_Bags 💎_Treasure 💊_Tabs 🧿_Amulet 🏹_Bow 🦾_Arm 🚀_Flight 🛸_Alien 🧬_Kod ☣️_Biohazard ☢️_Radiation 🏁_Finish"

:show_group
color %t_code%
cls
echo.
echo   [ %L_SEL_MODE% ]  ──────────────────────────────────────────────────────────────────────────────────────────────
echo.
setlocal enabledelayedexpansion
set n=1
set "line="
for %%a in (%list%) do (
    for /f "tokens=1,2 delims=_" %%b in ("%%a") do (
        set "icon_!n!=%%b"
        set "name_!n!=%%c"
        if !n! LSS 10 (set "line=!line!  [!n!] %%b    ") else (set "line=!line! [!n!] %%b    ")
    )
    set /a mod=!n!%%8
    if !mod! equ 0 (echo !line! & echo. & set "line=")
    set /a n+=1
)
if not "!line!"=="" echo !line!

echo.
echo   [ %L_IDX% ] ──────────────────────────────────────────────────────────────────────────────────────────────────────
echo.
set n=1
set "idx_line="
for %%a in (%list%) do (
    for /f "tokens=1,2 delims=_" %%b in ("%%a") do (
        set "nm=%%c                "
        if !n! LSS 10 (set "idx_line=!idx_line! [!n!] !nm:~0,14! ") else (set "idx_line=!idx_line![!n!] !nm:~0,14! ")
    )
    set /a mod=!n!%%5
    if !mod! equ 0 (echo    !idx_line! & set "idx_line=")
    set /a n+=1
)
if not "!idx_line!"=="" echo    !idx_line!

echo.
echo   ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo          [B] %L_COL_W%   [N] %L_COL_B%   [C] %L_COL_K%   [S] %L_COL_S%   ^|   [M] %L_MAIN%
echo   ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
set /p choice="  » %L_INPUT%: "

if /i "%choice%"=="M" (
    endlocal & set "t_code=F0"
    if "%lang%"=="EN" goto main_menu_en
    goto main_menu_pl
)
if /i "%choice%"=="B" endlocal & set "t_code=F0" & goto show_group
if /i "%choice%"=="N" endlocal & set "t_code=1F" & goto show_group
if /i "%choice%"=="C" endlocal & set "t_code=0F" & goto show_group
if /i "%choice%"=="S" endlocal & set "t_code=8F" & goto show_group

if defined icon_%choice% (
    set "to_copy=!icon_%choice%!"
    echo | set /p="!to_copy!" | clip
    if "%sound%"=="ON" powershell -c "[console]::beep(1200,80)" >nul
    echo.
    echo    ✨ %L_COPIED%: !to_copy!
    timeout /t 1 > nul
    endlocal & set "t_code=F0"
    if "%lang%"=="EN" goto main_menu_en
    goto main_menu_pl
) else (
    color 4F
    echo.
    echo    [!] %L_ERR_SEL%
    if "%sound%"=="ON" powershell -c "[console]::beep(400,250)" >nul
    timeout /t 2 > nul
    endlocal & goto show_group
)

:input_error
color 4F
echo.
echo    [!] %L_ERR_CAT%
if "%sound%"=="ON" powershell -c "[console]::beep(400,250)" >nul
timeout /t 2 > nul
if "%lang%"=="EN" goto main_menu_en
goto main_menu_pl

:info_en
color 0B
cls
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo                                         📖 Emoji Library v1.5 - INFO
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo.
echo        ✅  SYSTEM STATISTICS
echo            - Total Icons: 600       - Categories: 20       - Audio Feedback: %sound%
echo            - Stability: 100%%        - Release Year: 2026
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo.
echo                                              Sebastian Januchowski
echo                                           polsoft.its@fastservice.com
echo                                           https://github.com/seb07uk
echo                                            2026© polsoft.ITS London
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pause
goto main_menu_en

:info_pl
color 0B
cls
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo                                        📖 Biblioteka Emoji v1.5 - INFO
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo.
echo        ✅  STATYSTYKI SYSTEMU
echo            - Ikony łącznie: 600     - Kategorie: 20        - Dźwięk: %sound%
echo            - Stabilność: 100%%      - Rok wydania: 2026
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
echo.
echo                                              Sebastian Januchowski
echo                                           polsoft.its@fastservice.com
echo                                           https://github.com/seb07uk
echo                                            2026© polsoft.ITS London
echo.
echo   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pause
goto main_menu_pl