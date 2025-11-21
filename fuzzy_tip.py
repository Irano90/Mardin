# Nama : Brilliant Irano Mardin
# NIM  : 32602200140
# Mata Kuliah : Kecerdasan Buatan_FKCBD_20251

def triangular(x, a, b, c):
    """Fungsi keanggotaan segitiga (termasuk left/right shoulder)."""
    if a == b and x <= b:  # left shoulder
        if x <= a:
            return 1.0
        elif x >= c:
            return 0.0
        else:
            return (c - x) / (c - a)

    if b == c and x >= b:  # right shoulder
        if x <= a:
            return 0.0
        elif x >= c:
            return 1.0
        else:
            return (x - a) / (b - a)

    # normal triangle
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0


def fuzzify_food(food):
    mu_bad = triangular(food, 0, 0, 5)
    mu_good = triangular(food, 5, 10, 10)
    return mu_bad, mu_good


def fuzzify_service(service):
    mu_poor = triangular(service, 0, 0, 5)
    mu_excellent = triangular(service, 5, 10, 10)
    return mu_poor, mu_excellent


def low_tip_membership(z):
    if z <= 0:
        return 1.0
    elif 0 < z < 10:
        return (10 - z) / 10.0
    else:
        return 0.0


def high_tip_membership(z):
    if z <= 10:
        return 0.0
    elif 10 < z < 20:
        return (z - 10) / 10.0
    else:
        return 1.0


def compute_tip(food, service, step=0.1):
    # 1. Fuzzifikasi
    mu_food_bad, mu_food_good = fuzzify_food(food)
    mu_service_poor, mu_service_excellent = fuzzify_service(service)

    # 2. Rule
    alpha1 = max(mu_service_poor, mu_food_bad)     # LOW
    alpha2 = min(mu_service_excellent, mu_food_good)  # HIGH

    # 3. Agregasi output
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

    # 4. Defuzzifikasi (centroid)
    numerator = sum(z_values[i] * mu_values[i] for i in range(len(z_values)))
    denominator = sum(mu_values[i] for i in range(len(mu_values)))

    if denominator == 0:
        tip = 0.0
    else:
        tip = numerator / denominator

    return tip, {
        "mu_food_bad": mu_food_bad,
        "mu_food_good": mu_food_good,
        "mu_service_poor": mu_service_poor,
        "mu_service_excellent": mu_service_excellent,
        "alpha1_low": alpha1,
        "alpha2_high": alpha2
    }


def main():
    food = 7
    service = 3

    tip, detail = compute_tip(food, service)

    print("=== Fuzzy Tip System (Tanpa NumPy) ===")
    print(f"Food Quality    = {food}")
    print(f"Service Quality = {service}\n")

    print("Derajat keanggotaan:")
    print(f"  Food Bad        = {detail['mu_food_bad']:.4f}")
    print(f"  Food Good       = {detail['mu_food_good']:.4f}")
    print(f"  Service Poor    = {detail['mu_service_poor']:.4f}")
    print(f"  Service Excellent = {detail['mu_service_excellent']:.4f}\n")

    print("Aktivasi Rule:")
    print(f"  Rule 1 (LOW)  = {detail['alpha1_low']:.4f}")
    print(f"  Rule 2 (HIGH) = {detail['alpha2_high']:.4f}\n")

    print(f"Hasil defuzzifikasi Tip = {tip:.4f} %")


if __name__ == "__main__":
    main()
