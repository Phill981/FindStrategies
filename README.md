# MarkovTransitionStates

This is a small project to test out streamit and learn about transition matrecies for financial markets

## Running
 
To run the program, first run

> chmod +x run.sh

> ./run.sh

This will create a list of all requirements and install them if they are not installed yet.
Afterwards it starts the streamlit server.

## Strategies

### TransitionStates

This strategies works by expecting, that after a period of bad or good days, the chance
of the opposit will be happending. For this we define a transition matrix as of the following:

|      | up | down |    |   
|------|----|------|----|
| up   |x_11| x_12 | =1 |   
| down |x_21| x_22 | =1 |   

from this matrix we get the chance of a value going from up to up, down to down etc...

By now determining the current phase and seeing how many positive or negative days in a row a company has, we  get the average movement after such days and decide if we want to take them.

As a result we get a table looking like this:
| index | ticker | call | price goal | current price | probability |
|-------|--------|------|------------|---------------|-------------|
|       |        |      |            |               |             |


### more strategies to come...