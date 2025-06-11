def is_factor(x, y):
    return y % x == 0

def maximize_earnings(remaining):
    memo = {}

    def dfs(pool):
        key = tuple(sorted(pool))
        if key in memo:
            return memo[key]

        max_total = 0
        best_path = []
        best_tax_log = []

        for paycheck in sorted(pool):
            factors = [x for x in pool if x != paycheck and is_factor(x, paycheck)]
            if not factors:
                total = paycheck
                if total > max_total:
                    max_total = total
                    best_path = [paycheck]
                    best_tax_log = [sorted(pool - {paycheck})]
                continue

            new_pool = pool - {paycheck} - set(factors)
            subtotal, subpath, subtax = dfs(new_pool)

            total = paycheck + subtotal
            if total > max_total:
                max_total = total
                best_path = [paycheck] + subpath
                best_tax_log = [factors] + subtax

        memo[key] = (max_total, best_path, best_tax_log)
        return memo[key]

    return dfs(set(remaining))

max_total, best_path, best_tax_log = maximize_earnings(range(1, 13))

print(f"Optimal earnings: ${max_total}")
for pick, tax in zip(best_path, best_tax_log):
    print(f"You picked {pick}, tax collector gets {tax}")
