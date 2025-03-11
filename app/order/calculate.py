def usage (orders):
    usages = []
    for order in orders:
        details = order['detail']

        for detail in details:
            menu = detail['Menu']
            qty = detail['amount']
            recipes = menu['recipe']
        
            for recipe in recipes:
                data = {
                    'ingredient': recipe['ingredient'],
                    'amount': recipe['amount'] * qty
                }
                usages.append(data)
    
    result_dict = {}
    for entry in usages:
        ingredient = entry['ingredient']
        amount = entry['amount']
        
        if ingredient in result_dict:
            result_dict[ingredient] += amount
        else:
            result_dict[ingredient] = amount

    result = [{'ingredient': key, 'amount': amount} for key, amount in result_dict.items()]
    return result