# Installation and Usage

## Installation

- Clone github repository as follows:
```bash
git clone https://github.com/60307390/scheduler-udst.git && cd scheduler-udst
```
- Make virtualenv:

  On Linux:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
  On Windows:
  ```bash
  python -m venv venv
  venv\Scripts\activate 
  ```

- Install requirements.txt
```bash
pip install -r requirements.txt
```

## Usage

### Text File Format
- Copy paste to a plain-text file (program uses `schedules.txt` as **default**) containing all sections (including section name).
- File would look something like:
```
SSHA 1004
Ethical Reasoning
Course Information
Class Selection
Select a class option
7 options
Option
Status
Session
Class
Meeting Dates
Days and Times
Room
Instructor
Seats
1
Open
Regular Academic Session
LecTheatre - Class 2518 -Section 1
Lecture - Class 2519 -Section 2
31/12/2024 - 15/04/2025
Sunday
5:00PM to 6:30PM
Tuesday
2:00PM to 3:30PM
01.2.05
05.1.65
Rodney Robertson
Rodney Robertson
Open Seats 109 of 120
Open Seats 28 of 30

...
```
- For adding more classes, simply append after a new line in the same format.
```
SSHA 1004
Ethical Reasoning
Course Information
Class Selection
...

INFS 3104
Data Structures & Algorithms
Course Information
Class Selection
...
```

### Program Usage
```
usage: scheduler.py [-h] [--list-schedules] [--query] [--schedule SCHEDULE] [--open-with OPEN_WITH]

options:
  -h, --help            show this help message and exit
  --list-schedules, --get-schedules, -ls
                        print compatible schedules
  --query, -q           go directly into query mode
  --schedule SCHEDULE, --sch SCHEDULE, -s SCHEDULE
                        uses the provided .txt file for schedule (default: schedules.txt)
  --open-with OPEN_WITH, --open OPEN_WITH, -o OPEN_WITH
                        open with specified program
```


- By **default**, the program uses `schedules.txt` as the input file. However, if you want to use other files, you can pass in the path with the `--schedule` flag
```bash
python scheduler.py --schedule "path/to/custom-schedules.txt"/[PATH TO TXT]
```
- Run the program with `--list-schedules` to view schedules and to make sure schedules are compatible (empty list or 0 in output means incompatile schedule). Will print a list of tuples you can use in the next step.
```bash
python scheduler.py --list-schedules
```
- To input the tuple you want, run the script normally as `python scheduler.py` and it generals a `.xlsx` file in the directory, containing timetable of the selected schedule.
- *NEW:* To open the output automatically with a program, can use `--open-with` flag and pass in the program's name/path as an argument. If given a valid schedule, it will open the excel sheet automatically. (*NOTE: not tested in Windows*).
```bash
python scheduler.py --open-with libreoffice/[PATH TO PROGRAM]
```
- Also contains query mode to query your schedules (search through your tuples) using the wildcard `*`. For example:
```bash
python scheduler.py --query
```
```
Enter course options: 2 * * * *

Here are the combinations that work: 
(2, 1, 6, 1, 1)
(2, 1, 7, 1, 1)
(2, 2, 6, 1, 1)
(2, 2, 7, 1, 1)
(2, 3, 1, 1, 2)
```
