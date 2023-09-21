import json
import random

r1 = open('test_hosts.json')
r2 = open('test_companies.json')

hosts = json.load(r1)
companies = json.load(r2)

i = 1
while(True):
    # First choice
    for company in companies:
        if companies[company]:
            continue
        tmp_hosts = []
        #print(company)
        for host in hosts:
            h = hosts[host]
            if len(h) == 2:
                continue
            # print(host)
            # print(h)
            if company == h["first"]:
                tmp_hosts.append(host)
        if len(tmp_hosts) == i:
            if len(tmp_hosts) > 1:
                min_remaining_lengths = {}
                for x in tmp_hosts:
                    y = hosts[x]
                    min_remaining_length = len(y["remaining"])
                    
                    # Update the dictionary with the minimum length
                    min_remaining_lengths.setdefault(min_remaining_length, []).append(x)
                    
                # Find the person with the lowest "remaining" length
                min_person = min(min_remaining_lengths, key=min_remaining_lengths.get)

                # Get the minimum "remaining" length
                min_length = min(min_remaining_lengths)

                # Get the list of people with the minimum "remaining" length
                min_people = min_remaining_lengths[min_length]
                
                # TODO:
                # OM båda studenterna enbart har ett företag kvar, då vinner studenten med
                # flest advantage. Studenten som förlorar får ett företag som ingen hade önskat.
                
                chosen = random.choice(min_people)
                for z in min_people:
                    if z != chosen:
                        hosts[z]["advantage"] += 1
            else:        
                chosen = random.choice(tmp_hosts)

            companies[company].append(chosen)
            
            
    # Second choice
    # for company in companies:
    #     if len(companies[company]) == 2:
    #         continue
    #     tmp_hosts = []
    #     for host in hosts:
    #         h = hosts[host]
    #         if company == h["second"]:
    #             tmp_hosts.append(host)
    #     if len(tmp_hosts) == i:
    #         chosen = random.choice(tmp_hosts)
    #         for x in tmp_hosts:
    #             if x != chosen:
    #                 hosts[x]["advantage"] += 1
    #         companies[company].append(chosen)
    
    i += 1
    print(hosts)
    print(companies)
    print("\n\n")
    if(i == 5):
        break
        
    
    


r1.close()
r2.close()