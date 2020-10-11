import csv
wordlist = []


with open("unsorted.txt", "r") as drinks_file:
    drinks_file_reader = csv.reader(drinks_file, quoting = csv.QUOTE_ALL)
    
    for drink in drinks_file_reader:
        wordlist.append(*drink)

wordlist = sorted(wordlist)

with open("available_passwords.txt", "w", newline = "") as drinks_file: #drinks_filepath.replace(".txt", ".csv")
    drinks_file_writer = csv.writer(drinks_file, quoting = csv.QUOTE_ALL)
    
    for drink in wordlist:
        drinks_file_writer.writerow([drink])