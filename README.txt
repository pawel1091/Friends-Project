Opis ogólny:
	Program służy do prostej analizy scenariusza serialu "Friends".
	Jedną z jego funkcjonalności jest tworzenie wykresów słupkowych
	najczęściej wypowiadanych słów w serialu.
	Istnieje możliwość wyboru postaci oraz sezonów/odcinków,
	aby określić zakres scenariusza, który nas interesuje.


Wymagania:
	- python 3
	- biblioteki: pandas, matplotlib, bs4, requests, os.path, operator, re

Instruckja:
	Aby stworzyć wykres należy uruchomić plik Friends.py,
	a następnie odpowiedzieć na pytania dotyczące zakresu 
	scenariusza. (postacie, sezon, odcinek)
	Istnieje możliwość wyboru czy program ma ignorować
	tzw. "stop words". Ta funkcja znacznie wydłuża 
	czas oczekiwania.
	Program wygeneruję plik graph.png zawierający
	10 najczęściej wypowiadanych słów w określonym
	zakresie scenariusza.

Opis działania:
	Program został napisany w języku Python 3.
	Zostały użyte wcześniej wymienione biblioteki.
		Do programu zostały dołączone pliki Friends_statistics.csv
	oraz DataFrame_lines_Friends.csv zawierające kolejno
	statystyki odcinków oraz scenariusz. Dane potrzebne do
	stworzenia tych plików zostały pobrane z następujących stron:
		https://en.wikipedia.org/wiki/List_of_Friends_episodes
		http://www.livesinabox.com/friends/
	        (za pomocą biblioteki bs4 oraz requests)
		Pobrane dane zostały przetworzone do postaci tabel
	za pomocą biblioteki pandas. Następnie na podstawie tych 
	tabel sporządzono wykresy za pomocą biblioteki matplotlib.	
	Istnieje również możliwość ponownego generowania plików zawierających
	dane, jednak trwa to co najmniej kilka minut.