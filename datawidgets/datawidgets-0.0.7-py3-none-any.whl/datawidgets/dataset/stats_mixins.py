from datawidgets.imports import *
from datawidgets.utils import *
from datawidgets.data import *
from .image_dataset import *

from matplotlib.ticker import MaxNLocator


def compute_label_distribution(df: pd.DataFrame, label_col="label") -> pd.Series:
    "Computes the frequency of labels from a dataset's internal DataFrame"

    # NOTE: It's assumed that `all_labels` is a collection of lists
    all_labels = df[label_col].values
    all_labels = flatten(all_labels)

    return pd.Series(all_labels).value_counts().sort_index()


class LabelsStatsMixin:
    def setup_labels_stats(self):
        self.stats_output_area = widgets.Output()

    def plot_stats(self, df: pd.DataFrame, title: str = ""):
        self.stats_output_area.clear_output()
        with self.stats_output_area:
            vc = compute_label_distribution(df=df, label_col=self.label_col)
            if len(vc) < 10:
                figsize = (10, 5)
            elif len(vc) < 50:
                figsize = (10, 10)
            elif len(vc) < 100:
                figsize = (10, 20)
            else:
                figsize = (10, 25)
            try:
                fig, ax = plt.subplots(figsize=figsize, dpi=100)
                vc.plot(kind="barh", ax=ax)
                ax.set_xlabel("Frequency")
                ax.set_title(
                    f"{title} Distribution [{len(df)} Images; {vc.sum()} Tags]"
                )
                # Force x-axis to integer type
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))

                # Annotate bar with frequency of label
                for i, v in enumerate(vc.tolist()):
                    ax.text(
                        v + 0.02, i - 0.075, str(v), color="#859296", fontweight="bold"
                    )

                display(fig)
                plt.close()
            except:
                self.stats_output_area.clear_output()
                print("!! Nothing to plot !!")
                plt.close()

    def generate_refresh_stats_button(self, callbacks=[]) -> List[Button]:
        filt_button = Button(description="⟳ All Filtered Images")
        active_button = Button(description="⟳ Main Grid Images")
        review_button = Button(description="⟳ Review Images")
        total_button = Button(description="⟳ Full Dataset Images")
        selected_button = Button(description="⟳ Selected Images")

        total_button.on_click(
            lambda x: self.plot_stats(
                df=self.df,
                title="Total Images",
            )
        )
        filt_button.on_click(
            lambda x: self.plot_stats(
                df=self.filter_dataset(self.class_map_subset_filter),
                title="Filtered Images",
            )
        )
        selected_button.on_click(
            lambda x: self.plot_stats(
                df=self.filter_dataset(self.selected_names),
                title="Filtered Images",
            )
        )
        active_button.on_click(
            lambda x: self.plot_stats(
                df=self.filter_dataset(
                    [item.source for item in self.active_datapoints]
                ),
                title="Active (Viewable) Images",
            )
        )
        review_button.on_click(
            lambda x: self.plot_stats(
                df=self.filter_dataset(
                    [item.source for item in self.review_datapoints]
                ),
                title="Active (Viewable) Images",
            )
        )

        # Add callbacks
        for cb in callbacks:
            filt_button.on_click(cb)
            total_button.on_click(cb)

        active_button.layout.width = "180px"
        filt_button.layout.width = "210px"
        total_button.layout.width = "210px"
        selected_button.layout.width = "180px"
        review_button.layout.width = "180px"

        return total_button, filt_button, selected_button, active_button, review_button
