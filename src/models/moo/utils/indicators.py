import numpy as np
from deap import tools
from deap.tools._hypervolume import hv
from pymoo.factory import get_performance_indicator

from src.models.moo.deap.utils import get_deap_pops_obj, get_pymoo_pops_obj
from src.models.moo.utils.plot import get_fitnesses


def hypervolume(individuals, ref=None):
    # front = tools.sortLogNondominated(individuals, len(individuals), first_front_only=True)
    wobjs = np.array([ind.fitness.wvalues for ind in individuals]) * -1
    if ref is None:
        ref = np.max(wobjs, axis=0) #+ 1
    return hv.hypervolume(wobjs, ref)

def get_hypervolume(pop):
    F = pop if isinstance(pop, np.ndarray) else get_fitnesses(pop)
    ref = np.max(F, axis=0)
    hv = get_performance_indicator("hv", ref_point=ref)
    hypervol = hv.calc(F)
    return hypervol

def get_hvs_from_log(hist, lib='deap'):
    pops_obj, ref = get_deap_pops_obj(hist) if lib == 'deap' else get_pymoo_pops_obj(hist)
    hv = get_performance_indicator("hv", ref_point=ref)
    hypervols = [hv.calc(pop_obj) for pop_obj in pops_obj]
    return hypervols