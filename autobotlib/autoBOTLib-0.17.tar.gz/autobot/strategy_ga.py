"""
This is the main GA underlying AutoBOT approach.
This file contains, without warranty, the code that performs the optimization.
It includes both iterative deepening, as well as the GA discussed in the paper.
Made by Blaz Skrlj, Lubljana 2020, Jozef Stefan Institute
All rights reserved.
"""

## some generic logging
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

## evolution helpers
from deap import base, creator, tools
import operator

## feature space construction
import random
from feature_constructors import *
from metrics import *
from collections import defaultdict
from scipy import sparse

## modeling
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV

## monitoring
import tqdm
import numpy as np
import itertools
import time

## more efficient computation
import multiprocessing as mp

## omit some redundant warnings
from warnings import simplefilter
simplefilter(action='ignore')

## relevant for visualization purposes, otherwise can be omitted.
try:
    import matplotlib.pyplot as plt
    import networkx as nx
    from networkx.drawing.nx_agraph import write_dot, graphviz_layout
    logging.info("Visualization libraries were found (NetworkX, MPL).")

except:
    logging.info("For full visualization, Networkx and Matplotlib are needed!")


class GAlearner:
    """
    The core GA class. It includes methods for evolution of a learner assembly.
    Each instance of autoBOT must be first instantiated.
    In general, the workflow for working with this class is as follows:
    1.) Instantiate the class
    2.) Evolve
    3.) Predict
    """
    def __init__(self,
                 train_sequences_raw,
                 train_targets,
                 time_constraint,
                 num_cpu=6,
                 task_name="update:",
                 hof_size=3,
                 top_k_importances=10,
                 representation_type="neurosymbolic",
                 heterogeneous_ensemble="yes",
                 binarize_importances=False,
                 memory_storage="memory/conceptnet.txt.gz"):

        logging.info("Instantiated the evolution-based learner.")
        self.representation_type = representation_type
        self.binarize_importances = binarize_importances

        ## parallelism settings
        if num_cpu == "all":
            self.num_cpu = mp.cpu_count()
        else:
            self.num_cpu = num_cpu

        self.task = task_name
        self.topk = top_k_importances

        if heterogeneous_ensemble == "yes" or heterogeneous_ensemble == "true":
            self.heterogeneous_ensemble = True

        train_sequences = []

        ## Do some mandatory encoding
        for sequence in train_sequences_raw.values:
            train_sequences.append(sequence.encode("utf-8").decode("utf-8"))

        ## build dataframe
        self.train_seq = self.return_dataframe_from_text(train_sequences)
        self.train_targets = train_targets

        ## names of the considered features
        symbolic_feature_names = [
            "word_features", "char_features", "pos_features",
            "relational_features", "keyword_features", "concept_features"
        ]

        neural_feature_names = ["neural_distributed_memory", "neural_dbow"]

        if self.representation_type == "neurosymbolic":
            self.feature_names = symbolic_feature_names + neural_feature_names

        elif self.representation_type == "symbolic":
            self.feature_names = symbolic_feature_names

        else:
            self.feature_names = neural_feature_names

        logging.info("Considering {}".format(self.feature_names))
        self.hof = []
        self.memory_storage = memory_storage
        self.neural_features = len(neural_feature_names)
        self.population = None  ## this object gets evolved

        ## establish constraints
        self.max_time = time_constraint
        self.unique_labels = len(set(train_targets))
        self.initial_time = None
        self.subspace_feature_names = None
        self.ensemble_of_learners = []
        self.performance_reports = []
        self.n_fold_cv = 5

        logging.info(
            "Initiating the seed vectorizer instance and initial feature space .."
        )

        ## hyperparameter space. Parameters correspond to weights of subspaces, as well as subsets + regularization of LR.

        self.weight_params = len(self.feature_names)
        self.total_params = self.weight_params

        ## other hyperparameters
        self.hof_size = hof_size  ## size of the hall of fame.

        if self.hof_size % 2 == 0:
            logging.info(
                "HOF size must be odd, adding one member ({}).".format(
                    self.hof_size))
            self.hof_size += 1

        self.fitness_container = []  ## store fitness across evalution

        ## stats
        self.feature_importances = []
        self.fitness_max_trace = []
        self.fitness_mean_trace = []
        self.feat_min_trace = []
        self.feat_mean_trace = []
        self.opt_population = None

        logging.info(
            "Loaded a dataset of {} texts with {} unique labels.".format(
                self.train_seq.shape[0], len(set(train_targets))))

    def update_global_feature_importances(self):
        """
        Aggregate feature importances across top learners.
        """

        fdict = {}
        self.sparsity_coef = []

        ## get an indicator of global feature space and re-map.
        global_fmaps = defaultdict(list)
        for enx, importance_tuple in enumerate(self.feature_importances):
            subspace_features = importance_tuple[1]
            coefficients = importance_tuple[0]
            assert len(subspace_features) == len(coefficients)
            sparsity_coef = np.count_nonzero(coefficients) / len(coefficients)
            self.sparsity_coef.append(sparsity_coef)
            logging.info("Importance (learner {}) sparsity of {}".format(
                enx, sparsity_coef))
            for fx, coef in zip(subspace_features, coefficients):
                space_of_the_feature = self.global_feature_name_hash[fx]
                if not fx in fdict:
                    fdict[fx] = np.abs(coef)
                else:
                    fdict[fx] += np.abs(coef)
                global_fmaps[space_of_the_feature].append((fx, coef))
        self.global_feature_map = {}
        for k, v in global_fmaps.items():
            tmp = {}
            for a, b in v:
                tmp[a] = round(b, 2)
            mask = ["x"] * self.topk
            top5 = [
                " : ".join([str(y) for y in x]) for x in sorted(
                    tmp.items(), key=operator.itemgetter(1), reverse=True)
            ][0:self.topk]
            mask[0:len(top5)] = top5
            self.global_feature_map[k] = mask
        self.global_feature_map = pd.DataFrame(self.global_feature_map)
        self.sparsity_coef = np.mean(self.sparsity_coef)
        self._feature_importances = sorted(fdict.items(),
                                           key=operator.itemgetter(1),
                                           reverse=True)
        logging.info(
            "Feature importances can be accessed by ._feature_importances")

    def compute_time_diff(self):
        """
        A method for time monitoring.
        """

        return ((time.time() - self.initial_time) / 60) / 60

    def parallelize_dataframe(self, df, func):
        """
        A method for parallel traversal of a given dataframe.
        param: dataframe of text (Pandas object)
        param: function to be executed (a function)
        """

        logging.info("Computing the seed dataframe ..")

        ## Do a pre-split of the data and compute in parallel.
        df_split = np.array_split(df, self.num_cpu * 10)
        pool = mp.Pool(self.num_cpu)
        df = pd.concat(
            tqdm.tqdm(pool.imap(func, df_split), total=len(df_split)))

        pool.close()
        pool.join()

        return df

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x.
        param: x (vector of floats)
        """

        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def return_dataframe_from_text(self, text):
        """
        A helper method that returns a given dataframe from text.
        param: list of texts
        """

        return self.parallelize_dataframe(text, build_dataframe)

    def generate_random_initial_state(self, weights_importances):
        """
        The initialization method, capable of generation of individuals.
        """

        weights = np.random.uniform(low=0.6, high=1,
                                    size=self.total_params).tolist()
        weights[0:len(weights_importances)] = weights_importances
        generic_individual = np.array(weights)

        assert len(generic_individual) == self.total_params
        return generic_individual

    def custom_initialization(self):
        """
        Custom initialization employs random uniform prior.
        """
        #self.feature_subspaces
        logging.info("Performing initial screening on {} subspaces.".format(
            len(self.feature_subspaces)))

        performances = []
        for subspace, name in zip(self.feature_subspaces, self.feature_names):
            f1, _ = self.cross_val_scores(subspace, n_cpu=self.num_cpu)
            performances.append(f1)

        pairs = [
            " -- ".join([str(y) for y in x])
            for x in list(zip(self.feature_names, performances))
        ]

        print("Initial screening report:")
        print("\n".join(pairs))

        weights = np.array(performances) / max(performances)
        generic_individual = self.generate_random_initial_state(weights)
        assert len(generic_individual) == self.total_params
        for ind in self.population:
            noise = np.random.uniform(low=0.95,
                                      high=1.05,
                                      size=self.total_params)
            generic_individual = generic_individual * noise
            ind[:] = np.abs(generic_individual)

    def apply_weights(self,
                      parameters,
                      custom_feature_space=False,
                      custom_feature_matrix=None):
        """
        This method applies weights to individual parts of the feature space.
        :param parameters: a vector of real-valued parameters - solution = an individual
        :param custom_feature_space: Custom feature space, relevant during making of predictions.
        """

        ## Compute cumulative sum across number of features per feature type.
        indices = self.intermediary_indices

        ## Copy the space as it will be subsetted.
        if not custom_feature_space:
            tmp_space = sparse.csr_matrix(self.train_feature_space.copy())
        else:
            tmp_space = sparse.csr_matrix(custom_feature_matrix)

        indices_pairs = []
        assert len(indices) == self.weight_params + 1

        for k in range(self.weight_params):
            i1 = indices[k]
            i2 = indices[k + 1]
            indices_pairs.append((i1, i2))

        ## subset the core feature matrix -- only consider non-neural features for this.
        for j, pair in enumerate(indices_pairs):
            tmp_space[:,
                      pair[0]:pair[1]] = tmp_space[:,
                                                   pair[0]:pair[1]].multiply(
                                                       parameters[j])

        return tmp_space

    def cross_val_scores(self, tmp_feature_space, final_run=False, n_cpu=None):

        if final_run:
            ## we can afford this final round to be more rigorous.
            parameters = {
                "loss": ["hinge", "log"],
                "penalty": ["elasticnet"],
                "alpha": [0.01, 0.001, 0.0001, 0.0005],
                "l1_ratio": [0.05, 0.25, 0.3, 0.6, 0.8, 0.95]
            }

        else:
            ## this is for screening purposes.
            parameters = {
                "loss": ["hinge", "log"],
                "penalty": ["elasticnet"],
                "alpha": [0.01, 0.001, 0.0001],
                "l1_ratio": [0.1, 0.5, 0.9]
            }

        svc = SGDClassifier()

        if self.unique_labels > 2:
            f1_scoring = "f1_macro"

        else:
            f1_scoring = "f1"

        if final_run:
            clf = GridSearchCV(svc,
                               parameters,
                               verbose=1,
                               n_jobs=self.num_cpu,
                               cv=10,
                               scoring=f1_scoring,
                               refit=True)

        else:
            clf = GridSearchCV(svc,
                               parameters,
                               verbose=1,
                               n_jobs=self.num_cpu,
                               cv=self.n_fold_cv,
                               scoring=f1_scoring,
                               refit=False)

        clf.fit(tmp_feature_space, self.train_targets)
        f1_perf = max(clf.cv_results_['mean_test_score'])

        if final_run:
            report = clf.cv_results_
            clf = clf.best_estimator_
            return f1_perf, clf, report

        return f1_perf, clf

    def evaluate_fitness(self,
                         individual,
                         max_num_feat=1000,
                         return_clf_and_vec=False):
        """
        A helper method for evaluating an individual solution. Given a real-valued vector, this constructs the representations and evaluates a given learner.
        :param individual: an individual (solution)
        :param max_num_feat: maximum number of features that are outputted
        :param return_clf_and_vec: return classifier and vectorizer? This is useful for deployment.
        """
        individual = np.array(individual)
        if np.sum(individual[:]) > self.total_params:
            return (0, )

        if (np.array(individual) <= 0).any():
            individual[(individual < 0)] = 0

        if self.binarize_importances:
            for k in range(len(self.feature_names)):
                weight = individual[k]
                if weight > 0.5:
                    individual[k] = 1
                else:
                    individual[k] = 0

        if self.vectorizer:

            tmp_feature_space = self.apply_weights(individual[:])
            feature_names = self.all_feature_names

            ## Return the trained classifier.
            if return_clf_and_vec:

                ## fine tune final learner
                logging.info("Final round of optimization.")
                f1_perf, clf, report = self.cross_val_scores(tmp_feature_space,
                                                             final_run=True)
                return clf, individual[:], f1_perf, feature_names, report

            f1_perf, _ = self.cross_val_scores(tmp_feature_space)
            return (f1_perf, )

        elif return_clf_and_vec:
            return (0, )

        else:
            return (0, )

    def generate_and_update_stats(self, fits):
        """
        A helper method for generating stats.
        :param fits: fitness values of the current population
        """

        f1_scores = []

        for fit in fits:

            f1_scores.append(fit)

        return np.mean(f1_scores)

    def report_performance(self, fits, gen=0):
        """
        A helper method for performance reports.
        :param fits: fitness values (vector of floats)
        :param gen: generation to be reported (int)
        """

        f1_top = self.generate_and_update_stats(fits)
        logging.info(r"{} (gen {}) F1: {}, time: {}min".format(
            self.task, gen, np.round(f1_top, 3),
            np.round(self.compute_time_diff(), 2) * 60))
        return f1_top

    def get_feature_space(self):
        """
        Extract final feature space considered for learning purposes.
        """
        transformed_instances, feature_indices = self.apply_weights(
            self.hof[0][1:])
        assert transformed_instances.shape[0] == len(self.train_targets)
        return (transformed_instances, self.train_targets)

    def predict(self, instances):
        """
        Predict on new instances. Note that the prediction is actually a maxvote across the hall-of-fame.
        :param instances: predict labels for new instances = texts.
        """

        logging.info("Obtaining final predictions from {} models.".format(
            len(self.ensemble_of_learners)))

        if not self.ensemble_of_learners:
            logging.info("Please, evolve the model first!")
            return None

        else:

            instances = self.return_dataframe_from_text(instances)
            transformed_instances = self.vectorizer.transform(instances)
            prediction_space = []
            # transformed_instances = self.update_intermediary_feature_space(custom_space = transformed_instances)
            logging.info("Representation obtained ..")
            for learner_tuple in self.ensemble_of_learners:

                try:

                    ## get the solution.
                    learner, individual, score = learner_tuple

                    ## Subset the matrix.
                    subsetted_space = self.apply_weights(
                        individual,
                        custom_feature_space=True,
                        custom_feature_matrix=transformed_instances)

                    ## obtain the predictions.
                    if not prediction_space is None:
                        prediction_space.append(
                            learner.predict(subsetted_space).tolist())

                    else:
                        prediction_space.append(
                            learner.predict(subsetted_space).tolist())

                except Exception as es:
                    print(
                        es,
                        "Please, re-check the data you are predicting from!")

            ## generate the prediction matrix by maximum voting scheme.
            pspace = np.matrix(prediction_space).T
            all_predictions = pd.DataFrame(pspace).mode(
                axis=1).values.reshape(-1)
            logging.info("Predictions obtained")
            return all_predictions

    def generate_id_intervals(self):
        """
        Generate independent intervals.
        """

        reg_range = [0.1, 1, 10, 100]
        self.total_params
        ks = [2]
        for k in ks:
            if k == 2:

                interval = [0, 1]
                layer_combs = list(
                    itertools.product(interval, repeat=self.total_params - 1))

                random.shuffle(layer_combs)
                logging.info(
                    "Ready to evaluate {} solutions at resolution: {}".format(
                        len(layer_combs) * len(reg_range), k))

                for comb in layer_combs:
                    for reg_val in reg_range:
                        otpt = np.array([reg_val] + list(comb))
                        yield otpt

    def get_feature_importance_report(self, individual, fitnesses):
        """
        Report feature importances.
        :param individual: an individual solution (a vector of floats)
        :param fitnesses: fitness space (list of reals)
        """

        f1_scores = []

        if self.binarize_importances:
            for k in range(len(self.feature_names)):
                weight = individual[k]
                if weight > 0.5:
                    individual[k] = 1
                else:
                    individual[k] = 0

        for fit in fitnesses:
            f1_scores.append(fit[0])

        try:
            max_f1 = np.max(f1_scores)
        except:
            max_f1 = 0

        try:
            importances = list(
                zip(self.feature_names,
                    individual[0:self.weight_params].tolist()))

        except:
            importances = list(
                zip(self.feature_names, individual[0:self.weight_params]))

        report = ["-" * 60, "|| Feature type   Importance ||", "-" * 60]
        cnt = -1

        for fn, imp in importances:
            cnt += 1
            if len(str(fn)) < 17:
                fn = str(fn) + (17 - len(str(fn))) * " "
            report.append(str(fn) + "  " + str(np.round(imp, 2)))

        report.append("-" * 60)
        report.append("Max F1: {}".format(max_f1))

        print("\n".join(report))

    def mutReg(self, individual, p=1):
        """
        Custom mutation operator used for regularization optimization.
        :param individual: individual (vector of floats)
        """

        individual[0] += random.random() * self.reg_constant
        return individual,

    def update_intermediary_feature_space(self, custom_space=None):
        """
        Create the subset of the origin feature space based on the starting_feature_numbers vector that gets evolved.
        """

        index_pairs = []
        for enx in range(len(self.initial_indices) - 1):
            diff1 = self.initial_indices[enx + 1] - self.initial_indices[enx]

            prop_diff = diff1
            i1 = int(self.initial_indices[enx])
            i2 = int(self.initial_indices[enx] + prop_diff)
            index_pairs.append((i1, i2))

        submatrices = []
        assert len(self.feature_names) == len(index_pairs)

        if not custom_space is None:
            considered_space = custom_space

        else:
            considered_space = self.train_feature_space

        fnames = []
        assert len(index_pairs) == len(self.feature_names)
        self.intermediary_indices = []

        for enx, el in enumerate(index_pairs):
            mx = considered_space[:, el[0]:el[1]]
            self.intermediary_indices.append(mx.shape[1])
            fnames += self.global_all_feature_names[el[0]:el[1]]
            submatrices.append(sparse.csr_matrix(mx))

        self.intermediary_indices = [0] + np.cumsum(
            self.intermediary_indices).tolist()
        assert len(submatrices) == len(self.feature_names)
        self.all_feature_names = fnames  ## this is the new set of features.
        output_matrix = sparse.hstack(submatrices).tocsr()
        logging.info("Space update finished. {}, {} matrices joined.".format(
            output_matrix.shape, len(submatrices)))
        assert len(self.all_feature_names) == output_matrix.shape[1]

        if not custom_space is None:
            return output_matrix

        else:
            self.intermediary_feature_space = output_matrix

        del submatrices

    def instantiate_validation_env(self):
        """
        This method refreshes the feature space. This is needed to maximize efficiency.
        """

        self.vectorizer, self.feature_names, self.train_feature_space = get_features(
            self.train_seq,
            representation_type=self.representation_type,
            targets=self.train_targets,
            memory_location=self.memory_storage)

        self.all_feature_names = []
        logging.info("Initialized training matrix of dimension {}".format(
            self.train_feature_space.shape))

        self.feature_space_tuples = []
        self.global_feature_name_hash = {}

        ## This information is used to efficiently subset and index the sparse representation
        self.feature_subspaces = []
        current_fnum = 0
        for transformer in self.vectorizer.named_steps[
                'union'].transformer_list:
            features = transformer[1].steps[1][1].get_feature_names()
            self.feature_subspaces.append(
                self.train_feature_space[:, current_fnum:(current_fnum +
                                                          len(features))])
            current_fnum += len(features)
            self.all_feature_names += features
            num_feat = len(features)
            for f in features:
                self.global_feature_name_hash[f] = transformer[0]
            self.feature_space_tuples.append((transformer[0], num_feat))

        self.global_all_feature_names = self.all_feature_names
        self.intermediary_indices = [0] + np.cumsum(
            np.array([x[1] for x in self.feature_space_tuples])).tolist()

    def visualize_genealogy(self, toolbox=None, path="../figures/evol.pdf"):
        """
        A generic method for visualization of fitness across population history.
        :param toolbox: an evolution toolbox (see Deap lib)
        """

        if not toolbox:
            toolbox = self.toolbox

        logging.info("Visualizing genealogy tree.")
        graph = nx.DiGraph(self.history.genealogy_tree)
        logging.info(nx.info(graph))
        graph = graph.reverse()
        logging.info("Evaluation in progress ..")
        colors = []
        for i in tqdm.tqdm(graph):
            colors.append(
                toolbox.evaluate(self.history.genealogy_history[i])[0])
        logging.info("Drawing ..")
        write_dot(graph, 'test.dot')

        # same layout using matplotlib with no labels
        plt.title('draw_networkx')
        pos = graphviz_layout(graph, prog='dot')
        nx.draw(graph, pos, with_labels=False, arrows=True)
        plt.savefig('nx_test.png')

        #        g = nx.draw(graph, node_color=colors)
        plt.tight_layout()
        plt.savefig(path, dpi=300)

    def evolve(self,
               nind=100,
               crossover_proba=0.4,
               mutpb=0.15,
               stopping_interval=10,
               strategy="evolution",
               validation_type="cv"):
        """
        The core evolution method. First constrain the maximum number of features to be taken into account by lowering the bound w.r.t performance.
        next, evolve.
        :param nind: number of individuals (int)
        :param crossover_proba: crossover probability (float)
        :param mutpb: mutation probability (float)
        :param stopping_interval: stopping interval -> for how long no improvement is tolerated before a hard reset (int)
        :param strategy: type of evolution (str)
        :param validation_type: type of validation, either train_val or cv (cross validation or train-val split)
        """

        self.validation_type = validation_type
        self.initial_time = time.time()
        self.popsize = nind

        logging.info("Evolution will last for ~{}h ..".format(self.max_time))

        ## if iterative deepening strategy is selected the following piece is executed

        logging.info("Selected strategy is evolution.")
        self.history = tools.History()

        creator.create("FitnessMulti", base.Fitness, weights=(1.0, ))
        creator.create("Individual", list, fitness=creator.FitnessMulti)
        toolbox = base.Toolbox()

        logging.info("Total number of parameters {}".format(self.total_params))

        toolbox.register("attr_float", random.uniform, 0.00001, 0.999999)
        toolbox.register("individual",
                         tools.initRepeat,
                         creator.Individual,
                         toolbox.attr_float,
                         n=self.total_params)
        toolbox.register("population",
                         tools.initRepeat,
                         list,
                         toolbox.individual,
                         n=nind)
        toolbox.register("evaluate", self.evaluate_fitness)
        toolbox.register("mate", tools.cxUniform, indpb=0.5)
        toolbox.register("mutate",
                         tools.mutGaussian,
                         mu=0,
                         sigma=0.2,
                         indpb=0.2)
        toolbox.register("mutReg", self.mutReg)
        toolbox.decorate("mate", self.history.decorator)
        toolbox.decorate("mutate", self.history.decorator)
        toolbox.register("select", tools.selTournament)

        ## Keep the best-performing individuals
        self.hof = tools.HallOfFame(self.hof_size)
        self.instantiate_validation_env()

        ## Parallel execution part
        #pool = mp.Pool(processes=self.num_cpu)
        #toolbox.register("map", pool.map)

        ## Population initialization
        if self.population == None:

            self.population = toolbox.population()
            self.custom_initialization()  ## works on self.population
            logging.info("Initialized population of size {}".format(
                len(self.population)))
            logging.info("Computing initial fitness ..")

        ## Gather fitness values.
        fits = list(map(toolbox.evaluate, self.population))

        for fit, ind in zip(fits, self.population):
            ind.fitness.values = fit

        self.report_performance(fits)
        self.hof.update(self.population)
        gen = 0
        logging.info("Initiating evaluation ..")

        stopping = 1
        cf1 = 0

        ## Start the evolution.
        while True:

            gen += 1
            tdiff = self.compute_time_diff()

            if tdiff >= self.max_time:
                break

            offspring = list(map(toolbox.clone, self.population))

            ## Perform crossover
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                if random.random() < crossover_proba:

                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            ## Perform mutation
            for mutant in offspring:

                if random.random() < mutpb:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            fits = list(map(toolbox.evaluate, offspring))
            for ind, fit in zip(offspring, fits):
                if isinstance(fit, int) and not isinstance(fit, tuple):
                    fit = (fit, )
                ind.fitness.values = fit

            self.hof.update(offspring)

            ## append to overall fitness container.
            self.fitness_container.append(fits)

            self.get_feature_importance_report(self.hof[0], fits)

            f1 = self.report_performance(fits, gen=gen)

            if f1 == cf1:
                stopping += 1

            else:
                cf1 = f1

            self.population = toolbox.select(self.population + offspring,
                                             k=len(self.population),
                                             tournsize=int(nind / 3))
            self.history.update(self.population)

        try:
            selections = self.hof

        except:
            selections = self.population

        self.selections = [np.array(x).tolist() for x in selections]
        self.toolbox = toolbox

        ## Ensemble of learners is finally filled and used for prediction.
        for enx, top_individual in enumerate(selections):

            if len(top_individual) == 1:
                top_individual = top_individual[0]

            try:
                learner, individual, score, feature_names, report = self.evaluate_fitness(
                    top_individual, return_clf_and_vec=True)
                self.performance_reports.append(report)

            except Exception as es:
                logging.info(
                    "Evaluation did not produce any viable learners. Increase time!",
                    es)

            coefficients = learner.coef_

            ## coefficients are given for each class. We take maximum one (abs val)
            coefficients = np.asarray(np.abs(np.max(coefficients,
                                                    axis=0))).reshape(-1)
            # assert len(coefficients) == len(feature_names)

            logging.info("Coefficients and indices: {}".format(
                len(coefficients)))
            logging.info(
                "Adding importances of shape {} for learner {} with score {}".
                format(coefficients.shape, enx, score))

            self.feature_importances.append((coefficients, feature_names))

            single_learner = (learner, individual, score)
            self.ensemble_of_learners.append(single_learner)

        self.update_global_feature_importances()


#        self.visualize_genealogy()
