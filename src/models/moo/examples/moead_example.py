import time

from pymoo.algorithms.moo.moead import MOEAD
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination, get_problem, \
    get_reference_directions
from pymoo.optimize import minimize

from src.models.moo.utils.indicators import get_hypervolume
from src.models.moo.utils.plot import plot_multiple_pop
from src.utils.plot.plot import plot_hist_hv
from src.utils.util import get_type_str

if __name__ == '__main__':

    prob_cfg = {'name': 'wfg2', 'n_obj': 3, 'n_variables': 10, 'hv_ref': [5, 5, 5], 'bounds_low': 0, 'bounds_up': 1}
    algo_cfg = {'termination': ('n_gen', 100), 'max_gen': 150, 'pop_size': 100}
    save_plots = False
    problem = get_problem(prob_cfg['name'], n_var=prob_cfg['n_variables'], n_obj=prob_cfg['n_obj'])

    # create the reference directions of size equal to population size
    ref_dirs = get_reference_directions("energy", 3, algo_cfg['pop_size'])

    algorithm = MOEAD(
        sampling=get_sampling("real_random"),
        crossover=get_crossover("real_sbx", prob=0.9, eta=15),
        mutation=get_mutation("real_pm", eta=20),
        ref_dirs=ref_dirs,
        n_neighbors=15,
        prob_neighbor_mating=0.7,
    )

    algo_cfg['name'] = get_type_str(algorithm)
    termination = get_termination(algo_cfg['termination'][0], algo_cfg['termination'][1])

    t0 = time.time()
    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=True)
    print('Algorithm finished in {}s'.format(round(time.time() - t0, 4)))

    # %%
    # Plotting hypervolume
    plot_hist_hv(res)

    # Plot Optimum Solutions
    pop_hist = [gen.pop.get('F') for gen in res.history]
    plot_multiple_pop([pop_hist[-1], res.opt.get('F')], labels=['population', 'optimum'], save=save_plots,
                      opacities=[.2, 1], plot_border=True, file_path=['img', 'opt_deap_res'],
                      title=prob_cfg['name']+' Optimum Solutions' + '<br>CFG: ' + str(algo_cfg))

    #%%
    hv_pop = get_hypervolume(pop_hist[-1], prob_cfg['hv_ref'])
    hv_opt = get_hypervolume(res.opt.get('F'), prob_cfg['hv_ref'])
    print('Hypervolume from all population for reference point {}: {}'.format(str(prob_cfg['hv_ref']), round(hv_pop, 4)))
    print('Hypervolume from opt population for reference point {}: {}'.format(str(prob_cfg['hv_ref']), round(hv_opt, 4)))
    print('Optimum population {}/{}'.format(len(res.opt), len(pop_hist[-1]) ))