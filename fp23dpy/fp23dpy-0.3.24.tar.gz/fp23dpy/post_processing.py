""" Functions to post process the reconstructed 3D data """

import numpy as np
from skimage import measure, morphology

from . import helpers
# from . import Roi
import matplotlib.pyplot as plt


# def get_shifted_area_segmentation(area, shift):
#     """Area is image with nonzero values that should be shifted and shift is a vector with the length of shift for each dimension of the area array"""
#     shape = area.shape
#     coordinates = np.where(area)
#     valid_rows = np.ones(len(coordinates[0]), dtype=bool)
#     shifted_coordinates = np.empty((len(shape), len(valid_rows)), dtype=int)
#     for i, c in enumerate(coordinates):
#         shifted_c = c + round(shift[i])
#         # remove coordinates that are outside of the image
#         valid_rows = valid_rows & (shifted_c >= 0) & (shifted_c < shape[i])
#         shifted_coordinates[i] = shifted_c
#     # print(np.sum(valid_rows) / len(valid_rows))
#     shifted_coordinates = shifted_coordinates[:, valid_rows]
# 
#     shifted_area = np.zeros(shape, dtype=bool)
#     shifted_area[tuple(shifted_coordinates)] = True
#     return shifted_area

def find_edge_coordinates(segmentation):
    eroded = morphology.erosion(segmentation, morphology.disk(1))
    edge_pixels = segmentation & ~eroded
    coords = np.array(np.where(edge_pixels)).T
    return coords

def temporal_alignment(reconstructions, mean_velocity=None):
    """Attempt to temporally align the reconstructions by tracking blobs.
    This will only be applied to blobs that get disconnected from the main area with pixels that are connected to the absolute_phase pixel in calibration.
    All reconstructions should have the same original shape of images and absolute_phase_coordinates set for their calibration. If not these are met, an assertion error is raised.

    This function is not that robust but works ok if the objects are moving less than 10 pixels per frame

    :reconstructions: list of dicts
        all reconstructions to align, each reconstruction is a dict with at least the keys grid and calibration
    :returns: None
    """
    # Check that all reconstructions have absolute_phase_coordinates
    # and check that the reconstructions all have the same shape
    absolute_phase_coordinates = []
    shape = reconstructions[0]["grid"].shape
    for reconstruction in reconstructions:
        if "absolute_phase" in reconstruction["calibration"]:
            absolute_phase_coordinates.append(
                reconstruction["calibration"]["absolute_phase"][:2]
            )
        assert (
            shape == reconstruction["grid"].shape
        ), "All shapes must be the same for temporal alignment"
    assert len(absolute_phase_coordinates) == len(
        reconstructions
    ), "Need absolute_phase_coordinates for all reconstructions to use --temporal-alignment"
    absolute_phase_coordinates = np.array(absolute_phase_coordinates)

    # last_last_threed_values = reconstructions[0]["grid"][2]
    # last_last_segmentation = ~helpers.get_mask(last_last_threed_values)
    # last_last_information = {"threed_values": reconstructions[0]["grid"][2]}
    # last_last_information["segmentation"] = ~helpers.get_mask(
    #     last_last_information["threed_values"]
    # )

    # last_information = {"threed_values": reconstructions[1]["grid"][2]}
    # # Removing the lines in the image
    # last_information["signal"] = filters.gaussian(
    #     reconstructions[1]["signal"], reconstructions[1]["calibration"]["T"] / 2
    # )
    # last_information["segmentation"] = ~helpers.get_mask(
    #     last_information["threed_values"]
    # )
    last_threed_values = reconstructions[0]["grid"][2]
    # last_segmentation = ~helpers.get_mask(last_threed_values)

    # last_labels, last_n_labels = measure.label(
    #     last_segmentation.astype(int), return_num=True
    # )
    # last_information["labels"] = last_labels
    # last_information["n_labels"] = last_n_labels
    # # this is some kind on mean velocity in the third dimension for each area in the image
    # last_information["threed_velocity"] = {}

    # absolute_phase_label = last_labels[tuple(absolute_phase_coordinates[0][::-1])]
    # last_information["threed_velocity"][absolute_phase_label] = "absolute"

    # # Removing areas that can not be found in the first two images
    # for i in range(2):
    #     reconstruction = reconstructions[i]
    #     segmentation = ~helpers.get_mask(reconstruction["grid"][2])

    #     labels, n_labels = measure.label((segmentation).astype(int), return_num=True)
    #     absolute_phase_label = labels[tuple(absolute_phase_coordinates[i][::-1])]
    #     for j in range(1, n_labels + 1):
    #         if j != absolute_phase_label:
    #             segmentation[labels == j] = False
    #     mask = np.tile(~segmentation, (3, 1, 1))
    #     reconstruction["grid"].mask = mask

    # to estimate velocity in 3D at least two previous reconstructions are required
    for i in range(1, len(reconstructions)):
        reconstruction = reconstructions[i]
        # signal = reconstruction["signal"]
        # Removing the lines in the image
        # signal = filters.gaussian(signal, reconstruction["calibration"]["T"] / 2)

        # reference_image = last_information["signal"]
        # moving_image = signal
        # shift, error, diffphase = registration.phase_cross_correlation(
        #     reference_image, moving_image
        # )
        # print(shift)
        # continue
        threed_values = reconstruction["grid"][2]
        # if np.ma.isMaskedArray(threed_values):
        #     segmentation = ~threed_values.mask
        # else:
        #     segmentation = np.ones(threed_values.shape, dtype=bool)
        segmentation = ~helpers.get_mask(threed_values)

        # Using labeled connected components to find the different areas in the image
        labels, n_labels = measure.label((segmentation).astype(int), return_num=True)
        absolute_phase_label = labels[tuple(absolute_phase_coordinates[i][::-1])]
        # threed_velocities = {absolute_phase_label: "absolute"}
        absolute_phase_area_coords = np.expand_dims(find_edge_coordinates(labels == absolute_phase_label), 1)

        area_tracks = {}
        if "area_tracks" in reconstruction["calibration"]:
            for tracked_area in reconstruction["calibration"]["area_tracks"]:
                area_label = labels[tuple(tracked_area[0][::-1])]
                if area_label == 0:
                    raise ValueError("Area track is on a masked area for {}".format(reconstruction["filename"]))
                area_tracks[area_label] = tracked_area

        for j in range(1, n_labels + 1):
            if j == absolute_phase_label:
                continue  # no tracking required for areas with known absolute phase
            area = labels == j
            if j in area_tracks:
                this_area_val = threed_values[tuple(area_tracks[j][0][::-1])]
                other_area_val = last_threed_values[tuple(area_tracks[j][1][::-1])]
            else:
                area_coords = np.expand_dims(find_edge_coordinates(area), 0)

                distances = np.linalg.norm(area_coords - absolute_phase_area_coords, axis=-1)
                closest_ind = np.argmin(distances)
                closest_absolute_pixel_ind, closest_area_ind = np.unravel_index(closest_ind, distances.shape)
                closest_absolute_pixel_coords = absolute_phase_area_coords[closest_absolute_pixel_ind, 0]
                other_area_val = threed_values[tuple(closest_absolute_pixel_coords)]
                closest_area_coords = area_coords[0, closest_area_ind]
                this_area_val = threed_values[tuple(closest_area_coords)]
            
            # threed_velocities[j] = threed_velocity
            # estimating the difference between the areas, using median to avoid outliers
            # l = np.median(np.ma.compressed(threed_values[area])) - np.median(
            #     np.ma.compressed(last_information["threed_values"][shifted_area])
            # )
            # remove median difference to last area and add the estimated 3D velocity
            threed_values[area] = threed_values[area] - this_area_val + other_area_val
            

           #  # area_roi = Roi.find_from_mask(~area)
           #  # area_roi.enlarge(40)
           #  # area_size = np.sum(area)
           #  reference_image = last_information["signal"]
           #  # if not mean_velocity is None:
           #  #     preshifted_area = get_shifted_area_segmentation(area, -np.asarray(mean_velocity))
           #  #     reference_image[(reference_image > 0) & (preshifted_area > 0)] = 1.2
           #  moving_image = area_roi.unapply(area_roi.apply(signal)).data
           #  # moving_image = area_roi.apply(signal)
           #  # plt.figure()
           #  # plt.imshow(reference_image)
           #  # plt.figure()
           #  # plt.imshow(moving_image)
           #  # plt.show()
           #  # exit()
           #  shift, error, diffphase = registration.phase_cross_correlation(
           #      reference_image, moving_image
           #  )
           #  print(shift)
           #  # Tracking to find where this area was in the last image
           #  shifted_area = get_shifted_area_segmentation(area, shift)
           #  # plt.figure()
           #  # plt.imshow(area)
           #  # plt.figure()
           #  # plt.imshow(last_information["segmentation"].astype(int) + shifted_area*2)
           #  # plt.show()
           #  # exit()

           #  tracked_labels, lengths = np.unique(
           #      last_labels[shifted_area], return_counts=True
           #  )
           #  if len(lengths) == 0:
           #      print(
           #          "Warning, no good match found, file {}, label {}".format(
           #              reconstruction["filename"], j
           #          )
           #      )
           #      continue
           #  best_track_ind = np.argmax(lengths)
           #  tracked_trueness = lengths[best_track_ind] / area_size
           #  if tracked_trueness < 0.4:
           #      print(
           #          "Warning, tracking match in temporal_alignment found to be too low, file {}, label {}".format(
           #              reconstruction["filename"], j
           #          )
           #      )
           #      continue
           #  tracked_label = tracked_labels[best_track_ind]  # area found

           #  if tracked_label in last_information["threed_velocity"]:
           #      if isinstance(
           #          last_information["threed_velocity"][tracked_label], float
           #      ):
           #          threed_velocity = last_information["threed_velocity"][tracked_label]
           #      elif last_information["threed_velocity"][tracked_label] == "absolute":
           #          # This is the first time the area is released from the area with absolute phase
           #          # First the threed velocity is estimated by looking one frame further back and same shift again
           #          shifted_shifted_area = get_shifted_area_segmentation(
           #              shifted_area, shift
           #          )
           #          remaining_area = (
           #              np.sum(
           #                  shifted_shifted_area & last_last_information["segmentation"]
           #              )
           #              / area_size
           #          )
           #          if remaining_area < 0.4:
           #              print(
           #                  "Warning, second shift in temporal_alignment is probably outside image, file {}, label {}".format(
           #                      reconstruction["filename"], j
           #                  )
           #              )
           #              continue

           #          last_information["threed_values"].shape
           #          shifted_area.shape
           #          threed_velocity = np.median(
           #              np.ma.compressed(
           #                  last_information["threed_values"][shifted_area]
           #              )
           #          ) - np.median(
           #              np.ma.compressed(
           #                  last_last_information["threed_values"][shifted_shifted_area]
           #              )
           #          )
           #      else:
           #          # Not possible to estimate velocity since last area is not a good match or absolute
           #          continue

        reconstruction["grid"][2] = threed_values
        mask = np.tile(~segmentation, (3, 1, 1))
        reconstruction["grid"].mask = mask
        
        last_threed_values = threed_values
        # last_labels = labels

        # Setting for next iteration
        # last_last_information = last_information
        # last_information = {
        #     "threed_values": threed_values,
        #     # "signal": signal,
        #     # "threed_velocity": threed_velocities,
        #     "segmentation": segmentation,
        #     "labels": labels,
        #     "n_labels": n_labels,
        # }
        # last_last_threed_values = last_threed_values
        # last_threed_values = threed_values
        # last_last_segmentation = segmentation
        # last_segmentation = segmentation
        # last_labels = labels
        # last_threed_velocity = threed_velocities
