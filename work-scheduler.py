from pulp import *
import random
from tabulate import tabulate

def main():
    dani = ['ponedjeljak', 'utorak', 'srijeda', 'cetvrtak', 'petak', 'subota', 'nedjelja']
    smjene = {
        'jutro': {'trajanje': 4, 'potrebno': 2},
        'popodne': {'trajanje': 6, 'potrebno': 3},
        'vece': {'trajanje': 4, 'potrebno': 1}
    }

    zaposleni_primjer = {
        'Alis': {'satnica': 15, 'max_sati': 20, 'nedostupni': [('ponedjeljak', 'vece')]},
        'Bob': {'satnica': 20, 'max_sati': 25, 'nedostupni': []},
        'Charlie': {'satnica': 18, 'max_sati': 15, 'nedostupni': [(dan, 'vece') for dan in dani]}
    }

    def generisi_instancu(broj_zaposlenih):
        imena = ["Ana", "Marko", "Ivana", "Petar", "Jovan", "Marija", "Nikola", "Sofija"]
        zaposleni = {}
        
        for i in range(broj_zaposlenih):
            ime = imena[i] if i < len(imena) else f"Zaposleni_{i+1}"
            satnica = random.randint(10, 25)
            max_sati = random.randint(15, 30)
            
            nedostupni = []
            for dan in dani:
                for smjena in smjene:
                    if random.random() < 0.2:
                        nedostupni.append((dan, smjena))
            
            zaposleni[ime] = {'satnica': satnica, 'max_sati': max_sati, 'nedostupni': nedostupni}
        
        return zaposleni

    #funkcija za lin. programiranje
    def linearno_programiranje(zaposleni, smjene, dani):
        prob = LpProblem("RadniRaspored", LpMinimize)

        x = LpVariable.dicts("x", 
                            [(i,j,k) for i in zaposleni 
                                     for j in smjene 
                                     for k in dani],
                            cat='Binary')

        #ciljna f-ja
        prob += lpSum(x[(i,j,k)] * zaposleni[i]['satnica'] * smjene[j]['trajanje'] 
                      for i in zaposleni 
                      for j in smjene 
                      for k in dani)

        #ogranicenja
        for j in smjene:
            for k in dani:
                prob += lpSum(x[(i,j,k)] for i in zaposleni) >= smjene[j]['potrebno']

        for i in zaposleni:
            prob += lpSum(x[(i,j,k)] * smjene[j]['trajanje'] 
                         for j in smjene 
                         for k in dani) <= zaposleni[i]['max_sati']

        for i in zaposleni:
            for k in dani:
                prob += lpSum(x[(i,j,k)] for j in smjene) <= 1

        for i in zaposleni:
            for nedostupan in zaposleni[i]['nedostupni']:
                k, j = nedostupan
                prob += x[(i,j,k)] == 0

        prob.solve()

        return {
            'status': LpStatus[prob.status],
            'ukupni_troskovi': value(prob.objective),
            'raspored': {k: {j: [] for j in smjene} for k in dani}
        }

    #funkcija za pohlepni algoritam
    def greedy_schedule(zaposleni, smjene, dani):
        raspored = {k: {j: [] for j in smjene} for k in dani}
        ukupni_troskovi = 0
        
        sortirani_zaposleni = sorted(zaposleni.keys(), 
                            key=lambda x: (zaposleni[x]['satnica'], 
                                          -zaposleni[x]['max_sati']))
        
        sortirane_smjene = sorted(smjene.keys(), key=lambda x: -smjene[x]['trajanje'])
        
        preostali_sati = {i: zaposleni[i]['max_sati'] for i in zaposleni}
        
        for k in dani:
            for j in sortirane_smjene:
                potrebno = smjene[j]['potrebno']
                dodijeljeno = 0
                
                for i in sortirani_zaposleni:
                    if (k, j) not in [(ned[0], ned[1]) for ned in zaposleni[i]['nedostupni']] and \
                       preostali_sati[i] >= smjene[j]['trajanje'] and \
                       dodijeljeno < potrebno:
                        
                        if not any(i in raspored[k][s] for s in smjene):
                            raspored[k][j].append(i)
                            preostali_sati[i] -= smjene[j]['trajanje']
                            ukupni_troskovi += zaposleni[i]['satnica'] * smjene[j]['trajanje']
                            dodijeljeno += 1
        
        pokrivenost = all(len(raspored[k][j]) >= smjene[j]['potrebno'] 
                        for k in dani for j in smjene)
        
        return {
            'ukupni_troskovi': ukupni_troskovi,
            'potpuna_pokrivenost': pokrivenost
        }

    #funkcija za prikaz rezultata
    def prikazi_rezultate(naziv, lp_rez, greedy_rez):
        tabela = [
            ["Metoda", "Status", "Ukupni troškovi", "Potpuna pokrivenost"],
            ["Linearno programiranje", lp_rez.get('status', 'N/A'), 
             f"${lp_rez.get('ukupni_troskovi', 'N/A')}", "N/A"],
            ["Pohlepni algoritam", "N/A", 
             f"${greedy_rez.get('ukupni_troskovi', 'N/A')}", 
             "DA" if greedy_rez.get('potpuna_pokrivenost', False) else "NE"]
        ]
        
        print(f"\n{naziv}")
        print(tabulate(tabela, headers="firstrow", tablefmt="grid"))
        print()

    #pokretanje
    print("\n=== REZULTATI ZA PRIMJER IZ ZADATKA ===\n")
    lp_rez = linearno_programiranje(zaposleni_primjer, smjene, dani)
    greedy_rez = greedy_schedule(zaposleni_primjer, smjene, dani)
    prikazi_rezultate("Primjer sa 3 zaposlena", lp_rez, greedy_rez)

    #testiranje dodatnih instanci
    velicine = [5, 10, 15]
    for velicina in velicine:
        print(f"\n=== REZULTATI ZA INSTANCU SA {velicina} ZAPOSLENIH ===\n")
        instanca = generisi_instancu(velicina)
        
        try:
            lp_rez = linearno_programiranje(instanca, smjene, dani)
        except Exception as e:
            lp_rez = {'status': f"Greška: {str(e)}"}
        
        greedy_rez = greedy_schedule(instanca, smjene, dani)
        prikazi_rezultate(f"Instanca sa {velicina} zaposlenih", lp_rez, greedy_rez)

if __name__ == "__main__":
    main()