
# Ambulance Pickup Problem

## Problem Proposal:
Description
The ambulance planning real-time problem is to rescue as many people as possible following a disaster. The problem statement identifies the locations of people and the time they have to live. You can also establish mobile hospitals at the beginning of the problem. The problem is to get as many people to the hospitals on time as possible.

In our case, the graph is the Manhattan grid with every street going both ways. It takes a minute to go one block either north-south or east-west. Each hospital has an (x,y) location that you can determine when you see the distribution of victims. The ambulances need not return to the hospital where they begin. Each ambulance can carry up to four people. It takes one minute to load a person and one minute to unload up to four people. Each person will have a rescue time which is the number of minutes from now when the person should be unloaded in the hospital to survive. By the way, this problem is very similar to the vehicle routing problem about which there is an enormous literature and nice code like "jsprit" which was used in 2015 to great effect. If anyone wants to take a break from programming, he/she may volunteer to look up that literature and propose some good heuristics.

So the data will be in the form:
person(xloc, yloc, rescuetime)

In our case, there will be 5 hospitals and 300 victims

## Architecture:
The architect should specify a format for the output of each program and then validate the solutions. Players will specify an ambulance number, a hospital location, the locations of each patient being picked up and the destination hospital. You are welcome to use Yusuke's validator as a starting point. If there is a problem with a proposed solution, please find a nice way to illustrate it. 
## Notes:

   1. You are responsible to check for the order in which the ambulances are departed. 
i.e. if A has 3 ambulances, there is a path B -> A making 4 total at A, 
you will need to print the result B -> A before departing the 4th ambulance from A.
   2. If you run into any format issues, the program will only leave an error output, but NOT stop the execution.
Even if your output is being validated, it may have some errors printed (Sample output has few such errors displayed)
   3. If you find any bugs in the code, feel free to let us know, and we'll fix it for you.
   4. Kindly make your submissions (even if a skeleton with proper but non-optimized output) before the final day (10/19). 
This gives us a buffer to get back to you incase there is any error in compiling your code.

## Packagaes:

`pip install -r requirements.txt`

Or

`pip install matplotlib`

## Usage (Python):

Place your logic in `my_solution()` on line 376 and the code should do the rest for you.

If you do not want to mess with the validator file, you are free to follow the approach below (for other languages)
and you should be fine with using another .py file.

NOTE: The `readdata()` returns the list of **objects** and not a dictionary. 
You can use `object.prettify()` to get the dictionary instead.

## For Languages other than python:

**Input:** The data will be in the data.txt file

The given format is:

```angular2html
person(xloc,yloc,rescuetime)
1,1,10
...
...
2,2,20

hospital(numambulance)
1
2
3
```

**Output:** Once you calculate your results, generate a "result.txt" file with the following format

PN is the path of that particular ambulance.
```angular2html
Hospital:x_coordinate,y_coordinate,num_ambulances
...
Hospital:x_coordinate,y_coordinate,num_ambulances

Ambulance: H1: (start_x_coordinate,start_y_coordinate), P1: (x_coordinate,y_coordinate), P2: (x_coordinate,y_coordinate) ... PN: (x_coordinate,y_coordinate), H2: (end_x_coordinate,end_y_coordinate)  
...
Ambulance: H1: (start_x_coordinate,start_y_coordinate), P1: (x_coordinate,y_coordinate) P2: (x_coordinate,y_coordinate) ... PN: (x_coordinate,y_coordinate), H2: (end_x_coordinate,end_y_coordinate)
```
You can refer to the "sample_result.txt" to get the idea. The sample result is NOT optimal by any means

**Validation:** Once done with your code, you can then validate the result using the following:

(Sorry, but you need to learn how to run python file for this)

`python validator.py`

## Plot:

If you wish to disable the graph plot, simply comment the `plot()` on last line of the code

--------------------------------------------------------------------------
## Previous Readme by Yusuke Shinyama
validator.py

by Yusuke Shinyama (yusuke at cs dot nyu dot edu)

(Python2.3 or higher required to run this program.) -- <The updated git for Fall 2021 uses Python 3.x>


USAGE:

   Give the original data file and the output file to the program:

     $ ./validator.py datafile resultfile

   Or you can feed the result from stdin:

     $ yourprogram datafile | ./validator datafile

   The result file should be like this:

     Ambulance: 1: (45,32), 5: (84,26,95) total: 92
     Ambulance: 1: (45,32), 6: (64,30,74), 11: (56,26,80) total: 53
     Ambulance: 1: (45,32), 42: (29,42,67) total: 54
     Ambulance: 2: (59,68), 8: (68,57,52) total: 42
     Ambulance: 2: (59,68), 14: (66,47,58) total: 58
     ...

   I assumed that every line should begin with a string 'Ambulance' (case ignored).
   Then one hospital and one or two people follow. The last 'total' value is ignored.
   Intermediate blanks and commas are ignored, so 

        ambulance:   2  : ( 59 ,  68 ) , 8 : (  68, 57,52)    foo bar

   is still considered as a valid input.


SAMPLE RUN:

   $ ./validator.py sample_data sample_result
   Reading data: sample_data
   Reading results...
   Rescued: 47: (58,41,85) and 20: (62,50,112) taking 73
   Rescued: 11: (56,26,80) and 6: (64,30,74) taking 53
   Rescued: 5: (84,26,95) taking 92
   Rescued: 44: (82,55,74) taking 74
   Rescued: 25: (82,67,56) taking 50
   Rescued: 19: (64,75,47) and 33: (69,72,37) taking 37
   Rescued: 10: (58,95,108) taking 58
   Rescued: 8: (68,57,52) taking 42
   Rescued: 14: (66,47,58) taking 58
   Rescued: 45: (36,57,55) and 28: (35,57,39) taking 17
   Rescued: 43: (30,50,73) and 42: (29,42,67) taking 39
   Rescued: 39: (38,41,69) taking 26
   Rescued: 34: (24,65,56) taking 54
   Rescued: 9: (39,77,58) taking 56
   Rescued: 46: (25,53,34) taking 28
   Rescued: 3: (17,20,102) taking 100
   Rescued: 18: (18,1,71) and 4: (15,7,78) taking 63
   Rescued: 24: (58,15,87) taking 60
   Rescued: 40: (74,11,96) taking 84
   Rescued: 31: (86,9,116) taking 104
   Total score: 26
