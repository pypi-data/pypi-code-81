#!python

import multiprocessing as mp
import time
import alphatims.utils
import alphatims.bruker
import numpy as np
import pandas as pd
import h5py

# win64\uff-cmdline2.exe --ff 4d --readconfig proteomics_4d.config --analysisDirectory D:\data\alphatims\20201207_tims03_Evo03_PS_SA_HeLa_200ng_EvoSep_prot_DDA_21min_8cm_S1-C10_1_22476.d

@alphatims.utils.pjit
def connect_pushes(
    push_index,
    push_indptr,
    tof_indices,
    frame_max_index,
    scan_max_index,
    push_offsets,
#     raw_quad_indptr,
    quad_mz_values,
    frame_range,
    scan_range,
    tof_range,
    connection_count_per_push,
    connections,
    count_connections,
):
    self_scan_index = push_index % scan_max_index
    self_frame_index = push_index // scan_max_index
    self_start_index = push_indptr[push_index]
    self_end_index = push_indptr[push_index + 1]
    self_quad_index = push_offsets[push_index]
    self_quad_low_mz, self_quad_high_mz = quad_mz_values[self_quad_index]
    if self_start_index == self_end_index:
        return
    max_frame = min(self_frame_index + frame_range + 1 , frame_max_index)
    min_scan = max(self_scan_index - scan_range, 0)
    max_scan = min(self_scan_index + scan_range + 1, scan_max_index)
#     TODO in current scan, or assume already centroided?
#     TODO check for precursor/ quad equality
    connection_index = connection_count_per_push[push_index]
    for other_scan_index in range(self_scan_index + 1, max_scan):
        other_push_index = self_frame_index * scan_max_index + other_scan_index
        other_quad_index = push_offsets[other_push_index]
        other_quad_low_mz, other_quad_high_mz = quad_mz_values[other_quad_index]
        #requires at least some overlap
        if other_quad_low_mz > self_quad_high_mz:
            continue
        if self_quad_low_mz > other_quad_high_mz:
            continue
        connection_index += connect_tof_indices(
            connection_index,
            push_index,
            other_push_index,
            tof_range,
            self_start_index,
            self_end_index,
            tof_indices,
            push_indptr,
            connection_count_per_push,
            connections,
            count_connections,
        )
    for other_frame_index in range(self_frame_index + 1, max_frame):
        for other_scan_index in range(min_scan, max_scan):
            other_push_index = other_frame_index * scan_max_index + other_scan_index
            other_quad_index = push_offsets[other_push_index]
            other_quad_low_mz, other_quad_high_mz = quad_mz_values[other_quad_index]
            #requires at least some overlap
            if other_quad_low_mz > self_quad_high_mz:
                continue
            if self_quad_low_mz > other_quad_high_mz:
                continue
            connection_index += connect_tof_indices(
                connection_index,
                push_index,
                other_push_index,
                tof_range,
                self_start_index,
                self_end_index,
                tof_indices,
                push_indptr,
                connection_count_per_push,
                connections,
                count_connections,
            )


@alphatims.utils.njit(nogil=True)
def connect_tof_indices(
    connection_index,
    self_push_index,
    other_push_index,
    tof_range,
    self_index,
    self_end_index,
    tof_indices,
    push_indptr,
    connection_count_per_push,
    connections,
    count_connections
):
    hit_count = 0
    other_index = push_indptr[other_push_index]
    other_end_index = push_indptr[other_push_index + 1]
    if other_index == other_end_index:
        return 0
    self_tof_index = tof_indices[self_index]
    while True:
        other_tof_index = tof_indices[other_index]
        if self_tof_index > (other_tof_index + tof_range):
            other_index += 1
            if other_index == other_end_index:
                break
        else:
            for i, other_tof_index in enumerate(
                tof_indices[other_index: other_end_index]
            ):
                if other_tof_index > (self_tof_index + tof_range):
                    break
                else:
                    if count_connections:
                        connection_count_per_push[self_push_index] += 1
                    else:
                        connections[connection_index + hit_count] = (
                            self_index,
                            # TODO rare border case where there is overflow?
                            other_index + i
                        )
                    hit_count += 1
            self_index += 1
            if self_index == self_end_index:
                break
            self_tof_index = tof_indices[self_index]
    return hit_count


@alphatims.utils.njit
def make_symmetric(
    indptr,
    indices,
):
    # TODO: multithread? Can be greatly sped up
#     connections = np.empty((connection_indices.shape[0] * 2, 2), dtype=np.int64)
# connections[:connection_indices.shape[0], 0] = connection_indices
# connections[connection_indices.shape[0]:, 1] = connections[:connection_indices.shape[0], 0]
# connections[:connection_indices.shape[0], 1] = np.repeat(np.arange(len(data)), np.diff(connection_indptr))
# connections[connection_indices.shape[0]:, 0] = connections[:connection_indices.shape[0], 1]

    indptr_ = indptr.copy()
    indptr_[1:] += np.cumsum(
        np.bincount(indices, minlength=indptr.shape[0] - 1)
    )
    indices_ = np.empty(indptr_[-1], np.int64)
    offsets = indptr_[:-1] + np.diff(indptr)
    for index in range(indptr.shape[0] - 1):
        start = indptr[index]
        end = indptr[index + 1]
        current_indices = indices[start: end]
        start_ = indptr_[index]
        end_ = start_ + current_indices.shape[0]
        indices_[start_: end_] = current_indices
        current_offsets = offsets[current_indices]
        indices_[current_offsets] = index
        offsets[current_indices] += 1
    return indptr_, indices_


def connect_datapoints(
    data,
    indices,
    frame_range,
    scan_range,
    tof_range,
    symmetric=True
):
    connection_count_per_push = np.zeros_like(data.push_indptr)
    push_offsets = np.repeat(
        np.arange(data.raw_quad_indptr.shape[0] - 1),
        np.diff(data.raw_quad_indptr),
    )
    connect_pushes(
        indices,
        data.push_indptr,
        data.tof_indices,
        data.frame_max_index,
        data.scan_max_index,
        push_offsets,
#         data.raw_quad_indptr,
        data.quad_mz_values,
        frame_range,
        scan_range,
        tof_range,
        connection_count_per_push,
        np.empty(shape=(0, 2), dtype=np.uint64),
        True
    )
    connection_count_per_push = np.cumsum(connection_count_per_push)
    connection_count_per_push[1:] = connection_count_per_push[:-1]
    connection_count_per_push[0] = 0
    connections = np.zeros((connection_count_per_push[-1], 2), dtype=np.int64)
    connect_pushes(
        indices,
        data.push_indptr,
        data.tof_indices,
        data.frame_max_index,
        data.scan_max_index,
        push_offsets,
#         data.raw_quad_indptr,
        data.quad_mz_values,
        frame_range,
        scan_range,
        tof_range,
        connection_count_per_push,
        connections,
        False
    )
    connection_indptr = np.cumsum(
        np.bincount(
            connections[:, 0],
            minlength=len(data) + 1
        )
    )
    connection_indptr[1:] = connection_indptr[:-1]
    connection_indptr[0] = 0
    order = np.argsort(connections[:, 0])
    connection_indices = connections[order, 1]
    if symmetric:
        connection_indptr, connection_indices = make_symmetric(
            connection_indptr,
            connection_indices,
        )
    return connection_indptr, connection_indices

@alphatims.utils.pjit
def centroid_spectrum(
    index,
    spectrum_indptr,
    spectrum_tof_indices,
    spectrum_intensity_values,
    tof_range,
    spectrum_offsets,
    connections,
    count_connections,
):
    if not count_connections:
        connection_start = spectrum_offsets[index]
        connection_end = spectrum_offsets[index + 1]
        if connection_start == connection_end:
            return
    offset = spectrum_indptr[index]
    end = spectrum_indptr[index + 1]
    tof_indices = spectrum_tof_indices[offset: end]
    result = []
    for i, tof_index in enumerate(tof_indices[:-1]):
        for j in range(i + 1, len(tof_indices)):
            if tof_indices[j] < tof_index + tof_range:
                result.append((offset + i, offset + j))
            else:
                break
#     print(result)
    if count_connections:
        spectrum_offsets[index] = len(result)
    else:
        connections[connection_start: connection_end] = np.array(result)


def centroid_spectra(
    indices,
    spectrum_indptr,
    spectrum_tof_indices,
    spectrum_intensity_values,
    tof_range,
    symmetric=True,
):
    spectrum_offsets = np.zeros(len(indices) + 1, np.int64)
    centroid_spectrum(
        indices,
        spectrum_indptr,
        spectrum_tof_indices,
        spectrum_intensity_values,
        tof_range,
        spectrum_offsets,
        np.empty(shape=(0,2), dtype=np.uint64),
        True,
    )
    spectrum_offsets[1:] = np.cumsum(spectrum_offsets[:-1])
    spectrum_offsets[0] = 0
    connections = np.empty((spectrum_offsets[-1], 2), dtype=np.int64)
    centroid_spectrum(
        indices,
        spectrum_indptr,
        spectrum_tof_indices,
        spectrum_intensity_values,
        tof_range,
        spectrum_offsets,
        connections,
        False,
    )
    connection_indptr = np.cumsum(
        np.bincount(
            connections[:, 0],
            minlength=len(spectrum_tof_indices) + 1
        )
    )
    connection_indptr[1:] = connection_indptr[:-1]
    connection_indptr[0] = 0
    order = np.argsort(connections[:, 0])
    connection_indices = connections[order, 1]
    if symmetric:
        connection_indptr, connection_indices = make_symmetric(
            connection_indptr,
            connection_indices,
        )
    return connection_indptr, connection_indices


@alphatims.utils.pjit
def smoothen_intensities(
    index,
    connection_indptr,
    connection_indices,
    intensities,
    smooth_intensities,
    smooth_factor=.25
):
    start = connection_indptr[index]
    end = connection_indptr[index + 1]
    if start < end:
        smooth_intensities[index] = intensities[index] * (1 - smooth_factor)
        smooth_intensities[index] += np.sum(
            intensities[connection_indices[start: end]]
        ) / (end - start) * smooth_factor
    else:
        smooth_intensities[index] = intensities[index]


@alphatims.utils.pjit
def smoothen_intensities_median(
    index,
    connection_indptr,
    connection_indices,
    intensities,
    smooth_intensities,
    smooth_factor=.25
):
    start = connection_indptr[index]
    end = connection_indptr[index + 1]
    if start < end:
        a = intensities[connection_indices[start: end]]
        np.append(a, intensities[index])
        smooth_intensities[index] = np.median(a)
    else:
        smooth_intensities[index] = intensities[index]


@alphatims.utils.pjit
def smoothen_intensities_mean(
    index,
    connection_indptr,
    connection_indices,
    intensities,
    smooth_intensities,
    smooth_factor=.25
):
    start = connection_indptr[index]
    end = connection_indptr[index + 1]
    if start < end:
        smooth_intensities[index] = (
            intensities[index] + np.sum(
                intensities[connection_indices[start: end]]
            )
        ) / (end - start + 1)
    else:
        smooth_intensities[index] = intensities[index]


@alphatims.utils.pjit
def find_local_maxima(
    index,
    connection_indptr,
    connection_indices,
    smooth_intensities,
    local_maxima,
    min_size=5
):
    start = connection_indptr[index]
    end = connection_indptr[index + 1]
    if start + min_size > end:
        return
    self_intensity = smooth_intensities[index]
    for other_index in connection_indices[start: end]:
        other_intensity = smooth_intensities[other_index]
        if other_intensity > self_intensity:
            return
    local_maxima[index] = True


@alphatims.utils.pjit
def initial_assignment(
    index,
    connection_indptr,
    connection_indices,
    smooth_intensities,
    assignments,
    to_check,
    min_size=5
):
    # -3 = unassigned
    # -2 = noise
    # -1 = check for mergability
    # >= 0 = assigned
    start = connection_indptr[index]
    end = connection_indptr[index + 1]
    if start == end:
        assignments[index] = -2
    elif start + min_size > end:
        assignments[index] = -3
    else:
        self_intensity = smooth_intensities[index]
        conflicts = [index]
        assignment = index
        for other_index in connection_indices[start: end]:
            other_intensity = smooth_intensities[other_index]
            if other_intensity > self_intensity:
                assignments[index] = -3
                return
            elif other_intensity == self_intensity:
                conflicts.append(other_index)
                if other_index > index:
                    assignment = other_index
        # for other_index in conflicts:
        #     assignments[other_index] = assignment
        assignments[index] = index
        to_check[index] = True
        # for other_index in connection_indices[start: end]:
        #     to_check[other_index] = True


@alphatims.utils.pjit(thread_count=1)
def find_components(
    index,
    connection_indptr,
    connection_indices,
    assignments,
    min_count=1,
):
    if assignments[index] == 0:
        neighbors = [index]
        while len(neighbors) > 0:
            neighbor_index = neighbors.pop()
            if assignments[neighbor_index] == 0:
                assignments[neighbor_index] = index + 1
                start = connection_indptr[neighbor_index]
                end = connection_indptr[neighbor_index + 1]
                if start + min_count <= end:
                    for neighbor_index in connection_indices[start: end]:
                        neighbors.append(neighbor_index)






# # @alphatims.utils.njit
# def top_down_cluster(
#     index,
#     smooth_intensities,
#     connection_indices,
#     connection_indptr,
#     merge_threshold,
#     neighbor_assignments,
#     neighbor_distances
# ):
#     start = connection_indptr[index]
#     end = connection_indptr[index + 1]
#     neighbors = connection_indices[start: end]
#     self_assignment = index + 1
#     self_distance = 0
#     assigned_neighbors = [index]
#     conflict = False
#     for neighbor_index in neighbors:
#         neighbor_assignment = neighbor_assignments[neighbor_index]
#         if neighbor_assignment != 0:
#             assigned_neighbors.append(neighbor_index)
#             if self_assignment == index + 1:
#                 self_assignment = neighbor_assignment
#                 self_distance = neighbor_distances[neighbor_index] + 1
#             elif self_assignment != neighbor_assignment:
#                 conflict = True
#     if conflict:
#         smooth_intensity = smooth_intensities[index]
#         peaks = [self_assignment]
#         for neighbor_index in assigned_neighbors[1:]:
#             neighbor_assignment = neighbor_assignments[neighbor_index]
#             while neighbor_index + 1 != neighbor_assignment:
#                 neighbor_index = neighbor_assignment - 1
#                 neighbor_assignment = neighbor_assignments[neighbor_index]
#             peaks.append(neighbor_index)
#         conflicts = [(0, 0)]
#         for i, peak1 in enumerate(peaks[1: -1]):
#             smooth_intensity1 = smooth_intensities[peak1]
#             for peak2 in peaks[i + 2]:
#                 smooth_intensity2 = smooth_intensities[peak2]
#                 if peak1 != peak2:
#                     if smooth_intensity1 > smooth_intensity2:
#                         relative_intensity = smooth_intensity / smooth_intensity2
#                         if relative_intensity >= merge_threshold:
#                             neighbor_assignments[peak2] = neighbor_assignments[peak1]
#                         else:
#                             conflicts.append((peak1, peak2))
#                     else:
#                         relative_intensity = smooth_intensity / smooth_intensity1
#                         if relative_intensity >= merge_threshold:
#                             neighbor_assignments[peak1] = neighbor_assignments[peak2]
#                         else:
#                             conflicts.append((peak1, peak2))
#     neighbor_assignments[index] = self_assignment
#     neighbor_distances[index] = self_distance




@alphatims.utils.njit
def top_down_cluster(
    index,
    smooth_intensities,
    connection_indices,
    connection_indptr,
    merge_threshold,
    neighbor_assignments,
):
    start = connection_indptr[index]
    end = connection_indptr[index + 1]
    potential_assignments = [index + 1]
    intensity = smooth_intensities[index]
    for neighbor_index in connection_indices[start: end]:
        peak_assignment = neighbor_assignments[neighbor_index]
        if peak_assignment != 0:
            peak_index = neighbor_index
            while peak_index + 1 != peak_assignment:
                peak_index = peak_assignment - 1
                peak_assignment = neighbor_assignments[peak_index]
            if potential_assignments[0] == index + 1:
                potential_assignments[0] = peak_assignment
            else:
                peak_intensity = smooth_intensities[peak_index]
                droppable = np.zeros(len(potential_assignments) + 1, dtype=np.bool_)
                for i, potential_assignment in enumerate(potential_assignments):
                    if peak_assignment != potential_assignment:
                        potential_intensity = smooth_intensities[potential_assignment - 1]
                        if potential_intensity > peak_intensity:
                            relative_intensity = intensity / peak_intensity
                            if relative_intensity > merge_threshold:
                                neighbor_assignments[peak_assignment - 1] = potential_assignment
                                droppable[-1] = True
                        else:
                            relative_intensity = intensity / potential_intensity
                            if relative_intensity > merge_threshold:
                                neighbor_assignments[potential_assignment - 1] = peak_assignment
                                droppable[i] = True
                potential_assignments.append(peak_assignment)
                potential_assignments = [
                    potential_assignments[i] for i, to_drop in enumerate(
                        droppable
                    ) if not to_drop
                ]
    if len(potential_assignments) == 1:
        neighbor_assignments[index] = potential_assignments[0]


@alphatims.utils.pjit
def top_down_cluster_all(
    component_index,
    assignment_indices,
    assignment_indptr,
    smooth_intensities,
    connection_indices,
    connection_indptr,
    merge_threshold,
    neighbor_assignments,
    neighbor_distances,
):
    start = assignment_indptr[component_index]
    end = assignment_indptr[component_index + 1]
    selection = assignment_indices[start: end]
    selection = selection[np.argsort(smooth_intensities[selection])][::-1]
    for strike_index in selection:
        alphatims.sandbox.top_down_cluster(
            strike_index,
            smooth_intensities,
            connection_indices,
            connection_indptr,
            merge_threshold,
            neighbor_assignments,
        )
    for index in selection:
        peak_assignment = neighbor_assignments[index]
        if peak_assignment != 0:
            peak_index = index
            while peak_index + 1 != peak_assignment:
                peak_index = peak_assignment - 1
                peak_assignment = neighbor_assignments[peak_index]
        neighbor_assignments[index] = peak_assignment
    # seeds = np.zeros(len(selection), dtype=np.bool_)
    # for i, index in enumerate(selection):
    #     if index + 1 == neighbor_assignments[index]:
    #         seeds[i] = True
    #         neighbor_distances[index] = 0
    # still_to_process = np.flatnonzero(seeds)
    # while len(still_to_process) > 0:
    #     for seed_index in still_to_process:
    #         seeds[seed_index] = False
    #         index = selection[seed_index]
    #         distance = neighbor_distances
    #         start = connection_indptr[index]
    #         end = connection_indptr[index + 1]
    #         # for
    #     still_to_process = np.flatnonzero(seeds)







































def max_frame_gap(data):
    a = np.flatnonzero(
        (
            data.precursor_indices[
                np.repeat(
                    np.arange(data.raw_quad_indptr.shape[0] - 1),
                    np.diff(data.raw_quad_indptr),
                )
            ]==0
        ) & (
            np.diff(data.push_indptr)
        )
    )
    return int(np.ceil(np.max(np.diff(a)) / data.scan_max_index))


def fast_components(
    data,
    frame_range,
    scan_range,
    tof_range,
    push_offsets,
):
    components = np.zeros(len(data), dtype=np.int64)
    alphatims.sandbox.initial_components(
        range(len(push_offsets)),
        data.push_indptr,
        data.tof_indices,
        data.frame_max_index,
        data.scan_max_index,
        data.quad_mz_values,
        frame_range,
        scan_range,
        tof_range,
        push_offsets,
        components,
    )
    components -= 1
    alphatims.sandbox.clean_components(
        range(len(components)),
        components
    )
    component_indices = np.argsort(components)
    component_indptr = np.bincount(components, minlength=len(data) + 1)
    component_indptr[1:] = np.cumsum(component_indptr[:-1])
    component_indptr[0] = 0
    # TODO: sort component_indices?
    return component_indptr, component_indices


@alphatims.utils.pjit(thread_count=1)
def initial_components(
    push_index,
    push_indptr,
    tof_indices,
    frame_max_index,
    scan_max_index,
    quad_mz_values,
    frame_range,
    scan_range,
    tof_range,
    push_offsets,
    components,
):
    self_start_index = push_indptr[push_index]
    self_end_index = push_indptr[push_index + 1]
    if self_start_index == self_end_index:
        return
    for index in range(self_start_index, self_end_index):
        if components[index] == 0:
            components[index] = index + 1
    for other_push_index in get_valid_pushes(
        push_index,
        push_indptr,
        tof_indices,
        frame_max_index,
        scan_max_index,
        quad_mz_values,
        frame_range,
        scan_range,
        push_offsets,
    ):
        cluster_components(
            push_index,
            other_push_index,
            tof_range,
            self_start_index,
            self_end_index,
            tof_indices,
            push_indptr,
            components,
        )


@alphatims.utils.pjit
def set_local_indices(
    component_index,
    component_indptr,
    component_indices,
    local_indices,
):
    start = component_indptr[component_index]
    end = component_indptr[component_index + 1]
    indices = np.sort(component_indices[start: end])
    local_indices[indices] = np.arange(len(indices))


@alphatims.utils.njit
def get_valid_pushes(
    push_index,
    push_indptr,
    tof_indices,
    frame_max_index,
    scan_max_index,
    quad_mz_values,
    frame_range,
    scan_range,
    push_offsets,
):
    valid_pushes = []
    self_scan_index = push_index % scan_max_index
    self_frame_index = push_index // scan_max_index
    self_quad_index = push_offsets[push_index]
    self_quad_low_mz, self_quad_high_mz = quad_mz_values[self_quad_index]
    max_frame = min(self_frame_index + frame_range + 1 , frame_max_index)
    min_scan = max(self_scan_index - scan_range, 0)
    max_scan = min(self_scan_index + scan_range + 1, scan_max_index)
#     TODO in current scan, or assume already centroided?
    for other_scan_index in range(self_scan_index + 1, max_scan):
        other_push_index = self_frame_index * scan_max_index + other_scan_index
        if valid_push(
            other_push_index,
            push_offsets,
            quad_mz_values,
            self_quad_low_mz,
            self_quad_high_mz,
        ):
            valid_pushes.append(other_push_index)
    for other_frame_index in range(self_frame_index + 1, max_frame):
        for other_scan_index in range(min_scan, max_scan):
            other_push_index = other_frame_index * scan_max_index + other_scan_index
            if valid_push(
                other_push_index,
                push_offsets,
                quad_mz_values,
                self_quad_low_mz,
                self_quad_high_mz,
            ):
                valid_pushes.append(other_push_index)
    return valid_pushes


@alphatims.utils.njit(nogil=True)
def valid_push(
    other_push_index,
    push_offsets,
    quad_mz_values,
    self_quad_low_mz,
    self_quad_high_mz,
):
    other_quad_index = push_offsets[other_push_index]
    other_quad_low_mz, other_quad_high_mz = quad_mz_values[other_quad_index]
    #requires at least some overlap
    if other_quad_low_mz > self_quad_high_mz:
        return False
    if self_quad_low_mz > other_quad_high_mz:
        return False
    return True


@alphatims.utils.njit(nogil=True)
def cluster_components(
    self_push_index,
    other_push_index,
    tof_range,
    self_index,
    self_end_index,
    tof_indices,
    push_indptr,
    components,
):
    other_index = push_indptr[other_push_index]
    other_end_index = push_indptr[other_push_index + 1]
    if other_index == other_end_index:
        return
    self_tof_index = tof_indices[self_index]
    self_component = trace_component(self_index, components)
    while True:
        other_tof_index = tof_indices[other_index]
        if self_tof_index > (other_tof_index + tof_range):
            other_index += 1
            if other_index == other_end_index:
                break
        else:
            for i, other_tof_index in enumerate(
                tof_indices[other_index: other_end_index]
            ):
                if other_tof_index > (self_tof_index + tof_range):
                    break
                else:
                    other_component = components[other_index + i]
                    if other_component == 0:
                        components[other_index + i] = self_component
                    else:
                        other_component = trace_component(other_index + i, components)
                        if other_component > self_component:
                            components[other_component - 1] = self_component
                        else:
                            components[self_component - 1] = other_component
                            self_component = other_component
            self_index += 1
            if self_index == self_end_index:
                break
            self_tof_index = tof_indices[self_index]
            self_component = trace_component(self_index, components)


@alphatims.utils.njit(nogil=True)
def trace_component(
    index,
    components,
):
    while index != components[index] - 1:
        index = components[index] - 1
    return components[index]


@alphatims.utils.pjit
def clean_components(
    index,
    components
):
    peak_assignment = components[index]
    peak_index = index
    while peak_index != peak_assignment:
        peak_index = peak_assignment
        peak_assignment = components[peak_index]
    components[index] = peak_assignment



@alphatims.utils.pjit
def split_component(
    component_index,
    component_indptr,
    component_indices,
    scan_max_index,
    frame_max_index,
    push_indptr,
    push_indices,
    push_offsets,
    quad_mz_values,
    tof_indices,
    # clusters,
    frame_range,
    scan_range,
    tof_range,
    intensities,
    assignments,
    local_indices,
    smooth_factor=.25,
    merge_threshold=0.75,
):
    start = component_indptr[component_index]
    end = component_indptr[component_index + 1]
    if end - start == 0:
        return
    if end - start == 1:
        index = component_indices[start]
        assignments[index] = index + 1
        return
    # if end - start > 10**6:
    #     # TODO: Too complex
    #     return
    indices = np.sort(component_indices[start: end])
    # return indices
    connection_indptr, connection_indices = get_component_connections(
        # indices,
        # scan_max_index,
        # push_indices,
        # tof_indices,
        # frame_range,
        # scan_range,
        # tof_range,
        indices,
        push_indptr,
        tof_indices,
        frame_max_index,
        scan_max_index,
        quad_mz_values,
        frame_range,
        scan_range,
        tof_range,
        push_offsets,
        push_indices,
        local_indices,
    )
    smooth_intensities = smoothen_component_intensities(
        indices,
        connection_indptr,
        connection_indices,
        intensities,
        smooth_factor
    )
    local_assignments = split_component_into_clusters(
        connection_indptr,
        connection_indices,
        smooth_intensities,
        merge_threshold,
    )
    for index, assignment in zip(indices, local_assignments):
        if assignment != 0:
            assignments[index] = indices[assignment - 1] + 1
        else:
            assignments[index] = 0
    # return (
    #     indices,
    #     connection_indptr,
    #     connection_indices,
    #     smooth_intensities,
    #     assignments
    # )


# @alphatims.utils.njit
# def get_component_connections(
#     indices,
#     scan_max_index,
#     push_indices,
#     tof_indices,
#     frame_range,
#     scan_range,
#     tof_range,
# ):
#     frames = push_indices[indices] // scan_max_index
#     scans = push_indices[indices] % scan_max_index
#     tofs = tof_indices[indices]
#     connections = []
#     # TODO: check precusor settings?
#     for self_index in range(len(indices) - 1):
#         self_frame = frames[self_index]
#         self_scan = scans[self_index]
#         self_tof = tofs[self_index]
#         for other_index in range(self_index + 1, len(indices)):
#             other_frame = frames[other_index]
#             other_scan = scans[other_index]
#             other_tof = tofs[other_index]
#             if (self_frame + frame_range) < other_frame:
#                 break
#             if (other_scan + scan_range) < self_scan:
#                 continue
#             if (self_scan + scan_range) < other_scan:
#                 continue
#             if (other_tof + tof_range) < self_tof:
#                 continue
#             if (self_tof + tof_range) < other_tof:
#                 continue
#             connections.append(
#                 (self_index, other_index)
#             )
#             connections.append(
#                 (other_index, self_index)
#             )
#     connections = np.array(connections)
#     connection_indptr = np.bincount(
#             connections[:, 0],
#             minlength=len(indices) + 1
#         )
#     connection_indptr[1:] = np.cumsum(connection_indptr[:-1])
#     connection_indptr[0] = 0
#     order = np.argsort(connections[:, 0])
#     connection_indices = connections[order, 1]
#     return connection_indptr, connection_indices


@alphatims.utils.njit
def get_component_connections(
    indices,
    push_indptr,
    tof_indices,
    frame_max_index,
    scan_max_index,
    quad_mz_values,
    frame_range,
    scan_range,
    tof_range,
    push_offsets,
    push_indices,
    local_indices,
):
    connections_list = []
    previous_push_index = -1
    for i, index in enumerate(indices):
        push_index = push_indices[index]
        if previous_push_index == push_index:
            continue
        else:
            previous_push_index = push_index
        self_indices = []
        while i < len(indices):
            other_index = indices[i]
            if push_indices[other_index] != push_index:
                break
            self_indices.append(other_index)
            i += 1
        for other_push_index in get_valid_pushes(
            push_index,
            push_indptr,
            tof_indices,
            frame_max_index,
            scan_max_index,
            quad_mz_values,
            frame_range,
            scan_range,
            push_offsets,
        ):
            other_index = push_indptr[other_push_index]
            other_end_index = push_indptr[other_push_index + 1]
            if other_index == other_end_index:
                continue
            self_offset = 0
            self_index = self_indices[self_offset]
            self_tof_index = tof_indices[self_index]
            while True:
                other_tof_index = tof_indices[other_index]
                # if other_tof_index>200000:
                #     print("self ", self_tof_index)
                #     print("other", other_tof_index)
                # print(self_tof_index, other_tof_index)
                if self_tof_index > (other_tof_index + tof_range):
                    other_index += 1
                    if other_index == other_end_index:
                        break
                else:
                    for i, other_tof_index in enumerate(
                        tof_indices[other_index: other_end_index]
                    ):
                        if other_tof_index > (self_tof_index + tof_range):
                            break
                        else:
                            connections_list.append(
                                (self_index, other_index + i)
                            )
                            connections_list.append(
                                (other_index + i, self_index)
                            )
                    self_offset += 1
                    if self_offset == len(self_indices):
                        break
                    self_index = self_indices[self_offset]
                    self_tof_index = tof_indices[self_index]
    connections = np.array(connections_list)
    # print(connections.dtype, connections.shape)
    # print(local_indices.dtype, local_indices.shape)
    # connections = local_indices[connections]
    connection_indptr = np.bincount(
            local_indices[connections[:, 0]],
            minlength=len(indices) + 1
        )
    connection_indptr[1:] = np.cumsum(connection_indptr[:-1])
    connection_indptr[0] = 0
    order = np.argsort(local_indices[connections[:, 0]])
    connection_indices = local_indices[connections[order, 1]]
    return connection_indptr, connection_indices


@alphatims.utils.njit
def smoothen_component_intensities(
    comonent_indices,
    connection_indptr,
    connection_indices,
    intensities,
    smooth_factor=.25
):
    smooth_intensities = np.empty(len(comonent_indices), dtype=np.float64)
    for index, index_in_component in enumerate(comonent_indices):
        start = connection_indptr[index]
        end = connection_indptr[index + 1]
        if start < end:
            smooth_intensities[index] = intensities[index_in_component] * (1 - smooth_factor)
            indices_in_component = comonent_indices[connection_indices[start: end]]
            smooth_intensities[index] += np.sum(
                intensities[indices_in_component]
            ) / (end - start) * smooth_factor
        else:
            smooth_intensities[index] = intensities[index_in_component]
    return smooth_intensities


@alphatims.utils.njit
def split_component_into_clusters(
    connection_indptr,
    connection_indices,
    smooth_intensities,
    merge_threshold=0.75,
):
    assignments = np.zeros(len(connection_indptr) - 1, dtype=np.int64)
    order = np.argsort(smooth_intensities)[::-1]
    for index in order:
        start = connection_indptr[index]
        end = connection_indptr[index + 1]
        potential_assignments = [index + 1]
        intensity = smooth_intensities[index]
        for neighbor_index in connection_indices[start: end]:
            peak_assignment = assignments[neighbor_index]
            if peak_assignment != 0:
                peak_index = neighbor_index
                while peak_index + 1 != peak_assignment:
                    peak_index = peak_assignment - 1
                    peak_assignment = assignments[peak_index]
                if potential_assignments[0] == index + 1:
                    potential_assignments[0] = peak_assignment
                else:
                    peak_intensity = smooth_intensities[peak_index]
                    droppable = np.zeros(len(potential_assignments) + 1, dtype=np.bool_)
                    for i, potential_assignment in enumerate(potential_assignments):
                        if peak_assignment != potential_assignment:
                            potential_intensity = smooth_intensities[potential_assignment - 1]
                            if potential_intensity > peak_intensity:
                                relative_intensity = intensity / peak_intensity
                                if relative_intensity > merge_threshold:
                                    assignments[peak_assignment - 1] = potential_assignment
                                    droppable[-1] = True
                            else:
                                relative_intensity = intensity / potential_intensity
                                if relative_intensity > merge_threshold:
                                    assignments[potential_assignment - 1] = peak_assignment
                                    droppable[i] = True
                    potential_assignments.append(peak_assignment)
                    potential_assignments = [
                        potential_assignments[i] for i, to_drop in enumerate(
                            droppable
                        ) if not to_drop
                    ]
        if len(potential_assignments) == 1:
            assignments[index] = potential_assignments[0]
        # TODO: else ?
    for index in order:
        peak_assignment = assignments[index]
        if peak_assignment != 0:
            peak_index = index
            while peak_index + 1 != peak_assignment:
                peak_index = peak_assignment - 1
                peak_assignment = assignments[peak_index]
        assignments[index] = peak_assignment
    return assignments
