import random
import pandas as pd
import json
import sys

df_hosts = pd.read_excel('VÄRDAR 2023.xlsx', sheet_name='ANDRÉS BLAD )', usecols='B:D')
df_companies = pd.read_excel('VÄRDAR 2023.xlsx', sheet_name='COMPANY HOST STATISTIK ')
df_companies_location = pd.read_excel('Företagsplacering 2023.xlsx', sheet_name='Andre')

companies = df_companies_location["företag"].tolist()
companies_location = df_companies_location["hus"].tolist()
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
    for name, first, remaining in zip(host_names, host_first, host_remaining)
}

companies = {
    company: {
        "host": [],
        "location": location,
    }
    for company, location in zip(companies, companies_location) if not company == "nan"
}


i = 1
# Before the while loop, create a list of companies prioritized by how many students have them as their first choice
company_priority = sorted(companies.keys(), key=lambda c: sum(1 for h, data in hosts.items() if data["first"] == c), reverse=True)

max_remaining_length = max(len(data["remaining"].split(", ")) for _, data in hosts.items() if data["remaining"] and not pd.isna(data["remaining"]))

while(i <= max_remaining_length):
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
            # Filter tmp_hosts by location (hus)
            tmp_hosts_same_location = [host for host in tmp_hosts if hosts[host].get("location") == companies[company]["location"]]
            if tmp_hosts_same_location:
                tmp_hosts = tmp_hosts_same_location
            
            if len(tmp_hosts) == 2:
                chosen = random.choice(tmp_hosts)
                for student in tmp_hosts[1:]:
                    hosts[student]["advantage"] += 1    
            elif len(tmp_hosts) > 2:
                # Modify your logic here to prioritize same-location hosts
                sorted_students = sorted(tmp_hosts, key=lambda x: (len(hosts[x]["remaining"]), -hosts[x]["advantage"], hosts[x]["location"] == companies[company]["location"]))
                chosen = sorted_students[0]
                for student in sorted_students[1:]:
                    hosts[student]["advantage"] += 1
            else:
                chosen = random.choice(tmp_hosts)
            
            hosts[chosen]["assigned"].append(company)
            companies[company]["host"].append(chosen)
            
            # Assign the host's location based on the location of their first assigned company
            hosts[chosen]["location"] = companies[company]["location"]
  
            
    # Second choice
    for company in companies:
        # If the company already has one or more hosts assigned, then it is done
        if len(companies[company]["host"]) >= 1:
            continue

        tmp_hosts = []

        for host in hosts:
            h = hosts[host]
            if pd.isna(h["first"]) or pd.isna(h["remaining"]):
                continue
            # If the host has already chosen two companies, the host is then done
            if len(h["assigned"]) > 1:
                continue

            # Check if the company is in the host's "remaining" list           
            if company in h["remaining"]:
                tmp_hosts.append(host)
        
        if tmp_hosts:
            # Filter tmp_hosts by location (hus)
            tmp_hosts_same_location = [host for host in tmp_hosts if hosts[host].get("location") == companies[company]["location"]]
            if tmp_hosts_same_location:
                tmp_hosts = tmp_hosts_same_location

            if len(tmp_hosts) == 2:
                chosen = random.choice(tmp_hosts)
                for student in tmp_hosts[1:]:
                    hosts[student]["advantage"] += 1
            elif len(tmp_hosts) > 2:
                # Modify your sorting key to handle missing "location" key
                sorted_students = sorted(tmp_hosts, key=lambda x: (
                    len(hosts[x]["remaining"]),
                    -hosts[x]["advantage"],
                    hosts.get(x, {}).get("location") == companies[company]["location"]
                ))
                # The first student in the sorted list is the chosen one
                chosen = sorted_students[0]
                # All other students receive an "advantage" point
                for student in sorted_students[1:]:
                    hosts[student]["advantage"] += 1
            else:
                chosen = random.choice(tmp_hosts)

            hosts[chosen]["assigned"].append(company)
            companies[company]["host"].append(chosen)
            
            # Assign the host's location based on the location of their second assigned company
            hosts[chosen]["location"] = companies[company]["location"]

        
    i += 1

# Additional Assignment Logic: Assign companies to hosts with 0 or 1 company assigned
while True:
    # Create a list of unassigned companies
    unassigned_companies = [company for company in companies if not companies[company]["host"]]
    
    # Create a list of hosts with less than two assigned companies
    hosts_with_less_than_two_companies = [host for host in hosts if len(hosts[host]["assigned"]) < 2]
    
    # Break if there are no more companies to assign or all hosts have at least two companies
    if not unassigned_companies or not hosts_with_less_than_two_companies:
        break

    # Track whether any company was assigned in this iteration
    company_assigned = False
    
    # Assign companies to hosts with priority given to same location (house)
    for host in hosts_with_less_than_two_companies:
        host_location = hosts[host].get("location")
        for company in unassigned_companies:
            company_location = companies[company].get("location")
            
            # Assign the company to the host if the location matches or if the host has no assigned companies
            if not host_location or not company_location or host_location == company_location:
                companies[company]["host"].append(host)
                hosts[host]["assigned"].append(company)
                unassigned_companies.remove(company)
                company_assigned = True  # Set the flag to indicate a company was assigned
                break
                
    # If no company was assigned in this iteration, break to avoid an infinite loop
    if not company_assigned:
        break



# Check for duplicate companies assigned to multiple hosts
assigned_company_hosts = {}
for host, data in hosts.items():
    for assigned_company in data["assigned"]:
        if assigned_company in assigned_company_hosts:
            assigned_company_hosts[assigned_company].append(host)
        else:
            assigned_company_hosts[assigned_company] = [host]
# Filter for duplicate companies
duplicate_companies = {company: hosts for company, hosts in assigned_company_hosts.items() if len(hosts) > 1}
# Print duplicate companies and the hosts they are assigned to
if duplicate_companies:
    print("\nDuplicate Companies and Their Assigned Hosts:")
    for company, hosts in duplicate_companies.items():
        host_list = ', '.join(hosts)
        print(f"{company}: {host_list}")
    print("CLOSING ALGORITHM")
    sys.exit()
else:
    print("No Duplicate Companies Assigned to Multiple Hosts")


# Print Hosts and their assigned companies
print("\nHosts and their assigned companies:")
for host, data in hosts.items():
    assigned_companies = ', '.join(data["assigned"])
    if len(data["assigned"]) == 1:
        print(f"{host} (One Company): {assigned_companies}")
    else:
        print(f"{host}: {assigned_companies}")


# Print Companies with no host assigned
print("\nCompanies with no host assigned:")
for company, data in companies.items():
    if not data["host"]:
        print(company)


# 1. Percentage of First Choices Fulfilled
first_choice_fulfilled = sum(1 for host, data in hosts.items() if (
    not pd.isna(data["first"]) and  # Check if "first" is not NaN
    not pd.isna(data["remaining"]) and  # Check if "remaining" is not NaN
    data["first"] in data["assigned"]
))
total_valid_hosts = sum(1 for data in hosts.values() if (
    not pd.isna(data["first"]) and  # Check if "first" is not NaN
    not pd.isna(data["remaining"])  # Check if "remaining" is not NaN
))
percentage_first_choice = (first_choice_fulfilled / total_valid_hosts) * 100

# 2. Percentage of Any Choice (First or Remaining) Fulfilled
any_choice_fulfilled = sum(1 for host, data in hosts.items() if (
    not pd.isna(data["first"]) and  # Check if "first" is not NaN
    not pd.isna(data["remaining"]) and  # Check if "remaining" is not NaN
    any(choice in data["assigned"] for choice in [data["first"]] + data["remaining"].split(", "))
))
percentage_any_choice = (any_choice_fulfilled / total_valid_hosts) * 100

# 3. Average Advantage Points
average_advantage = sum(data["advantage"] for host, data in hosts.items() if (
    not pd.isna(data["first"]) and  # Check if "first" is not NaN
    not pd.isna(data["remaining"])  # Check if "remaining" is not NaN
)) / total_valid_hosts

# 4. Number of Hosts with Unfulfilled Choices
unfulfilled_hosts_data = [host for host, data in hosts.items() if (
    not pd.isna(data["first"]) and  # Check if "first" is not NaN
    not pd.isna(data["remaining"]) and  # Check if "remaining" is not NaN
    not any(choice in data["assigned"] for choice in [data["first"]] + data["remaining"].split(", "))
)]
unfulfilled_hosts = len(unfulfilled_hosts_data)
unfulfilled_hosts_data = ', '.join(unfulfilled_hosts_data)


print(f"\n\nPercentage of First Choices Fulfilled: {percentage_first_choice}%")
print(f"Percentage of Any Choice Fulfilled: {percentage_any_choice:.2f}%")
print(f"Average Advantage Points: {average_advantage}\n")
print(f"Number of Hosts with Unfulfilled Choices: {unfulfilled_hosts}")
print(f"The Hosts with Unfulfilled Choices: {unfulfilled_hosts_data}")
