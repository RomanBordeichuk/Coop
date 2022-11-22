Separation = 18 # length (in relative int) / separation
Acceleration = 1
StartVelocity = 0
MaxVelocity = 4
Probability = 0.8  # for city - 0.5; for highway - 0.8 Probability of accidentally stopping of car (1 - value)
StartPeriodLow = 10
StartPeriodHigh = 30
DelayForCarLow = 10 # lower bound for car's delay between the courses

DelayForCarHigh = 15 # higher bound for car's delay between the courses

ProbabilityOfEntertainment = 0.333 # probability of choosing entertainment facility 

PeriodStopFlow = 3 # Time for changing roads in Controller (TrafficLight)

IngnoringSupreme = 0.3 # Controller ignors the roads, which have K < value

Scale = 100000 # dangle (longitude) * Scale (the value is Scale)

ForbiddenHighways = ["cycleway", "construction", "busway", "motorway", "pedestrian", "track", "escape", "footway", "bridleway", "steps", "corridor", "path"]
NameCarsFile = "data/cars.json"
NameMapFile = "data/map.json"
NameOsmFile = "data/map_small.osm"