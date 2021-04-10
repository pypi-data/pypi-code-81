import sys
import logging
import numpy as np
from scipy import linalg
import pandas as pd
import time
from gmat.process_plink.process_plink import impute_geno
from pysnptools.snpreader import Bed
from tqdm import tqdm


def output_mat(mat, id_df, out_file, out_fmt):
    if out_fmt == 'mat':
        np.savetxt(out_file + '.mat_fmt', mat)
    elif out_fmt == 'row_col_val':
        ind = np.tril_indices_from(mat)
        df = pd.DataFrame({
            "row": ind[0]+1,
            "col": ind[1]+1,
            "val": mat[ind]
        })
        df.to_csv(out_file + '.ind_fmt', sep=' ', index=False, header=False, columns=["row", "col", "val"])
    elif out_fmt == 'id_id_val':
        id = np.array(id_df)
        ind = np.tril_indices_from(mat)
        df = pd.DataFrame({
            "id0": id[ind[0]],
            "id1": id[ind[1]],
            "val": mat[ind]
        })
        df.to_csv(out_file + '.id_fmt', sep=' ', index=False, header=False, columns=["id0", "id1", "val"])
    else:
        logging.error('The output format {} is not recognized, please check!'.format(out_fmt))
        sys.exit()
    return 1


def agmat(bed_file, out_file, inv=False, out_fmt='mat', npart=10, small_val=0.001):
    """
    additive genomic relationship matrix and its inversion
    :param bed_file: The prefix for plink binary file
    :param out_file: the prefix for the output file
    :param inv: Whether to calculate the inversion. Default value is True
    :param out_fmt: the output format. mat: matrix format (default); row_col_val: row-column-value format;
    id_id_val: id-id-value format.
    :param npart: the number of part. If memory is not enough, please increase the value.
    :param small_val: A small vale added to the diagonal to grant the positive definite. Default value is 0.001.
    :return: return numpy array for genomic relationship matrix and its inversion. Output the matrixes into the file
    with prefix of out_file.
    """
    logging.info("{:#^80}".format("Read the SNP and calculate"))
    snp_on_disk = Bed(bed_file, count_A1=False)
    num_snp = snp_on_disk.sid_count
    num_id = snp_on_disk.iid_count
    logging.info("There are {} individuals, {} SNPs.".format(num_id, num_snp))
    snp_index = []
    for i in range(npart):
        snp_index.append(int(num_snp/npart)*i)
    snp_index.append(num_snp)
    clock_t0 = time.perf_counter()
    cpu_t0 = time.process_time()
    scale = 0.0
    kin = np.zeros((num_id, num_id))
    for i in tqdm(range(npart)):
        snp_mat = snp_on_disk[:, snp_index[i]:snp_index[i+1]].read().val
        if np.any(np.isnan(snp_mat)):
            snp_mat = impute_geno(snp_mat)
        freq = np.sum(snp_mat, axis=0) / (2 * num_id)
        freq.shape = (1, -1)
        scale += np.sum(2 * freq * (1 - freq))  # scale factor
        snp_mat = snp_mat - 2 * freq
        kin += np.dot(snp_mat, snp_mat.T)
    kin = kin / scale
    kin_diag = np.diag(kin)
    kin_diag = kin_diag + kin_diag * small_val
    np.fill_diagonal(kin, kin_diag)
    clock_t1 = time.perf_counter()
    cpu_t1 = time.process_time()
    logging.info("Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0, cpu_t1 - cpu_t0))
    logging.info("{:#^80}".format("Output"))
    fam_info = pd.read_csv(bed_file + '.fam', sep='\s+', header=None)
    logging.info("The prefix of output file is " + out_file)
    fam_info.iloc[:, 1].to_csv(out_file + '.id', index=False, header=False, sep=' ')
    output_mat(kin, fam_info.iloc[:, 1], out_file + '.agrm', out_fmt)
    kin_inv = None
    if inv:
        logging.info("{:#^80}".format("Calculate the inversion of kinship"))
        clock_t0 = time.perf_counter()
        cpu_t0 = time.process_time()
        kin_inv = linalg.inv(kin)
        clock_t1 = time.perf_counter()
        cpu_t1 = time.process_time()
        logging.info("Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0,
                                                                                   cpu_t1 - cpu_t0))
        logging.info("{:#^80}".format("Output the inversion"))
        logging.info("The prefix of output file is: " + out_file)
        output_mat(kin_inv, fam_info.iloc[:, 1], out_file + '.agiv', out_fmt)
    return kin, kin_inv


def agmat_dosage(geno_file, out_file, inv=False, out_fmt='mat', npart=10, small_val=0.001):
    """
    additive genomic relationship matrix and its inversion using dosage genotype.
    :param geno_file: dosage genotype file. The first row is the individual id. The dosage genotype of each individual
    is saved from the second row.
    :param out_file: the prefix for the output file
    :param inv: Whether to calculate the inversion. Default value is True
    :param out_fmt: the output format. mat: matrix format (default); row_col_val: row-column-value format;
    id_id_val: id-id-value format.
    :param npart: the number of part. If memory is not enough, please increase the value.
    :param small_val: A small vale added to the diagonal to grant the positive definite. Default value is 0.001.
    :return: return numpy array for genomic relationship matrix and its inversion. Output the matrixes into the file
    with prefix of out_file.
    """
    logging.info("{:#^80}".format("Read the SNP and calculate"))
    num_snp = 0
    with open(geno_file, 'r') as fin:
        line = fin.readline()
        id = line.split()
        for _ in fin:
            num_snp += 1
    num_id = len(id)
    np.savetxt(out_file + '.id', np.array(id).reshape(-1, 1), fmt="%s")
    logging.info("There are {} individuals, {} SNPs.".format(num_id, num_snp))
    snp_index = []
    for i in range(npart):
        snp_index.append(int(num_snp/npart)*i)
    snp_index.append(num_snp)
    clock_t0 = time.perf_counter()
    cpu_t0 = time.process_time()
    scale = 0.0
    kin = np.zeros((num_id, num_id))
    for i in tqdm(range(npart)):
        snp_mat = np.loadtxt(geno_file, skiprows=snp_index[i]+1, max_rows=snp_index[i+1]-snp_index[i])
        snp_mean = np.mean(snp_mat, axis=1).reshape(-1, 1)
        snp_var = np.var(snp_mat, axis=1)
        scale += np.sum(snp_var)  # scale factor
        snp_mat = snp_mat - snp_mean
        kin += np.dot(snp_mat.T, snp_mat)
    kin = kin / scale
    kin_diag = np.diag(kin)
    kin_diag = kin_diag + kin_diag * small_val
    np.fill_diagonal(kin, kin_diag)
    clock_t1 = time.perf_counter()
    cpu_t1 = time.process_time()
    logging.info("Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0, cpu_t1 - cpu_t0))
    logging.info("{:#^80}".format("Output"))
    output_mat(kin, id, out_file + '.agrm', out_fmt)
    kin_inv = None
    if inv:
        logging.info("{:#^80}".format("Calculate the inversion of kinship"))
        clock_t0 = time.perf_counter()
        cpu_t0 = time.process_time()
        kin_inv = linalg.inv(kin)
        clock_t1 = time.perf_counter()
        cpu_t1 = time.process_time()
        logging.info("Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0,
                                                                                   cpu_t1 - cpu_t0))
        logging.info("{:#^80}".format("Output the inversion"))
        logging.info("The prefix of output file is: " + out_file)
        output_mat(kin_inv, id, out_file + '.agiv', out_fmt)
    return kin, kin_inv


def dgmat_as(bed_file, out_file, inv=False, out_fmt='mat', npart=10, small_val=0.001):
    """
    dominance genomic relationship matrix and its inversion
    :param bed_file: The prefix for plink binary file
    :param out_file: the prefix for the output file
    :param inv: Whether to calculate the inversion. Default value is True
    :param out_fmt: the output format. mat: matrix format (default); row_col_val: row-column-value format;
    id_id_val: id-id-value format.
    :param npart: the number of part. If memory is not enough, please increase the value.
    :param small_val: A small vale added to the diagonal to grant the positive definite. Default value is 0.001.
    :return: return numpy array for genomic relationship matrix and its inversion. Output the matrixes into the file
    with prefix of out_file.
    """
    logging.info("{:#^80}".format("Read the SNP and calculate"))
    snp_on_disk = Bed(bed_file, count_A1=False)
    num_snp = snp_on_disk.sid_count
    num_id = snp_on_disk.iid_count
    logging.info("There are {} individuals, {} SNPs.".format(num_id, num_snp))
    snp_index = []
    for i in range(npart):
        snp_index.append(int(num_snp / npart) * i)
    snp_index.append(num_snp)
    clock_t0 = time.perf_counter()
    cpu_t0 = time.process_time()
    scale = 0.0
    kin = np.zeros((num_id, num_id))
    for i in tqdm(range(npart)):
        snp_mat = snp_on_disk[:, snp_index[i]:snp_index[i + 1]].read().val
        if np.any(np.isnan(snp_mat)):
            snp_mat = impute_geno(snp_mat)
        freq = np.sum(snp_mat, axis=0) / (2 * num_id)
        freq.shape = (1, -1)
        scale_vec = 2 * freq * (1 - freq)
        scale += np.sum(scale_vec * (1 - scale_vec))
        snp_mat[snp_mat > 1.5] = 0.0
        snp_mat = snp_mat - scale_vec
        kin += np.dot(snp_mat, snp_mat.T)
    kin = kin / scale
    kin_diag = np.diag(kin)
    kin_diag = kin_diag + kin_diag * small_val
    np.fill_diagonal(kin, kin_diag)
    clock_t1 = time.perf_counter()
    cpu_t1 = time.process_time()
    logging.info(
        "Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0, cpu_t1 - cpu_t0))
    logging.info("{:#^80}".format("Output"))
    fam_info = pd.read_csv(bed_file + '.fam', sep='\s+', header=None)
    logging.info("The prefix of output file is " + out_file)
    fam_info.iloc[:, 1].to_csv(out_file + '.id', index=False, header=False, sep=' ')
    output_mat(kin, fam_info.iloc[:, 1], out_file + '.dgrm_as', out_fmt)
    kin_inv = None
    if inv:
        logging.info("{:#^80}".format("Calculate the inversion of kinship"))
        clock_t0 = time.perf_counter()
        cpu_t0 = time.process_time()
        kin_inv = linalg.inv(kin)
        clock_t1 = time.perf_counter()
        cpu_t1 = time.process_time()
        logging.info("Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0,
                                                                                   cpu_t1 - cpu_t0))
        logging.info("{:#^80}".format("Output the inversion"))
        logging.info("The prefix of output file is: " + out_file)
        output_mat(kin_inv, fam_info.iloc[:, 1], out_file + '.dgiv_as', out_fmt)
    return kin, kin_inv
