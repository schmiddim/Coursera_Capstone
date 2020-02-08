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

## How data will be used to solve the problem
1. I will declare some cities with
    - a negative Score
    - a neutral Score
    - a positive Score
  to define the boundaries.
2. I will group venue types (hotels, restaurants,souvenir shops, ... ) to categories that affect the touristy score. 
  This will be set in a relation to the population density of the city. 

3. Now I can use the scores from point 1. and the numbers from point 2. to label cities with the scoring value. 




  

