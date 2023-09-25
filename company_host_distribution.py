import random
import pandas as pd

df_hosts = pd.read_excel('VÄRDAR 2023.xlsx', sheet_name='COMPANY HOST DATA', usecols='B:D')
df_companies = pd.read_excel('VÄRDAR 2023.xlsx', sheet_name='COMPANY HOST STATISTIK ')

companies = df_companies["Företag"].tolist()
host_names = df_hosts["Unnamed: 1"].tolist()
host_first = df_hosts["Unnamed: 2"].tolist()
host_remaining = df_hosts["Unnamed: 3"].tolist()

hosts = {
    name: {
        "first": first,
        "remaining": remaining,
        "advantage": 0,
        "assigned": []
    }
    for name, first, remaining in zip(host_names, host_first, host_remaining) if not str(name) == "nan"
}

companies = {
    company: []
    for company in companies if not company == "nan"
}


i = 1
# Before the while loop, create a list of companies prioritized by how many students have them as their first choice
company_priority = sorted(companies.keys(), key=lambda c: sum(1 for h, data in hosts.items() if data["first"] == c), reverse=True)

while(True):
    # Check if all hosts have two companies assigned
    all_assigned = all(len(data["assigned"]) == 2 for _, data in hosts.items())
    if all_assigned:
        break
    
    # First choice
    for company in company_priority:
        if companies[company]:  # If the company already has one host assigned, then it is done
            continue
        tmp_hosts = [host for host, data in hosts.items() if data["first"] == company and len(data["assigned"]) < 2]
        
        if tmp_hosts:
            if len(tmp_hosts) > 1:
                sorted_students = sorted(tmp_hosts, key=lambda x: (len(hosts[x]["remaining"]), -hosts[x]["advantage"]))
                chosen = sorted_students[0]
                for student in sorted_students[1:]:
                    hosts[student]["advantage"] += 1
            else:
                chosen = tmp_hosts[0]
            
            hosts[chosen]["assigned"].append(company)
            companies[company].append(chosen)    
            
    # Second choice
    for company in companies:
        # If the company already has one or more hosts assigned, then it is done
        if len(companies[company]) >= 1:
            continue

        tmp_hosts = []

        for host in hosts:
            h = hosts[host]
            # If the host has already chosen two companies, the host is then done
            if len(h["assigned"]) > 1:
                continue

            # Check if the company is in the host's "remaining" list           
            if company in h["remaining"]:
                tmp_hosts.append(host)

        if len(tmp_hosts) == i:
            if len(tmp_hosts) > 1:
                sorted_students = sorted(tmp_hosts, key=lambda x: (len(hosts[x]["remaining"]), -hosts[x]["advantage"]))
                
                # The first student in the sorted list is the chosen one
                chosen = sorted_students[0]
                
                # All other students receive an "advantage" point
                for student in sorted_students[1:]:
                    hosts[student]["advantage"] += 1
            else:
                chosen = random.choice(tmp_hosts)

            hosts[chosen]["assigned"].append(company)
            companies[company].append(chosen)
    
    
    i += 1
    # break
    if(i == 5):
        break

# Post-processing to ensure all hosts have two companies
for host, data in hosts.items():
    while len(data["assigned"]) < 2:
        assigned_company = False  # Flag to check if a company was assigned in the current iteration
        
        for company, assigned_hosts in companies.items():
            if len(assigned_hosts) == 0:
                data["assigned"].append(company)
                companies[company].append(host)
                assigned_company = True
                break
        
        # If no company was assigned in the current iteration, break out of the while loop
        if not assigned_company:
            break
        

print("Companies with no host assigned:")
for company in companies:
    if not companies[company]:
        print(company)

# 1. Percentage of First Choices Fulfilled
first_choice_fulfilled = sum(1 for host, data in hosts.items() if data["first"] in data["assigned"])
percentage_first_choice = (first_choice_fulfilled / len(hosts)) * 100

# 2. Percentage of Any Choice (First or Remaining) Fulfilled
any_choice_fulfilled = sum(1 for host, data in hosts.items() if any(choice in data["assigned"] for choice in [data["first"]] + data["remaining"].split(", ")))
percentage_any_choice = (any_choice_fulfilled / len(hosts)) * 100

# 3. Average Advantage Points
average_advantage = sum(data["advantage"] for data in hosts.values()) / len(hosts)

# 4. Number of Hosts with Unfulfilled Choices
unfulfilled_hosts_data = [host for host, data in hosts.items() if not any(choice in data["assigned"] for choice in [data["first"]] + data["remaining"].split(", "))]
unfulfilled_hosts = len(unfulfilled_hosts_data)


print(f"\n\nPercentage of First Choices Fulfilled: {percentage_first_choice}%")
print(f"Percentage of Any Choice Fulfilled: {percentage_any_choice:.2f}%")
print(f"Average Advantage Points: {average_advantage}\n")
print(f"Number of Hosts with Unfulfilled Choices: {unfulfilled_hosts}")
print(f"The Hosts with Unfulfilled Choices: {unfulfilled_hosts_data}")
