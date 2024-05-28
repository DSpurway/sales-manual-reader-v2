import csv

MTM = "9080MME"

with open("C:\\Users\\029878866\\Downloads\\ibm_product_lifecycle_list.csv", encoding='latin1') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    headers = next(reader, None)
    print (headers)
    for row in reader:
        if MTM == row[5]:
            GA = row[6]
            EOM = row[8]
            EOS = row[12]
            print (MTM, GA, EOM, EOS)
