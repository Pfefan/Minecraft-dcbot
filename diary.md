# Ingenieurstagebuch

## Stefan Pfeiffer

### 17.03.2022 Implemented "-rand"

#### 14:55 - 17:35

Added "-rand" which searchs through the database until a server with players online is found then its gona print details about the server (modt, version, players online, icon)

### 18.02.2022 bug fixes and performance improvements

#### 15:00 - 18:00

Reworked my code from yesterday

### 20.02.2022 tried to add details

#### 12:00 - 14:00

Added details but removed it afterwards because it was buggy

### 1.03.2022

#### 11:35 - 13:15

Used pylint to fix code formating

### 2.03.2022

#### 7:50 - 9:30

Moved bot token out of main to a seperate file because security flaw

### 3.03.2022 - 14.03.2022 Fixed issue

Tried to fix a error where the bot would search through all servers but then would restart after he was done -> data was lost 
Rewrote my code so the data is written to a database which is read out by a seperate func

### 15.03.2022

#### 7:25 - 12:25

Fixed pylint errors, new embled for details method for displaying more infos

### 16.03.2022

#### 7:50 - 9:30

All playersnames of the curently selected server will be show if u use -details

### 17.03.2022

#### 14:55 - 17:35

-details will now also show the geolocation of the server, worked on rewritting the database when servers are looked up

### 05.04.2022

#### 09:45 - 10:35

moved every command to a separete file added -list to show servers with specific properties

### 25.04.2022

#### 7:20 - 7:50

added players option to -list fixed a ping error when a port was added to port and wasnt reachable

### 27.04.2022

#### 7:50 - 9:30

working on -list, removed randomcmd because it was used as for testing as beginning, added onlinecmd, adjusted programm to mcstatus update, moved geolocation from a seperate file to a databasecmd because its a general command.

### 27.04.2022

#### 9:45 - 10:25

Multithreaded player search

### 28.04.2022

#### 14:15 - 17:35

Fixed embeds for -list players and version, moved databases and database structure files in a subdirectory, moved pingserver to a seprate file to automaticly ping every 1 hour 

### 5.5.2022

### 14:55 - 17:35

working on serverhistory fixing issues

### 24.5.2022

#### 14:04 - 17:35

working on displaying player activity on a server, modifyed exeptions in listcmd

### 9.6.2022

#### 14:55 - 17:35

Added mutlti prozessing so other code can be run without affecting the main programm, started to work on logging the playeractivity

### 16.06.2022

#### # 10.00 - 20.00

working on logging playeractivity and remade the database so the data can be stored more logical

### 17.06.2022

#### 10.00 - 20.00

used mathlib libary to display data info in discord, added a requirements.txt so required libaries can be install more easily working on plot so text wont overlap anymore

### 18.06.2022

#### 10.00 - 20.00

Updated Readme, removed ".vscode" folder from repository

### 19.06.2022

#### 13.00 - 14.00

Fixed overlapping text

### 21.06.2022

### 11:35 - 13:15

changed diagramm size

