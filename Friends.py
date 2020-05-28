# imports libraries
import pandas as pd
from bs4 import BeautifulSoup as bs
import operator
import requests
import re
from matplotlib import pyplot as plt
import os.path
from os import path
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})


# Creating DataFrame from tables

def requests_html_code(URL):
    views_code = requests.get(URL).text
    scrapped_text = bs(views_code)
    return scrapped_text


def fixing_double_ep_df(df):
    # addding "/" to double episodes
    df_2 = []
    normal_len = 1
    for i in df:
        if normal_len - len(i) in [-1, 0, 1]:
            normal_len = len(i)
            df_2.append(i)
        else:
            a = i[:normal_len] + "/" + i[normal_len:]
            df_2.append(a)
    return df_2


def fixing_double_ep_df2(word):
    word = word[0]
    if len(word) > 2:
        a = word[:2] + "/" + word[2:]
        return a
    else:
        return word


def creating_Data_frame_with_No_Overall(URL):
    scrapped_text = requests_html_code(URL)
    # Creating "No.overall" index
    number_list = []
    for post in scrapped_text.find_all('th', {'scope': "row"}):
        a = post.text

        # removing special episodes
        if "S" in a:
            continue
        number_list.append(a)
    # deleting_wrong numbers
    number_list = number_list[10:-3]

    # addding "/" to double episodes
    number_list_fixed = fixing_double_ep_df(number_list)
    number_over = pd.DataFrame(number_list_fixed, columns=["No_overall"])
    return number_over


def Creating_tittle_list(URL):
    # creating "Tittle" List
    scrapped_text = requests_html_code(URL)
    title_list = []
    for post in scrapped_text.find_all('td', {'class': "summary"}):
        a = post.text
        # removing   => "
        a = a.replace('"', '')
        title_list.append(a)
    # manual removes special episodes
    title_list.remove("The One with All the Other Ones")
    title_list.remove("Friends: The Stuff You've Never Seen")

    title = pd.DataFrame(title_list, columns=["Values"])
    return title


def creating_rest_of_columns(URL):
    # creating DataFrame to extract rest of columns
    views_text = requests_html_code(URL)
    tittle_list = []
    for post in views_text.find_all('td'):
        a = post.text
        tittle_list.append(a)
    scrap_df = pd.DataFrame(tittle_list, columns=["Values"])
    return scrap_df


def creating_datatype(Data_column):
    for row in Data_column:
        temp_list = row.split("(")
        return temp_list[1][:10]


def removing_tail(df):
    for i in df:
        temp_list = i.split("[")
        return temp_list[0]


def final_DataFrame_with_stat():
    def Concateing_df(no_1, no_2):
        scrap_df = creating_rest_of_columns("https://en.wikipedia.org/wiki/List_of_Friends_episodes")
        merged_df = pd.concat([scrap_df.iloc[no_1], scrap_df.iloc[no_2]])
        cleaned_df = merged_df.reset_index()
        cleaned_df.drop(labels=["index"], axis=1, inplace=True)
        return cleaned_df

    def creating_datatype(Data_column):
        for row in Data_column:
            temp_list = row.split("(")
            return temp_list[1][:10]

    def removing_tail(df):
        for i in df:
            temp_list = i.split("[")
            return temp_list[0]

    number_over = creating_Data_frame_with_No_Overall("https://en.wikipedia.org/wiki/List_of_Friends_episodes")
    title = Creating_tittle_list("https://en.wikipedia.org/wiki/List_of_Friends_episodes")

    no_season_1 = range(60, 1202, 7)
    no_direc_1 = range(62, 1204, 7)
    no_written_1 = range(63, 1205, 7)
    no_date_1 = range(64, 1206, 7)
    no_views_1 = range(66, 1208, 7)

    no_season_2 = range(1211, 1647, 7)
    no_direc_2 = range(1213, 1649, 7)
    no_written_2 = range(1214, 1650, 7)
    no_date_2 = range(1215, 1651, 7)
    no_views_2 = range(1217, 1653, 7)

    no_season = Concateing_df(no_season_1, no_season_2)
    no_season_applied = no_season.apply(fixing_double_ep_df2, axis="columns")
    directors = Concateing_df(no_direc_1, no_direc_2)
    written = Concateing_df(no_written_1, no_written_2)
    dates = Concateing_df(no_date_1, no_date_2)

    applied_dates = dates.apply(creating_datatype, axis="columns")
    applied_dates = pd.DataFrame(applied_dates)
    applied_dates.columns = ["Col_Name_Dates"]
    # changing datatype
    applied_dates["Col_Name_Dates"] = pd.to_datetime(applied_dates["Col_Name_Dates"])

    viewers = Concateing_df(no_views_1, no_views_2)
    viewers_applied = viewers.apply(removing_tail, axis="columns")

    # season number

    season_number_list = []
    season = 1
    temp_no = 1
    for ep_no in no_season_applied:
        try:
            int_ep_no = int(ep_no)
        except:
            pass
        difference = int_ep_no - temp_no

        if difference < 0:
            season += 1
        temp_no = int_ep_no
        season_number_list.append(season)

        # Creating last Dataframe
    number_over["Season"] = season_number_list
    number_over["No_in_season"] = no_season_applied
    number_over["Title"] = title
    number_over["Directed_by"] = directors
    number_over["Written_by"] = written
    number_over["Air_date"] = applied_dates
    number_over["US_viewers(milion)"] = viewers_applied
    number_over.set_index(["Season", "No_in_season"], inplace=True)
    number_over.to_csv("Friends_statistics.csv", index=True, encoding="utf-8")


def creating_DataFrame_with_lines(URL):
    # Creating list of links to episodes
    links_list = []
    # searching for link tails
    page_with_dialogues_texts = requests_html_code(URL)
    for post in page_with_dialogues_texts.find_all("a"):
        b = post.get("href")
        if b[:6] == "season" or b[:2] == "10":
            links_list.append(b)

    # removing duplicated from list without changing its order
    del links_list[0]
    del links_list[-1]
    del links_list[-18]
    links_list.remove("season4/423uncut.htm")
    links_list.remove("season7/outtakes.htm")
    lines_list = []
    episode_list = []
    character_list = []
    # using list from previous part

    scrapped_text = requests_html_code("https://en.wikipedia.org/wiki/List_of_Friends_episodes")
    number_list = creating_Data_frame_with_No_Overall("https://en.wikipedia.org/wiki/List_of_Friends_episodes")
    number_list = number_list.values.tolist()

    for part in links_list:
        # matching list with episode
        proper_index = links_list.index(part)
        merged_URL = "http://www.livesinabox.com/friends/" + part
        dialogue_text = requests_html_code(merged_URL)

        for line in dialogue_text.find_all("p"):
            c = line.text
            temp_list = c.split(" ")
            try:
                colon = temp_list[0][-1]
                first_letter = temp_list[0][0]
                banned_first_letters = ["[", '(']
            except:
                continue

            if colon == ":" and first_letter not in banned_first_letters:
                # removing "\n" and deleting text in () and []
                d = " ".join(c.splitlines())
                e = re.sub(r" ?\([^)]+\)", "", d)
                # avoiding problems with empty line

                try:
                    Lines = e.split(' ', 1)[1]  # split every " " one time, [1] - take second word
                except:
                    continue
                # They renamed "Chandler" with "Chan" and because of this i cant scrap from few episodes
                actor = e.split(" ", 1)[0]
                if actor == "Chandler:" or actor == "CHANDLER:" or actor == "CHAN:":
                    character_list.append("Chandler")
                elif actor == "Ross:" or actor == "ROSS:":
                    character_list.append("Ross")
                elif actor == "Phoebe:" or actor == "PHOEBE:" or actor == "PHOE:":
                    character_list.append("Phoebe")
                elif actor == "Joey:" or actor == "JOEY:":
                    character_list.append("Joey")
                elif actor == "Rachel:" or actor == "RACHEL:" or actor == "RACH:":
                    character_list.append("Rachel")
                elif actor == "Monica:" or actor == "MONICA:" or actor == "MNCA:":
                    character_list.append("Monica")
                else:
                    character_list.append("Other")

                # matching line with every actor and episode

                lines_list.append(Lines)
                episode = number_list[proper_index][0]
                episode_list.append(episode)
                # matching every line with episode text

    Lines_dataFrame = pd.DataFrame(lines_list, columns=["Lines"])
    Lines_dataFrame["Character"] = character_list
    Lines_dataFrame["No_overall"] = episode_list
    return Lines_dataFrame


def choosing_rows(Seasons="all", Episode_in_season="all", Character="all"):
    Lines_table = pd.read_csv("DataFrame_lines_Friends.csv")
    Lines_table = Lines_table.drop(columns=["Unnamed: 0"], axis=1)
    choosed_rows = Lines_table
    if Character != "all":
        choosed_rows = choosed_rows[(choosed_rows["Character"] == Character)]
    if Seasons != "all":
        Seasons = int(Seasons)
        choosed_rows = choosed_rows[(choosed_rows["Season"] == Seasons)]
    if Episode_in_season != "all":
        Episode_in_season = str(Episode_in_season)
        choosed_rows = choosed_rows[(choosed_rows["No_in_season"] == Episode_in_season)]
    return (choosed_rows)


def creating_graph(specified_rows, stop_words):
    extracted_word_list = []

    def creating_mega_string(extracted_lines):  # it creates a list of splitted word
        try:
            word_list = extracted_lines.split(" ")
            for word in word_list:
                symbols = "!@#$%^&*()'-_+|},{\".:?><"
                for i in range(0, len(symbols)):
                    word = word.replace(symbols[i], "")
                if len(word) > 0:
                    extracted_word_list.append(word)
        except:
            pass

    def creating_top_words_and_occurences(extracted_word_list, stop_words):
        for word in extracted_word_list:
            symbols = "!@#$%^&*()'_+|},{\".:?><"
            for i in range(0, len(symbols)):
                word = word.replace(symbols[i], "")
        most_frequent_words = []
        occurence_of_words = []
        stop_words_list = ["0o", "gonna", "Shes", "shes", "Well", "dont", "cant", "were", "Yknow", "doesnt", "Were",
                           "didnt", "thats", "Thats", "Youre", "youre", "She's", "she's", "Well", "don't", "can't",
                           "we're", "doesn't", "We're", "didn't", "that's", "That's", "You're", "you're", "thing",
                           "Yeah", "What", "her", "you'are", "she", "I", "know", "Oh", "I'm", "You", "don't", "it's",
                           "uh", "No", "Hey" "0s", "3a", "3b", "3d", "6b", "6o", "a", "A", "a1", "a2", "a3", "a4", "ab",
                           "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across",
                           "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "after",
                           "afterwards", "ag", "again", "against", "ah", "ain", "aj", "al", "all", "allow", "allows",
                           "almost", "alone", "along", "already", "also", "although", "always", "am", "among",
                           "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody",
                           "anyhow", "anymore", "anyone", "anyway", "anyways", "anywhere", "ao", "ap", "apart",
                           "apparently", "appreciate", "approximately", "ar", "are", "aren", "arent", "arise", "around",
                           "as", "aside", "ask", "asking", "at", "au", "auth", "av", "available", "aw", "away",
                           "awfully", "ax", "ay", "az", "b", "B", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be",
                           "became", "been", "before", "beforehand", "beginnings", "behind", "below", "beside",
                           "besides", "best", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both",
                           "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "C",
                           "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "cc", "cd", "ce", "certain",
                           "certainly", "cf", "cg", "ch", "ci", "cit", "cj", "cl", "clearly", "cm", "cn", "co", "com",
                           "come", "comes", "con", "concerning", "consequently", "consider", "considering", "could",
                           "couldn", "couldnt", "course", "cp", "cq", "cr", "cry", "cs", "ct", "cu", "cv", "cx", "cy",
                           "cz", "d", "D", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described",
                           "despite", "detail", "df", "di", "did", "didn", "dj", "dk", "dl", "do", "does", "doesn",
                           "doing", "don", "done", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during",
                           "dx", "dy", "e", "E", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "eg", "ei",
                           "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "en", "end",
                           "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et",
                           "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything",
                           "everywhere", "ex", "exactly", "example", "except", "ey", "f", "F", "f2", "fa", "far", "fc",
                           "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "five", "fix", "fj",
                           "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth",
                           "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further",
                           "furthermore", "fy", "g", "G", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give",
                           "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr",
                           "greetings", "gs", "gy", "h", "H", "h2", "h3", "had", "hadn", "happens", "hardly", "has",
                           "hasn", "hasnt", "have", "haven", "having", "he", "hed", "hello", "help", "hence", "here",
                           "hereafter", "hereby", "herein", "heres", "hereupon", "hes", "hh", "hi", "hid", "hither",
                           "hj", "ho", "hopefully", "how", "howbeit", "however", "hr", "hs", "http", "hu", "hundred",
                           "hy", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "ie", "if", "ig",
                           "ignored", "ih", "ii", "ij", "il", "im", "immediately", "in", "inasmuch", "inc", "indeed",
                           "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead",
                           "interest", "into", "inward", "io", "ip", "iq", "ir", "is", "isn", "it", "itd", "its", "iv",
                           "ix", "iy", "iz", "j", "J", "jj", "jr", "js", "jt", "ju", "just", "k", "K", "ke", "keep",
                           "keeps", "kept", "kg", "kj", "km", "ko", "l", "L", "l2", "la", "largely", "last", "lately",
                           "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let",
                           "lets", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ln", "lo", "look",
                           "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "M", "m2", "ma", "made", "mainly",
                           "make", "makes", "many", "may", "maybe", "me", "meantime", "meanwhile", "merely", "mg",
                           "might", "mightn", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover",
                           "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn",
                           "my", "n", "N", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly",
                           "necessarily", "neither", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj",
                           "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos",
                           "not", "noted", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "O", "oa", "ob",
                           "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj",
                           "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto",
                           "oo", "op", "oq", "or", "ord", "os", "ot", "otherwise", "ou", "ought", "our", "out",
                           "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "P", "p1", "p2", "p3",
                           "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past",
                           "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please",
                           "plus", "pm", "pn", "po", "poorly", "pp", "pq", "pr", "predominantly", "presumably",
                           "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu",
                           "put", "py", "q", "Q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "R", "r2", "ra",
                           "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently",
                           "ref", "refs", "regarding", "regardless", "regards", "related", "relatively",
                           "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri",
                           "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s",
                           "S", "s2", "sa", "said", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second",
                           "secondly", "section", "seem", "seemed", "seeming", "seems", "seen", "sent", "seven",
                           "several", "sf", "shall", "shan", "shed", "shes", "show", "showed", "shown", "showns",
                           "shows", "si", "side", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm",
                           "sn", "so", "some", "somehow", "somethan", "sometime", "sometimes", "somewhat", "somewhere",
                           "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr",
                           "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such",
                           "sufficiently", "suggest", "take",
                           "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than",
                           "thank", "thanks", "thanx", "that", "thats", "the", "their", "theirs", "them", "themselves",
                           "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein",
                           "thereof", "therere", "theres", "thereto", "thereupon", "these", "they", "theyd", "theyre",
                           "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou",
                           "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus",
                           "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward",
                           "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "tt", "tv",
                           "twelve", "twenty", "twice",
                           "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up",
                           "upon", "ups", "ur", "us", "used", "useful", "usefully", "usefulness", "using", "usually",
                           "volumtype", "wasn", "wasnt", "way", "we",
                           "wed", "welcome", "well", "well-b", "went", "were", "weren", "werent", "what", "whatever",
                           "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby",
                           "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither",
                           "who", "whod", "whoever", "whole", "whom", "whomever", "whos", "whose", "why", "wi",
                           "widely", "with", "within", "without", "wo", "won", "wonder", "wont", "would", "wouldn",
                           "wouldnt"]
        while len(most_frequent_words) < 10:
            most_freq_word = max(set(extracted_word_list), key=extracted_word_list.count)
            occurence = extracted_word_list.count(most_freq_word)
            if stop_words == "yes":
                if most_freq_word not in stop_words_list and len(most_freq_word) > 4:
                    most_frequent_words.append(most_freq_word)
                    occurence_of_words.append(occurence)
                while most_freq_word in extracted_word_list:
                    extracted_word_list.remove(most_freq_word)
            if stop_words == "no":
                if len(most_freq_word) > 4:
                    most_frequent_words.append(most_freq_word)
                    occurence_of_words.append(occurence)
                while most_freq_word in extracted_word_list:
                    extracted_word_list.remove(most_freq_word)
        return occurence_of_words, most_frequent_words

    specified_rows["Lines"].apply(creating_mega_string)

    graph_data = creating_top_words_and_occurences(extracted_word_list, stop_words)
    bar_DataFrame = pd.DataFrame(graph_data[1], columns=["Most_common_words"])
    bar_DataFrame["Quantity"] = graph_data[0]
    plt.tight_layout()
    graph = bar_DataFrame.plot.bar(x="Most_common_words", y="Quantity")
    graph.figure.savefig('graph.png', dpi=100)

def main(Seasons="all", Episode_in_season="all", Character="all", stop_words="no"):
    # Creating Statistics Table
    if path.exists("Friends_statistics.csv") == False:
        print("Creating Statistics table")
        number_over = creating_Data_frame_with_No_Overall("https://en.wikipedia.org/wiki/List_of_Friends_episodes")
        scrap_df = creating_rest_of_columns("https://en.wikipedia.org/wiki/List_of_Friends_episodes")
        final_DataFrame_with_stat()
        Statistics_table = pd.read_csv("Friends_statistics.csv")
        print("Created Statistics table")
    else:
        Statistics_table = pd.read_csv("Friends_statistics.csv")
    if path.exists("DataFrame_lines_Friends.csv") == False:
        print("Creating Lines table")
        Lines_table = creating_DataFrame_with_lines("http://www.livesinabox.com/friends/scripts.shtml")
        cut_Statistics_table = Statistics_table[["Season", "No_in_season", "No_overall"]]
        Lines_table = Lines_table.merge(cut_Statistics_table, how="left", on="No_overall", sort=False)
        Lines_table.to_csv("DataFrame_lines_Friends.csv", index=True, encoding="utf-8")
        Lines_table = pd.read_csv("DataFrame_lines_Friends.csv")
        Lines_table = Lines_table.drop(columns=["Unnamed: 0"], axis=1)
        print("Created Lines table")
    else:
        Lines_table = pd.read_csv("DataFrame_lines_Friends.csv")
        Lines_table = Lines_table.drop(columns=["Unnamed: 0"], axis=1)
    choosed_rows = choosing_rows(Seasons, Episode_in_season, Character)
    creating_graph(choosed_rows, stop_words)


condition1 = input("Do you want to specify seasons?(yes/no)")
if condition1 == "yes":
    Seasons = input("Enter season[1-10], (for every season write 'all')")
else:
    Seasons = "all"
condition2 = input("Do you want to specify season episode?(yes/no)")
if condition2 == "yes":
    Episode_in_season = input("Enter episode[check on web], (for every episode write 'all')")
else:
    Episode_in_season = "all"
condition3 = input("Do you want to specify character?(yes/no)")
if condition3 == "yes":
    Character = input(
        "Enter character[Monica, Chandler, Ross, Phoebe, Rachel, Joey], (for every character write 'all')")
else:
    Character = "all"
stop_words = input("Do you want to reject stop words?(yes/no)[rejecting stop words will extend the waiting time]")
main(Seasons, Episode_in_season, Character, stop_words)
print("Created file graph.png, check it!!!")
