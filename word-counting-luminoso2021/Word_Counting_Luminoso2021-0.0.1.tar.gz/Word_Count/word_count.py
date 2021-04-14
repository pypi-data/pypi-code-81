"""
This main word_count function will

1. Read-in the text file
2. Send line by line to count function for word counting of each line
3. Create total counts dictionary by combining each word counting results
4. Check whether user want the JSON format or Human readable format
5. Return the result with correct format for users

"""
import sys


def word_count(file, out_format="Basic"):
    from count import word_counting
    import collections
    import json

    # Reading the file, count using word_counting line by line,
    # create the sorted dictionary(sort by value(DESC) first, then key(ASC) next)
    reading_file = open(file, 'r')
    total_counts = dict()
    for line in reading_file:
        counts = word_counting(line)
        for key in counts:
            if key in total_counts.keys():
                total_counts[key] += counts[key]
            else:
                total_counts[key] = counts[key]
    sorted_total_counts = sorted(total_counts.items(), key=lambda kv: (-kv[1], kv[0]), reverse=False)
    sorted_total_counts = collections.OrderedDict(sorted_total_counts)

    # check out the desired output format, print out accordingly
    if out_format.upper() == "JSON":
        print(json.dumps(sorted_total_counts))
        return json.dumps(sorted_total_counts)

    else:
        d = collections.Counter(sorted_total_counts)
        d.most_common()
        # for human readable format, I assume most common means top 10 words
        for k, v in d.most_common(10):
            print('%s - %i' % (k, v))
        return '%s - %i' % (k, v)


# calling the function from terminal
if __name__ == "__main__":
    file_name = sys.argv[1]
    if len(sys.argv) == 3:
        out_format = sys.argv[2]
    else:
        out_format = "Basic"
    word_count(file_name, out_format)
