import numpy as np
import SimpleITK as sitk
from wsireg.utils.reg_utils import (
    RegImage,
    register_2d_images,
    sitk_pmap_to_dict,
    pmap_dict_to_json,
    json_to_pmap_dict,
    transform_2d_image,
)
from wsireg.wsireg2d import WsiReg2D
import pandas as pd

# TODO: test 3D on a sequence of 5 images


class WsiRegSeq3D(WsiReg2D):
    def __init__(self, project_name: str, output_dir: str, cache_images=True):
        super(WsiRegSeq3D, self).__init__(
            project_name, output_dir, cache_images
        )

        self._seq_idx_modality_name = dict()
        self._seq_min = None
        self._seq_max = None
        self._seq_indices = []

        self.target_seq_idx = None

    def add_modality(
        self,
        modality_name,
        image_fp,
        seq_idx,
        image_res=1,
        channel_names=None,
        channel_colors=None,
        prepro_dict={},
        initial_transforms=None,
        mask=None,
    ):
        """
        Add an image modality (node) to the registration graph

        Parameters
        ----------
        modality_name : str
            Unique name identifier for the modality
        image_fp : str
            file path to the image to be read
        seq_idx : int
            position of image in 3D sequence
        image_res : float
            spatial resolution of image in units per px (i.e. 0.9 um / px)
        prepro_dict :
            preprocessing parameters for the modality for registration. Registration images should be a xy single plane
            so many modalities (multi-channel, RGB) must "create" a single channel.
            Defaults: multi-channel images -> max intensity project image
            RGB -> greyscale then intensity inversion (black background, white foreground)
        """
        if modality_name in self._modality_names:
            raise ValueError(
                'modality named "{}" is already in modality_names'.format(
                    modality_name
                )
            )

        if seq_idx in self._seq_indices:
            raise ValueError(
                'modality\'s index "{}" is already in indices'.format(seq_idx)
            )

        self.modalities = {
            modality_name: {
                "image_fp": image_fp,
                "image_res": image_res,
                "seq_idx": seq_idx,
                "channel_names": channel_names,
                "channel_colors": channel_colors,
                "preprocessing": prepro_dict,
                "initial_transforms": None
                if initial_transforms is None
                else json_to_pmap_dict(initial_transforms),
                "mask": mask,
            }
        }

        self.modality_names = modality_name
        self.seq_idx_modality_name = {seq_idx: modality_name}
        self.seq_indices = seq_idx

    @property
    def seq_idx_modality_name(self):
        return self._seq_idx_modality_name

    @seq_idx_modality_name.setter
    def seq_idx_modality_name(self, seq_dict):
        self._seq_idx_modality_name.update(seq_dict)
        full_seq_indices = [k for k in self._seq_idx_modality_name.keys()]
        if len(full_seq_indices) > 0:
            self._seq_min = np.min(full_seq_indices)
            self._seq_max = np.max(full_seq_indices)

    @property
    def seq_indices(self):
        return self._seq_indices

    @seq_indices.setter
    def seq_indices(self, seq_idx):
        self._seq_indices.append(seq_idx)

    def build_seq_reg_paths(self, target_modality_idx):

        full_seq_indices = np.array(self.seq_indices)
        self.target_seq_idx = self.modalities.get(
            self.seq_idx_modality_name.get(target_modality_idx)
        ).get("seq_idx")

        if self._seq_min < self.target_seq_idx:
            back_seq_indices = full_seq_indices[
                full_seq_indices < self.target_seq_idx
            ]
            back_seq_indices = np.append(
                back_seq_indices, self.target_seq_idx
            )[::-1]
        else:
            back_seq_indices = None
        if self._seq_max > self.target_seq_idx:
            forw_seq_indices = full_seq_indices[
                full_seq_indices > self.target_seq_idx
            ][::-1]
            forw_seq_indices = np.append(
                forw_seq_indices, self.target_seq_idx
            )[::-1]
        else:
            forw_seq_indices = None

        if back_seq_indices is not None:
            for idx, reg_pair in enumerate(back_seq_indices):
                if idx + 1 < len(back_seq_indices):
                    self.add_reg_path(
                        self.seq_idx_modality_name.get(
                            back_seq_indices[idx + 1]
                        ),
                        self.seq_idx_modality_name.get(reg_pair),
                        thru_modality=None,
                        reg_params=["rigid", "nl"],
                        override_prepro={"source": None, "target": None},
                    )
        if forw_seq_indices is not None:
            for idx, reg_pair in enumerate(forw_seq_indices):
                if idx + 1 < len(forw_seq_indices):
                    self.add_reg_path(
                        self.seq_idx_modality_name.get(
                            forw_seq_indices[idx + 1]
                        ),
                        self.seq_idx_modality_name.get(reg_pair),
                        thru_modality=None,
                        reg_params=["rigid", "nl"],
                        override_prepro={"source": None, "target": None},
                    )

    def _check_cache_seq_modality(self, modality_name):
        cache_im_fp = self.image_cache / f"{modality_name}_3dReg.tiff"
        cache_mask_im_fp = (
            self.image_cache / f"{modality_name}_3dReg_mask.tiff"
        )
        im_initial_transforms = None
        return cache_im_fp, im_initial_transforms, True, cache_mask_im_fp

    def _check_cache_modality(self, modality_name):
        cache_im_fp = self.image_cache / "{}_prepro.tiff".format(modality_name)
        cache_mask_im_fp = self.image_cache / "{}_prepro_mask.tiff".format(
            modality_name
        )

        cache_transform_fp = cache_im_fp.parent / "{}_init_tforms.json".format(
            cache_im_fp.stem
        )

        if cache_im_fp.exists() is True:
            im_fp = str(cache_im_fp)
            im_from_cache = True
            if cache_mask_im_fp.exists() is True:
                mask = str(cache_mask_im_fp)
        else:
            im_fp = self.modalities[modality_name]["image_fp"]
            im_from_cache = False
            mask = self.modalities[modality_name]["mask"]

        if cache_transform_fp.exists() is True:
            im_initial_transforms = [json_to_pmap_dict(cache_transform_fp)]
        else:
            im_initial_transforms = None

        return im_fp, im_initial_transforms, im_from_cache, mask

    def _prepare_modality(self, modality_name, reg_edge, src_or_tgt):
        # if modality name = target modality name, preprocess in full
        # source = preprocess from file
        # if modality name != target modality name
        # read from .im_cache "modality_name_prepro_aligned"

        mod_data = self.modalities[modality_name].copy()
        target_modality_name = self.seq_idx_modality_name.get(
            self.target_seq_idx
        )

        if reg_edge.get("override_prepro") is not None:
            override_preprocessing = reg_edge.get("override_prepro")[
                src_or_tgt
            ]
        else:
            override_preprocessing = None

        if override_preprocessing is not None:

            return (
                mod_data["image_fp"],
                mod_data["image_res"],
                mod_data["preprocessing"],
                None,
                mod_data["mask"],
            )
        elif src_or_tgt == "source":

            (
                mod_data["image_fp"],
                mod_data["transforms"],
                im_from_cache,
                mask,
            ) = self._check_cache_modality(modality_name)

            if im_from_cache is True:
                image_res = mod_data.get("image_res")
                ds = mod_data.get("preprocessing").get("downsample")
                if ds is not None:
                    image_res = image_res * ds
                mod_data["image_res"] = image_res
                mod_data["preprocessing"] = None

            else:
                mod_data.update({"transforms": mod_data["initial_transforms"]})

            return (
                mod_data["image_fp"],
                mod_data["image_res"],
                mod_data["preprocessing"],
                mod_data["transforms"],
                mask,
            )

        elif src_or_tgt == "target" and modality_name != target_modality_name:

            (
                mod_data["image_fp"],
                mod_data["transforms"],
                im_from_cache,
                mask,
            ) = self._check_cache_seq_modality(modality_name)

            # if im_from_cache is True:
            # mod_data["preprocessing"] = None

            # image_res for sequentially regged images will always match the singular
            # target modality's image_res
            image_res = self.modalities.get(target_modality_name).get(
                "image_res"
            )
            ds = mod_data.get("preprocessing").get("downsample")
            if ds is not None:
                image_res = image_res * ds
            if mask.is_file() is False:
                mask = None
            else:
                mask = str(mask)

            return (mod_data["image_fp"], image_res, None, None, mask)

        else:
            (
                mod_data["image_fp"],
                mod_data["transforms"],
                im_from_cache,
                mask,
            ) = self._check_cache_modality(modality_name)

            if im_from_cache is True:
                image_res = mod_data.get("image_res")
                ds = mod_data.get("preprocessing").get("downsample")
                if ds is not None:
                    image_res = image_res * ds
                mod_data["image_res"] = image_res
                mod_data["preprocessing"] = None
                mod_data["mask"] = mask
            else:
                mod_data.update({"transforms": mod_data["initial_transforms"]})

            return (
                mod_data["image_fp"],
                mod_data["image_res"],
                mod_data["preprocessing"],
                mod_data["transforms"],
                mod_data["mask"],
            )

    def register_images(
        self,
        parallel=False,
        compute_inverse=False,
        restart_idx=None,
        n_regs=None,
        use_masks=True,
    ):
        """
        Start image registration process for all modalities

        Parameters
        ----------
        parallel : bool
            whether to run each edge in parallel (not implemented yet)
        compute_inverse : bool
            whether to compute the inverse transformation for each modality, may be used for point transformations but
            isn't currently working universally
        """

        if restart_idx is not None:

            restart_src_name = self.seq_idx_modality_name[restart_idx]
            restart_edge_idx = [
                idx
                for idx, re in enumerate(self.reg_graph_edges)
                if re.get("modalities").get("source") == restart_src_name
            ][0]

            if restart_idx != self.target_seq_idx:
                if n_regs is None:
                    self._reg_graph_edges = self._reg_graph_edges[
                        restart_edge_idx:
                    ]
                else:
                    self._reg_graph_edges = self._reg_graph_edges[
                        restart_edge_idx : restart_edge_idx + n_regs
                    ]

            print(f"restarting from {restart_src_name}")

        reg_edge = self.reg_graph_edges[0]
        for reg_edge in self.reg_graph_edges:

            src_name = reg_edge.get("modalities").get("source")
            tgt_name = reg_edge.get("modalities").get("target")

            (
                src_reg_image_fp,
                src_res,
                src_prepro,
                src_transforms,
                src_mask,
            ) = self._prepare_modality(src_name, reg_edge, "source")

            (
                tgt_reg_image_fp,
                tgt_res,
                tgt_prepro,
                tgt_transforms,
                tgt_mask,
            ) = self._prepare_modality(tgt_name, reg_edge, "target")

            print(f"preprocessing {src_name}")
            src_reg_image = RegImage(
                src_reg_image_fp,
                src_res,
                src_prepro,
                src_transforms,
                mask=src_mask,
            )

            print(f"preprocessing {tgt_name}")
            tgt_reg_image = RegImage(
                tgt_reg_image_fp,
                tgt_res,
                tgt_prepro,
                tgt_transforms,
                mask=tgt_mask,
            )

            if self.cache_images is True:
                if reg_edge.get("override_prepro") is not None:
                    if reg_edge.get("override_prepro").get("source") is None:
                        self._cache_images(src_name, src_reg_image)
                    if reg_edge.get("override_prepro").get("target") is None:
                        self._cache_images(tgt_name, tgt_reg_image)
                else:
                    self._cache_images(src_name, src_reg_image)
                    self._cache_images(tgt_name, tgt_reg_image)

            reg_params = reg_edge["params"]
            # reg_params = ["rigid"]

            output_path = self.output_dir / "{}-{}_to_{}_reg_output".format(
                self.project_name,
                reg_edge["modalities"]["source"],
                reg_edge["modalities"]["target"],
            )

            output_path.mkdir(parents=False, exist_ok=True)

            output_path_tform = (
                self.output_dir
                / "{}-{}_to_{}_transformations.json".format(
                    self.project_name,
                    reg_edge["modalities"]["source"],
                    reg_edge["modalities"]["target"],
                )
            )

            if src_reg_image.mask is not None:
                mask_to_tform = src_reg_image.mask
            else:
                mask_to_tform = None

            if tgt_reg_image.mask is not None:
                tgt_mask = tgt_reg_image.mask
            else:
                tgt_mask = None

            if use_masks is False:
                src_reg_image.mask = None
                tgt_reg_image.mask = None

            split_reg = True
            if split_reg is True:
                reg_tforms = []
                idx = 1
                reg_param = "nl"
                compute_inverse = False
                for idx, reg_param in enumerate(reg_params):
                    if idx == 0:
                        if reg_param in ["rigid", "affine", "similarity"]:
                            src_reg_image.mask = None
                            tgt_reg_image.mask = None

                        reg_tform, tform_image = register_2d_images(
                            src_reg_image,
                            tgt_reg_image,
                            [reg_param],
                            output_path,
                            compute_inverse=compute_inverse,
                            return_image=True,
                        )

                    else:
                        src_reg_image.image = tform_image

                        if reg_param in ["rigid", "affine", "similarity"]:
                            src_reg_image.mask = None
                            tgt_reg_image.mask = None
                        else:
                            if mask_to_tform is not None:
                                tform_mask = transform_2d_image(
                                    mask_to_tform, [reg_tform[0]]
                                )
                                src_reg_image.mask = tform_mask

                            tgt_reg_image.mask = tgt_mask

                        reg_tform, tform_image = register_2d_images(
                            src_reg_image,
                            tgt_reg_image,
                            [reg_param],
                            output_path,
                            compute_inverse=compute_inverse,
                            return_image=True,
                        )
                    reg_tforms.append(reg_tform[0])

            else:
                reg_tforms, tform_image = register_2d_images(
                    src_reg_image,
                    tgt_reg_image,
                    reg_params,
                    output_path,
                    compute_inverse=compute_inverse,
                    return_image=True,
                )

            if mask_to_tform is not None:
                tform_mask = transform_2d_image(mask_to_tform, reg_tforms)
                sitk.WriteImage(
                    tform_mask,
                    str(self.image_cache / f"{src_name}_3dReg_mask.tiff"),
                    True,
                )

            sitk.WriteImage(
                tform_image,
                str(self.image_cache / f"{src_name}_3dReg.tiff"),
                True,
            )

            reg_tforms = [sitk_pmap_to_dict(tf) for tf in reg_tforms]

            reg_edge["transforms"] = {
                'initial': src_reg_image.transforms,
                'registration': reg_tforms,
            }
            reg_edge["registered"] = True
            pmap_dict_to_json(reg_edge["transforms"], str(output_path_tform))

        # self.transformations = self.reg_graph_edges


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Perform 3D reconstructive alignment'
    )

    parser.add_argument(
        "--r",
        metavar="restart",
        type=int,
        nargs=1,
        help="restart index",
    )

    parser.add_argument(
        "--n",
        type=int,
        nargs=1,
        help="number of registrations to perform from restart",
    )

    parser.add_argument(
        "--m",
        type=int,
        nargs=1,
        help="number of registrations to perform from restart",
    )

    args = parser.parse_args()
    restart_idx = args.r
    n_regs = args.n
    use_mask = args.m

    if restart_idx is not None:
        restart_idx = restart_idx[0]
    if n_regs is not None:
        n_regs = n_regs[0]
    if use_mask is not None:
        use_mask = True
    else:
        use_mask = True

    # reg_3D = WsiRegSeq3D(
    #     "VAN0006-LK-002",
    #     "/dors/biomic/S108_3D/IMS_sec_micro_reg/registration_outputs_3d",
    #     cache_images=True,
    # )
    # reg_3D_info = pd.read_csv(
    #     "/dors/biomic/S108_3D/IMS_sec_micro_reg/registration_configs/VAN0006_3D_processing_setup.csv"
    # )

    reg_3D = WsiRegSeq3D(
        "masktest-VAN0006-LK-002", "C:/biomic", cache_images=True
    )
    reg_3D_info = pd.read_csv(
        "C:/Users/john/Dropbox (VU Basic Sciences)/S108_3dtesting_data/VAN0006_3D_processing_setup_mod.csv"
    )

    for idx, depth in reg_3D_info.iterrows():
        tag = depth["tag"].strip(" ")
        im_fp = depth["image_fp"]
        rotation = depth["rotation"]
        if rotation == 0:
            rotation = None
        seq_idx = depth["seq"]
        tf = depth["transformations"]
        mask_fp = depth["mask"]

        if isinstance(tf, str) is False:
            tf = None

        reg_3D.add_modality(
            f"{tag}",
            f"{im_fp}",
            seq_idx,
            image_res=0.65,
            initial_transforms=tf,
            prepro_dict={
                "image_type": "FL",
                "ch_indices": [1],
                "as_uint8": True,
                "rot_cc": rotation,
                "downsample": 10,
            },
            channel_names=[
                "DAPI - autofluorescence",
                "eGFP - autofluorescence",
                "DsRed - autofluorescence",
            ],
            channel_colors=["blue", "green", "red"],
            mask=mask_fp,
        )

    reg_3D.build_seq_reg_paths(20)
    self = reg_3D

    reg_3D.register_images()

    # reg_3D.save_transformations()
