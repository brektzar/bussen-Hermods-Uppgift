import random

# import matplotlib.pyplot as plt  -  Används inte just nu!

'''
Passenger klassen innehåller grunden för alla passagerare.
All informationstyp som passageraren ska ha och i vilken ordning.
'''


class Passenger:
    def __init__(self, seat, name, gender, age, stops, price, coupon, final_stop, poke, poke_id):
        self.seat = seat
        self.name = name
        self.gender = gender
        self.age = age
        self.stops = stops
        self.price = price
        self.coupon = coupon
        self.final_stop = final_stop
        self.poke_reaction = poke
        self.poke_id = poke_id


'''
Bus klassen är huvudklassen för programmet.
Här sker allt från att köra rutter till att peta på passagerare.
Av och påstigning av passagerare sker också här med hjälp av Passenger klassen.
'''


class Bus:
    # Text färger i ANSI-Kod
    CB = "\033[0;34m"  # Color Blue
    CY = "\033[0;33m"  # Color Yellow
    CR = "\033[0;31m"  # Color Red
    CG = "\033[0;32m"  # Color Green
    CM = "\033[0;35m"  # Color Magenta
    CC = "\033[0;36m"  # Color Cyan
    CLR = "\033[0m"  # Color Reset

    # Två listor med namn, en för manliga namn och en för kvinnliga.
    # Jag har inte hittat på alla namnen själv utan tagit dessa från en lista online.
    names_male = ["Erik", "Axel", "William", "Liam", "Noah", "Elias", "Hugo", "Oscar",
                  "Lucas", "Oliver", "Albert", "Karl", "Benjamin", "Arvid", "Melker", "Emil",
                  "Love", "Birk", "Valter", "Nils", "Isak", "Viggo", "Edvin", "Vincent",
                  "Theodore", "Alfred", "Elliot", "Adrian", "Fabian", "Simon", "Viktor",
                  "Leo", "Julian", "Matteo", "Ivar", "John", "David", "Mohammed", "Omar",
                  "Ali", "Alexander", "Filip", "Gabriel", "Abbe", "Kasper", "Anton", "Robin"]

    names_female = ["Astrid", "Ebba", "Elvira", "Elsa", "Freja", "Greta", "Hanna", "Ingrid",
                    "Isabella", "Juni", "Kajsa", "Linnea", "Linnéa", "Lisa", "Lovisa", "Maja",
                    "Märta", "Nova", "Saga", "Selma", "Signe", "Siri", "Sofia", "Stella",
                    "Stina", "Tindra", "Tyra", "Tova", "Wilma", "Alma", "Agnes", "Alice",
                    "Emilia", "Elin", "Elina", "Ellen", "Emma", "Ester", "Eva", "Frida",
                    "Heja", "Hedda", "Hilma", "Ina", "Iris", "Julia", "Karla", "Klara",
                    "Kristina", "Leona", "Liv"]

    '''
    Ett första försök till att öka slumpade val mellan kvinnor och män och göra det hela mer realistiskt och ojämnt.
    Om valet bara är ett nummer så är chansen för varje nummer 50%, men med tio nummer blir varje nummers chans 10%,
    dock förblir den totala chansen fortfarande 50% och min "smarta" idé var mest bara dålig matte...
    En (kanske?) bättre idé kommer längre ner i add_passenger metoden.
    '''
    female_selection = [2, 4, 6, 8, 10]
    male_selection = [1, 3, 5, 7, 9]

    max_seats = 49  # Max sittplatser på bussen
    passengers = []  # Listan som håller Passenger objekten, endast de som är på bussen just nu dock
    all_passengers = []  # Ännu en lista som håller Passenger objekt, men denna håller ALLA som åkt bussen
    occupied_seats = []  # Vilka sätesnummer som är upptagna, känns snabbare än att kolla alla passagerarobjekt
    coupon_amount = 0  # Hur många kuponger som har använts för att resa billigare
    passengers_total = 0  # Hur många passagerare som åkt totalt
    passengers_done = 0  # Hur många passagerare som går av bussen vid nuvarande hållplats
    stops_visited = 1  # Vilken hållplats bussen är på just nu
    total_earned = 0  # Hur mycket pengar Bussbolaget AB tjänat på rutten
    total_stops = 0  # Hur många hållplatser alla passagerare ska\har åka\åkt sammanräknat
    total_age = 0  # Räknar ihop alla åldrar för att räkna ut medel på alla passagerare som åkt
    total_age_current = 0  # Räknar ihop alla åldrar för att räkna ut medel på alla passagerare på bussen just nu
    total_earned_current = 0  # Den totala summan Bussbolaget AB tjänat på de passagerare som åker just nu
    total_stops_current = 0  # Hur många hållplatser nuvarande passagerare ska åka sammanräknat
    extra_info = False  # Ger extra information vid varje hållplats
    data_exists = False  # Om True så har man haft minst en passagerare så data finns
    poking = False  # True om man petar på någon annars False

    passengers_ps = []  # En extra lista för att skapa graf över antalet passagerare per stop
    passenger_al = []  # En extra lista för att skapa graf över antalet passagerare per ålder
    passenger_td = []  # En extra lista för att skapa graf över vanligaste reslängderna

    ''' Metoden Run
        Styr huvudmenyn och kallar på relevanta metoder
    '''
    def run(self):
        # Huvudmenyn för programmet
        while True:
            while True:
                try:  # Ser till att valet inte är något annat än de som kan väljas
                    print(f"{self.CG}")
                    print("Meny:")
                    print(f"{self.CY}1.{self.CG} Kör till nästa hållplats")
                    print(f"{self.CY}2.{self.CG} Kör ett antal hållplatser")
                    print(f"{self.CY}3.{self.CG} Visa information om resan")
                    print(f"{self.CY}4.{self.CG} Avsluta")
                    print(f"{self.CY}5.{self.CG} Sätt på eller stäng av extra info vid hållplatser{self.CLR}")
                    print(f"{self.CY}6.{self.CG} Peta på en passagerare{self.CLR}")

                    # Menyval kan bara vara heltal
                    choice = int(input(f"{self.CG}Välj alternativ: {self.CLR}"))
                    print(f"\n")
                    break
                except ValueError:
                    print(f"\n")
                    print(f"{self.CR}Var god skriv in numret på det alternativ du vill välja.{self.CLR}")

            if choice == 1:
                self.first_choice()  # Kör till nästa hållplats och hanterar passageraravgång och påstigning

            elif choice == 2:
                self.second_choice()  # Kör till nästa hållplats och hanterar passageraravgång och påstigning

            elif choice == 3:
                if self.data_exists:
                    self.route_info()  # Visar detaljerad information om resan
                else:
                    # Om data inte finns så kan vi inte visa något, felmeddelande
                    print(f"{self.CR}Finns ingen data att visa ännu!{self.CLR}")

            elif choice == 4:  # Avsluta
                print(f"{self.CY}Tack för att du använder dig av BussBolaget ABs app för statistik")
                exit()
            elif choice == 5:  # Visar namn på de som stiger på eller av
                if self.extra_info:
                    print(f"{self.CR}Extra info Stängs Av!{self.CLR}")
                    self.extra_info = False
                else:
                    print(f"{self.CR}Extra info Sätts På!{self.CLR}")
                    self.extra_info = True
            elif choice == 6:  # Petfunktionen, vissa går av bussen om de blir petade på
                self.poke_passenger()

            else:
                print(f"{self.CR}Var god skriv in numret på det alternativ du vill välja.{self.CLR}")

            '''
            #Nedan kod är inte implementerat ännu, jag jobbar på det...
            #Försöker lära mig matplotlib för att visa grafer och känner att detta var en bra uppgift att testa i
            #då bussen innehåller mycket data.
            # elif choice == 7:
            # 
            #     sorted_td = {i: self.passenger_td.count(i) for i in self.passenger_td}  # Travel distances
            #     sorted_ps = {i: self.passengers_ps.count(i) for i in self.passengers_ps}  # passagerare per stopp
            #     sorted_ages = {i: self.passenger_al.count(i) for i in self.passenger_al}  # Vilka åldrar åker
            #     print("sorted_td", sorted_td)
            #     print("sorted_ps", sorted_ps)
            #     print("sorted_ages", sorted_ages)
            # 
            #     plt.figure(figsize=(20, 10))
            # 
            #     figure, axis = plt.subplots(3, 1, figsize=(10, 6))
            # 
            #     axis[0].bar(list(sorted_ages.keys()),
            #                 list(sorted_ages.values()),
            #                 color="skyblue", edgecolor="black", linewidth=1)
            #     axis[0].set_title("Age of passengers")
            #     axis[0].set_xlabel("Stop")
            #     axis[0].set_ylabel("Number of Passengers")
            # 
            #     axis[1].bar(list(sorted_ps.keys()),
            #                 list(sorted_ps.values()),
            #                 color="lightgreen", edgecolor="black", linewidth=1)
            #     axis[1].set_title("Passengers per stop")
            #     axis[1].set_xlabel("Stop")
            #     axis[1].set_ylabel("Number of Passengers")
            # 
            #     axis[2].bar(list(sorted_td.keys()),
            #                 list(sorted_td.values()),
            #                 color="maroon", edgecolor="black", linewidth=1)
            #     axis[2].set_title("passengers per distance")
            #     axis[2].set_xlabel("Stop")
            #     axis[2].set_ylabel("Number of Passengers")
            # 
            #     figure.tight_layout()
            #     plt.show()
            '''  # EJ IMPLEMENTERAT! - Matplotlib för grafer

    ''' Metoden First Choice 
        Simulerar av och påstigande passagerare vid en hållplats.
        Kollar om bussen redan har åkt förbi 100 hållplatser, om man åkt mer än 100 hållplatser ges ett felmeddelande.
    '''
    def first_choice(self):
        random_new = random.randint(0, 10)  # Slumpat antal nya passagerare (0-10)
        new_passengers = 0
        if self.stops_visited > 100:
            print(f"{self.CR}Du har redan åkt genom 100 hållplatser, starta om programmet för fler resor.")
        else:
            self.stops_visited += 1  # Lägg till +1 för varje besökt hållplats
            for passenger in self.passengers:  # Ta bort passagerare som ska gå av
                if passenger.final_stop == self.stops_visited:
                    self.remove_passenger(passenger)

            for i in range(random_new):  # Lägg till nya passagerare om det finns plats
                if len(self.occupied_seats) < self.max_seats:
                    new_passengers += 1
                    self.passengers, self.occupied_seats, coupon, name = self.add_passenger()
                    self.data_exists = True
                    if self.extra_info:
                        print(f"{self.CY}{name}{self.CB} gick på bussen{self.CLR}")
                    if coupon != "Ingen kupong":
                        self.coupon_amount += 1
                else:
                    pass  # Om bussen är full läggs ingen ny till

            if self.extra_info:  # Skriv ut lite mer detaljerad information om hållplatsen(nr + på och avstigande)
                print(f"{self.CB}Hållplats {self.CY}{self.stops_visited - 1}{self.CLR}")
                print(f"{self.CR}{new_passengers}{self.CB} gick på vid detta stopp{self.CLR}")
                print(f"{self.CB}{self.passengers_done}{self.CR} gick av vid detta stopp\n{self.CLR}")
            else:  # Skriv ut information om hållplatsen(endast nummer)
                print(f"{self.CB}Nuvarande hållplats:{self.CY}{self.stops_visited - 1}{self.CLR}")

            self.passengers_ps.append(new_passengers)  # Spara antalet påstigande

    ''' Metoden Second Choice 
        Simulerar av och påstigande passagerare vid flera hållplats.
        Kollar om bussen redan har åkt förbi 100 hållplatser, om man åkt mer än 100 hållplatser ges ett felmeddelande.
    '''
    def second_choice(self):
        self.passengers_done = 0  # Nollställ avstigna passagerare
        stops_input = int(input(f"{self.CG}Hur många hållplatser? {self.CLR}"))
        if self.stops_visited > 100:  # Över 100 hållplatser ger felmeddelande
            print(f'''
    {self.CR}Du har redan åkt genom 100 hållplatser, starta om programmet för fler resor.
    100 hållplatser skapar väldigt många passagerare och det kan bli väldigt mycket data att hantera
    ''')
        elif self.stops_visited + stops_input > 101:  # Över 100 hållplatser ger felmeddelande
            print(f'''
    {self.CR}Du kan bara resa {101 - self.stops_visited} gånger till
    100 hållplatser skapar väldigt många passagerare och det kan bli väldigt mycket data att hantera
    ''')

        else:  # Reser valt antal hållplatser och vid varje hållplats går passagerare av och på
            for i in range(stops_input):
                self.stops_visited += 1
                random_new = random.randint(0, 10)
                new_passengers = 0
                for passenger in self.passengers:
                    if passenger.final_stop == self.stops_visited:
                        self.remove_passenger(passenger)
                for j in range(random_new):
                    if len(self.occupied_seats) < self.max_seats:
                        self.passengers, self.occupied_seats, coupon, name = self.add_passenger()
                        self.data_exists = True  # Sätter en bool till sann eftersom det nu finns data
                        if self.extra_info:
                            print(f"{self.CY}{name}{self.CB} gick på bussen{self.CLR}")
                        if coupon != "Ingen kupong":
                            self.coupon_amount += 1
                    else:
                        pass
                if self.extra_info:
                    print(f"{self.CB}Hållplats {self.CY}{self.stops_visited - 1}{self.CLR}")
                    print(f"{self.CR}{new_passengers}{self.CB} gick på vid detta stopp{self.CLR}")
                    print(f"{self.CB}{self.passengers_done}{self.CR} gick av vid detta stopp\n{self.CLR}")
                if not self.extra_info:
                    print(f"{self.CB}Nuvarande hållplats:{self.CY}{self.stops_visited - 1}{self.CLR}")
                self.passengers_ps.append(new_passengers)

    ''' Metoden Remove Passenger
        Tar bort en passagerare från bussen och uppdaterar relevant information.
    '''
    def remove_passenger(self, passenger):
        self.passengers_done += 1
        if self.extra_info:
            print(f"{self.CY}{passenger.name}{self.CR} går nu av bussen{self.CLR}")

        if self.poking:  # Om man petat på någon som blev sur så går denne av här
            print(f"{self.CG}{self.CY}{passenger.name}{self.CLR} {self.CR}går nu av bussen..!{self.CLR}")
            print(f'''
{self.CR}På grund av vår policy returneras pengarna{self.CY}({passenger.price}){self.CR} för biljetten.{self.CLR}
            ''')
            self.total_earned -= passenger.price  # Återbetala biljettpriset
            self.poking = False  # när man inte längre petar på någon är denna bool falsk

        self.total_age_current -= passenger.age  # ta bort passagerarens ålder från listan
        self.total_stops_current -= passenger.stops  # ta bort passagerarens reslängd från listan
        self.total_earned_current -= passenger.price  # ta bort passagerarens biljettpris från listan
        self.passengers.remove(passenger)  # ta bort passageraren
        self.occupied_seats.remove(passenger.seat)  # Gör sittplatsen tillgänglig igen

    ''' Metoden Add Passenger
        Lägger till en passagerare från bussen och uppdaterar relevant information.
    '''
    def add_passenger(self):
        gender_choice = int  # används för att slumpa kön, ska vara int
        name = str  # namen på passagerare ska vara sträng
        gender = str  # Könet ska vara en sträng
        coupon = str  # kupongen är en sträng
        self.passengers_total += 1  # lägger till en passagerare till totalen för hela resan

        while True:
            if len(self.occupied_seats) < self.max_seats:
                '''
                Nedan är mitt bästa försök till att få ojämn fördelning mellan män och kvinnor, det fungerar hyfsat.
                Antalen håller sig inte för långt ifrån varandra men de är inte heller super täta.
                '''
                for i in range(random.randint(1, 100)):  # väljer en "slumpad" siffra mellan 1 - 100
                    gender_choice = random.randint(1, 10)  # väljer en "slumpad" siffra mellan 1 - 10
                    if random.random() < 0.25:  # 25% chans att bryta ut ur loopen och fortsätta koden
                        break
                if gender_choice in self.male_selection:  # om man så väljs namn från listan på manliga namn
                    name = random.choice(self.names_male)
                    gender = "Man"  # Sätter könet på passenger objektet

                elif gender_choice in self.female_selection:  # om kvinna så väljs namn från listan på kvinnliga namn
                    name = random.choice(self.names_female)
                    gender = "Kvinna"  # Sätter könet på passenger objektet

                stops = random.randint(1, 10)  # bestämmer hur många hållplatser passageraren åker
                age = random.randint(13, 80)  # bestämmer passagerarens ålder
                seat = random.randint(1, self.max_seats)  # bestämmer passagerarens säte
                price, coupon = self.calculate_price(age, stops)  # bestämmer passagerarens pris och kupong
                final_stop = self.stops_visited + stops  # bestämmer passagerarens avgångshållplats
                if final_stop < self.stops_visited:  # passagerare ska inte kunna få tidigare hållplats som avgång
                    final_stop = self.stops_visited + 1
                if final_stop > 99:  # passagerare ska inte kunna vara kvar efter hållplats 100 men
                    final_stop = 100  # det fungerar inte helt hundra ännu, jobbar på det!

                poke, poke_id = self.poke_reaction(age)  # bestämmer passagerarens petreaktion

                if seat not in self.occupied_seats:
                    # lägger till passagerarens data i olika listor
                    self.total_earned += price
                    self.total_stops += stops
                    self.total_age += age
                    self.total_age_current += age
                    self.total_stops_current += stops
                    self.total_earned_current += price
                    # Uppdaterar listor med passagerarens data och objekt
                    new_passenger = Passenger(seat, name, gender, age, stops, price, coupon, final_stop, poke, poke_id)
                    self.passengers.append(new_passenger)
                    self.all_passengers.append(new_passenger)
                    self.occupied_seats.append(seat)
                    self.passenger_al.append(age)
                    self.passenger_td.append(stops)
                    break

                else:
                    pass

            else:
                break
        return self.passengers, self.occupied_seats, coupon, name  # returnerar variabler utanför add_passenger metoden

    @staticmethod  # Metoden är Static för att den inte använder sig av self
    def poke_reaction(age):  # Baserat på ålder så väljs en slumpad petreaktion
        adult_react = [
            ["Ursäkta mig? Varför petar du på mig? Jag vill inte bli rörd."],
            ["Ursäkta?, jag känner inte dig. Vad vill du?"],
            ["Vad sysslar du med? Jag har inte tid med sånt här trams! (Passageraren är irriterad och går av bussen)."]
        ]
        retired_react = [
            ["Oj! Jag trodde du var någon jag kände. Vad kan jag hjälpa dig med?"],
            ["Ursäkta mig, jag är lite döv. Kan du säga det igen?"],
            ["Vad gör du!? Peta på människor sådär... (Passageraren är irriterad och går av bussen)"]
        ]
        young_react = [
            ["Va? Varför petar du på mig?"],
            ["Vem är du och Vad vill du mig?"],
            ["Vad är det för fel på dig? Sluta peta på mig! (Passageraren är irriterad och går av bussen)"]
        ]

        poke_randomizer = random.randint(0, 2)
        if age < 20:
            return young_react[poke_randomizer], poke_randomizer
        elif 19 < age < 67:
            return adult_react[poke_randomizer], poke_randomizer
        elif age > 66:
            return retired_react[poke_randomizer], poke_randomizer
        else:
            print("detta funka inte...")

    ''' Metoden Poke Passenger
        Petar på en passagerare, om passageraren blir sur går hen av bussen.
    '''
    def poke_passenger(self):
        try:
            while True:
                seat_choice = int(input(f"{self.CG}Välj sätesnumret du vill peta på: {self.CLR}"))  # Säte att peta på
                if seat_choice in self.occupied_seats:
                    for passenger in self.passengers:
                        if passenger.seat == seat_choice:  # vem du petar på och dennes reaktion
                            print(f"{self.CG}Du petar på: {self.CY}{passenger.name}{self.CLR}")
                            print(f"{self.CY}{passenger.name}- {self.CR}{passenger.poke_reaction}{self.CLR}")
                            if passenger.poke_id == 2:  # om passageraren blev sur så går hen av bussen
                                self.poking = True
                                self.remove_passenger(passenger)
                else:  # om man petar på ett tomt säte ges felmeddelande
                    print(f"{self.CR}Det sitter ingen i den stolen...{self.CLR}")
                break
        except ValueError:  # Om man skriver in fel sak i input ges ett felmeddelande
            print(f"{self.CR}Skriv in NUMMER i heltal på den sittplats du vill peta på{self.CLR}")

    ''' Metoden Calculate Price
        Räknar ut biljettpris med eller utan kupong
    '''
    @staticmethod  # Metoden är Static för att den inte använder sig av self
    def calculate_price(age, stops):
        coupon_list = [0, 0, 0, 0, 0, 0, 0, 10, 25, 50]  # 30% chans att få en kupong

        if age < 15:  # Räknar ut priset för passagerarens reslängd
            price = 0
        elif 20 > age > 15:
            price = 15 * stops
        elif age > 67:
            price = 10 * stops
        else:
            price = 30 * stops

        coupon = random.choice(coupon_list)  # Väljer en kupong från listan coupon_list
        if coupon == 10 or coupon == 25 or coupon == 50:  # om kupong ej är 0 så ges avdrag på biljettpriset
            if coupon == 10:
                price = price * 0.90
                coupon = "10%"
            elif coupon == 25:
                price = price * 0.75
                coupon = "25%"
            elif coupon == 50:
                price = price * 0.5
                coupon = "50%"
        elif coupon == 0:  # om kupong är 0 ges inget avdrag
            coupon = "Ingen kupong"

        return price, coupon  # returnerar variablerna utanför metoden

    ''' Metoden route_info
        Visar all data kring resan och passagerare för användaren
    '''
    def route_info(self):

        # Räknar ut medeltalen och antal per kön
        average_stops = int(self.total_stops / self.passengers_total)
        average_price = self.total_earned / self.passengers_total
        average_age = int(self.total_age / self.passengers_total)
        amount_female = sum(1 for passenger in self.all_passengers if passenger.gender == "Kvinna")
        amount_male = sum(1 for passenger in self.all_passengers if passenger.gender == "Man")

        # Räknar ut data baserat på de som åker just nu
        current_passengers = len(self.passengers)
        current_female = sum(1 for passenger in self.passengers if passenger.gender == "Kvinna")
        current_male = sum(1 for passenger in self.passengers if passenger.gender == "Man")
        average_age_current = self.total_age_current // current_passengers
        average_stops_current = self.total_stops_current // current_passengers
        average_price_current = self.total_earned_current / current_passengers

        # Presenterar informationen på ett förståeligt sätt för användaren
        print(f'''{self.CG}
Antal passagerare just nu är: {self.CB}{current_passengers}{self.CG}
Av dessa är {self.CY}{current_female}{self.CG} kvinnor och {self.CY}{current_male}{self.CG} män.
De ockuperar för närvarande dessa säten: {self.CB}{self.occupied_seats}{self.CG}
Medelåldern på bussen just nu är {self.CB}{average_age_current}{self.CG} år.
Medellängden på resor just nu är {self.CB}{average_stops_current}{self.CG} hållplatser.
Medelpriset på biljetter just nu är {self.CR}{average_price_current:.2f}{self.CG} kronor.

Totalt har {self.CB}{self.passengers_total}{self.CG} åkt med bussen idag,
av dessa var {self.CY}{amount_female}{self.CG} kvinnor och {self.CY}{amount_male}{self.CG} män.
Medelåldern under turen har varit {self.CB}{average_age}{self.CG} år.
Medellängden på resor har varit {self.CB}{average_stops}{self.CG} hållplatser.
''')

        if self.coupon_amount == 1:
            print(f"{self.CR}{self.coupon_amount} {self.CG}Kupong har använts{self.CLR}")
        if self.coupon_amount == 0:
            print(f"{self.CR}Inga Kuponger har använts{self.CLR}")
        elif self.coupon_amount >= 2:
            print(f"{self.CR}{self.coupon_amount} {self.CG}Kuponger har använts{self.CLR}")

        print(f"{self.CG}Medelpriset på biljetter har under resan varit {self.CR}{average_price:.2f}{self.CG} kronor.")
        print(f"{self.CG}Hittills har BussBolaget AB tjänat {self.CR}{self.total_earned:.0f}{self.CG} kronor på resan.")

        print("\n")

        while True:
            while True:
                try:
                    detailed_info = str(input(f"{self.CG}Vill du se mer info passagerarna?(J/N){self.CLR}").lower())
                    break
                except ValueError:  # Skriver du in annat än en sträng får du ett felmeddelande och nytt försök
                    print("Skriv in 'J' för ja eller 'N' för nej")

                # om detaljerad info efterfrågas ges en mängd information om varje passagerare på bussen just nu
            if detailed_info == "j":
                # Sorterar baserat på ålder
                self.passengers = sorted(self.passengers, key=lambda passenger: passenger.age)
                for i in self.passengers:  # Visar detaljerad info om varje passagerare
                    print(f'''{self.CG}
-------------------------------
| Passagerarinfo:
| Sittplats: {self.CM}{i.seat}{self.CG}
| Namn: {self.CY}{i.name}{self.CG}
| Kön: {self.CB}{i.gender}{self.CG}
| Ålder: {self.CC}{i.age}{self.CG}
| 
| Biljettinfo:
| {self.CY}{i.name}{self.CG} ska åka genom {self.CB}{i.stops}{self.CG} Hållplatser
| Pris: {self.CR}{i.price}{self.CG} Kr
| Kupong: {self.CB}{i.coupon}{self.CG}
|
| Petfras: {self.CR}{i.poke_reaction}{self.CG}
-------------------------------''')
                break

            elif detailed_info == "n":
                break
            else:  # Skriver du in annat än J eller N så får du felmeddelande och försöka igen
                print("Skriv in 'J' för ja eller 'N' för nej")


class Program:
    def __init__(self):
        mybus = Bus()  # Skapar en instans av klassen Bus lägger den i en variabel som heter mybus.
        mybus.run()  # kallar på metoden Run i instansen mybus.


if __name__ == "__main__":  # kollar om man kör importerat eller direkt, direkt = kör, importerad = körs ej
    # Skapar en instans av klassen Program i variabeln my_program
    my_program = Program()
