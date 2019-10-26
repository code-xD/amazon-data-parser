import csv
def appendvolume(filepath):
    with open(filepath,'r') as csvinput:
        with open('output.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row.append('Volume')
            all.append(row)
            i = 1
            for row in reader:
                row.append(i)
                all.append(row)
                print(row)
                i += 1

            writer.writerows(all)

appendvolume('/home/xd101/Desktop/amazon-data-parser/media/machinelearned/Etsy-abc.csv')
