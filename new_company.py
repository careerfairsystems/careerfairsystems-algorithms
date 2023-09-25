import json
import random

r1 = open('test_hosts.json')
r2 = open('test_companies.json')

hosts = json.load(r1)
companies = json.load(r2)

# TODO: Någonstans i koden så skriver den över en tidigare vald company och inte hanterar 
# advantage. T.ex Niklas får Fogarolli när André, Enya och Linus har Fogarolli som första 
# val. Någon av dessa tre ska ha den och resterande två ska ha högre advantage.
# Gissningsvis är detta ett problem från "Second choice", dubbelkolla så first choice fungerar

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
    if(i == 10):
        break
    
# Post-processing to ensure all hosts have two companies
for host, data in hosts.items():
    while len(data["assigned"]) < 2:
        for company, assigned_hosts in companies.items():
            if len(assigned_hosts) == 0:
                data["assigned"].append(company)
                companies[company].append(host)
                break

    
print(json.dumps(hosts, indent=2))
print(json.dumps(companies, indent=2))
        

print("Companies with no host assigned:")
for company in companies:
    if not companies[company]:
        print(company)

r1.close()
r2.close()