# CRSEnlistmentTool

Here's the README file for your CRS Enlistment Probability Tool, including instructions on how to use it and the required CSV file format.

CRS Enlistment Probability Tool
This Python script helps students estimate their chances of getting a desired, non-conflicting roster of classes during a batch enlistment process, based on class availability and demand. It uses a Monte Carlo simulation to account for the probabilistic nature of enlistment and resolves conflicts (overlapping times, same subject) based on your class rankings.

Features
Calculates the overall probability of securing a non-conflicting final roster based on your desired classes.
Provides subject-wise recommendations, indicating the probability of getting at least one class for each desired subject and suggestions for optimizing your applications.
Reads class data directly from a user-friendly CSV file.
How it Works
The tool simulates the batch enlistment process many times (default 100,000 simulations):

Individual Class Probabilities: For each class you apply for, it calculates the individual probability of getting a slot: (Available Slots / Demand).
Random Allocation: In each simulation run, it randomly determines which classes you get based on these individual probabilities.
Conflict Resolution: If you are "granted" conflicting classes (either due to overlapping schedules or attempting to get more than one class under the same subject), the system automatically drops the lower-ranked class to keep the higher-ranked one.
Roster Formation: A final, non-conflicting roster is formed for that simulation run.
Success Check: A simulation is considered "successful" if your final roster contains at least one class for every unique subject you initially desired, without any remaining conflicts among them.
Overall Probability: The overall probability is then calculated as (Number of Successful Simulations / Total Simulations) * 100.
Setup
Save the Script: Copy the entire Python code provided to you and save it in a file named up_enlistment_tool.py (or any other name ending with .py).
Save Your CSV File: Create your class data in a CSV file and save it as asdfghjkl - Sheet1.csv. This CSV file MUST be in the same directory as your up_enlistment_tool.py script.
CSV File Format Specification
Your asdfghjkl - Sheet1.csv file must have the following column headers and data formats:

Column Header	Description	Data Type	Example Value(s)
Subject	The unique subject code (e.g., "PE 2", "MATH 101"). Crucial for the "one class per subject" rule.	Text	PE 2, FIL 40
Class Name	A unique identifier for the specific class section (e.g., "WF W1", "Sec A").	Text	WF W1, THX, Sec A
Available Slots	The number of available slots for this specific class.	Integer	20, 15, 25
Demand	The total number of students who applied for this class.	Integer	62, 70, 80
Rank	Your personal preference rank for this class (1 being highest priority).	Integer	1, 2, 3
Days	The days the class meets, represented as concatenated single letters. (Case-Insensitive)	Text	MWF, TH, S, U
Start Time	The class start time in 24-hour HHMM format (no colon).	Text (HHMM)	0830, 1300, 1745
End Time	The class end time in 24-hour HHMM format (no colon).	Text (HHMM)	1000, 1500, 1915
Notes	(Optional) Any personal notes or comments. This column is ignored by the script.	Text	Conflicts with Math 101, Preferred section

Export to Sheets
Day Letter Mapping:

M = Monday
T = Tuesday
W = Wednesday
H = Thursday
F = Friday
S = Saturday
U = Sunday
Example CSV Content:

Code snippet

Subject,Class Name,Available Slots,Demand,Rank,Days,Start Time,End Time,Notes
PE 2,WF W1,20,62,1,WF,0830,1000,
PE 2,CH W1,20,55,2,MH,0900,1030,
FIL 40,THX,15,70,3,TH,0900,1030,
MATH 101,Sec A,25,80,4,MWF,1100,1200,
ARTS 1,Lec B,30,120,5,TH,1000,1130,
PE 2,ST W1,20,50,6,MW,0830,1000,Conflicts with PE 2 WF W1 and PE 2 CH W1 by subject code, and with MATH 101 by time
Running the Tool
Open Terminal/Command Prompt: Navigate to the directory where you saved up_enlistment_tool.py and asdfghjkl - Sheet1.csv.
On Windows, search for "cmd" or "Command Prompt".
On macOS/Linux, search for "Terminal".
Use the cd command to change directory (e.g., cd C:\Users\YourUser\Documents\EnlistmentTool).
Execute the Script: Run the script using the Python interpreter:
Bash

python up_enlistment_tool.py

Output
The script will print the following information to your terminal:

Simulation Progress: Indicates the number of simulations being run.
Overall Roster Probability: Your estimated percentage chance of getting a non-conflicting final roster that includes at least one class for every unique subject you applied for.
Subject-wise Recommendations: For each unique subject you listed, it will display:
The probability of getting at least one class for that subject.
A recommendation (High, Medium, or Low probability) with guidance on whether to add more alternatives for that subject or reconsider existing applications to free up slots.
Important Notes
The 'Overall Roster Probability' assumes that for each unique subject you desire, getting at least one class for that subject (the highest ranked non-conflicting one) counts as success.
The simulation accounts for time conflicts and 'same subject' conflicts, dropping lower-ranked classes as per UP rules.
This tool does NOT consider unit limits (e.g., 21 units max for undergrads) or PE class limits. You must ensure your desired classes adhere to these.
This tool does NOT optimize your schedule (e.g., minimize breaks). It focuses purely on probability of acquisition.
The accuracy of the probability depends on the 'Available Slots' and 'Demand' data being accurate for your specific enlistment period.
'Demand' can change dynamically, so probabilities are a snapshot at the time of data collection.
Days are parsed as single concatenated letters: M=Monday, T=Tuesday, W=Wednesday, H=Thursday, F=Friday, S=Saturday, U=Sunday. Input is converted to uppercase for parsing.
Time (Start Time, End Time) is parsed in HHMM format (e.g., 0700 for 07:00, 1330 for 13:30).
