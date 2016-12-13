import codecs


all_data_raw =  codecs.open('crosschecked_data.csv', "r", encoding = 'utf-8', errors='ignore')

all_data = []
for line in all_data_raw:
    line = line.split(',')
    for word in line:
        all_data.append(word)


all_data_sorted = ["","","","","", "", "",  "", "", "", ""]*int(24383)
all_data_sorted[0] = ["Name", "Country", "Title", "Current Year", "DOB", "DOD", "Living", "First Name", "Last Name", "Original Name", "Flag"]



for i in range(0, 24383):
    name = all_data[i*13]
    country = all_data[i*13 + 1]
    title = all_data[i*13+2]
    currentyear = all_data[i*13+3]
    DOB = all_data[i*13+4]
    DOD = all_data[i*13+5]
    Living = all_data[i*13+6]
    Firstname = all_data[i*13+7]
    Lastname = all_data[i*13+8]
    Original_name = all_data[i*13+10]
    flag = all_data[i*13+11]

    Lastname = Lastname.replace('\"', "")
    Firstname = Firstname.replace('\"', "")

    all_data_sorted[i] = [name, country, title, currentyear, DOB, DOD, Living, Firstname, Lastname, Original_name, flag]

complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "argentina":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Argentina:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "australia":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Australia:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "brazil":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Brazil:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "canada":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Canada:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "chile":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Chile:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "china":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("China:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "colombia":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Colombia:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "ethiopia":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Ethiopia:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "france":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("France:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")

complete = 0
incomplete = 0
empty = 0




for i in range(0, 24383):
    if all_data_sorted[i][1] == "germany":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Germany:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "ghana":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Ghana:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "greece":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Greece:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "india":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("India:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "ireland":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Ireland:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "italy":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Italy:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "japan":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Japan:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "kenya":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("kenya:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "mexico":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Mexico:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "mozambique":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Mozambique:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "new zealand":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("New Zealand:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "nicaragua":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Nicaragua:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "nigeria":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Nigeria:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "poland":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Poland:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "portugal":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Portugal:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "singapore":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Singapore:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "spain":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Spain:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "sweden":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Sweden:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "tanzania":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Tanzania:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "turkey":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Turkey:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "united kingdom":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("United Kingdom:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "united states":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("United States:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")


complete = 0
incomplete = 0
empty = 0

for i in range(0, 24383):
    if all_data_sorted[i][1] == "zambia":
        if all_data_sorted[i][4] != "" and all_data_sorted[i][6] != "":
            complete = complete +1
        elif all_data_sorted[i][4] == "" and all_data_sorted[i][6] != "":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] != "" and all_data_sorted[i][6] =="":
            incomplete = incomplete +1
        elif all_data_sorted[i][4] =="" and all_data_sorted[i][6] == "":
            empty = empty +1

print("Zambia:")
print("Complete:")
print(complete)

print("Partially Complete:")
print(incomplete)

print("No Data:")
print(empty)
print("")



