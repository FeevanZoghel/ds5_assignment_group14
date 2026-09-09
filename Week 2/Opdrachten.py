def import_file(file_path):
    """
    Importeerd het csv bestand via een input statement.
    
    Fee
    
    """

    file_path = input("Enter the path to the CSV file: ")

records = []


with open(file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        records.append(row)
        total = sum(float(record['Grade']) for record in records)
        average = total / len(records)


total = sum(float(record['Grade']) for record in records)
average = total / len(records)


print(f"Average Grade: {average}")
print("--------------------")

filtered_records = [record for record in records if float(record['Grade']) >= 80.0]
    """
    Kijkt of een cijfer hoger is dan een 80.0 en filterd die eruit
    """"

print("Student Report")
print("--------------")


def print_records(filtered_records):
    """
    Print de naam en grade van elk record in een lijst

    Returns: print alleen de records en geeft geen waarde

    Julien 
    
    """
    for record in filtered_records:
        print(f"Name: {record['Name']}")
        print(f"Grade: {record['Grade']}")
        print("--------------------")


