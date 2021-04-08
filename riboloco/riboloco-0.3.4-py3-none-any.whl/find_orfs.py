import re
import pandas as pd
from riboloco.shared_riboloco_functions import read_fasta, read_info_file
import argparse


def find_all_orfs(fasta, info, max_tx=1_000_000):
    """
    Finds all ORFs with canonical start codon and stops codons. Values are 1 based!
    """
    cds_start_dict = {}
    for transcript_id, cds_start in zip(info["transcript_id"], info["cds_start"]):
        cds_start_dict[transcript_id] = cds_start

    counter = 0

    for tx_id, tx_seq in fasta.items():
        cds_start = cds_start_dict[tx_id]
        starts = [m.start() for m in re.finditer('ATG', tx_seq)]  # 0 based
        starts1 = [a + 1 for a in starts]

        stops = [m.start() + 1 for m in re.finditer('TGA', tx_seq)]  # first nt of stop codon
        stops += [m.start() + 1 for m in re.finditer('TAA', tx_seq)]
        stops += [m.start() + 1 for m in re.finditer('TAG', tx_seq)]

        start_frames_list = [(a - cds_start) % 3 for a in starts1]
        start_frames = {}
        for start, frame in zip(starts1, start_frames_list):
            start_frames[start] = frame

        stop_frames_list = [(a - cds_start) % 3 for a in stops]
        stop_frames = {}
        for stop, frame in zip(stops, stop_frames_list):
            stop_frames[stop] = frame

        first_stop = {}
        for start in starts1:
            z = [100_000_000]
            try:
                first_stop[start] = min(z + [a for a in stops if a > start and start_frames[start] == stop_frames[a]])
            except KeyError:
                print(start)
                print([a for a in stops if a not in stop_frames.keys()])
                print(start_frames)
                print(stop_frames)
                assert 1 == 0

        all_linked_starts = {}
        furthest_starts = {}
        for start, stop in first_stop.items():
            try:
                all_linked_starts[stop].append(start)
            except KeyError:
                all_linked_starts[stop] = [start]

        annotated_start = int(info[info["transcript_id"] == tx_id].cds_start)

        frames = []
        annotated = []
        for stop, starts in all_linked_starts.items():
            if stop != 100_000_000:
                furthest_starts[stop] = min(starts)
                frames.append((min(starts) - annotated_start) % 3)
                annotated.append(min(starts) == annotated_start)

        this_df = pd.DataFrame.from_dict({"transcript_id": tx_id, "orf_start": furthest_starts.values(),
                                          "orf_stop": furthest_starts.keys(),
                                          "orf_frame": frames, "annotated": annotated})

        if counter == 0:
            orf_df = this_df
            counter += 1
        else:
            orf_df = orf_df.append(this_df)
            counter += 1

        if counter >= max_tx:
            break

        if counter % 1000 == 0:
            print(str(counter) + " transcripts searched for ORFs")

    return orf_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fasta", required=True, type=str, help="Transciptome fasta - can be generated with "
                                                                       "riboloco_convert_gff")
    parser.add_argument("-i", "--info", required=True, type=str, help="A info file with transcript details - can "
                                                                      "also be generated with riboloco_convert_gff")
    parser.add_argument("-d", "--output_directory", type=str, required=False, default="",
                        help="The directory to save outputs.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file")
    args = parser.parse_args()

    fasta_d = read_fasta(args.fasta)
    info = read_info_file(args.info)
    orf_df = find_all_orfs(fasta_d, info)
    print("Saving orf file")
    orf_df.to_csv(args.output_directory + args.output + '.orf_file.csv', index=False)
    print("Complete")


if __name__ == '__main__':
    main()