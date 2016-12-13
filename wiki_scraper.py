from bs4 import BeautifulSoup
import codecs
import requests
import csv

# Standard checking if a string is actually a float
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# this takes some time to explain
# So we take in the 4 bits of info we know, along with something called counter which is typically 0.

# We first try the disambiguation page. If that exists and there are people there, we search for the name +
#  the country + the word 'politician' in order to find the individual page.
# Note we only require the first 4 letters of the country to be in there. This is due to the fact that, for example,
# Liu Jiayi would be written "Liu Jiayi (Chinese Politician)" not "Liu Jiayi (China Politician)"
# This is route A.

# If that fails, we look for just the name and the word politician to find the individual page. This is route A1.

# If there is no disambiguation page, we try looking for just the name. If such a page exists, we look first for the tag
# 'bday', which is linked with the birthday of the individual. We take the first 4 digits (the year),
#  and, as long as it is reasonable, we return it. This is route B.

# If this tag does not exist, we look for the category "births".
# Typically individuals are stored by wikipedia as "1900 births", for example. This format is standard across wikipedia
# We find this tag, and take the word before it. If that number is > 1800, we return it.
# This is route C

# If nothing has worked so far, we check counter. If counter is large (>1), we give up.
# If not, and the name has 3 or more parts (i.e., John Adam Smith), we take out all the middle names
# (so John Adam Smith --> John Smith) and try the whole process again, meanwhile incrementing the counter by 1
# to indicate that this process was done.

# Next, we try "Firstname_Lastname_(politician)". This should be caught by route a, however, it appears
# that some people (see Roy MacLaren, below) do not have politician in the <a> tag. I do not know if this is a
# BeautifulSoup thing or a wikipedia thing. I have marked these routes with a (P).
# Very rarely should this step ever occur.

# Now we try different languages, first spanish if they are in a list of countries (listed below) or italian if they are
# from italy. We only try route B (from above) because I am not fluent in either language and do not want to mess things up.
# The rules for keeping the name are much looser: because we cannot translate their titles, we simply look for the word
# politician (translated into the appropriate langauge). If it is present, and the name matches, we assume we are correct

# KEY: Failure = 0,  A = 1, A1 =2, B = 3, C = 4, B(P) = 5, C(P) = 6, C(Spanish) = 7

def find_birthday(name, country, title, currentyear, counter):
    if name == "" or country == "" or title == "" or currentyear == "":
        #print("Something's missing")
        return ["", "" , 0]

    counter = counter +1
    if counter > 2:
        return ["", "", 0]

    birthday = ""
    deathday = ""

    if country == "united states":
        country = "U.S."



    correct_page = 0
    title = title.replace(".", "")
    title = title.replace("(", "")
    title = title.replace(")", "")
    words_in_title = sorted(title.split(), key=len)


## Start Route A
    page = requests.get("https://en.wikipedia.org/wiki/" + name + "_(disambiguation)")
    soup = BeautifulSoup(page.content, 'html.parser')

    for text in soup.find_all('a'):
        for words in text.contents:
            if country[0] + country[1] + country[2] + country[3] in words and "policitian" in words:
                page = requests.get("https://en.wikipedia.org/wiki/" + words)
                soup = BeautifulSoup(page.content, 'html.parser')

                for stuff in soup.find_all(True):
                    for sub_stuff in stuff:
                        if words_in_title[-1] in sub_stuff:
                            correct_page = 1

                if len(soup.find_all('span', attrs="bday")) != 0 and correct_page ==1 :
                    temp = soup.find_all('span', attrs="bday")
                    full_bday = temp[0].contents[0]
                    birthday = full_bday[0] + full_bday[1] + full_bday[2] + full_bday[3]

                    if len(soup.find_all('span', attrs = "noprint ForceAgeToShow")) !=0:
                        deathday = "Alive"
                        # print("Route A")
                        if float(birthday) < float(currentyear):
                            return [birthday, deathday, 1]

                if len(soup.find_all('span', attrs= "dday deathdate" )) != 0 and correct_page ==1:
                    temp = soup.find_all('span', attrs = "dday deathdate")
                    full_dday = temp[0].contents[0]
                    deathday = full_dday[0] + full_dday[1] + full_dday[2] + full_dday[3]
                    # print("Route A")
                    if float(birthday) < float(currentyear) and float(deathday) >= float(currentyear):
                        return[birthday, deathday, 1]


## Start Route A1
    for text in soup.find_all('a'):
        for words in text.contents:
            if "politician" in words:
                page = requests.get("https://en.wikipedia.org/wiki/" + words)
                soup = BeautifulSoup(page.content, 'html.parser')

                for stuff in soup.find_all(True):
                    for sub_stuff in stuff:
                        if words_in_title[-1] in sub_stuff:
                            correct_page = 1

                if len(soup.find_all('span', attrs="bday")) != 0 and correct_page ==1 :
                    temp = soup.find_all('span', attrs="bday")
                    full_bday = temp[0].contents[0]
                    birthday = full_bday[0] + full_bday[1] + full_bday[2] + full_bday[3]

                    if len(soup.find_all('span', attrs = "noprint ForceAgeToShow")) !=0:
                        deathday = "Alive"
                        # print("Route A1")
                        if float(birthday) < float(currentyear):
                            return [birthday, deathday, 2]

                if len(soup.find_all('span', attrs= "dday deathdate" )) != 0 and correct_page ==1:
                    temp = soup.find_all('span', attrs = "dday deathdate")
                    full_dday = temp[0].contents[0]
                    deathday = full_dday[0] + full_dday[1] + full_dday[2] + full_dday[3]
                    # print("Route A1")
                    if float(birthday) < float(currentyear) and float(deathday) >= float(currentyear):
                        return[birthday, deathday, 2]



    correct_page = 0
    page = requests.get("https://en.wikipedia.org/wiki/" + name)
    soup = BeautifulSoup(page.content, 'html.parser')
    for stuff in soup.find_all(True):
        for sub_stuff in stuff:
            if words_in_title[-1] in sub_stuff:
                correct_page = 1

## Start Route B
    if len(soup.find_all('span', attrs="bday")) != 0 and correct_page ==1:
        temp = soup.find_all('span', attrs="bday")
        full_bday = temp[0].contents[0]
        birthday = full_bday[0] + full_bday[1] + full_bday[2] + full_bday[3]

        if len(soup.find_all('span', attrs = "noprint ForceAgeToShow")) !=0:
            deathday = "Alive"
            # print("Route B")
            if float(birthday) < float(currentyear):
                return [birthday, deathday, 3]

        if len(soup.find_all('span', attrs= "dday deathdate" )) != 0 and correct_page ==1:
            temp = soup.find_all('span', attrs = "dday deathdate")
            full_dday = temp[0].contents[0]
            deathday = full_dday[0] + full_dday[1] + full_dday[2] + full_dday[3]
            # print("Route B")
            if float(birthday) < float(currentyear) and float(deathday) >= float(currentyear):
                return [birthday, deathday, 3]

## Start Route C
    for stuff in soup.find_all(True):
        for sub_stuff in stuff:
            if "births" in sub_stuff and correct_page ==1:
                words = sub_stuff.split()

                for i in range(1, len(words)):
                    if "births" in words[i]:
                        if isfloat(words[i-1]):
                            if float(words[i-1]) > 1800:
                                birthday = words[i-1]

            if "Living people" in sub_stuff and correct_page ==1:
                deathday = "Alive"

            if "deaths" in sub_stuff and correct_page ==1:
                words = sub_stuff.split()

                for i in range(1, len(words)):
                    if "deaths" in words[i]:
                        if isfloat(words[i-1]):
                            if float(words[i-1]) > 1800:
                                #print("Route C")
                                deathday = words[i-1]
                                return[birthday, deathday, 4]

            if birthday != "" and deathday != "":
                # print("Route C")
                return[birthday, deathday, 4]

## Start try with politician
    correct_page = 0
    page = requests.get("https://en.wikipedia.org/wiki/" + name + "_(politician)")
    soup = BeautifulSoup(page.content, 'html.parser')
    for stuff in soup.find_all(True):
        for sub_stuff in stuff:
            if words_in_title[-1] in sub_stuff:
                correct_page = 1


    if len(soup.find_all('span', attrs="bday")) != 0 and correct_page ==1:
        temp = soup.find_all('span', attrs="bday")
        full_bday = temp[0].contents[0]
        birthday = full_bday[0] + full_bday[1] + full_bday[2] + full_bday[3]

        if len(soup.find_all('span', attrs = "noprint ForceAgeToShow")) !=0:
            deathday = "Alive"
            # print("Route B(P)")
            if float(birthday) < float(currentyear):
                return [birthday, deathday ,5]

        if len(soup.find_all('span', attrs= "dday deathdate" )) != 0 and correct_page ==1:
            temp = soup.find_all('span', attrs = "dday deathdate")
            full_dday = temp[0].contents[0]
            deathday = full_dday[0] + full_dday[1] + full_dday[2] + full_dday[3]
            # print("Route B(P)")
            if float(birthday) < float(currentyear) and float(deathday) >= float(currentyear):
                return [birthday, deathday, 5]

    for stuff in soup.find_all(True):
        for sub_stuff in stuff:
            if "births" in sub_stuff and correct_page ==1:
                words = sub_stuff.split()

                for i in range(1, len(words)):
                    if "births" in words[i]:
                        if isfloat(words[i-1]):
                            if float(words[i-1]) > 1800:
                                birthday = words[i-1]

            if "Living people" in sub_stuff and correct_page ==1:
                deathday = "Alive"

            if "deaths" in sub_stuff and correct_page ==1:
                words = sub_stuff.split()

                for i in range(1, len(words)):
                    if "deaths" in words[i]:
                        if isfloat(words[i-1]):
                            if float(words[i-1]) > 1800:
                                # print("Route C(P)")
                                deathday = words[i-1]
                                return[birthday, deathday, 6]

            if birthday != "" and deathday != "":
                # print("Route C(P)")
                return[birthday, deathday, 6 ]



# Start try with spanish

    if country == "argentina" or country == "brazil" or country == "chile" or country == "colombia" or country == "mexico" or country == "nicaragua" or country == "spain":
        correct_page = 0
        page = requests.get("https://es.wikipedia.org/wiki/" + name)
        soup = BeautifulSoup(page.content, 'html.parser')
        for stuff in soup.find_all(True):
            for sub_stuff in stuff:
                if "político" in sub_stuff or "política" in sub_stuff:
                    correct_page = 1
                    break


        for stuff in soup.find_all(True):
            for sub_stuff in stuff:
                if "Nacidos" in sub_stuff and correct_page == 1:
                    words = sub_stuff.split()

                    for i in range(0, len(words)):
                        if "Nacidos" in words[i]:
                            if isfloat(words[i + 2]):
                                if float(words[i + 2]) > 1800:
                                    birthday = words[i + 2]

                if "Fallecidos" in sub_stuff and correct_page == 1:
                    words = sub_stuff.split()

                    for i in range(0, len(words)):
                        if "Fallecidos" in words[i]:
                            if isfloat(words[i + 2]):
                                if float(words[i + 2]) > 1800:
                                    # print("Route C(Spanish)")
                                    deathday = words[i - 1]
                                    return [birthday, deathday, 7]

                if birthday != "" and deathday != "":
                    #print("Route C(Spanish)")
                    return [birthday, deathday, 7]


    if birthday != "" or deathday != "":
        #print("Route C(Spanish)")
        return [birthday, deathday, 7 ]


# Start try with Italian

    if country == "italy":
        correct_page = 0
        page = requests.get("https://it.wikipedia.org/wiki/" + name)
        soup = BeautifulSoup(page.content, 'html.parser')
        for stuff in soup.find_all(True):
            for sub_stuff in stuff:
                if "politico" in sub_stuff or "politica" in sub_stuff:
                    correct_page = 1
                    break


        for stuff in soup.find_all(True):
            for sub_stuff in stuff:
                if "Nati" in sub_stuff and correct_page == 1:
                    words = sub_stuff.split()

                    for i in range(0, len(words)):
                        if "Nati" in words[i]:
                            if isfloat(words[i + 2]):
                                if float(words[i + 2]) > 1800:
                                    birthday = words[i + 2]

                if "Morti" in sub_stuff and correct_page == 1:
                    words = sub_stuff.split()

                    for i in range(0, len(words)):
                        if "Morti" in words[i]:
                            if isfloat(words[i + 2]):
                                if float(words[i + 2]) > 1800:
                                    #print("Route C(Italian)")
                                    deathday = words[i - 1]
                                    return [birthday, deathday, 8]

                if birthday != "" and deathday != "":
                    #print("Route C(Italian)")
                    return [birthday, deathday, 8]


    if birthday != "" or deathday != "":
        #print("Route C(Italian)")
        return [birthday, deathday, 8]

# Start try with German

# After looking through, it seems that german articles are actually almost always translated to English
# This section was removed because the English search would fail typically when the name was heavily accented
# and the CIA data either did not pick this up or did not include it; as such, searching the name on the german
# Wikipedia did not yield any better results.

#     if country == "germany":
#         correct_page = 0
#         page = requests.get("https://de.wikipedia.org/wiki/" + name)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         for stuff in soup.find_all(True):
#             for sub_stuff in stuff:
#                 if "politikeren" in sub_stuff:
#                     correct_page = 1
#                     break
#
#
#         for stuff in soup.find_all(True):
#             for sub_stuff in stuff:
#                 if "Geboren" in sub_stuff and correct_page == 1:
#                     words = sub_stuff.split()
#
#                     for i in range(0, len(words)):
#                         if "Geboren" in words[i]:
#                             if isfloat(words[i + 1]):
#                                 if float(words[i + 1]) > 1800:
#                                     birthday = words[i + 1]
#
#                 if "Gestorben" in sub_stuff and correct_page == 1:
#                     words = sub_stuff.split()
#
#                     for i in range(0, len(words)):
#                         if "Gestorben" in words[i]:
#                             if isfloat(words[i + 2]):
#                                 if float(words[i + 2]) > 1800:
#                                     print("Route C(German)")
#                                     deathday = words[i - 1]
#                                     return [birthday, deathday, 9]
#
#                 if birthday != "" and deathday != "":
#                     print("Route C(German)")
#                     return [birthday, deathday, 9]
#
#
#     if birthday != "" or deathday != "":
#         print("Route C(German)")
#         return [birthday, deathday, 9]


## Start Try with no middle name
    temp_name = name.split()
    new_name = temp_name[0] + " " + temp_name[-1]
    if len(temp_name) > 2 and temp_name[-1] != "(politician)":
        #print("Trying with no middle name")
        return find_birthday(new_name, country, title, currentyear, counter)



    #print("Failure")
    return ["", "", 0]



#
#
#
#
#
#                               BEGIN CODE
#
#
#
#






all_data_raw =  codecs.open('all_data_CIA_SYB_rulers.csv', "r", encoding = 'utf-8', errors='ignore')


all_data = []
for line in all_data_raw:
    line = line.split(',')
    for word in line:
        all_data.append(word)

num_names = 24384

all_data_sorted = ["","","","","", "", "",  "", "", ""]*int(num_names)

for i in range(1, int(num_names)):
    name = ""
    country = all_data[i*9]
    title = all_data[i*9+1]
    currentyear = all_data[i*9 +3]
    DOB = all_data[i*9+5]
    DOD = all_data[i*9+6]
    firstname = all_data[i*9 + 7]
    lastname = all_data[i*9 + 8]
    original_name = all_data[i*9 + 4]

    temp = all_data[i*9+2].split('.')
    if len(temp) == 2:
        name = temp[1] + " " + temp[0]
    elif len(temp ) ==1:
        name = temp[0]

    all_data_sorted[i] = [name, country, title, currentyear, DOB, DOD, "", firstname, lastname, original_name]



#### TESTING PURPOSES ####
# Route A1
#print(find_birthday("Ron Brown", "united states", "Secretary of Commerce", "1993", 0))

# Route B
#print(find_birthday("Peter_Dutton", "united states", "Min. for Workforce Participation", "2000", 0))
#print(find_birthday("Christine Albanel", "France", "Min of Culture & Communication. Government Spokesman", "2008", 0))
#print(find_birthday("PV Narashimha Rao", "india", "Min of Rural Development", "1995"))

# Route C
#print(find_birthday("Pierre Blais", "canada", "Min of Consumer & Corporate Affairs", "1992",0))
#print(find_birthday("Gines Gonzalez Garcia", "Argentina", "Min. of Health", "2005",0))
#print(find_birthday("Liu Jiayi", "China", "Audit", "2000",0))
#print(find_birthday("Hiroshi Miyazawa", "japan", "Min of Justice", "1995",0))

# No middle name, Spanish
#print(find_birthday("Raul Granillo Ocampo", "argentina", "Min of Justice", "1997", 0))

# Spanish
#print(find_birthday("Eduardo_A._Elizondo_Lozano", "mexico", "govenor", "1971",0))

# Italian
#print(find_birthday("Stefania Prestigiacomo", "italy", "Min of Equal Opportunity", "2002", 0))


counter0 = 0
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
counter5 = 0
counter6 = 0
counter7 = 0
counter8 = 0

total = 24384

for i in range(1, 24384):
    #print(all_data_sorted[i])
    try:
        [born, died, route] = find_birthday(all_data_sorted[i][0], all_data_sorted[i][1], all_data_sorted[i][2],
                                        all_data_sorted[i][3], 0)

    except Exception:
        print("Wifi, failure")
        print(i)
        [born, died, route] = ["", "", 0]

    #print([born, died, route])

    if all_data_sorted[i][4] == "":
        all_data_sorted[i][4] = born


    if all_data_sorted[i][5] == "":
        if died != "Alive" and died != "":
            all_data_sorted[i][5] = died
            all_data_sorted[i][6] = "Dead"

        if died == "Alive":
            all_data_sorted[i][5] = ""
            all_data_sorted[i][6] = "Alive"

    #print(all_data_sorted[i])
    #print("")
    if i%100 == 0:
        print(i)

    if route == 0:
        counter0 = counter0 + 1

    if route == 1:
        counter1 = counter1 + 1

    if route == 2:
        counter2 = counter2 + 1

    if route == 3:
        counter3 = counter3 + 1

    if route == 4:
        counter4 = counter4 + 1

    if route == 5:
        counter5 = counter5 + 1

    if route == 6:
        counter6 = counter6 + 1

    if route == 7:
        counter7 = counter7 + 1

    if route == 8:
        counter8 = counter8 + 1

    if i%10000 ==0:
        with open("output1.csv", "w", newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            writer.writerows(all_data_sorted)

print(["Failure", "A", "A1", "B", "C", "B(P)", "C(P)", "C(Spanish)", "C(Italian)"])
print([counter0, counter1, counter2, counter3, counter4, counter5, counter6, counter7, counter8])

# fixing inconsistencies: I looked up all these people by hand.
# Juan Manuel Abal Medina
all_data_sorted[1][5] = ""
all_data_sorted[1][6] = "Alive"
all_data_sorted[2][5] = ""
all_data_sorted[2][6] = "Alive"

# Alberto Fernandez
all_data_sorted[56][5] = ""
all_data_sorted[56][6] = "Alive"
all_data_sorted[57][5] = ""
all_data_sorted[57][6] = "Alive"
all_data_sorted[58][5] = ""
all_data_sorted[58][6] = "Alive"
all_data_sorted[59][5] = ""
all_data_sorted[59][6] = "Alive"
all_data_sorted[263][5] = ""
all_data_sorted[263][6] = "Alive"

# Carlos Fernandez
all_data_sorted[67][4] = "1954"
all_data_sorted[67][5] = ""
all_data_sorted[67][6] = "Alive"


# Alicia Kirchner
all_data_sorted[94][4] = "1946"
all_data_sorted[94][5] = ""
all_data_sorted[94][6] = "Alive"
all_data_sorted[95][4] = "1946"
all_data_sorted[95][5] = ""
all_data_sorted[95][6] = "Alive"
all_data_sorted[96][4] = "1946"
all_data_sorted[96][5] = ""
all_data_sorted[96][6] = "Alive"
all_data_sorted[97][4] = "1946"
all_data_sorted[97][5] = ""
all_data_sorted[97][6] = "Alive"
all_data_sorted[98][4] = "1946"
all_data_sorted[98][5] = ""
all_data_sorted[98][6] = "Alive"
all_data_sorted[99][4] = "1946"
all_data_sorted[99][5] = ""
all_data_sorted[99][6] = "Alive"
all_data_sorted[100][4] = "1946"
all_data_sorted[100][5] = ""
all_data_sorted[100][6] = "Alive"
all_data_sorted[101][4] = "1946"
all_data_sorted[101][5] = ""
all_data_sorted[101][6] = "Alive"


# Eduardo Bazuro
all_data_sorted[201][5] = ""
all_data_sorted[201][6] = "Alive"
all_data_sorted[202][5] = ""
all_data_sorted[202][6] = "Alive"
all_data_sorted[203][5] = ""
all_data_sorted[203][6] = "Alive"


# Graciela Camano
all_data_sorted[209][4] = "1953"
all_data_sorted[209][5] = ""
all_data_sorted[209][6] = "Alive"


# Jorge Rodriguez-
all_data_sorted[372][5] = ""
all_data_sorted[372][6] = "Alive"
all_data_sorted[373][5] = ""
all_data_sorted[373][6] = "Alive"
all_data_sorted[374][5] = ""
all_data_sorted[374][6] = "Alive"
all_data_sorted[375][5] = ""
all_data_sorted[375][6] = "Alive"
all_data_sorted[376][5] = ""
all_data_sorted[376][6] = "Alive"
all_data_sorted[377][5] = ""
all_data_sorted[377][6] = "Alive"

# Quentin Alive Louise Bryce
all_data_sorted[463][5] = ""
all_data_sorted[463][6] = "Alive"

# Michael Jeffrey
all_data_sorted[1109][5] = ""
all_data_sorted[1109][6] = "Alive"

# Paul Keating
all_data_sorted[1115][5] = ""
all_data_sorted[1115][6] = "Alive"
all_data_sorted[1116][5] = ""
all_data_sorted[1116][6] = "Alive"
all_data_sorted[1117][5] = ""
all_data_sorted[1117][6] = "Alive"
all_data_sorted[1118][5] = ""
all_data_sorted[1118][6] = "Alive"
all_data_sorted[1119][5] = ""
all_data_sorted[1119][6] = "Alive"
all_data_sorted[1120][5] = ""
all_data_sorted[1120][6] = "Alive"

# Moreira  Franco
all_data_sorted[1498][4] = "1944"
all_data_sorted[1498][5] = ""
all_data_sorted[1498][6] = "Alive"
all_data_sorted[1499][4] = "1944"
all_data_sorted[1499][5] = ""
all_data_sorted[1499][6] = "Alive"
all_data_sorted[1500][4] = "1944"
all_data_sorted[1500][5] = ""
all_data_sorted[1500][6] = "Alive"
all_data_sorted[1500][4] = "1944"
all_data_sorted[1501][5] = ""
all_data_sorted[1501][6] = "Alive"

# Luiz Ignacio Da Lula Silva
all_data_sorted[1546][5] = ""
all_data_sorted[1546][6] = "Alive"

# Marina Silva
all_data_sorted[1650][4] = "1958"
all_data_sorted[1650][5] = ""
all_data_sorted[1650][6] = "Alive"
all_data_sorted[1651][4] = "1958"
all_data_sorted[1651][5] = ""
all_data_sorted[1651][6] = "Alive"
all_data_sorted[1652][4] = "1958"
all_data_sorted[1652][5] = ""
all_data_sorted[1652][6] = "Alive"
all_data_sorted[2086][4] = "1958"
all_data_sorted[2086][5] = ""
all_data_sorted[2086][6] = "Alive"
all_data_sorted[2087][4] = "1958"
all_data_sorted[2087][5] = ""
all_data_sorted[2087][6] = "Alive"
all_data_sorted[2088][4] = "1958"
all_data_sorted[2088][5] = ""
all_data_sorted[2088][6] = "Alive"




# Orlando Silva
# No data availible. I assume the data was erroneously matched from rulers.org
all_data_sorted[1653][4] = ""
all_data_sorted[1653][5] = ""
all_data_sorted[1653][6] = ""
all_data_sorted[1654][4] = ""
all_data_sorted[1654][5] = ""
all_data_sorted[1654][6] = ""
all_data_sorted[1655][4] = ""
all_data_sorted[1655][5] = ""
all_data_sorted[1655][6] = ""
all_data_sorted[1656][4] = ""
all_data_sorted[1656][5] = ""
all_data_sorted[1656][6] = ""
all_data_sorted[1657][4] = ""
all_data_sorted[1657][5] = ""
all_data_sorted[1657][6] = ""
all_data_sorted[1658][4] = ""
all_data_sorted[1658][5] = ""
all_data_sorted[1658][6] = ""

# Femando Henrique Cardoso
# This must be a typo- there exists a "FERNANDO Henrique Cardoso" who occupied the same position during the same time
all_data_sorted[1777][5] = ""
all_data_sorted[1777][6] = "Alive"
all_data_sorted[1778][5] = ""
all_data_sorted[1778][6] = "Alive"
all_data_sorted[1779][5] = ""
all_data_sorted[1779][6] = "Alive"
all_data_sorted[1780][5] = ""
all_data_sorted[1780][6] = "Alive"
all_data_sorted[1781][5] = ""
all_data_sorted[1781][6] = "Alive"

# Femando Collor de Mello"
# Same things as above, seems like it should be Fernando
all_data_sorted[1801][5] = ""
all_data_sorted[1801][6] = "Alive"

# Itamar Franco
# Sometimes name was spelled ltamar (with an L as opposed to an I)
all_data_sorted[1860][4] = "1930"
all_data_sorted[1860][5] = "2011"
all_data_sorted[1860][6] = "Dead"
all_data_sorted[1861][4] = "1930"
all_data_sorted[1861][5] = "2011"
all_data_sorted[1861][6] = "Dead"
all_data_sorted[1863][4] = "1930"
all_data_sorted[1863][5] = "2011"
all_data_sorted[1863][6] = "Dead"
all_data_sorted[1864][4] = "1930"
all_data_sorted[1864][5] = "2011"
all_data_sorted[1864][6] = "Dead"
all_data_sorted[1865][4] = "1930"
all_data_sorted[1865][5] = "2011"
all_data_sorted[1865][6] = "Dead"


# Romeo Le Blanc
all_data_sorted[2937][4] = "1927"
all_data_sorted[2937][5] = "2009"
all_data_sorted[2937][6] = "Dead"
all_data_sorted[2938][4] = "1927"
all_data_sorted[2938][5] = "2009"
all_data_sorted[2938][6] = "Dead"
all_data_sorted[2939][4] = "1927"
all_data_sorted[2939][5] = "2009"
all_data_sorted[2939][6] = "Dead"
all_data_sorted[2940][4] = "1927"
all_data_sorted[2940][5] = "2009"
all_data_sorted[2940][6] = "Dead"


# Paul Martin
all_data_sorted[2990][5] = ""
all_data_sorted[2990][6] = "Alive"
all_data_sorted[2991][5] = ""
all_data_sorted[2991][6] = "Alive"
all_data_sorted[2992][5] = ""
all_data_sorted[2992][6] = "Alive"
all_data_sorted[2993][5] = ""
all_data_sorted[2993][6] = "Alive"
all_data_sorted[2994][5] = ""
all_data_sorted[2994][6] = "Alive"
all_data_sorted[2995][5] = ""
all_data_sorted[2995][6] = "Alive"
all_data_sorted[2996][5] = ""
all_data_sorted[2996][6] = "Alive"
all_data_sorted[2997][5] = ""
all_data_sorted[2997][6] = "Alive"
all_data_sorted[2998][5] = ""
all_data_sorted[2998][6] = "Alive"
all_data_sorted[2999][5] = ""
all_data_sorted[2999][6] = "Alive"
all_data_sorted[3000][5] = ""
all_data_sorted[3000][6] = "Alive"
all_data_sorted[3001][5] = ""
all_data_sorted[3001][6] = "Alive"
all_data_sorted[3002][5] = ""
all_data_sorted[3002][6] = "Alive"

# Eduardo Frei Ruiz-Tagle
all_data_sorted[3602][4] = "1942"
all_data_sorted[3602][5] = ""
all_data_sorted[3602][6] = "Alive"
all_data_sorted[3603][4] = "1942"
all_data_sorted[3603][5] = ""
all_data_sorted[3603][6] = "Alive"
all_data_sorted[3604][4] = "1942"
all_data_sorted[3604][5] = ""
all_data_sorted[3604][6] = "Alive"
all_data_sorted[3605][4] = "1942"
all_data_sorted[3605][5] = ""
all_data_sorted[3605][6] = "Alive"
all_data_sorted[3606][4] = "1942"
all_data_sorted[3606][5] = ""
all_data_sorted[3606][6] = "Alive"
all_data_sorted[3607][4] = "1942"
all_data_sorted[3607][5] = ""
all_data_sorted[3607][6] = "Alive"

# Andres  Pastrana Arango
all_data_sorted[5162][5] = ""
all_data_sorted[5162][6] = "Alive"

#Alvaro Uribe Velez
all_data_sorted[5208][5] = ""
all_data_sorted[5208][6] = "Alive"
all_data_sorted[5209][5] = ""
all_data_sorted[5209][6] = "Alive"
all_data_sorted[5210][5] = ""
all_data_sorted[5210][6] = "Alive"
all_data_sorted[5211][5] = ""
all_data_sorted[5211][6] = "Alive"
all_data_sorted[5212][5] = ""
all_data_sorted[5212][6] = "Alive"
all_data_sorted[5213][5] = ""
all_data_sorted[5213][6] = "Alive"

# Maria Emma Mejia Velez
all_data_sorted[5214][4] = "1953"
all_data_sorted[5214][5] = ""
all_data_sorted[5214][6] = "Alive"

# Cesar Gaviria Trujillo
# data is correct, not sure why it is giving me an error
all_data_sorted[5302][5] = ""
all_data_sorted[5302][6] = "Alive"
all_data_sorted[5303][5] = ""
all_data_sorted[5303][6] = "Alive"
all_data_sorted[5304][5] = ""
all_data_sorted[5304][6] = "Alive"
all_data_sorted[5305][5] = ""
all_data_sorted[5305][6] = "Alive"

# Andres Pastrana
all_data_sorted[5420][5] = ""
all_data_sorted[5420][6] = "Alive"
all_data_sorted[5421][5] = ""
all_data_sorted[5421][6] = "Alive"
all_data_sorted[5422][5] = ""
all_data_sorted[5422][6] = "Alive"
all_data_sorted[5423][5] = ""
all_data_sorted[5423][6] = "Alive"
all_data_sorted[5424][5] = ""
all_data_sorted[5424][6] = "Alive"

# Ernesto Samper Pizano
all_data_sorted[5461][4] = "1950"
all_data_sorted[5461][5] = ""
all_data_sorted[5461][6] = "Alive"
all_data_sorted[5462][4] = "1950"
all_data_sorted[5462][5] = ""
all_data_sorted[5462][6] = "Alive"
all_data_sorted[5463][4] = "1950"
all_data_sorted[5463][5] = ""
all_data_sorted[5463][6] = "Alive"
all_data_sorted[5464][4] = "1950"
all_data_sorted[5464][5] = ""
all_data_sorted[5464][6] = "Alive"
all_data_sorted[5465][4] = "1950"
all_data_sorted[5465][5] = ""
all_data_sorted[5465][6] = "Alive"

# Girma Woldegiorgis
# Wikipedia is incorrect
all_data_sorted[5811][6] = "Dead"
all_data_sorted[5812][6] = "Dead"
all_data_sorted[5813][6] = "Dead"
all_data_sorted[5814][6] = "Dead"
all_data_sorted[5815][6] = "Dead"
all_data_sorted[5816][6] = "Dead"
all_data_sorted[5817][6] = "Dead"
all_data_sorted[5818][6] = "Dead"
all_data_sorted[5819][6] = "Dead"
all_data_sorted[5854][6] = "Dead"
all_data_sorted[5854][5] = "2013"
all_data_sorted[5855][6] = "Dead"
all_data_sorted[5855][5] = "2013"

# Metes Zenawi
all_data_sorted[6080][6] = "Dead"
all_data_sorted[6081][6] = "Dead"
all_data_sorted[6082][6] = "Dead"

# Negasso Gidada
all_data_sorted[6094][4] = "1943"
all_data_sorted[6094][5] = ""
all_data_sorted[6094][6] = "Alive"
all_data_sorted[6095][4] = "1943"
all_data_sorted[6095][5] = ""
all_data_sorted[6095][6] = "Alive"
all_data_sorted[6096][4] = "1943"
all_data_sorted[6096][5] = ""
all_data_sorted[6096][6] = "Alive"
all_data_sorted[6097][4] = "1943"
all_data_sorted[6097][5] = ""
all_data_sorted[6097][6] = "Alive"
all_data_sorted[6098][4] = "1943"
all_data_sorted[6098][5] = ""
all_data_sorted[6098][6] = "Alive"
all_data_sorted[6099][4] = "1943"
all_data_sorted[6099][5] = ""
all_data_sorted[6099][6] = "Alive"
all_data_sorted[6100][4] = "1943"
all_data_sorted[6100][5] = ""
all_data_sorted[6100][6] = "Alive"
all_data_sorted[6101][4] = "1943"
all_data_sorted[6101][5] = ""
all_data_sorted[6101][6] = "Alive"
all_data_sorted[6102][4] = "1943"
all_data_sorted[6102][5] = ""
all_data_sorted[6102][6] = "Alive"
all_data_sorted[6103][4] = "1943"
all_data_sorted[6103][5] = ""
all_data_sorted[6103][6] = "Alive"

# Tarnrat Layne
all_data_sorted[6156][5] = ""
all_data_sorted[6156][6] = "Alive"

# Dominique De Villepin
all_data_sorted[6308][5] = ""
all_data_sorted[6308][6] = "Alive"
all_data_sorted[6309][5] = ""
all_data_sorted[6309][6] = "Alive"
all_data_sorted[6310][5] = ""
all_data_sorted[6310 ][6] = "Alive"
all_data_sorted[6675][5] = ""
all_data_sorted[6675 ][6] = "Alive"


# Edouard Balladur
all_data_sorted[6571][5] = "2014"
all_data_sorted[6571][6] = "Dead"
all_data_sorted[6572][5] = "2014"
all_data_sorted[6572][6] = "Dead"

#Pierre Beregovy
all_data_sorted[6625][6] = "Dead"
all_data_sorted[6626][6] = "Dead"
all_data_sorted[6627][6] = "Dead"

#Jean-Pierre Raffarin
all_data_sorted[6971][5] = ""
all_data_sorted[6971][6] = "Alive"

#Nicolas Sarkozy
all_data_sorted[7013][5] = ""
all_data_sorted[7013][6] = "Alive"

#Richard von Weizsocker
all_data_sorted[7607][6] = "Dead"
all_data_sorted[7608][6] = "Dead"

# Addo Kufuor
all_data_sorted[8236][4] = "1940"
all_data_sorted[8236][5] = ""
all_data_sorted[8236][6] = "Alive"
all_data_sorted[8237][4] = "1940"
all_data_sorted[8237][5] = ""
all_data_sorted[8237][6] = "Alive"
all_data_sorted[8242][4] = "1940"
all_data_sorted[8242][5] = ""
all_data_sorted[8242][6] = "Alive"
all_data_sorted[8243][4] = "1940"
all_data_sorted[8243][5] = ""
all_data_sorted[8243][6] = "Alive"

#Johns Evans Atta Mills
all_data_sorted[8273][6] = "Alive"

#Jerry John Rawlings
all_data_sorted[8360][5] = ""
all_data_sorted[8360][6] = "Alive"
all_data_sorted[8361][5] = ""
all_data_sorted[8361][6] = "Alive"
all_data_sorted[8363][5] = ""
all_data_sorted[8363][6] = "Alive"

#Georgios Andreas  Papandreou
all_data_sorted[8578][5] = ""
all_data_sorted[8578][6] = "Alive"

# Andonios  Samaras
all_data_sorted[8578][5] = ""
all_data_sorted[8578][6] = "Alive"

# Konstandinos Karamanlis
all_data_sorted[8803][6] = "Dead"

#Constantinos Mitsotakis
all_data_sorted[8912][5] = ""
all_data_sorted[8912][6] = "Alive"
all_data_sorted[8913][5] = ""
all_data_sorted[8913][6] = "Alive"
all_data_sorted[8914][5] = ""
all_data_sorted[8914][6] = "Alive"

#Konstandinos Simitis
all_data_sorted[9106][4] = "1936"
all_data_sorted[9106][5] = ""
all_data_sorted[9106][6] = "Alive"
all_data_sorted[9107][4] = "1936"
all_data_sorted[9107][5] = ""
all_data_sorted[9107][6] = "Alive"
all_data_sorted[9108][4] = "1936"
all_data_sorted[9108][5] = ""
all_data_sorted[9108][6] = "Alive"
all_data_sorted[9109][4] = "1936"
all_data_sorted[9109][5] = ""
all_data_sorted[9109][6] = "Alive"
all_data_sorted[9110][4] = "1936"
all_data_sorted[9110][5] = ""
all_data_sorted[9110][6] = "Alive"
all_data_sorted[9111][4] = "1936"
all_data_sorted[9111][5] = ""
all_data_sorted[9111][6] = "Alive"
all_data_sorted[9112][4] = "1936"
all_data_sorted[9112][5] = ""
all_data_sorted[9112][6] = "Alive"
all_data_sorted[9113][4] = "1936"
all_data_sorted[9113][5] = ""
all_data_sorted[9113][6] = "Alive"
all_data_sorted[9114][4] = "1936"
all_data_sorted[9114][5] = ""
all_data_sorted[9114][6] = "Alive"
all_data_sorted[9115][4] = "1936"
all_data_sorted[9115][5] = ""
all_data_sorted[9115][6] = "Alive"

# Konstandinos "Kostis" "Stephanopoulos
all_data_sorted[9151][5] = ""
all_data_sorted[9151][6] = "Alive"
all_data_sorted[9152][5] = ""
all_data_sorted[9152][6] = "Alive"
all_data_sorted[9153][5] = ""
all_data_sorted[9153][6] = "Alive"
all_data_sorted[9154][5] = ""
all_data_sorted[9154][6] = "Alive"
all_data_sorted[9155][5] = ""
all_data_sorted[9155][6] = "Alive"
all_data_sorted[9156][5] = ""
all_data_sorted[9156][6] = "Alive"
all_data_sorted[9157][5] = ""
all_data_sorted[9157][6] = "Alive"

# Shiv Shankar  Menon
all_data_sorted[9468][4] = "1949"
all_data_sorted[9468][5] = ""
all_data_sorted[9468][6] = "Alive"
all_data_sorted[9469][4] = "1949"
all_data_sorted[9469][5] = ""
all_data_sorted[9469][6] = "Alive"
all_data_sorted[9470][4] = "1949"
all_data_sorted[9470][5] = ""
all_data_sorted[9470][6] = "Alive"
all_data_sorted[9471][4] = "1949"
all_data_sorted[9471][5] = ""
all_data_sorted[9471][6] = "Alive"
all_data_sorted[9472][4] = "1949"
all_data_sorted[9472][5] = ""
all_data_sorted[9472][6] = "Alive"

#Pranab  Mukherjee
all_data_sorted[9476][5] = ""
all_data_sorted[9476][6] = "Alive"
all_data_sorted[9477][5] = ""
all_data_sorted[9477][6] = "Alive"

# M K Narayanan
all_data_sorted[9500][4] = "1934"
all_data_sorted[9500][5] = ""
all_data_sorted[9500][6] = "Alive"
all_data_sorted[9501][4] = "1934"
all_data_sorted[9501][5] = ""
all_data_sorted[9501][6] = "Alive"
all_data_sorted[9502][4] = "1934"
all_data_sorted[9502][5] = ""
all_data_sorted[9502][6] = "Alive"
all_data_sorted[9503][4] = "1934"
all_data_sorted[9503][5] = ""
all_data_sorted[9503][6] = "Alive"
all_data_sorted[9503][0] = "M K Narayanan"
all_data_sorted[9504][4] = "1934"
all_data_sorted[9504][5] = ""
all_data_sorted[9504][6] = "Alive"

# Shivraj  Patil
all_data_sorted[9553][4] = "1934"
all_data_sorted[9553][5] = ""
all_data_sorted[9553][6] = "Alive"
all_data_sorted[9554][4] = "1934"
all_data_sorted[9554][5] = ""
all_data_sorted[9554][6] = "Alive"
all_data_sorted[9555][4] = "1934"
all_data_sorted[9555][5] = ""
all_data_sorted[9555][6] = "Alive"
all_data_sorted[9556][4] = "1934"
all_data_sorted[9556][5] = ""
all_data_sorted[9556][6] = "Alive"

#Nirupama  Rao
all_data_sorted[9614][4] = "1950"
all_data_sorted[9614][5] = ""
all_data_sorted[9614][6] = "Alive"
all_data_sorted[9615][4] = "1950"
all_data_sorted[9615][5] = ""
all_data_sorted[9615][6] = "Alive"

# PM Sayeed
all_data_sorted[9655][4] = "1941"
all_data_sorted[9644][6] = "Dead"
all_data_sorted[9656][4] = "1941"
all_data_sorted[9656][6] = "Dead"
all_data_sorted[9656][0] = "P M Sayeed"

#K Chandra  Shekhar Rao
all_data_sorted[9690][4] = "1954"
all_data_sorted[9690][5] = ""
all_data_sorted[9690][6] = "Alive"

#Manmohan  Singh
all_data_sorted[9740][5] = ""
all_data_sorted[9740][6] = "Alive"
all_data_sorted[9743][5] = ""
all_data_sorted[9743][6] = "Alive"
all_data_sorted[9747][5] = ""
all_data_sorted[9747][6] = "Alive"
all_data_sorted[9749][5] = ""
all_data_sorted[9749][6] = "Alive"
all_data_sorted[9753][5] = ""
all_data_sorted[9753][6] = "Alive"
all_data_sorted[9755][5] = ""
all_data_sorted[9755][6] = "Alive"
all_data_sorted[9758][5] = ""
all_data_sorted[9758][6] = "Alive"
all_data_sorted[9761][5] = ""
all_data_sorted[9761][6] = "Alive"
all_data_sorted[9764][5] = ""
all_data_sorted[9764][6] = "Alive"

# Raghuvansh Prasad  Singh
all_data_sorted[9765][4] = "1946"
all_data_sorted[9765][5] = ""
all_data_sorted[9765][6] = "Alive"
all_data_sorted[9766][4] = "1946"
all_data_sorted[9766][5] = ""
all_data_sorted[9766][6] = "Alive"
all_data_sorted[9767][4] = "1946"
all_data_sorted[9767][5] = ""
all_data_sorted[9767][6] = "Alive"
all_data_sorted[9768][4] = "1946"
all_data_sorted[9768][5] = ""
all_data_sorted[9768][6] = "Alive"
all_data_sorted[9769][4] = "1946"
all_data_sorted[9769][5] = ""
all_data_sorted[9769][6] = "Alive"

#Virbhadra  Singh
all_data_sorted[9770][4] = "1934"
all_data_sorted[9770][5] = ""
all_data_sorted[9770][6] = "Alive"
all_data_sorted[9771][4] = "1934"
all_data_sorted[9771][5] = ""
all_data_sorted[9771][6] = "Alive"
all_data_sorted[9772][4] = "1934"
all_data_sorted[9772][5] = ""
all_data_sorted[9772][6] = "Alive"

#Gowda H D Deve
all_data_sorted[10037][5] = ""
all_data_sorted[10037][6] = "Alive"
all_data_sorted[10040][5] = ""
all_data_sorted[10040][6] = "Alive"

#Inder Kumar Gujral
all_data_sorted[10046][5] = "2012"
all_data_sorted[10046][6] = "Dead"

#Balasaheb Vikhe Patil
all_data_sorted[10355][5] = ""
all_data_sorted[10355][6] = "Alive"
all_data_sorted[10356][5] = ""
all_data_sorted[10356][6] = "Alive"

#Jaisingrao Gaikwadh Patil
all_data_sorted[10358][4] = "1949"
all_data_sorted[10358][5] = ""
all_data_sorted[10358][6] = "Alive"

#Chennamaneni Vidyasagar Rao
all_data_sorted[10445][4] = "1942"
all_data_sorted[10445][5] = ""
all_data_sorted[10445][6] = "Alive"
all_data_sorted[10446][4] = "1942"
all_data_sorted[10446][5] = ""
all_data_sorted[10446][6] = "Alive"
all_data_sorted[10447][4] = "1942"
all_data_sorted[10447][5] = ""
all_data_sorted[10447][6] = "Alive"

#P V Narasimha Rao
all_data_sorted[10448][4] = "1921"
all_data_sorted[10448][5] = "2004"
all_data_sorted[10448][6] = "Dead"
all_data_sorted[10449][4] = "1921"
all_data_sorted[10449][5] = "2004"
all_data_sorted[10449][6] = "Dead"
all_data_sorted[10450][4] = "1921"
all_data_sorted[10450][5] = "2004"
all_data_sorted[10450][6] = "Dead"
all_data_sorted[10452][4] = "1921"
all_data_sorted[10452][5] = "2004"
all_data_sorted[10452][6] = "Dead"
all_data_sorted[10453][4] = "1921"
all_data_sorted[10453][5] = "2004"
all_data_sorted[10453][6] = "Dead"
all_data_sorted[10455][4] = "1921"
all_data_sorted[10455][5] = "2004"
all_data_sorted[10455][6] = "Dead"
all_data_sorted[10458][4] = "1921"
all_data_sorted[10458][5] = "2004"
all_data_sorted[10458][6] = "Dead"
all_data_sorted[10460][4] = "1921"
all_data_sorted[10460][5] = "2004"
all_data_sorted[10460][6] = "Dead"
all_data_sorted[10461][4] = "1921"
all_data_sorted[10461][5] = "2004"
all_data_sorted[10461][6] = "Dead"
all_data_sorted[10463][4] = "1921"
all_data_sorted[10463][5] = "2004"
all_data_sorted[10463][6] = "Dead"
all_data_sorted[10464][4] = "1921"
all_data_sorted[10464][5] = "2004"
all_data_sorted[10464][6] = "Dead"
all_data_sorted[10466][4] = "1921"
all_data_sorted[10466][5] = "2004"
all_data_sorted[10466][6] = "Dead"
all_data_sorted[10467][4] = "1921"
all_data_sorted[10467][5] = "2004"
all_data_sorted[10467][6] = "Dead"
all_data_sorted[10468][4] = "1921"
all_data_sorted[10468][5] = "2004"
all_data_sorted[10468][6] = "Dead"
all_data_sorted[10470][4] = "1921"
all_data_sorted[10470][5] = "2004"
all_data_sorted[10470][6] = "Dead"
all_data_sorted[10471][4] = "1921"
all_data_sorted[10471][5] = "2004"
all_data_sorted[10471][6] = "Dead"
all_data_sorted[10472][4] = "1921"
all_data_sorted[10472][5] = "2004"
all_data_sorted[10472][6] = "Dead"
all_data_sorted[10473][4] = "1921"
all_data_sorted[10473][5] = "2004"
all_data_sorted[10473][6] = "Dead"
all_data_sorted[10474][4] = "1921"
all_data_sorted[10474][5] = "2004"
all_data_sorted[10474][6] = "Dead"
all_data_sorted[10478][4] = "1921"
all_data_sorted[10478][5] = "2004"
all_data_sorted[10478][6] = "Dead"
all_data_sorted[10480][4] = "1921"
all_data_sorted[10480][5] = "2004"
all_data_sorted[10480][6] = "Dead"
all_data_sorted[10481][4] = "1921"
all_data_sorted[10481][5] = "2004"
all_data_sorted[10481][6] = "Dead"
all_data_sorted[10484][4] = "1921"
all_data_sorted[10484][5] = "2004"
all_data_sorted[10484][6] = "Dead"
all_data_sorted[10485][4] = "1921"
all_data_sorted[10485][5] = "2004"
all_data_sorted[10485][6] = "Dead"
all_data_sorted[10487][4] = "1921"
all_data_sorted[10487][5] = "2004"
all_data_sorted[10487][6] = "Dead"
all_data_sorted[10488][4] = "1921"
all_data_sorted[10488][5] = "2004"
all_data_sorted[10488][6] = "Dead"
all_data_sorted[10490][4] = "1921"
all_data_sorted[10490][5] = "2004"
all_data_sorted[10490][6] = "Dead"
all_data_sorted[10491][4] = "1921"
all_data_sorted[10491][5] = "2004"
all_data_sorted[10491][6] = "Dead"
all_data_sorted[10492][4] = "1921"
all_data_sorted[10492][5] = "2004"
all_data_sorted[10492][6] = "Dead"
all_data_sorted[10495][4] = "1921"
all_data_sorted[10495][5] = "2004"
all_data_sorted[10495][6] = "Dead"
all_data_sorted[10496][4] = "1921"
all_data_sorted[10496][5] = "2004"
all_data_sorted[10496][6] = "Dead"
all_data_sorted[10497][4] = "1921"
all_data_sorted[10497][5] = "2004"
all_data_sorted[10497][6] = "Dead"
all_data_sorted[10498][4] = "1921"
all_data_sorted[10498][5] = "2004"
all_data_sorted[10498][6] = "Dead"
all_data_sorted[10499][4] = "1921"
all_data_sorted[10499][5] = "2004"
all_data_sorted[10499][6] = "Dead"
all_data_sorted[10502][4] = "1921"
all_data_sorted[10502][5] = "2004"
all_data_sorted[10502][6] = "Dead"

#Rajnath Singh
all_data_sorted[10626][4] = "1951"
all_data_sorted[10626][5] = ""
all_data_sorted[10626][6] = "Alive"

#Shatrughan Sinha
all_data_sorted[10635][4] = "1945"
all_data_sorted[10635][5] = ""
all_data_sorted[10635][6] = "Alive"

#Yashwant Sinha
all_data_sorted[10639][4] = "1932"
all_data_sorted[10639][5] = ""
all_data_sorted[10639][6] = "Alive"
all_data_sorted[10640][4] = "1932"
all_data_sorted[10640][5] = ""
all_data_sorted[10640][6] = "Alive"
all_data_sorted[10641][4] = "1932"
all_data_sorted[10641][5] = ""
all_data_sorted[10641][6] = "Alive"
all_data_sorted[10642][4] = "1932"
all_data_sorted[10642][5] = ""
all_data_sorted[10642][6] = "Alive"

#Atal Behari Vajpayee
all_data_sorted[10691][5] = ""
all_data_sorted[10691][6] = "Alive"
all_data_sorted[10692][5] = ""
all_data_sorted[10692][6] = "Alive"
all_data_sorted[10699][5] = ""
all_data_sorted[10699][6] = "Alive"
all_data_sorted[10700][5] = ""
all_data_sorted[10700][6] = "Alive"

#Mary  Coughlan
all_data_sorted[10800][5] = ""
all_data_sorted[10800][6] = "Alive"
all_data_sorted[10803][5] = ""
all_data_sorted[10803][6] = "Alive"

#Brian Cowen
all_data_sorted[10811][5] = ""
all_data_sorted[10811][6] = "Alive"
all_data_sorted[10812][5] = ""
all_data_sorted[10812][6] = "Alive"
all_data_sorted[11019][5] = ""
all_data_sorted[11019][6] = "Alive"

#Eamon O  Cuiv
all_data_sorted[10814][4] = "1950"
all_data_sorted[10814][5] = ""
all_data_sorted[10814][6] = "Alive"

#Eamon  Gilmore
all_data_sorted[10836][4] = "1955"
all_data_sorted[10836][5] = ""
all_data_sorted[10836][6] = "Alive"
all_data_sorted[10838][4] = "1955"
all_data_sorted[10838][5] = ""
all_data_sorted[10838][6] = "Alive"
all_data_sorted[10840][4] = "1955"
all_data_sorted[10840][5] = ""
all_data_sorted[10840][6] = "Alive"
all_data_sorted[10843][4] = "1955"
all_data_sorted[10843][5] = ""
all_data_sorted[10843][6] = "Alive"

#Mary  Harney
all_data_sorted[10852][5] = ""
all_data_sorted[10852][6] = "Alive"
all_data_sorted[11071][5] = ""
all_data_sorted[11071][6] = "Alive"
all_data_sorted[11073][5] = ""
all_data_sorted[11073][6] = "Alive"
all_data_sorted[11075][5] = ""
all_data_sorted[11075][6] = "Alive"
all_data_sorted[11077][5] = ""
all_data_sorted[11077][6] = "Alive"
all_data_sorted[11078][5] = ""
all_data_sorted[11078][6] = "Alive"
all_data_sorted[11080][5] = ""
all_data_sorted[11080][6] = "Alive"
all_data_sorted[11082][5] = ""
all_data_sorted[11082][6] = "Alive"
all_data_sorted[11084][5] = ""
all_data_sorted[11084][6] = "Alive"
all_data_sorted[11087][5] = ""
all_data_sorted[11087][6] = "Alive"


#Tony Killeen
all_data_sorted[10883][5] = ""
all_data_sorted[10883][6] = "Alive"

#Brian  Lenihan
all_data_sorted[10884][4] = "1959"
all_data_sorted[10884][5] = "2011"
all_data_sorted[10884][6] = "Dead"
all_data_sorted[10885][4] = "1959"
all_data_sorted[10885][5] = "2011"
all_data_sorted[10885][6] = "Dead"
all_data_sorted[10886][4] = "1959"
all_data_sorted[10886][5] = "2011"
all_data_sorted[10886][6] = "Dead"

#Michael  Mcdowell
all_data_sorted[10898][4] = "1951"
all_data_sorted[10898][5] = ""
all_data_sorted[10898][6] = "Alive"
all_data_sorted[10899][4] = "1951"
all_data_sorted[10899][5] = ""
all_data_sorted[10899][6] = "Alive"
all_data_sorted[10900][4] = "1951"
all_data_sorted[10900][5] = ""
all_data_sorted[10900][6] = "Alive"
all_data_sorted[11137][4] = "1951"
all_data_sorted[11137][5] = ""
all_data_sorted[11137][6] = "Alive"
all_data_sorted[11138][4] = "1951"
all_data_sorted[11138][5] = ""
all_data_sorted[11138][6] = "Alive"
all_data_sorted[11139][4] = "1951"
all_data_sorted[11139][5] = ""
all_data_sorted[11139][6] = "Alive"
all_data_sorted[11140][4] = "1951"
all_data_sorted[11140][5] = ""
all_data_sorted[11140][6] = "Alive"
all_data_sorted[11141][4] = "1951"
all_data_sorted[11141][5] = ""
all_data_sorted[11141][6] = "Alive"


#Willie O'Dea
all_data_sorted[10910][5] = ""
all_data_sorted[10910][6] = "Alive"
all_data_sorted[10911][5] = ""
all_data_sorted[10911][6] = "Alive"
all_data_sorted[10912][5] = ""
all_data_sorted[10912][6] = "Alive"
all_data_sorted[10913][5] = ""
all_data_sorted[10913][6] = "Alive"

#John  O�Donoghue
all_data_sorted[10915][5] = ""
all_data_sorted[10915][6] = "Alive"
all_data_sorted[10916][5] = ""
all_data_sorted[10916][6] = "Alive"
all_data_sorted[11190][5] = ""
all_data_sorted[11190][6] = "Alive"
all_data_sorted[11191][5] = ""
all_data_sorted[11191][6] = "Alive"


#Batt O'Keeffe
all_data_sorted[10917][5] = ""
all_data_sorted[10917][6] = "Alive"
all_data_sorted[10918][5] = ""
all_data_sorted[10918][6] = "Alive"

#Bertte Ahern
all_data_sorted[10952][5] = ""
all_data_sorted[10952][6] = "Alive"
all_data_sorted[10952][0] = "Bertie Ahern"
all_data_sorted[10966][5] = ""
all_data_sorted[10966][6] = "Alive"
all_data_sorted[10952][0] = "Bertie Ahern"

#David Andrews
all_data_sorted[10976][5] = ""
all_data_sorted[10976][6] = "Alive"
all_data_sorted[10977][5] = ""
all_data_sorted[10977][6] = "Alive"

#Noel Dempsey
all_data_sorted[11038][5] = ""
all_data_sorted[11038][6] = "Alive"
all_data_sorted[11039][5] = ""
all_data_sorted[11039][6] = "Alive"
all_data_sorted[11040][5] = ""
all_data_sorted[11040][6] = "Alive"
all_data_sorted[11041][5] = ""
all_data_sorted[11041][6] = "Alive"
all_data_sorted[11042][5] = ""
all_data_sorted[11042][6] = "Alive"
all_data_sorted[11043][5] = ""
all_data_sorted[11043][6] = "Alive"

#Ivan Gates
#Wiki has no data
all_data_sorted[11064][5] = ""
all_data_sorted[11064][6] = ""
all_data_sorted[11065][5] = ""
all_data_sorted[11065][6] = ""

#Charles Haughey
all_data_sorted[11088][4] = "1925"
all_data_sorted[11088][5] = "2006"
all_data_sorted[11088][6] = "Dead"

#Michael Higgins
all_data_sorted[11093][5] = ""
all_data_sorted[11093][6] = "Alive"
all_data_sorted[11094][5] = ""
all_data_sorted[11094][6] = "Alive"
all_data_sorted[11095][5] = ""
all_data_sorted[11095][6] = "Alive"

#Michael Lowry
all_data_sorted[11102][4] = "1953"
all_data_sorted[11102][5] = ""
all_data_sorted[11102][6] = "Alive"
all_data_sorted[11103][4] = "1953"
all_data_sorted[11103][5] = ""
all_data_sorted[11103][6] = "Alive"

#Michael Martin
all_data_sorted[11106][5] = ""
all_data_sorted[11106][6] = "Alive"
all_data_sorted[11107][5] = ""
all_data_sorted[11107][6] = "Alive"
all_data_sorted[11108][5] = ""
all_data_sorted[11108][6] = "Alive"

#Mary O'Rourke
all_data_sorted[11192][5] = ""
all_data_sorted[11192][6] = "Alive"
all_data_sorted[11193][5] = ""
all_data_sorted[11193][6] = "Alive"

#Albert Reynolds
all_data_sorted[11199][5] = "2014"
all_data_sorted[11199][6] = "Dead"

#Michael Smith
all_data_sorted[11219][4] = "1940"
all_data_sorted[11219][5] = ""
all_data_sorted[11219][6] = "Dead"
all_data_sorted[11220][4] = "1940"
all_data_sorted[11220][5] = ""
all_data_sorted[11220][6] = "Dead"
all_data_sorted[11221][4] = "1940"
all_data_sorted[11221][5] = ""
all_data_sorted[11221][6] = "Dead"
all_data_sorted[11222][4] = "1940"
all_data_sorted[11222][5] = ""
all_data_sorted[11222][6] = "Dead"
all_data_sorted[11223][4] = "1940"
all_data_sorted[11223][5] = ""
all_data_sorted[11223][6] = "Dead"
all_data_sorted[11224][4] = "1940"
all_data_sorted[11224][5] = ""
all_data_sorted[11224][6] = "Dead"
all_data_sorted[11225][4] = "1940"
all_data_sorted[11225][5] = ""
all_data_sorted[11225][6] = "Dead"
all_data_sorted[11226][4] = "1940"
all_data_sorted[11226][5] = ""
all_data_sorted[11226][6] = "Dead"
all_data_sorted[11227][4] = "1940"
all_data_sorted[11227][5] = ""
all_data_sorted[11227][6] = "Dead"
all_data_sorted[11228][4] = "1940"
all_data_sorted[11228][5] = ""
all_data_sorted[11228][6] = "Dead"

#Richard Spring
all_data_sorted[11229][5] = ""
all_data_sorted[11229][6] = "Alive"
all_data_sorted[11230][5] = ""
all_data_sorted[11230][6] = "Alive"
all_data_sorted[11231][5] = ""
all_data_sorted[11231][6] = "Alive"
all_data_sorted[11232][5] = ""
all_data_sorted[11232][6] = "Alive"
all_data_sorted[11233][5] = ""
all_data_sorted[11233][6] = "Alive"
all_data_sorted[11234][5] = ""
all_data_sorted[11234][6] = "Alive"
all_data_sorted[11235][5] = ""
all_data_sorted[11235][6] = "Alive"
all_data_sorted[11236][5] = ""
all_data_sorted[11236][6] = "Alive"

#Michael Woods
all_data_sorted[11268][5] = ""
all_data_sorted[11268][6] = "Alive"
all_data_sorted[11269][5] = ""
all_data_sorted[11269][6] = "Alive"
all_data_sorted[11270][5] = ""
all_data_sorted[11270][6] = "Alive"

#Massimo  D�Alema
all_data_sorted[11367][5] = ""
all_data_sorted[11367][6] = "Alive"
all_data_sorted[11368][5] = ""
all_data_sorted[11368][6] = "Alive"
all_data_sorted[11369][5] = ""
all_data_sorted[11369][6] = "Alive"
all_data_sorted[11370][5] = ""
all_data_sorted[11370][6] = "Alive"

#Gianni  Letta
all_data_sorted[11420][5] = ""
all_data_sorted[11420][6] = "Alive"
all_data_sorted[11421][5] = ""
all_data_sorted[11421][6] = "Alive"
all_data_sorted[11422][5] = ""
all_data_sorted[11422][6] = "Alive"
all_data_sorted[11423][5] = ""
all_data_sorted[11423][6] = "Alive"
all_data_sorted[11424][5] = ""
all_data_sorted[11424][6] = "Alive"

#Romano Prodi
all_data_sorted[11904][4] = "1939"
all_data_sorted[11904][5] = ""
all_data_sorted[11904][6] = "Alive"
all_data_sorted[11905][4] = "1939"
all_data_sorted[11905][5] = ""
all_data_sorted[11905][6] = "Alive"

#Oscar Luigi Scalfaro
all_data_sorted[11944][5] = "2012"
all_data_sorted[11944][6] = "Dead"
all_data_sorted[11945][5] = "2012"
all_data_sorted[11945][6] = "Dead"
all_data_sorted[11946][5] = "2012"
all_data_sorted[11946][6] = "Dead"
all_data_sorted[11947][5] = "2012"
all_data_sorted[11947][6] = "Dead"
all_data_sorted[11948][5] = "2012"
all_data_sorted[11948][6] = "Dead"
all_data_sorted[11949][5] = "2012"
all_data_sorted[11949][6] = "Dead"

#Taro Aso
all_data_sorted[12060][5] = ""
all_data_sorted[12060][6] = "Alive"
all_data_sorted[12065][5] = ""
all_data_sorted[12065][6] = "Alive"
all_data_sorted[12372][5] = ""
all_data_sorted[12372][6] = "Alive"
all_data_sorted[12373][5] = ""
all_data_sorted[12373][6] = "Alive"


#Kunio Hatoyama
all_data_sorted[12110][5] = ""
all_data_sorted[12110][6] = "Alive"
all_data_sorted[12111][5] = ""
all_data_sorted[12111][6] = "Alive"

#Eisuke  Mori
all_data_sorted[12210][4] = "1948"
all_data_sorted[12210][5] = ""
all_data_sorted[12210][6] = "Alive"

#Masako  Mori
all_data_sorted[12211][4] = "1964"
all_data_sorted[12211][5] = ""
all_data_sorted[12211][6] = "Alive"
all_data_sorted[12212][4] = "1964"
all_data_sorted[12212][5] = ""
all_data_sorted[12212][6] = "Alive"
all_data_sorted[12213][4] = "1964"
all_data_sorted[12213][5] = ""
all_data_sorted[12213][6] = "Alive"
all_data_sorted[12214][4] = "1964"
all_data_sorted[12214][5] = ""
all_data_sorted[12214][6] = "Alive"
all_data_sorted[12215][4] = "1964"
all_data_sorted[12215][5] = ""
all_data_sorted[12215][6] = "Alive"
all_data_sorted[12216][4] = "1964"
all_data_sorted[12216][5] = ""
all_data_sorted[12216][6] = "Alive"
all_data_sorted[12217][4] = "1964"
all_data_sorted[12217][5] = ""
all_data_sorted[12217][6] = "Alive"
all_data_sorted[12218][4] = "1964"
all_data_sorted[12218][5] = ""
all_data_sorted[12218][6] = "Alive"

#Hiroshi  Nakai
all_data_sorted[12233][4] = "1942"
all_data_sorted[12233][5] = ""
all_data_sorted[12233][6] = "Alive"
all_data_sorted[12234][4] = "1942"
all_data_sorted[12234][5] = ""
all_data_sorted[12234][6] = "Alive"

#Hirofumi  Nakasone
all_data_sorted[12237][4] = "1945"
all_data_sorted[12237][5] = ""
all_data_sorted[12237][6] = "Alive"

#Seiko  Noda
all_data_sorted[12249][4] = "1960"
all_data_sorted[12249][5] = ""
all_data_sorted[12249][6] = "Alive"

#Yuko Obuchi
all_data_sorted[12254][4] = "1973"
all_data_sorted[12254][5] = ""
all_data_sorted[12254][6] = "Alive"

#Mikio Aoki
all_data_sorted[12368][5] = ""
all_data_sorted[12368][6] = "Alive"

#Ryutaro Hashimoto
all_data_sorted[12392][4] = "1937"
all_data_sorted[12392][5] = "2006"
all_data_sorted[12392][6] = "Dead"
all_data_sorted[12393][4] = "1937"
all_data_sorted[12393][5] = "2006"
all_data_sorted[12393][6] = "Dead"
all_data_sorted[12394][4] = "1937"
all_data_sorted[12394][5] = "2006"
all_data_sorted[12394][6] = "Dead"
all_data_sorted[12395][4] = "1937"
all_data_sorted[12395][5] = "2006"
all_data_sorted[12395][6] = "Dead"
all_data_sorted[12396][4] = "1937"
all_data_sorted[12396][5] = "2006"
all_data_sorted[12396][6] = "Dead"
all_data_sorted[12397][4] = "1937"
all_data_sorted[12397][5] = "2006"
all_data_sorted[12397][6] = "Dead"

#Keizo Obuchi
all_data_sorted[12572][4] = "1937"
all_data_sorted[12572][5] = "2000"
all_data_sorted[12572][6] = "Dead"
all_data_sorted[12573][4] = "1937"
all_data_sorted[12573][5] = "2000"
all_data_sorted[12573][6] = "Dead"
all_data_sorted[12574][4] = "1937"
all_data_sorted[12574][5] = "2000"
all_data_sorted[12574][6] = "Dead"

#Seiichi Ota
all_data_sorted[12593][4] = "1945"
all_data_sorted[12593][5] = ""
all_data_sorted[12593][6] = "Alive"

#Mohamed Najib  Balala
all_data_sorted[12715][4] = "1967"
all_data_sorted[12715][5] = ""
all_data_sorted[12715][6] = "Alive"
all_data_sorted[12716][4] = "1967"
all_data_sorted[12716][5] = ""
all_data_sorted[12716][6] = "Alive"
all_data_sorted[12717][4] = "1967"
all_data_sorted[12717][5] = ""
all_data_sorted[12717][6] = "Alive"

#Daniel T. Arap
all_data_sorted[13288][0] = "Daniel Toroitich arap Moi"
all_data_sorted[13288][5] = ""
all_data_sorted[13288][6] = "Alive"
all_data_sorted[13289][0] = "Daniel Toroitich arap Moi"
all_data_sorted[13289][5] = ""
all_data_sorted[13289][6] = "Alive"
all_data_sorted[13290][0] = "Daniel Toroitich arap Moi"
all_data_sorted[13290][5] = ""
all_data_sorted[13290][6] = "Alive"
all_data_sorted[13291][0] = "Daniel Toroitich arap Moi"
all_data_sorted[13291][5] = ""
all_data_sorted[13291][6] = "Alive"
all_data_sorted[13292][0] = "Daniel Toroitich arap Moi"
all_data_sorted[13292][5] = ""
all_data_sorted[13292][6] = "Alive"

#Felipe De Jesus Calderon  Hinojosa
all_data_sorted[13650][5] = ""
all_data_sorted[13650][6] = "Alive"
all_data_sorted[13651][5] = ""
all_data_sorted[13651][6] = "Alive"
all_data_sorted[13652][5] = ""
all_data_sorted[13652][6] = "Alive"
all_data_sorted[13653][5] = ""
all_data_sorted[13653][6] = "Alive"
all_data_sorted[13654][5] = ""
all_data_sorted[13654][6] = "Alive"
all_data_sorted[13655][5] = ""
all_data_sorted[13655][6] = "Alive"

#Ramon Martin  Huerta
all_data_sorted[13658][4] = "1957"
all_data_sorted[13658][5] = "2005"
all_data_sorted[13658][6] = "Dead"

#Juan Rafael Elvira  Quesada
all_data_sorted[13720][4] = "1956"
all_data_sorted[13720][5] = ""
all_data_sorted[13720][6] = "Alive"
all_data_sorted[13721][4] = "1956"
all_data_sorted[13721][5] = ""
all_data_sorted[13721][6] = "Alive"
all_data_sorted[13722][4] = "1956"
all_data_sorted[13722][5] = ""
all_data_sorted[13722][6] = "Alive"
all_data_sorted[13723][4] = "1956"
all_data_sorted[13723][5] = ""
all_data_sorted[13723][6] = "Alive"
all_data_sorted[13724][4] = "1956"
all_data_sorted[13724][5] = ""
all_data_sorted[13724][6] = "Alive"

#Ernesto Zedilio Ponce de Leon
all_data_sorted[14100][4] = "1951"
all_data_sorted[14100][5] = ""
all_data_sorted[14100][6] = "Alive"
all_data_sorted[14101][4] = "1951"
all_data_sorted[14101][5] = ""
all_data_sorted[14101][6] = "Alive"
all_data_sorted[14102][4] = "1951"
all_data_sorted[14102][5] = ""
all_data_sorted[14102][6] = "Alive"
all_data_sorted[14103][4] = "1951"
all_data_sorted[14103][5] = ""
all_data_sorted[14103][6] = "Alive"
all_data_sorted[14104][4] = "1951"
all_data_sorted[14104][5] = ""
all_data_sorted[14104][6] = "Alive"
all_data_sorted[14105][4] = "1951"
all_data_sorted[14105][5] = ""
all_data_sorted[14105][6] = "Alive"
all_data_sorted[14106][4] = "1951"
all_data_sorted[14106][5] = ""
all_data_sorted[14106][6] = "Alive"
all_data_sorted[14107][4] = "1951"
all_data_sorted[14107][5] = ""
all_data_sorted[14107][6] = "Alive"
all_data_sorted[14108][4] = "1951"
all_data_sorted[14108][5] = ""
all_data_sorted[14108][6] = "Alive"

#Vitoria Dias  Diogo
all_data_sorted[14204][5] = ""
all_data_sorted[14204][6] = "Alive"
all_data_sorted[14205][5] = ""
all_data_sorted[14205][6] = "Alive"
all_data_sorted[14206][5] = ""
all_data_sorted[14206][6] = "Alive"
all_data_sorted[14207][5] = ""
all_data_sorted[14207][6] = "Alive"
all_data_sorted[14208][5] = ""
all_data_sorted[14208][6] = "Alive"
all_data_sorted[14209][5] = ""
all_data_sorted[14209][6] = "Alive"

#Alberto Clementino Antonio  Vaquina
#Wiki has no info
all_data_sorted[14408][6] = "Dead"
all_data_sorted[14409][6] = "Dead"


#Joaqu�m Alberto Chissano
all_data_sorted[14480][5] = ""
all_data_sorted[14480][6] = "Alive"
all_data_sorted[14481][5] = ""
all_data_sorted[14481][6] = "Alive"
all_data_sorted[14482][5] = ""
all_data_sorted[14482][6] = "Alive"

#Jenny Shipley
all_data_sorted[16263][5] = ""
all_data_sorted[16263][6] = "Alive"
all_data_sorted[16264][5] = ""
all_data_sorted[16264][6] = "Alive"

#Amoldo Aleman Lacayo
all_data_sorted[16711][5] = ""
all_data_sorted[16711][6] = "Alive"
all_data_sorted[16715][5] = ""
all_data_sorted[16715][6] = "Alive"

#Mario Montenegro
#Wiki does not have data
all_data_sorted[16890][6] = "Dead"

#Umaru  Yar�Adua
all_data_sorted[17422][4] = "1951"
all_data_sorted[17422][5] = "2010"
all_data_sorted[17422][6] = "Dead"
all_data_sorted[17423][4] = "1951"
all_data_sorted[17423][5] = "2010"
all_data_sorted[17423][6] = "Dead"
all_data_sorted[17424][4] = "1951"
all_data_sorted[17424][5] = "2010"
all_data_sorted[17424][6] = "Dead"
all_data_sorted[17425][4] = "1951"
all_data_sorted[17425][5] = "2010"
all_data_sorted[17425][6] = "Dead"

#Sani Abacha
all_data_sorted[17429][4] = "1943"
all_data_sorted[17429][5] = "1998"
all_data_sorted[17429][6] = "Dead"
all_data_sorted[17430][4] = "1943"
all_data_sorted[17430][5] = "1998"
all_data_sorted[17430][6] = "Dead"
all_data_sorted[17431][4] = "1943"
all_data_sorted[17431][5] = "1998"
all_data_sorted[17431][6] = "Dead"
all_data_sorted[17432][4] = "1943"
all_data_sorted[17432][5] = "1998"
all_data_sorted[17432][6] = "Dead"

#Abdulsalam Abubakar
all_data_sorted[17452][5] = ""
all_data_sorted[17452][6] = "Alive"

#Jerzy  Miller
all_data_sorted[18135][4] = "1952"
all_data_sorted[18135][5] = ""
all_data_sorted[18135][6] = "Alive"

#Hanna Sucbocka
all_data_sorted[18554][5] = ""
all_data_sorted[18554][6] = "Alive"

#Pedro Manuel Passos  Coelho Mamede
all_data_sorted[18678][5] = ""
all_data_sorted[18678][6] = "Alive"
all_data_sorted[18679][5] = ""
all_data_sorted[18679][6] = "Alive"
all_data_sorted[18680][5] = ""
all_data_sorted[18680][6] = "Alive"

#Carlos  Costa
all_data_sorted[18700][4] = "1949"
all_data_sorted[18700][5] = ""
all_data_sorted[18700][6] = "Alive"
all_data_sorted[18701][4] = "1949"
all_data_sorted[18701][5] = ""
all_data_sorted[18701][6] = "Alive"
all_data_sorted[18702][4] = "1949"
all_data_sorted[18702][5] = ""
all_data_sorted[18702][6] = "Alive"
all_data_sorted[18703][4] = "1949"
all_data_sorted[18703][5] = ""
all_data_sorted[18703][6] = "Alive"

#Anibal Cavaco Silva
all_data_sorted[18905][4] = "1939"
all_data_sorted[18905][5] = ""
all_data_sorted[18905][6] = "Alive"
all_data_sorted[18906][4] = "1939"
all_data_sorted[18906][5] = ""
all_data_sorted[18906][6] = "Alive"
all_data_sorted[18907][4] = "1939"
all_data_sorted[18907][5] = ""
all_data_sorted[18907][6] = "Alive"
all_data_sorted[18908][4] = "1939"
all_data_sorted[18908][5] = ""
all_data_sorted[18908][6] = "Alive"
all_data_sorted[18909][4] = "1939"
all_data_sorted[18909][5] = ""
all_data_sorted[18909][6] = "Alive"

#Artur Consolado
#Wiki has no data
all_data_sorted[18917][6] = "Dead"
all_data_sorted[18918][6] = "Dead"

#Alberto Costa
all_data_sorted[18925][4] = "1947"
all_data_sorted[18925][5] = ""
all_data_sorted[18925][6] = "Alive"
all_data_sorted[18926][4] = "1947"
all_data_sorted[18926][5] = ""
all_data_sorted[18926][6] = "Alive"

#M�rio Alberto Soares
all_data_sorted[19129][5] = ""
all_data_sorted[19129][6] = "Alive"

#Jose Socrates
all_data_sorted[19130][5] = ""
all_data_sorted[19130][6] = "Alive"
all_data_sorted[19131][5] = ""
all_data_sorted[19131][6] = "Alive"
all_data_sorted[19136][5] = ""
all_data_sorted[19136][6] = "Alive"

#Antonio Rebelo de Sousa
all_data_sorted[19141][4] = "1952"
all_data_sorted[19141][5] = ""
all_data_sorted[19141][6] = "Alive"

#Tony Tan  Keng Yam
all_data_sorted[19293][5] = ""
all_data_sorted[19293][6] = "Alive"

#Goh Chok  Tong
all_data_sorted[19404][5] = ""
all_data_sorted[19404][6] = "Alive"
all_data_sorted[19406][5] = ""
all_data_sorted[19406][6] = "Alive"
all_data_sorted[19408][5] = ""
all_data_sorted[19408][6] = "Alive"
all_data_sorted[19409][5] = ""
all_data_sorted[19409][6] = "Alive"
all_data_sorted[19412][5] = ""
all_data_sorted[19412][6] = "Alive"
all_data_sorted[19479][5] = ""
all_data_sorted[19479][6] = "Alive"

#Ong Teng Cheong
all_data_sorted[19680][5] = "2002"
all_data_sorted[19680][6] = "Dead"
all_data_sorted[19682][5] = "2002"
all_data_sorted[19682][6] = "Dead"
all_data_sorted[19685][5] = "2002"
all_data_sorted[19685][6] = "Dead"

#Jose  Blanco Lopez
all_data_sorted[19818][4] = "1962"
all_data_sorted[19818][5] = ""
all_data_sorted[19818][6] = "Alive"
all_data_sorted[19819][4] = "1962"
all_data_sorted[19819][5] = ""
all_data_sorted[19819][6] = "Alive"

#Fernando Arias  Gonzalez
all_data_sorted[19884][4] = "1952"
all_data_sorted[19884][5] = ""
all_data_sorted[19884][6] = "Alive"

#Jose Maria Azoar
all_data_sorted[20059][5] = ""
all_data_sorted[20059][6] = "Alive"

#Felipe Gonz�lez Marquez
all_data_sorted[20125][4] = "1942"
all_data_sorted[20125][5] = ""
all_data_sorted[20125][6] = "Alive"
all_data_sorted[20126][4] = "1942"
all_data_sorted[20126][5] = ""
all_data_sorted[20126][6] = "Alive"
all_data_sorted[20127][4] = "1942"
all_data_sorted[20127][5] = ""
all_data_sorted[20127][6] = "Alive"

#G�ran Persson
all_data_sorted[20843][5] = ""
all_data_sorted[20843][6] = "Alive"

#Jakay Mrisho  Kikwete
all_data_sorted[21054][5] = ""
all_data_sorted[21054][6] = "Alive"
all_data_sorted[21439][5] = ""
all_data_sorted[21439][6] = "Alive"
all_data_sorted[21440][5] = ""
all_data_sorted[21440][6] = "Alive"
all_data_sorted[21441][5] = ""
all_data_sorted[21441][6] = "Alive"
all_data_sorted[21442][5] = ""
all_data_sorted[21442][6] = "Alive"



#Salmin Amour
all_data_sorted[21337][5] = ""
all_data_sorted[21337][6] = "Alive"
all_data_sorted[21338][5] = ""
all_data_sorted[21338][6] = "Alive"
all_data_sorted[21339][5] = ""
all_data_sorted[21339][6] = "Alive"
all_data_sorted[21340][5] = ""
all_data_sorted[21340][6] = "Alive"
all_data_sorted[21341][5] = ""
all_data_sorted[21341][6] = "Alive"
all_data_sorted[21342][5] = ""
all_data_sorted[21342][6] = "Alive"
all_data_sorted[21343][5] = ""
all_data_sorted[21343][6] = "Alive"
all_data_sorted[21344][5] = ""
all_data_sorted[21344][6] = "Alive"
all_data_sorted[21345][5] = ""
all_data_sorted[21345][6] = "Alive"
all_data_sorted[21346][5] = ""
all_data_sorted[21346][6] = "Alive"
all_data_sorted[21347][5] = ""
all_data_sorted[21347][6] = "Alive"
all_data_sorted[21348][5] = ""
all_data_sorted[21348][6] = "Alive"
all_data_sorted[21349][5] = ""
all_data_sorted[21349][6] = "Alive"

#Rashidi Mfaume Kawawa
all_data_sorted[21409][6] = "Dead"
all_data_sorted[21410][6] = "Dead"
all_data_sorted[21411][6] = "Dead"
all_data_sorted[21412][6] = "Dead"
all_data_sorted[21413][6] = "Dead"

#Edward Lowassa
all_data_sorted[21494][5] = ""
all_data_sorted[21494][6] = "Alive"
all_data_sorted[21496][5] = ""
all_data_sorted[21496][6] = "Alive"

#Benjamin Mkapa
all_data_sorted[21584][5] = ""
all_data_sorted[21584][6] = "Alive"

#Idris Abdul Wakil
all_data_sorted[21774][6] = "Dead"

#Joseph S Warioba
all_data_sorted[21746][5] = ""
all_data_sorted[21746][6] = "Alive"
all_data_sorted[21747][5] = ""
all_data_sorted[21747][6] = "Alive"
all_data_sorted[21748][5] = ""
all_data_sorted[21748][6] = "Alive"
all_data_sorted[21749][5] = ""
all_data_sorted[21749][6] = "Alive"
all_data_sorted[21749][0] = "Joseph S Warioba"


#Suleyrnan Demirel
all_data_sorted[22229][4] = "1924"
all_data_sorted[22229][5] = "2015"
all_data_sorted[22229][6] = "Dead"

#Bulent Ecev�t
all_data_sorted[22252][6] = "Dead"

#Necmeuin Erbakan
all_data_sorted[22259][5] = "2011"
all_data_sorted[22259][6] = "Dead"

#Ahmed Necdet Sezer
all_data_sorted[22491][5] = ""
all_data_sorted[22491][6] = "Alive"
all_data_sorted[22492][5] = ""
all_data_sorted[22492][6] = "Alive"

#Mesut Yilmaz
all_data_sorted[22596][4] = "1947"
all_data_sorted[22596][5] = ""
all_data_sorted[22596][6] = "Alive"
all_data_sorted[22597][4] = "1947"
all_data_sorted[22597][5] = ""
all_data_sorted[22597][6] = "Alive"
all_data_sorted[22614][4] = "1947"
all_data_sorted[22614][5] = ""
all_data_sorted[22614][6] = "Alive"

#Turgut �zal
all_data_sorted[22620][6] = "Dead"
all_data_sorted[22621][6] = "Dead"

#John  Hutton
all_data_sorted[22765][6] = "Alive"
all_data_sorted[22766][6] = "Alive"
all_data_sorted[22767][6] = "Alive"

#David  Jones
all_data_sorted[22782][6] = "Alive"
all_data_sorted[22783][6] = "Alive"

#Peter  Mandelson
all_data_sorted[22809][6] = "Alive"

#Ian  Mccartney
all_data_sorted[22822][6] = "Alive"

#Patrick  Mcloughlin
all_data_sorted[22823][6] = "Alive"
all_data_sorted[22824][6] = "Alive"
all_data_sorted[22825][6] = "Alive"
all_data_sorted[22826][6] = "Alive"

#James  Murphy
all_data_sorted[22846][6] = "Alive"
all_data_sorted[22847][6] = "Alive"

#Paul Murphy
all_data_sorted[22847][6] = "Alive"
all_data_sorted[22848][6] = "Alive"
all_data_sorted[23190][6] = "Alive"
all_data_sorted[23191][6] = "Alive"


#Jacqui  Smith
all_data_sorted[22879][4] = "1962"
all_data_sorted[22879][6] = "Alive"
all_data_sorted[22880][4] = "1962"
all_data_sorted[22880][6] = "Alive"

#Jonathan Altken
all_data_sorted[22910][6] = "Alive"

#Kenneth Baker
all_data_sorted[22915][6] = "Alive"
all_data_sorted[22916][6] = "Alive"
all_data_sorted[22917][6] = "Alive"

#Michael Forsyth
all_data_sorted[23029][6] = "Alive"
all_data_sorted[23030][6] = "Alive"

#Roger Freeman
all_data_sorted[23031][6] = "Alive"
all_data_sorted[23032][6] = "Alive"

#David Hunt
all_data_sorted[23083][6] = "Alive"
all_data_sorted[23084][6] = "Alive"
all_data_sorted[23085][6] = "Alive"
all_data_sorted[23086][6] = "Alive"
all_data_sorted[23087][6] = "Alive"

#Thomas King
all_data_sorted[23107][6] = "Alive"
all_data_sorted[23108][6] = "Alive"
all_data_sorted[23109][6] = "Alive"

#John MacGregor
all_data_sorted[23135][6] = "Alive"
all_data_sorted[23136][6] = "Alive"
all_data_sorted[23137][6] = "Alive"
all_data_sorted[23138][6] = "Alive"

#Mayhew Patrick
all_data_sorted[23160][6] = "Alive"
all_data_sorted[23161][6] = "Alive"
all_data_sorted[23162][6] = "Alive"
all_data_sorted[23163][6] = "Alive"

#Alan Milburn
all_data_sorted[23173][6] = "Alive"

#Michael Portillo
all_data_sorted[23205][6] = "Alive"
all_data_sorted[23206][6] = "Alive"
all_data_sorted[23207][6] = "Alive"

#George Robertson
all_data_sorted[23237][6] = "Alive"
all_data_sorted[23238][6] = "Alive"

#Chris Smith
all_data_sorted[23257][6] = "Alive"
all_data_sorted[23258][6] = "Alive"
all_data_sorted[23259][6] = "Alive"
all_data_sorted[23260][6] = "Alive"
all_data_sorted[23261][6] = "Alive"

#Gavin Strang
all_data_sorted[23262][6] = "Alive"

#David Waddington
all_data_sorted[23278][6] = "Alive"

#William Waldegrave
all_data_sorted[23283][6] = "Alive"
all_data_sorted[23284][6] = "Alive"
all_data_sorted[23285][6] = "Alive"
all_data_sorted[23286][6] = "Alive"
all_data_sorted[23287][6] = "Alive"
all_data_sorted[23288][6] = "Alive"
all_data_sorted[23289][6] = "Alive"

#George Young
all_data_sorted[23294][6] = "Alive"
all_data_sorted[23294][6] = "Alive"

#All of the US data from wikipedia is correct- but before we did not include DODs. Some of them get filled in, if they do not
# we mark them as alive

for i in range(1, total):
    if all_data_sorted[i][1] == "united states" and all_data_sorted[i][5] == "":
        all_data_sorted[i][6] = "Alive"


#Levy Patrick  Mwanawasa
all_data_sorted[23855][6] = "Dead"
all_data_sorted[23855][6] = "Dead"

#Godden Mandandi
#Wiki has no data
all_data_sorted[24140][6] = "Dead"

#Levy Mwanawasa
all_data_sorted[24216][6] = "Dead"

#Michael Sata
all_data_sorted[24292][6] = "Dead"
all_data_sorted[24294][6] = "Dead"
all_data_sorted[24295][6] = "Dead"
all_data_sorted[24296][6] = "Dead"
all_data_sorted[24297][6] = "Dead"
all_data_sorted[24298][6] = "Dead"
all_data_sorted[24299][6] = "Dead"
all_data_sorted[24300][6] = "Dead"
all_data_sorted[24301][6] = "Dead"
all_data_sorted[24302][6] = "Dead"



print("We made it")

with open("output1.csv", "w", newline='', encoding='utf-8') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(all_data_sorted)