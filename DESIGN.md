Technisch Ontwerp
=======


**Ontwerp**  
  
minimaal: de verticale arc-diagram, tooltip met artikel informatie.

aanvullingen: sortering van de artikelen, generatie, aantal citaties, clusters, alfabetisch.

![interface schets] (/DOCS/arc-diagram.PNG)  

**objecten en functies**  
scraper:  

    object: artikel; titel, doi, link naar citaties, citaties, link naar geciteerd door, geciteerd door.
  
    functies: scrape; krijgt een url en returnt een artikel.
              crawl; recursief, krijgt een lijst met artikelen returnt een lijst met artikelen.
              cited_by; krijgt een url, returnt een lijst met url's van artikelen.
              referenced; krijgt een url, returnt een lijst met url's van artikelen.
              write; krijgt een lijst met artikelen en schrijft een json bestand.
              
visualisation:
d3  
  
