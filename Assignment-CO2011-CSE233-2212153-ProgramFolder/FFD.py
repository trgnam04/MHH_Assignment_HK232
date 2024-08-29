from itertools import combinations_with_replacement
import time, copy
# Tạo tất cả tập hợp với 1 thanh
def generate_patterns_for_stock(lengths, quantities, stock_length, min_length):
    valid_patterns = []
    
    for i in range(1, max(stock_lengths)//min(lengths) + 1):
        # tạo tất cả tổ hợp
        all_combinations = combinations_with_replacement(range(len(lengths)), i)
        for comb in all_combinations:
            new_remaining_quantities = quantities[:]
            pattern = [0] * len(lengths)
            total_length = 0
            valid = True
            
            # duyệt qua index
            for index in comb:
                pattern[index] += 1
                total_length += lengths[index]
                
                # kiểm tra chiều dài
                if total_length > stock_length:
                    valid = False
                    break
                
                # kiểm tra số lượng
                if pattern[index] > quantities[index]:
                    valid = False
                    break
                else:
                    new_remaining_quantities[index] -= 1
            
            # phần dư
            leftover_length = stock_length - total_length
            
            # nếu hợp lệ thì append
            if valid and (leftover_length < min_length or sum(new_remaining_quantities) == 0):
                if (pattern, stock_length, leftover_length) not in valid_patterns:
                    valid_patterns.append((pattern, stock_length, leftover_length))
    
    return valid_patterns

# Tạo với nhiều thanh
def generate_all_patterns(lengths, quantities, stock_lengths, min_length):
    if len(lengths) != len(quantities):
        raise ValueError("Input Error: the length of item demand list are different from the lenght of item list")
    if max(lengths) > max(stock_lengths):
        raise ValueError("Input Error: One or more item is longer than the maximum length of the stock.")
    all_patterns = []
    for stock_length in stock_lengths:
        patterns = generate_patterns_for_stock(lengths, quantities, stock_length, min_length)
        all_patterns.extend(patterns)
    return all_patterns

# Filter patterns with minimal leftover length
def filter_min_leftover_patterns(patterns):
    min_leftover = min(pattern[2] for pattern in patterns)
    return [pattern for pattern in patterns if pattern[2] == min_leftover]

# Sort patterns by cut priority
def sort_patterns_by_cut_priority(patterns, lengths):
    sorted_lengths = sorted(range(len(lengths)), key=lambda x: lengths[x], reverse=True)
    
    def pattern_priority(pattern):
        return tuple(pattern[0][i] for i in sorted_lengths)
    
    sorted_patterns = sorted(patterns, key=pattern_priority, reverse=True)
    return sorted_patterns

# Cut materials using patterns
def cut_materials(lengths, quantities, sorted_patterns):
    cut_list = []
    remaining_quantities = quantities[:]
    
    for pattern, stock_length, _ in sorted_patterns:
        can_cut = True
        
        # Lặp qua từng phần cắt trong pattern
        while can_cut:
            for i in range(len(lengths)):
                if remaining_quantities[i] < pattern[i]:
                    can_cut = False
                    break
            
            if can_cut:
                for i in range(len(lengths)):
                    remaining_quantities[i] -= pattern[i]
                
                cut_list.append((pattern, stock_length, stock_length - sum(pattern[i] * lengths[i] for i in range(len(lengths)))))
    
    return cut_list, remaining_quantities

# Remove zero entries from lengths and quantities
def remove_zero_entries(lengths, quantities):
    non_zero_indices = [i for i, qty in enumerate(quantities) if qty != 0]
    filtered_lengths = [lengths[i] for i in non_zero_indices]
    filtered_quantities = [quantities[i] for i in non_zero_indices]
    return filtered_lengths, filtered_quantities

# Cut until all quantities are zero
def cut_until_zero(lengths, quantities, stock_lengths):
    cut_list = []
    remaining_quantities = quantities[:]    
    remaining_lengths = lengths[:]
    
    while sum(remaining_quantities) > 0:
        idx_lst = [i for i, qty in enumerate(remaining_quantities) if qty == 0]
        remaining_lengths, remaining_quantities = remove_zero_entries(remaining_lengths, remaining_quantities)
        new_all_patterns = generate_all_patterns(remaining_lengths, remaining_quantities, stock_lengths, min(remaining_lengths))
        new_filter_patterns = filter_min_leftover_patterns(new_all_patterns)
        new_sorted_patterns = sort_patterns_by_cut_priority(new_filter_patterns, remaining_lengths)
        
        patterns_used, remaining_quantities = cut_materials(remaining_lengths, remaining_quantities, new_sorted_patterns)

        if idx_lst:
            new_patterns_used = []
            for tmp in patterns_used:
                tmp_copy = copy.deepcopy(tmp)
                pattern, _, _ = tmp_copy
                for i in idx_lst:
                    pattern.insert(i, 0)
                new_patterns_used.append(tmp_copy)
            cut_list.extend(new_patterns_used)
            for i in idx_lst:
                remaining_quantities.insert(i, 0)
            remaining_lengths = lengths[:]
        else:
            cut_list.extend(patterns_used)
    
    return cut_list, remaining_quantities

# Count pattern usage in the cut list
def count_pattern_usage(patterns, cut_list):
    pattern_count = {i: 0 for i in range(len(patterns))}
    
    for cut in cut_list:
        for i, pattern in enumerate(patterns):
            if cut == pattern:
                pattern_count[i] += 1
    
    pattern_usage_list = [pattern_count[i] for i in range(len(patterns))]
    
    return pattern_usage_list

# Calculate total leftover from the cut list
def calculate_total_leftover(cut_list):
    total_leftover = 0
    for _, _, leftover in cut_list:
        total_leftover += leftover
    return total_leftover  

def format_patterns(patterns):
    formatted_patterns = []
    for pattern, stock_length, leftover in patterns:
        cuts_dict = {i: pattern[i] for i in range(len(pattern))}
        formatted_patterns.append({"stock": stock_length, "cuts": cuts_dict, "leftover": leftover})
    return formatted_patterns   

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

def write_output_file(file_path, new_cut_list, summarize_lst, remaining_quantities, cut_list, total_time):
    with open(file_path, "w") as f:
        f.write("All patterns need to use:\n")
        for pattern in new_cut_list:
            f.write(f"{pattern}\n")
            
        f.write("\nSummarize:\n")
        for tmp in summarize_lst:
            f.write(f"{tmp}\n")

        f.write(f"\nRemaining quantities: {remaining_quantities}\n")
        f.write(f"Sum of leftover: {calculate_total_leftover(cut_list)}\n")
        f.write(f"Total time: {total_time} sec\n")
        f.write(f"Total stock: {len(cut_list)}\n")

if __name__ == "__main__":
    input_file_names = [f"Appendix_problem_{i}" for i in range(1, 11)]
    output_file_names = [f"FFD_Appendix_problem_{i}_output" for i in range(1, 11)]

    for input_file_name, output_file_name in zip(input_file_names, output_file_names):
        input_path = f"./input/{input_file_name}.txt"
        output_path = f"./output/{output_file_name}.txt"
        
        lengths, quantities, stock_lengths = read_input_file(input_path)
        min_length = min(lengths)
        
        start_time = time.time()
        cut_list, remaining_quantities = cut_until_zero(lengths, quantities, stock_lengths)
        end_time = time.time()
        
        new_cut_list = format_patterns(cut_list)
        summarize_lst = summarize_list(new_cut_list)
        total_time = end_time - start_time
        
        write_output_file(output_path, new_cut_list, summarize_lst, remaining_quantities, cut_list, total_time)

    input_file_names = [f"Appendix_problem_{i}a" for i in range(1, 11)]
    output_file_names = [f"FFD_Appendix_problem_{i}a_output" for i in range(1, 11)]
    
    for input_file_name, output_file_name in zip(input_file_names, output_file_names):
        input_path = f"./input/{input_file_name}.txt"
        output_path = f"./output/{output_file_name}.txt"
        
        lengths, quantities, stock_lengths = read_input_file(input_path)
        min_length = min(lengths)
        
        start_time = time.time()
        cut_list, remaining_quantities = cut_until_zero(lengths, quantities, stock_lengths)
        end_time = time.time()
        
        new_cut_list = format_patterns(cut_list)
        summarize_lst = summarize_list(new_cut_list)
        total_time = end_time - start_time
        
        write_output_file(output_path, new_cut_list, summarize_lst, remaining_quantities, cut_list, total_time)

    input_file_name =  "caseStudy"
    output_file_name = "FFD_caseStudy_output"
    input_path = f"./input/{input_file_name}.txt"
    output_path = f"./output/{output_file_name}.txt"
    
    lengths, quantities, stock_lengths = read_input_file(input_path)
    min_length = min(lengths)        

    start_time = time.time()
    cut_list, remaining_quantities = cut_until_zero(lengths, quantities, stock_lengths)
    end_time = time.time()

    new_cut_list = format_patterns(cut_list)
    summarize_lst = summarize_list(new_cut_list)
    total_time = end_time - start_time
    
    write_output_file(output_path, new_cut_list, summarize_lst, remaining_quantities, cut_list, total_time)
    
