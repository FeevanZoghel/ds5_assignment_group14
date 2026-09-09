def import_file() -> list:
    """
    Importeert een CSV-bestand via een input statement.

    Returns:
        list: Een lijst met alle records uit het CSV-bestand.

    """
    file_path = input("Enter the path to the CSV file: ")

    records = []

    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            records.append(row)
            total = sum(float(record['Grade']) for record in records)
            average = total / len(records)

    return records

def gemiddelde_score(records) -> float:
    """
    Print het gemiddelde cijfer van alle records
    """
    total = sum(float(record['Grade']) for record in records)
    average = total / len(records)
    print(f"Average Grade: {average}")
    print("--------------------")

    return average

def Excellent_records(records):
    """
    Kijkt of een cijfer hoger is dan een 80.0 en filterd die eruit
    """
    filtered_records = [record for record in records if float(record['Grade']) >= 80.0]
    
    """
    Kijkt of een cijfer hoger is dan een 80.0 en filterd die eruit
    
    returns: 
        list: Een lijst met namen + gehaalde cijfers van studenten met een cijfer gelijk of hoger dan 80.0

    """"
    filtered_records = [record for record in records if float(record['Grade']) >= 80.0]
    print("Student Report")
    print("--------------")
    for record in filtered_records:
        print(f"Name: {record['Name']}")
        print(f"Grade: {record['Grade']}")
        print("--------------------")

    return filtered_records
    


