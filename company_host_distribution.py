import pandas as pd

def program_to_text(program):
    return ""


# Prepare companies data
companies_df = pd.read_excel('companies.xlsx', sheet_name="profile")
companies = []
for company in companies_df.iterrows():
    props = company[1]
    name = props["name"]
    desired_programme = props["profile.desiredProgramme"]
    companies.append((name, desired_programme))

# Prepare company host data
hosts_df = pd.read_excel('hosts.xlsx')
company_hosts = []
for host in hosts_df.iterrows():
    props = host[1]
    name = props["Name"]
    email = props["Email"]
    program = program_to_text(props["Program and year of enrollment"])

    first, first_company = props["First choice of role"], props["If you selected COMPANY HOST as first choice, what organisation would you prefer to represent?"]
    second, second_company = props["Second choice"], props["If you selected COMPANY HOST as second choice, what organisation would you prefer to represent?"]
    third, third_company = props["Third choice"], props["If you selected COMPANY HOST as third choice, what organisation would you prefer to represent?"]
    
    company_priority = []
    for company in [first_company, second_company, third_company]:
        company_priority.append(company if company else "")
    company_priority.extend([""] * (3 - len(company_priority)))

    is_all_empty = all(item == "" for item in company_priority)
    if is_all_empty:
        continue

    company_hosts.append((name, email, program, company_priority))

print(company_hosts)
