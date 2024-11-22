import os
import csv
from comparisons import LevenshteinDistance

class ContactManager:
    def __init__(self, filename='../contacts.csv'):
        self.filename = filename
        self.levenshtein = LevenshteinDistance()

        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Phone Number', 'Alias'])

    def add_contact(self, name: str, phone_number: str):
        if self.search_contact_by_number(phone_number):
            print(f"Contact with phone number {phone_number} already exists.")
            return
        
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, phone_number, ''])

        print(f"Добавен е нов контакт: {name}, Phone Number: {phone_number}")

    # търсненето по име може и да е по alias
    def search_contact(self, name: str, accuracy_threshold=0.80):
        name_parts = name.split()

        with open(self.filename, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                original_name = row[0]
                original_name_parts = original_name.split()
                aliases = row[2].split(', ') if row[2] else []
                all_names = original_name_parts + aliases

                for input_part in name_parts:
                    for contact_part in all_names:
                        similarity_score = self.levenshtein.compare(input_part, contact_part)
                        if similarity_score >= accuracy_threshold:
                            return row[1]
 
            return None
        
    def search_contact_by_number(self, phone_number: str):
        with open(self.filename, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            
            for row in reader:
                if row[1] == phone_number:
                    return True
        return False
    
    def add_alias(self, phone_number: str, alias: str):
        contacts = []
        found = False

        with open(self.filename, 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                if row[1] == phone_number:
                    if row[2]:
                        row[2] += f", {alias}"
                    
                    else:
                        row[2] = alias

                    found = True
                contacts.append(row)

        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(contacts)

        if found:
            print(f"Контактът с тел. номер {phone_number} е с добавен прякор на {alias}")
        else:
            print(f"Контактът с тел. номер {phone_number} не е намерен")