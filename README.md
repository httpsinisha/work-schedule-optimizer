# work-schedule-optimizer
Projekat za planiranje radnog rasporeda koristeći linearno programiranje i pohlepne algoritme.

Model linearnog programiranja
Cilj je minimizovati ukupne troškove uz data ograničenja:
• Varijable:
xijk∈{0,1}: binarna varijabla koja označava je li zaposleni i dodijeljen
smjeni j na dan k.
• Ciljna funkcija:
Minimizovanje ∑𝑖∈𝑍 ∑𝑗∈𝑆 ∑𝑘∈𝐷 𝑐𝑖
⋅ 𝑡𝑗
⋅ 𝑥𝑖,𝑗,𝑘
• Ograničenja:
1. Pokrivenost smjena:
∑𝑥𝑖,𝑗,𝑘
𝑖∈𝑍
≥ 𝑝𝑗
, ∀𝑗 ∈ 𝑆, ∀𝑘 ∈ 𝐷
2. Maksimalno sati za zaposlenike:
∑∑ 𝑡𝑗
𝑗∈𝑆 𝑘∈𝐷
⋅ 𝑥𝑖,𝑗,𝑘 ≤ 𝑚𝑖
, ∀𝑖 ∈ 𝑍
3. Jedna smjena dnevno po zaposleniku:
∑𝑥𝑖,𝑗,𝑘
𝑗∈𝑆
≤ 1, ∀𝑖 ∈ 𝑍, ∀𝑘 ∈ 𝐷
4. Nedostupnost:
𝑥𝑖,𝑗,𝑘 ≤ 𝐷𝑖,𝑗,𝑘, ∀𝑖 ∈ 𝐼, ∀𝑗 ∈ 𝐽, ∀𝑘 ∈ �

Pohlepni algoritam
1. Sortiranje zaposlenika: Zaposlenici se sortiraju prema satnici (od najniže prema
najvišoj) i maksimalnom broju sati (od najvišeg prema najnižem). Cilj je prvo
dodijeliti smjene jeftinijim zaposlenicima koji mogu raditi više sati.
2. Sortiranje smjena: Smjene se sortiraju prema trajanju (od najduže prema
najkraćoj) kako bi se prvo pokušale pokriti najzahtjevnije smjene.
3. Dodjeljivanje smjena: Za svaki dan i svaku smjenu, algoritam prolazi kroz sortirane
zaposlenike i dodjeljuje smjene onima koji su dostupni, imaju dovoljno preostalih
sati i nisu već dodijeljeni u drugu smjenu tog dana.
4. Provjera pokrivenosti: Nakon dodjele, provjerava se jesu li sve smjene pokrivene s
potrebnim brojem radnika.
Neka je Z skup zaposlenika, S skup smjena i D skup dana.
Za svakog zaposlenog 𝑖 ∈ 𝑍 definišemo:
• 𝑐𝑖
: satnica
• 𝑚𝑖
: maksimalan broj sati
• 𝑁𝑖
: skup nedostupnih smjena
Za svaku smjenu 𝑗 ∈ 𝑆 definišemo:
• 𝑡𝑗
: trajanje smjene
• 𝑝𝑗
: potreban broj radnika
Algoritam dodjeljuje smjene tako da minimiyuje ukupne troškove 𝑍𝑖𝑗𝑘 𝑐𝑖
⋅ 𝑡𝑗
⋅ 𝑥𝑖,𝑗,𝑘
gdje je 𝑥𝑖,𝑗,𝑘 = 1 ako je zaposlenik i dodijeljen smjeni j na dan k, inače 0.

Testiranje LP-a I pohlepnog pristupa
![reyultatiii](https://github.com/user-attachments/assets/74122455-51c3-418c-a6cd-3c8a43d79395)

LP model pruža optimalna rješenja kada su ulazni podaci takvi da postoji
dopustivo rješenje. Kod većine testiranih instanci sa dovoljnim brojem zaposlenih
i realističnim ograničenjima (maksimalni broj sati, dostupnost), model linearnog
programiranja je uspio pronaći optimalnu dodjelu smjena.
Pohlepni algoritam je brz i efikasan i često pronalazi rješenja koja su blizu
optimalnim. U većini slučajeva koje smo ovde testirali razlika u ukupnim
troškovima u odnosu na LP rješenje iznosi manje od 5–10%, što ga čini korisnim za
velike instance gdje je vrijeme izvođenja važno.
