import torch as t
import tqdm as tqdm
from torch.multiprocessing import Pool
from torch.optim import Adam

from evostrat import compute_centered_ranks, CategoricalPopulation
from evostrat.examples.lunar_lander import LunarLander

if __name__ == '__main__':
    """
    Lunar landers weights and biases are all binary (-1.0 or 1.0) and drawn from learned categorical distributions. 
    """

    def constructor(params):
        values = t.tensor([-1.0, 1.0], dtype=t.float32)
        binary_params = {k: values[v] for k, v in params.items()}
        return LunarLander.from_params(binary_params)


    param_shapes = {k: v.shape + (2,) for k, v in LunarLander().get_params().items()}
    population = CategoricalPopulation(param_shapes, constructor)

    learning_rate = 0.1
    iterations = 1000
    pop_size = 200

    optim = Adam(population.parameters(), lr=learning_rate)
    pbar = tqdm.tqdm(range(iterations))
    pool = Pool()

    for _ in pbar:
        optim.zero_grad()
        raw_fit = population.fitness_grads(pop_size, pool, compute_centered_ranks)
        optim.step()
        pbar.set_description("fit avg: %0.3f, std: %0.3f" % (raw_fit.mean().item(), raw_fit.std().item()))
        if raw_fit.mean() > 200:
            print("Solved.")
            break

    pool.close()
