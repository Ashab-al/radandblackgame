from datetime import datetime


def time(function):
    def wrapper(max_range, *args, **kwargs):
       start_function_time = datetime.now()
       function(max_range)
       result_of_function_time = datetime.now() - start_function_time
       print(result_of_function_time)
       return function(max_range, *args, **kwargs)
    return wrapper


@time
def count_of_evens(max_range):
    result = 0
    for number in range(0, max_range + 1):
        if number % 2 == 0:
            result += 1
    return result

print(count_of_evens(100000))