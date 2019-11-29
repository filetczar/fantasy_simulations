## Fantasy Football Simulations 

Ran 10,000 Monte Carlo Simulations to predict who will make the playoffs entering the final week of my fantasy football league. 


#### Methodology

Used a weighted average of weekly performances with more emphasis on recency plus expected points to score this week based on Yahoo's predictions. 

1) Average & Standard Deviation = .67 x Weighted Average + .33 x Weekly Predicion Points

2) Weighted Average = Weight*Points Scored

3) Weights = [.025, .025, .025, .08333, .08333, .08333, .08333, .08333, .08333, .14166, .14166, .14166]

Each matchup this week was simulated using a Monte Carlo simulation around a gaussian distribution for the Average and Standard Deviation. After each simulation, the league was ranked on wins and points scored to get a prediction of how the league will be seeded. 
 




