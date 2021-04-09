'''
Utility data structures
Written by Emanuel Ramirez (emanuel2718@gmail.com)
'''


def get_available_colors():
    ''' Returns the a list of available pygments.styles colorschemes

    NOTE:   Can't be a hardcoded list of selected colorschemes because
            some colorschemes are added by external plugins.
            Plus some colors are not available in all Operating systems.

    '''
    from pygments.styles import get_all_styles
    return list(get_all_styles())


'''
    ALGORITHMS configuration

    key: user input algorithm flag
    value[0]:  Rosseta Code algorithms format
    value[1]:  Formal algorithm name to be displayed as output title
'''
ALGORITHMS = {
    'astar': ['A*_search_algorithm', 'A* Search algorithm'],
    'avltrees': ['AVL_tree', 'AVL Trees'],
    'b64': ['Base64_decode_data', 'Decode Base64 data'],
    'beadsort': ['Sorting_algorithms/Bead_sort', 'Bead Sort algorithm'],
    'binarysearch': ['Binary_search', 'Binary Search algorithm'],
    'bogosort': ['Sorting_algorithms/Bogosort', 'Bogo Sort algorithm'],
    'bubblesort': ['Sorting_algorithms/Bubble_sort', 'Bubble Sort algorithm'],
    'caesarcipher': ['Caesar_cipher', 'Caesar Cipher'],
    'cocktailsort': ['Sorting_algorithms/Cocktail_sort', 'Cocktail Sort algorithm'],
    'combsort': ['Sorting_algorithms/Comb_sort', 'Comb Sort algorithm'],
    'countingsort': ['Sorting_algorithms/Counting_sort', 'Counting Sort algorithm'],
    'cyclesort': ['Sorting_algorithms/Cycle_sort', 'Cycle Sort algorithm'],
    'damm': ['Damm_algorithm', 'Damm algorithm'],
    'dijkstra': ['Dijkstra%27s_algorithm', 'Dijkstra algorithm'],
    'e': ['Calculating_the_value_of_e', 'Calculate the value of e'],
    'eulermethod': ['Euler_method', 'Euler method'],
    'evolutionary': ['Evolutionary_algorithm', 'Evolutionary algorithm'],
    'factorial': ['Factorial', 'Calculate factorials'],
    'factorions': ['Factorions', 'Calculate factorions'],
    'fft': ['Fast_Fourier_transform', 'Fast Fourier Transforms'],
    'fib': ['Fibonacci_sequence', 'Fibonacci Sequence'],
    'fibnstep': ['Fibonacci_n-step_number_sequences', 'Fibonacci N-step Number Sequence'],
    'fileexists': ['Check_that_file_exists', 'Check if a given file exists or not'],
    'fizzbuzz': ['FizzBuzz', 'FizzBuzz'],
    'floydwarshall': ['Floyd-Warshall_algorithm', 'Floy Warshall algorithm'],
    'gnomesort': ['Sorting_algorithms/Gnome_sort', 'Gnome Sort algorithm'],
    'hammingnumbers': ['Hamming_numbers', 'Hamming numbers'],
    'heapsort': ['Sorting_algorithms/Heapsort', 'Heap Sort algorithm'],
    'helloworld': ['Hello_world/Text', 'Print Hello world in the given language'],
    'huffman': ['Huffman_coding', 'Huffman coding'],
    'insertionsort': ['Sorting_algorithms/Insertion_sort', 'Insertion Sort algorithm'],
    'isaac': ['The_ISAAC_Cipher', 'ISAAC Cipher'],
    'knapsack': ['Knapsack_problem/0-1', 'Knapsack Problem 0-1'],
    'knapsackbound': ['Knapsack_problem/Bounded', 'Knapsack Problem Bounded'],
    'knapsackcont': ['Knapsack_problem/Continous', 'Knapsack Problem Continous'],
    'knapsackunbound': ['Knapsack_problem/Unbounded', 'Knapsack Problem Unbounded'],
    'kolakoski': ['Kolakoski_sequence', 'Kolakoski Sequence'],
    'mandelbrot': ['Mandelbrot_set', 'Mandelbrot Set'],
    'mazegen': ['Maze_generation', 'Maze Generation'],
    'mazesolve': ['Maze_solving', 'Maze Solving'],
    'md4': ['MD4', 'How to use MD4'],
    'md5': ['MD5', 'How to use MD5'],
    'md5imp': ['MD5/Implementation', 'MD5 Algorithm implementation'],
    'mergesort': ['Sorting_algorithms/Merge_sort', 'Merge Sort algorithm'],
    'nqueen': ['N-queens_problem', 'N-Queens Problem'],
    'pancakesort': ['Sorting_algorithms/Pancake_sort', 'Pancake Sort algorithm'],
    'patiencesort': ['Sorting_algorithms/Patience_sort', 'Patience Sort algorithm'],
    'permutationsort': ['Sorting_algorithms/Permutation_sort', 'Permutation Sort algorithm'],
    'quickselect': ['Quickselect_algorithm', 'Quickselect Algorithm'],
    'quicksort': ['Sorting_algorithms/Quicksort', 'Quick Sort algorithm'],
    'radixsort': ['Sorting_algorithms/Radix_sort', 'Radix Sort algorithm'],
    'recaman': ['Recaman%27s_sequence', 'Recaman Sequence'],
    'regex': ['Regular_expressions', 'Simple Regular Expressions'],
    'rot13': ['Rot-13', 'Rot-13 Algorithm'],
    'rsa': ['RSA_code', 'RSA code'],
    'selectionsort': ['Sorting_algorithms/Selection_sort', 'Selection Sort algorithm'],
    'sexyprime': ['Sexy_primes', 'Sexy primes'],
    'sha1': ['SHA-1', 'SHA-1 Algorithm'],
    'sha256': ['SHA-256', 'SHA-256 Algorithm'],
    'shellsort': ['Sorting_algorithms/Shell_sort', 'Shell Sort algorithm'],
    'sieve': ['Sieve_of_Eratosthenes', 'Sieve of Eratosthenes Algorithm'],
    'sleepsort': ['Sorting_algorithms/Sleep_sort', 'Sleep Sort algorithm'],
    'stoogesort': ['Sorting_algorithms/Stooge_sort', 'Stooge Sort algorithm'],
    'strandsort': ['Sorting_algorithms/Strand_sort', 'Strand Sort algorithm'],
    'subcipher': ['Substitution_cipher', 'Substitution Cipher'],
    'toposort': ['Topological_sort', 'Topological Sort Algorithm']
}


'''
    SUPPORTED_LANGUAGE configuration

    key: user input language flag
    value[0]:  Rosseta Code language format
    value[1]:  Formal language name to be displayed as output title
'''
SUPPORTED_LANGUAGES = {
    'actionscript': ['ActionScript', 'Actionscript'],
    'ada': ['Ada', 'Ada'],
    'algol68': ['ALGOL_68', 'ALGOL68'],
    'applescript': ['AppleScript', 'Applescript'],
    'autohotkey': ['AutoHotkey', 'Autohotkey'],
    'awk': ['AWK', 'AWK'],
    'c': ['C', 'C'],
    'cpp': ['C.2B.2B', 'C++'],
    'csharp': ['C.23', 'C#'],
    'd': ['D', 'D'],
    'delphi': ['Delphi', 'Delphi'],
    'fsharp': ['F.23', 'F#'],
    'eiffel': ['Eiffel', 'Eiffel'],
    'fortran': ['Fortran', 'Fortran'],
    'go': ['Go', 'Go'],
    'haskell': ['Haskell', 'Haskell'],
    'objc': ['Objective-C', 'Objective-C'],
    'java': ['Java', 'Java'],
    'javascript': ['JavaScript', 'Javascript'],
    'lua': ['Lua', 'Lua'],
    'matlab': ['MATLAB', 'Matlab'],
    'ocaml': ['Ocaml', 'Ocaml'],
    'pascal': ['Pascal', 'Pascal'],
    'perl': ['Perl', 'Perl'],
    'php': ['PHP', 'PHP'],
    'powershell': ['PowerShell', 'PowerShell'],
    'python': ['Python', 'Python'],
    'ruby': ['Ruby', 'Ruby'],
    'rust': ['Rust', 'Rust'],
    'scala': ['Scala', 'Scala'],
    'swift': ['Swift', 'Swift']

}

if __name__ == '__main__':
     print('This file is not intended to be called by the user. See algocli --help')
