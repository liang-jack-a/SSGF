import codecs
from fuzzywuzzy import fuzz
import csv

# Standard checking if a string is actually a float
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def most_common(lst):
    return max(set(lst), key=lst.count)

def direct_merge(all_data_sorted):
    counter = 0

    for i in range(0, 24383):
        for j in range(0, 24383):
            if all_data_sorted[i][9] != "" and all_data_sorted[j][9] != "" and i != j:
                if all_data_sorted[i][9] == all_data_sorted[j][9] and all_data_sorted[i][1] == all_data_sorted[j][1]:
                    if all_data_sorted[i][4] == "" and all_data_sorted[j][4] != "":
                        all_data_sorted[i][4] = all_data_sorted[j][4]
                        all_data_sorted[i][10] = "Direct Merge"
                        counter = counter +1
                    if all_data_sorted[i][5] == "" and all_data_sorted[j][5] != "":
                        all_data_sorted[i][5] = all_data_sorted[j][5]
                        all_data_sorted[i][10] = "Direct Merge"
                        counter = counter + 1
                    if all_data_sorted[i][6] == "" and all_data_sorted[j][6] != "":
                        all_data_sorted[i][6] = all_data_sorted[j][6]
                        all_data_sorted[i][10] = "Direct Merge"
                        all_data_sorted[i][10] = "Direct Merge"
                        counter = counter +1

    return(all_data_sorted)



def fuzzy_merge1(index, data):

    #We first compare firstname + lastname and see if they are VERY similar (middle names fail here)
    #We weight last names twice as much as firstnames

    firstlast = []
    for i in range(0, 24383):
        if data[i][1] == data[index][1] and i != index:
            if fuzz.token_sort_ratio(data[index][7], data[i][7]) + 2 * fuzz.ratio(data[index][8], data[i][8]) > 280:
                firstlast.append(i)

    DOB = ['']
    DOD = ['']
    Living = ['']

    if len(firstlast) >= 1:
        for i in firstlast:
            if data[i][4] != '':
                DOB.append(data[i][4])
            if data[i][5] != '':
                DOD.append(data[i][5])
            if data[i][6] != '':
                Living.append(data[i][6])
        if most_common(DOB)!= "" or most_common(Living) != "" or most_common(DOD) != "":
            return([most_common(DOB), most_common(DOD), most_common(Living), "Firstname and Lastname"])

    return ["", "", "", ""]


def fuzzy_merge2(index, data):
    ## We now look at firstname + middle initial(s) + lastname
    ## The rule we follow is this: the firstname and lastname must match VERY closely (same criteria as above)
    ## With regard to the middle initials, one set of middle initials must be a subset of the other

    index_names = data[index][0].split()
    if len(index_names)  < 2:
        return ["", "", "", ""]

    indexfirstname = index_names[0]
    indexlastname = index_names[-1]
    index_middle = []
    for words in index_names:
        if words!= indexfirstname and words != indexlastname:
            index_middle.append(words[0])

    indicies = []
    for i in range(0, 24383):
        if data[i][1] == data[index][1] and i != index:

            names = data[i][0].split()
            if len(names) > 1:
                firstfirstname = names[0]
                lastlastname = names[-1]

                middle_initials = []
                for words in names:
                    if words != firstfirstname and words != lastlastname:
                        middle_initials.append(words[0])


                if fuzz.ratio(indexfirstname, firstfirstname) + 2 * fuzz.ratio(indexlastname, lastlastname) > 280:
                    if set(index_middle).issubset(set(middle_initials)) or set(middle_initials).issubset(set(index_middle)):
                        indicies.append(i)

    DOB = ['']
    DOD = ['']
    Living = ['']

    if len(indicies) >= 1:
        for i in indicies:
            if data[i][4] != '':
                DOB.append(data[i][4])
            if data[i][5] != '':
                DOD.append(data[i][5])
            if data[i][6] != '':
                Living.append(data[i][6])
        if most_common(DOB)!= "" or most_common(Living) != "" or most_common(DOD) != "":
            return([most_common(DOB), most_common(DOD), most_common(Living), "Middle Initial"])

    return ["", "", "", ""]










#
#
#
#
#
#
#
#
#               BEGIN CODE
#
#
#
#
#
#
#
#
#
#

all_data_raw =  codecs.open('Wikipedia_Scraped.csv', "r", encoding = 'utf-8', errors='ignore')

all_data = []
for line in all_data_raw:
    line = line.split(',')
    for word in line:
        all_data.append(word)



all_data_sorted = ["","","","","", "", "",  "", "", "", ""]*int(24383)
all_data_sorted[0] = ["Name", "Country", "Title", "Current Year", "DOB", "DOD", "Living", "First Name", "Last Name", "Original Name", "Flag"]

for i in range(0, 24383):
    name = all_data[i*11]
    country = all_data[i*11 + 1]
    title = all_data[i*11+2]
    currentyear = all_data[i*11+3]
    DOB = all_data[i*11+4]
    DOD = all_data[i*11+5]
    Living = all_data[i*11+6]
    Firstname = all_data[i*11+7]
    Lastname = all_data[i*11+8]
    Original_name = all_data[i*11+10]

    Lastname = Lastname.replace('\"', "")
    Firstname = Firstname.replace('\"', "")


    if isfloat(DOD):
        Living = "Dead"

    all_data_sorted[i] = [name, country, title, currentyear, DOB, DOD, Living, Firstname, Lastname, Original_name, ""]


all_data_sorted = direct_merge(all_data_sorted)


counter = 0
for i in range(0, 24383):
    [DOB, DOD, Living, method] = fuzzy_merge1(i, all_data_sorted)
    [DOB1, DOD1, Living1, method1] = fuzzy_merge2(i, all_data_sorted)

    if [DOB, DOD, Living, method] != ["", "", "", ""]:
        if DOB != "" and all_data_sorted[i][4] == "":
            all_data_sorted[i][4] = DOB
            all_data_sorted[i][10] = method
            counter = counter + 1
            #print(i)
        if DOD != "" and all_data_sorted[i][5] == "":
            all_data_sorted[i][5] = DOD
            all_data_sorted[i][10] = method
            counter = counter +1
            #print(i)
        if Living != "" and all_data_sorted[i][6] == "":
            all_data_sorted[i][6] = Living
            all_data_sorted[i][10] = method
            counter = counter +1
            #print(i)

    if [DOB1, DOD1, Living1, method1] != ["", "", "", ""]:
        if DOB1 != "" and all_data_sorted[i][4] == "":
            all_data_sorted[i][4] = DOB1
            all_data_sorted[i][10] = method1
            counter = counter + 1
            #print(i)
        if DOD1 != "" and all_data_sorted[i][5] == "":
            all_data_sorted[i][5] = DOD1
            all_data_sorted[i][10] = method1
            counter = counter +1
            #print(i)
        if Living1 != "" and all_data_sorted[i][6] == "":
            all_data_sorted[i][6] = Living1
            all_data_sorted[i][10] = method1
            counter = counter +1
            #print(i)

with open("crosschecked_data.csv", "w", newline='', encoding='utf-8') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(all_data_sorted)


complete = 0
incomplete = 0
empty = 0

for i in range(1, 24383):
    if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
        complete = complete +1
    elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
        incomplete = incomplete +1
    elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
        incomplete = incomplete +1
    elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
        empty = empty +1

print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
