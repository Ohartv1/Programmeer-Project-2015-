Programmeer-Project-2015
=======

Ontwerpvoorstel
-------

**Probleemstelling**

Hoe verhoudt het eerste artikel wat ik ga lezen voor een essay zich tot de rest?


**Hoe zal de interface eruit zien?**

Statisch:
Een artikel zal als uitgangspunt centraal worden weergegeven in een verticale Arc-diagram. De titles van de artikelen
staan onder elkaar en kunnen per cluster gekleurd worden. Boven het artikel van uitgangspunt zullen de artikelen staan
die het artikel refereren met de arcen rechts, onder het artikel van uitgangspunt de artikelen die het artikel citeerd
met de arcen links.

Dynamisch:
De volgorde kan worden gesorteerd aan de hand van het aantal citaties, cluster of alfabetisch.
Door het selecteren van een perifeer artikelen zal de positie worden overgenomen van het centrale uitgangspunt. 


**Data bron**

De data wordt gescraped van PsyInfo en worden omgezet in een lijst van dictionaries per artikel. 

[{Title: ,Doi: ,Referenced: ,Cited: }, {...}]


**Project onderdelen**

Het project kan worden in de volgende onderdelen:
* Data verzameling
* Inplementatie:
    * Statisch deel:
        * Verticaal Arc-diagram
        * Cluster kleuring
    * Dynamisch deel:
        * Sorteren:
            * Aantal citatie
            * Cluster
            * Alfabetisch
        * Herladen na wisseling van uitgangs artikel
  
        
**Potenciele obstakels**

Mogelijk komt er een artikel voor met teveel citaties dan de visulatisatie aan kan. Er zal een beperking moeten 
worden gesteld zodanig dat de probleemstelling beantwoord blijft.


**gelijksoortige visualisaties**

In de eigenfactor visualisatie worden de relaties van publicaties in verschillende tijdschriften weergegeven.
http://well-formed.eigenfactor.org/radial.html

De visualisaties van web of science zijn opbasis van relaties van auteurs.
http://webofscience.com


    


