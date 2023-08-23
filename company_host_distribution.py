import pandas as pd

# Function to extract host section into textformat
def program_to_text(program):
    model = {
        "A": ["Arkitekt", "Industridesign"],
        "B": "Bioteknik",
        "BI": "Brandingenjörsutbildning",
        "V": ["Väg- och vatttenbyggnad", "Byggteknik med arkitektur", "Byggteknik med järnvägsteknik", "Byggteknik med väg- och trafikteknik"],
        "D": "Datateknik",
        "W": "Ekosystemteknik",
        "E": "Elektroteknik",
        "I": "Industriell ekonomi",
        "C": "Informations- och kommunikationsteknik",
        "K": "Kemiteknik",
        "L": "Lantmäteri",
        "MD": ["Maskinteknik med teknisk design", "Industridesign"],
        "M": ["Maskinteknik", "Automotive", "Automation"],
        "BME": ["Medicin och teknik", "Riskhantering"],
        "F": "Teknisk Fysik",
        "Pi": "Teknisk Matematik",
        "N": "Teknisk Nanovetenskap"
    }

    if "Pi" in program:
        section = "Pi"
    else:
        section = "".join(letter.upper() for letter in str(program) if letter.isalpha())

    return model[section] if section in model else ""


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
no_correct_programme_format = []
for host in hosts_df.iterrows():
    props = host[1]
    name = str(props["Name"])
    email = str(props["Email"])
    program = program_to_text(str(props["Program and year of enrollment"]))

    if not program:
        no_correct_programme_format.append((name, email, props["Program and year of enrollment"]))

    first, first_company = props["First choice of role"], props["If you selected COMPANY HOST as first choice, what organisation would you prefer to represent?"]
    second, second_company = props["Second choice"], props["If you selected COMPANY HOST as second choice, what organisation would you prefer to represent?"]
    third, third_company = props["Third choice"], props["If you selected COMPANY HOST as third choice, what organisation would you prefer to represent?"]
    
    company_priority = []
    for company in [first_company, second_company, third_company]:
        company_priority.append(str(company) if company else "")
    company_priority.extend([""] * (3 - len(company_priority)))

    is_all_empty = all(item == 'nan' for item in company_priority)
    if is_all_empty:
        continue

    company_hosts.append((name, email, program, company_priority))


