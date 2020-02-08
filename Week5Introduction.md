# Business Problem
If you travel to a foreign Country it is hard to determine if a city is worth a visit. 
Some cities have a lot of interesting sightseeing but they are also very crowdy and very touristy. 

**Positive** Examples for very touristy cities are:
- Venice
- Las Vegas
- Jerusalem

**Negatives**:

- Saarbrücken
- Bochum

**Neutral** (a little touristy)
- New York
- Amsterdam
- Munich
 

I want to create a System that can predict the touristic Score (from 0.0f to 1.0) for a City.  

## Assumption
Touristic Cities can be identified by features like the amount of restaurants, hotels in relation to the population density (Humans / km^2)


## Datasources
- I will use the Squarespace API to get Data about restaurants, hotels etc..
- Wikidata Query Service for population Data