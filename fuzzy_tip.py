# Nama : Nama Kamu
# NIM  : NIM Kamu

def triangular(x, a, b, c):
    if a == b and x <= b:
        if x <= a:
            return 1.0
        elif x >= c:
            return 0.0
        else:
            return (c - x) / (c - a)

    if b == c and x >= b:
        if x <= a:
            return 0.0
        elif x >= c:
            return 1.0
        else:
            return (x - a) / (b - a)

    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0


def fuzzify_food(food):
    return triangular(food, 0, 0, 5), triangular(food, 5, 10, 10)


def fuzzify_service(service):
    return triangular(service, 0, 0, 5), triangular(service, 5, 10, 10)


def low_tip_membership(z):
    if z <= 0:
        return 1.0
    elif 0 < z < 10:
        return (10 - z) / 10.0
    return 0.0


def high_tip_membership(z):
    if z <= 10:
        return 0.0
    elif 10 < z < 20:
        return (z - 10) / 10.0
    return 1.0


def compute_tip(food, service, step=0.1):
    mu_food_bad, mu_food_good = fuzzify_food(food)
    mu_service_poor, mu_service_excellent = fuzzify_service(service)

    alpha1 = max(mu_service_poor, mu_food_bad)
    alpha2 = min(mu_service_excellent, mu_food_good)

    z_values = []
    mu_values = []

    z = 0.0
    while z <= 20.0:
        mu_low = min(low_tip_membership(z), alpha1)
        mu_high = min(high_tip_membership(z), alpha2)
        mu = max(mu_low, mu_high)

        z_values.append(z)
        mu_values.append(mu)

        z = round(z + step, 4)

    numerator = sum(z_values[i] * mu_values[i] for i in range(len(z_values)))
    denominator = sum(mu_values)

    tip = numerator / denominator if denominator != 0 else 0
    return tip


def main():
    food = 7
    service = 3

    tip = compute_tip(food, service)
    print(f"Food = {food}, Service = {service}")
    print(f"Rekomendasi Tip = {tip:.4f}%")

if __name__ == "__main__":
    main()
