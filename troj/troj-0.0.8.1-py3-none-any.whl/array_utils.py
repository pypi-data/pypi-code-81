import numpy as np


def AdvLossSort(adv_examples, adv_losses, k=5):
    # adversarial examples, and their adersarial losses are taken as input
    # sorts examples by maximum adversarial loss, returns top k
    index_order = np.argsort(adv_losses, axis=1)
    outs_array = adv_examples
    for i in range(index_order.shape[0]):
        outs_array[i] = outs_array[i, index_order[i]]
    return outs_array[:, :k]


def get_min_pert(original_ims, outs_array, norm=np.inf):
    # original_ims is the original images, and the outs_array are the adversarial examples, sorted by highest loss
    # make a copy of the original images the same shape as the output, copying the images along the second axis
    tile_list = [original_ims for i in range(outs_array.shape[1])]
    tiled = np.stack(tile_list)
    # swap the first and second axis
    tiled = np.swapaxes(tiled, 0, 1)
    assert tiled[0, 0, 0, 0, 0] == tiled[0, 1, 0, 0, 0]

    # reshape outputs and original images to collection of vectors
    flattened_shape = (
        outs_array.shape[0],
        outs_array.shape[1],
        outs_array.shape[2] * outs_array.shape[3] * outs_array.shape[4],
    )
    flattened_outs = np.reshape(outs_array, flattened_shape)
    flattened_original = np.reshape(tiled, flattened_shape)

    # subtract the original from the perturbed to get the perturbation vector
    perturbations = flattened_outs - flattened_original
    perturbation_norms = np.linalg.norm(perturbations, norm, axis=2)
    min_per_sample_idx = np.argmax(perturbation_norms, axis=1)

    min_pert_outs = []
    for idx in range(len(min_per_sample_idx)):
        min_pert_outs.append(outs_array[idx, min_per_sample_idx[idx]])

    min_pert_outs = np.asarray(min_pert_outs)
    return min_pert_outs


def compute_Lp_distance(x1, x2, p=np.inf):
    x1 = np.reshape(x1, (x1.shape[0], -1))
    x2 = np.reshape(x2, (x2.shape[0], -1))
    difference_vect = x1 - x2
    lp_distance = np.linalg.norm(difference_vect, p, axis=1)
    return lp_distance
