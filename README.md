# FOOTBALLSTATS
This program is built for showing the information about various football clubs and competitions from the command-line using [API](https://en.wikipedia.org/wiki/Application_programming_interface). The API used here is from [football-data.org](https://www.football-data.org/). Please refer to the website to get more information about the API.

## Prerequisites
Python 3.8 is used
This program utilizes the ```requests``` library which doesn't come with the default python packages, you need to install the library additionally.
>pip install requests

## Usage
The program needs a API key to get the informations, so to get a free API key go to [football-data.org](https://www.football-data.org/) and get a API key. Then you will need to put the API key in the ```src``` directory with a filename of ```api_key.txt``` (the one given in this repo is a sample and not a valid key). There are several queries you can perform through this program. Use the command promt or any terminal of your choice where you can run python. You will need to navigate to this ```footballstats``` directory in the terminal to run this program.

The list of actions that can be done

* To access the id of a perticular club

Check [this]() file if you're unable to find your club, names of the clubs may differ from traditional.
>python main.py club_info {club_name}

#### Example:
```
>> python main.py club_info Juventus FC

Club name: Juventus FC
Club id: 109
```
This id is what you'll need to provide for later queries.

* **To access the player names of a club**

>python main.py squad_info {club_name}

#### Example:
```
>> python main.py squad_info FC Bayern Munich

Club Name: FC Bayern Munich
Players:
Manuel Neuer (GK)
Sven Ulreich (GK)
Jérôme Boateng (DF)
....
```

* **To get the standings of a competitions**

To get the list od the compettions available for the free tier users check [this]() page
>python main.py league_table {comptetition_name}

#### Example:
```
>> python main.py league_table PL

Total Matches:
=============
     Club Name       ||   Played   ||    Won     ||    Draw    ||    Lost    ||   Points   ||    For     || ....
-------------------------------------------------------------------------------------------------------------------
    Liverpool FC     ||     29     ||     27     ||     1      ||     1      ||     82     ||     66     || ....
 Manchester City FC  ||     28     ||     18     ||     3      ||     7      ||     57     ||     68     || ....
     Chelsea FC      ||     29     ||     14     ||     6      ||     9      ||     48     ||     51     || ....
....
```

* **To access the matches of a club**

To get the club use the earlier mentioned command.
>python main.py club_match_info {club_id} {start date}(optional) {end date}(optional)

#### Example:
```
>> python main.py club_match_info 86

Showing all the matches of Real Madrid CF:
Match scheduled on: 2019-08-17
Match status: FINISHED
Matchday: 37
Winner: Real Madrid CF
Home team: RC Celta de Vigo: 1
Away team: Real Madrid CF: 3
========================
Match scheduled on: 2019-08-24
Match status: FINISHED
....
```

You can also give additional two arguments as start date and end date to get the matches during that period (the dates must be given in YYYY-MM-DD format)
#### Example:
```
>> python main.py club_match_info 86 2019-03-01 2019-06-01
```
Or you can provid only the starting date and it'll show you all the matches till today(for free tier users this is limited)
#### Example:
```
>> python main.py club_match_info 86 2020-03-01
```

* **To access the matches of a competition**

For competition names check [this]() file.
>pyton main.py comp_match_info {competition_name} {start date}(optional) {end date}(optional)

#### Example:
```
>> python main.py comp_match_info SA

Showing all the matches of SA:
Match scheduled on: 2019-08-24
Match status: FINISHED
Matchday: 37
Winner: Juventus FC
Home team: Parma Calcio 1913: 0
Away team: Juventus FC: 1
========================
Match scheduled on: 2019-08-24
Match status: FINISHED
.....
```

For this also you can use a starting and end date to get the matches of certain time period
#### Example:
```
>> python main.py comp_match_info SA 2018-05-11 2018-10-20
```
Or you can give the starting date only (for free tier users this also is limited)
#### Example:
```
>> python main.py comp_match_info SA 2020-01-07
```
