# careerfairsystems-algorithms

## Company host distribution
=============================
There now exist a company host distribution with a accuracy of >90% for disributed hosts.
Please check the code if the Excel sheets or names is corresponding to the one in the code. Otherwise fix it.

#### Pseudo code
================
```
WHILE loop (runs until all hosts have two companies assigned or until the loop counter exceeds the maximum length of the "remaining" list):

    1. Check if all hosts have two companies assigned:
       - If all hosts have two companies, exit the loop.

    2. Assign the first choice of companies to hosts:
       a. Iterate over the prioritized list of companies:
          i. If the current company already has a host assigned, skip to the next company.
          ii. Create a temporary list of hosts whose first choice is the current company and who have less than two companies assigned.
          iii. If there are hosts in the temporary list:
               - If there's more than one host in the list:
                 1. Sort the hosts based on the length of their "remaining" list and their advantage points.
                 2. Choose the first host from the sorted list.
                 3. Increase the advantage points for the other hosts in the list.
               - If there's only one host in the list, choose that host.
               - Assign the current company to the chosen host.
               - Add the chosen host to the list of hosts assigned to the current company.

    3. Assign the second choice of companies to hosts:
       a. Iterate over all companies:
          i. If the current company already has one or more hosts assigned, skip to the next company.
          ii. Create a temporary list of hosts who have the current company in their "remaining" list and have less than two companies assigned.
          iii. If the number of hosts in the temporary list matches the loop counter:
               - If there's more than one host in the list:
                 1. Sort the hosts based on the length of their "remaining" list and their advantage points.
                 2. Choose the first host from the sorted list.
                 3. Increase the advantage points for the other hosts in the list.
               - If there's only one host in the list, randomly choose that host.
               - Assign the current company to the chosen host.
               - Add the chosen host to the list of hosts assigned to the current company.

    4. Increment the loop counter by 1.
```

#### The data
==============

Inside the company host distribution folder there exist two test files for showing how the data is supposed to look like for the algorithm to work.

The company data is simply an dict where the key is the company name and each key value has an empty list where the assigned host name is supposed to be. Only one company host is applicable for a company.
```
{
    "ARKAD": [],
    "TLTH": [],
    ...
}
```

The host data is a dict where each key is the host name of the applied company host. Each host have some values which have an important role in the algorithm.
```
{
    "Test Person 2": {
        "first": "ARKAD",
        "remaining": [...],
        "advantage": 0,
        "assigned": []
    },
    "Test Person 2": {
        "first": "TLTH",
        "remaining": ["ARKAD", ...],
        "advantage": 0,
        "assigned": []
    },
    ...
}
```
The `first` value is the company hosts priority choice of company. The `remaining` is the other choices from the company host which is not the first priority. `advantage` is simply when a student loses the lottery of a company if e.g. two students want the same company and have the same amount of total applied companies it is randomised which company host will be assigned to this company. The one who lost will get a higher advantage which increases the chances for assigning a company to you. `assigned` is simply the companies that have been assigned to the company host. A maximum of two companies can be assigned per company host.


## TBD
======
- BANQUET SEATMAP (https://github.com/careerfairsystems/gasque-algorithm)[Potential algorithm]
- Booking system for interviews for LG/PG/Coordinators
