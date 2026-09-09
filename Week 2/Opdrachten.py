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

<<<<<<< HEAD
>>>>>>> f760b71aa4da231b107898180242c720055d2761
=======
>>>>>>> 8a20a76c34e3a3ee4a3a78c122e49ea8e41de1af
print(f"Average Grade: {average}")
print("--------------------")

filtered_records = [record for record in records if float(record['Grade']) >= 80.0]

print("Student Report")
print("--------------")

