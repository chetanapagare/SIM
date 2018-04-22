
import collections
import random

import simpy


RANDOM_SEED = 42
TICKETS = 60  # Number of tickets per movie
SIM_TIME = 120  # Simulate until


def movie_viewer(env, movie, num_tickets, theater):
    
    with theater.counter.request() as turn_comes:
        # Wait until its our turn or until the movie is sold out
        result = yield turn_comes | theater.sold_out[movie]

        # Check if it's our turn of if movie is sold out
        if turn_comes not in result:
            theater.num_return[movie] += 1
            env.exit()

        # Check if enough tickets left.
        if theater.available[movie] < num_tickets:
            # movie_viewer leaves after some discussion
            yield env.timeout(0.5)
            env.exit()

        # Buy tickets
        theater.available[movie] -= num_tickets
        if theater.available[movie] < 2:
            # Trigger the "sold out" event for the movie
            theater.sold_out[movie].succeed()
            theater.when_sold_out[movie] = env.now
            theater.available[movie] = 0
        yield env.timeout(1)


def customer_arrivals(env, theater):
    """Create new *movie_viewers* until the sim time reaches 120."""
    while True:
        yield env.timeout(random.expovariate(1 / 0.5))

        movie = random.choice(theater.movies)
        num_tickets = random.randint(1, 6)
        if theater.available[movie]:
            env.process(movie_viewer(env, movie, num_tickets, theater))


Theater = collections.namedtuple('Theater', 'counter, movies, available, '
                                            'sold_out, when_sold_out, '
                                            'num_return')


# Setup and start the simulation
print('Housefull (no more tickets)')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Create movie theater
counter = simpy.Resource(env, capacity=1)
movies = ['Thor', 'Iron Man', 'Hulk','Black Panther']
available = {movie: TICKETS for movie in movies}
sold_out = {movie: env.event() for movie in movies}
when_sold_out = {movie: None for movie in movies}
num_return = {movie: 0 for movie in movies}
theater = Theater(counter, movies, available, sold_out, when_sold_out,
                  num_return)

# Start process and run
env.process(customer_arrivals(env, theater))
env.run(until=SIM_TIME)

# Analysis/results
for movie in movies:
    if theater.sold_out[movie]:
        print('Movie "%s" sold out %.1f minutes after ticket counter '
              'opening.' % (movie, theater.when_sold_out[movie]))
        print('  Number of people leaving queue when film sold out: %s' %
              theater.num_return[movie])
