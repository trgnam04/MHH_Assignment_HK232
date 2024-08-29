from itertools import combinations_with_replacement
import time

def count_pattern_usage(formatted_patterns, cut_list):
    pattern_count = {i: 0 for i in range(len(formatted_patterns))}
    
    for cut in cut_list:
        for i, pattern in enumerate(formatted_patterns):
            if cut == pattern:
                pattern_count[i] += 1
    
    pattern_usage_list = [pattern_count[i] for i in range(len(formatted_patterns))]
    
    return pattern_usage_list

def calculate_total_leftover(cut_list):
    total_leftover = 0
    for pattern in cut_list:
        total_leftover += pattern['leftover']
    return total_leftover     

# Greedy procedure
def solve_greedy(lengths, quantities, stock_length):
    remaining_stock = stock_length
    pattern = [0] * len(lengths)
    
    sorted_items = sorted(range(len(lengths)), key=lambda i: lengths[i], reverse=True)
    
    for i in sorted_items:
        while remaining_stock >= lengths[i] and quantities[i] > 0:
            pattern[i] += 1
            quantities[i] -= 1
            remaining_stock -= lengths[i]
    
    leftover = remaining_stock
    return pattern, leftover

def greedy_cutting(lengths, quantities, stock_lengths):
    if len(lengths) != len(quantities):
        raise ValueError("Input Error: the length of item demand list are different from the lenght of item list")
    if max(lengths) > max(stock_lengths):
        raise ValueError("Input Error: One or more item is longer than the maximum length of the stock.")
    cut_list = []
    remaining_quantities = quantities[:]
    
    while sum(remaining_quantities) > 0 and len(stock_lengths) > 0:
        solutions = []
        for stock_length in stock_lengths:
            temp_quantities = remaining_quantities[:]
            pattern, leftover = solve_greedy(lengths, temp_quantities, stock_length)
            solutions.append((pattern, stock_length, leftover))
            
        selected_pattern, selected_stock_length, selected_leftover = min(solutions, key=lambda x: x[2])
        
        can_cut = True
        while can_cut:
            for i in range(len(lengths)):
                if remaining_quantities[i] < selected_pattern[i]:
                    can_cut = False
                    break
            
            if can_cut:
                for i in range(len(lengths)):
                    remaining_quantities[i] -= selected_pattern[i]
                
                cut_list.append({"stock": selected_stock_length, "cuts": {i: selected_pattern[i] for i in range(len(selected_pattern))}, "leftover": selected_leftover})
        
    return cut_list, remaining_quantities

def summarize_list(elements):
    if not elements:
        return []

    summary = []
    current_element = elements[0]
    count = 1
    
    for elem in elements[1:]:
        if elem == current_element:
            count += 1
        else:
            summary.append(f"use {{'stock': {current_element['stock']}, 'cuts': {current_element['cuts']}, 'leftover': {current_element['leftover']}}} {count} times")
            current_element = elem
            count = 1
    
    summary.append(f"use {{'stock': {current_element['stock']}, 'cuts': {current_element['cuts']}, 'leftover': {current_element['leftover']}}} {count} times")
    
    return summary

def read_input_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        
    lengths = list(map(int, lines[0].strip().split(',')))
    quantities = list(map(int, lines[1].strip().split(',')))
    stock_lengths = list(map(int, lines[2].strip().split(',')))
    
    return lengths, quantities, stock_lengths

def write_output_file(file_path, cut_list, summarize_lst, remaining_quantities, total_time):
    with open(file_path, "w") as file:
        file.write("All patterns need to use:\n")
        for pattern in cut_list:
            file.write(f"{pattern}\n")
            
        file.write("\nSummarize:\n")
        for tmp in summarize_lst:
            file.write(f"{tmp}\n")

        file.write(f"\nRemaining quantities: {remaining_quantities}\n")
        file.write(f"Sum of leftover: {calculate_total_leftover(cut_list)}\n")
        file.write(f"Total time (greedy): {total_time} sec\n")
        file.write(f"Total stock (greedy): {len(cut_list)}\n")

if __name__ == "__main__":
    
    input_file_names = [f"Appendix_problem_{i}" for i in range(1, 11)]
    output_file_names = [f"Appendix_problem_{i}" for i in range(1, 11)]

    for input_file_name, output_file_name in zip(input_file_names, output_file_names):
        input_path = f"./input/{input_file_name}.txt"
        output_path = f"./output/Greedy_{output_file_name}_output.txt"
        
        lengths, quantities, stock_lengths = read_input_file(input_path)
        min_length = min(lengths)
        
        start_time_greedy = time.time()
        greedy_cut_list, greedy_remaining_quantities = greedy_cutting(lengths, quantities, stock_lengths[:])
        end_time_greedy = time.time()
        
        total_time = end_time_greedy - start_time_greedy
        summarize_lst = summarize_list(greedy_cut_list)
        
        write_output_file(output_path, greedy_cut_list, summarize_lst, greedy_remaining_quantities, total_time)
    
    input_file_names = [f"Appendix_problem_{i}a" for i in range(1, 11)]
    output_file_names = [f"Appendix_problem_{i}a_output" for i in range(1, 11)]

    for input_file_name, output_file_name in zip(input_file_names, output_file_names):
        input_path = f"./input/{input_file_name}.txt"
        output_path = f"./output/Greedy_{output_file_name}.txt"
        
        lengths, quantities, stock_lengths = read_input_file(input_path)
        min_length = min(lengths)
        
        start_time_greedy = time.time()
        greedy_cut_list, greedy_remaining_quantities = greedy_cutting(lengths, quantities, stock_lengths[:])
        end_time_greedy = time.time()
        
        total_time = end_time_greedy - start_time_greedy
        summarize_lst = summarize_list(greedy_cut_list)
        
        write_output_file(output_path, greedy_cut_list, summarize_lst, greedy_remaining_quantities, total_time)
    
    input_file_name =  "caseStudy"
    output_file_name = "Greedy_caseStudy_output"
    input_path = f"./input/{input_file_name}.txt"
    output_path = f"./output/{output_file_name}.txt"

    lengths, quantities, stock_lengths = read_input_file(input_path)
    min_length = min(lengths)
    
    start_time_greedy = time.time()
    greedy_cut_list, greedy_remaining_quantities = greedy_cutting(lengths, quantities, stock_lengths[:])
    end_time_greedy = time.time()
    
    total_time = end_time_greedy - start_time_greedy
    summarize_lst = summarize_list(greedy_cut_list)
    
    write_output_file(output_path, greedy_cut_list, summarize_lst, greedy_remaining_quantities, total_time)