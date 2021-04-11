from datetime import datetime
from typing import Dict, List

from openapi_client import ProtoExperimentPlotMetric, ProtoExperimentPlotFile
from savvihub import ArgumentException
from savvihub.cli.commands.volume import volume_file_copy_local_to_remote
from savvihub.constants import SAVVIHUB_IMAGES, SAVVIHUB_PLOTS_FILETYPE_IMAGE


class History:
    def __init__(self, experiment):
        self.experiment = experiment
        self.rows = []
        self.images = []
        self._step = 0

    def validate_step(self, step):
        if step < 0 or step > self._step:
            return False
        return True

    def update_metrics(self, client, row):
        """
        Update row in history
        """
        plot_metrics: Dict[str, List[ProtoExperimentPlotMetric]] = {}
        for k, v in row.items():
            if k in plot_metrics:
                plot_metrics[k].append(ProtoExperimentPlotMetric(
                    step=self._step,
                    timestamp=datetime.utcnow().timestamp(),
                    value=float(v),
                ))
            else:
                plot_metrics[k] = [ProtoExperimentPlotMetric(
                    step=self._step,
                    timestamp=datetime.utcnow().timestamp(),
                    value=float(v),
                )]

        self.rows.append(row)
        self._step += 1
        client.experiment_plots_metrics_update(self.experiment.id, plot_metrics)

    def update_images(self, client, row):
        """
        Update images in history
        """
        if not self.experiment.get_plot_volume_id():
            raise ArgumentException("Experiment plot volume id is not set")

        source_path = SAVVIHUB_IMAGES + '/'
        dest_volume_id = self.experiment.get_plot_volume_id()
        dest_snapshot = 'latest'
        dest_path = source_path

        for images in row.values():
            self.images = self.images + images

        responses = volume_file_copy_local_to_remote(
            client,
            source_path=source_path,
            dest_volume_id=dest_volume_id,
            dest_path=dest_path,
            dest_snapshot=dest_snapshot,
            recursive=True
        )

        captions = []
        for images in row.values():
            for image in images:
                captions.append(image.get_caption())
                image.flush()

        plot_files = [ProtoExperimentPlotFile(
            step=None,
            path=response.path,
            caption=caption,
            timestamp=datetime.utcnow().timestamp(),
        ) for response, caption in zip(responses, captions)]
        client.experiment_plots_files_update(self.experiment.id, plot_files, SAVVIHUB_PLOTS_FILETYPE_IMAGE)
