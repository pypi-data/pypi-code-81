from analysis.manifold import MDSManifoldFactory, UMAPManifoldFactory
from .composers.mds_page_composer import MdsPageComposer
from .composers.pie_page_composer import PiePageComposer
from .composers.first_page_composer import FirstPageComposer
from time import localtime, strftime
import warnings
import matplotlib
matplotlib.use('Agg')
warnings.filterwarnings("ignore")


class Rendering:
    def __init__(self, tool_name):
        self.time = strftime("%a, %d %b %Y %H:%M:%S %Z", localtime())
        self.tool_name = tool_name

    def render(self, annotation, title, seed, mds_scatter_plot,
               umap_scatter_plot, ordered_group_names, rescale_heatmap=False):
        matrix = annotation.get_matrix()

        composers = [FirstPageComposer(
            annotation, title, ordered_group_names, rescale_heatmap)]

        for group_name in ordered_group_names:
            composers.append(PiePageComposer(annotation, title, group_name))

        if mds_scatter_plot:
            p_matrix = MDSManifoldFactory(seed).make().fit_transform(
                matrix.to_distance().get_matrix())
            if len(p_matrix) != len(matrix.get_file_names()):
                raise Exception("Ops! Something is went wrong with the MDS.")

            for group_name in ordered_group_names:
                composers.append(MdsPageComposer(
                    p_matrix, annotation, group_name, title, "MDS"))

        if umap_scatter_plot:
            p_matrix = UMAPManifoldFactory(seed).make().fit_transform(
                matrix.to_distance().get_matrix())
            if len(p_matrix) != len(matrix.get_file_names()):
                raise Exception("Ops! Something is went wrong with the UMAP.")

            for group_name in ordered_group_names:
                composers.append(MdsPageComposer(
                    p_matrix, annotation, group_name, title, "UMAP"))

        return [composers[i].run(self.make_left_lower_page(),
                                 self.make_rigth_lower_page(i + 1))
                for i in range(len(composers))]

    def make_left_lower_page(self):
        return self.time + '; ' + self.tool_name

    def make_rigth_lower_page(self, page_number):
        return 'Page ' + str(page_number)
