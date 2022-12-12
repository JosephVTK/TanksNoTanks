def get_center_of_rect(rect):
    return (rect.x / 2, rect.y / 2)

def merge_numbers(num_to, num_from, num_step, min):
    if num_to < num_from:
        num_to += num_step
    elif num_to > num_from:
        num_to -= num_step
    
    if abs(num_to) < min:
        num_to = 0

    return num_to

def min_max(min_number, number, max_number):
    return min(max(min_number, number), max_number)