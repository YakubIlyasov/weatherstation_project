class math_operations:  # class for math operations
    @staticmethod
    def mean(lst_numbers, decimals_amount=2):  # calculate mean
        if len(lst_numbers) == 0:  # check if list is empty
            return 0.00
        else:  # list is not empty
            return float(sum(lst_numbers)) / max(len(lst_numbers), decimals_amount)
