# Nama : Nama Kamu
# NIM  : NIM Kamu
# Mata Kuliah : Fuzzy Logic / AI (contoh, sesuaikan)

import numpy as np

def triangular(x, a, b, c):
    """
    Fungsi keanggotaan segitiga generik.
    Menangani juga kasus left-shoulder (a==b) dan right-shoulder (b==c).
    """
    # Left-shoulder: (a, a, c) misal (0,0,5)
    if a == b and x <= b:
        if x <= a:
            return 1.0
        elif x >= c:
            return 0.0
        else:
            return (c - x) / (c - a)

    # Right-shoulder: (a, c, c) misal (10,20,20)
    if b == c and x >= b:
        if x <= a:
            return 0.0
        elif x >= c:
            return 1.0
        else:
            return (x - a) / (b - a)

    # Segitiga biasa
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0


def fuzzify_food(food):
    """
    Food Quality: 0..10
    Bad  : (0, 0, 5)
    Good : (5, 10, 10)
    """
    mu_bad = triangular(food, 0, 0, 5)
    mu_good = triangular(food, 5, 10, 10)
    return mu_bad, mu_good


def fuzzify_service(service):
    """
    Service Quality: 0..10
    Poor      : (0, 0, 5)
    Excellent : (5, 10, 10)
    """
    mu_poor = triangular(service, 0, 0, 5)
    mu_excellent = triangular(service, 5, 10, 10)
    return mu_poor, mu_excellent


def low_tip_membership(z):
    """
    Tip Low: (0, 0, 10)
    Di sini kita langsung pakai bentuk manual agar jelas.
    """
    if z <= 0:
        return 1.0
    elif 0 < z < 10:
        return (10 - z) / 10.0
    else:
        return 0.0


def high_tip_membership(z):
    """
    Tip High: (10, 20, 20)
    """
    if z <= 10:
        return 0.0
    elif 10 < z < 20:
        return (z - 10) / 10.0
    else:
        return 1.0


def compute_tip(food, service, step=0.1):
    """
    Menghitung Tip (%) menggunakan sistem Fuzzy:
    - Input: Food Quality (0-10), Service Quality (0-10)
    - Output: Tip (0-20) dalam persen (float)
    
    Fuzzy Set:
      Food Bad: (0,0,5)
      Food Good: (5,10,10)
      Service Poor: (0,0,5)
      Service Excellent: (5,10,10)
      Tip Low: (0,0,10)
      Tip High: (10,20,20)

    Rules:
      1. IF Service is Poor OR Food is Bad THEN Tip is Low
      2. IF Service is Excellent AND Food is Good THEN Tip is High
    """
    # 1. Fuzzifikasi
    mu_food_bad, mu_food_good = fuzzify_food(food)
    mu_service_poor, mu_service_excellent = fuzzify_service(service)

    # 2. Evaluasi rule (Inferensi)
    # Rule 1: IF Service is Poor OR Food is Bad THEN Tip is Low
    alpha1 = max(mu_service_poor, mu_food_bad)

    # Rule 2: IF Service is Excellent AND Food is Good THEN Tip is High
    alpha2 = min(mu_service_excellent, mu_food_good)

    # 3. Agregasi output (discretization 0..20)
    z_values = np.arange(0, 20 + step, step)
    mu_aggregated = []

    for z in z_values:
        # Output dari Rule 1: Low, di-clip pada alpha1
        mu_low = min(low_tip_membership(z), alpha1)

        # Output dari Rule 2: High, di-clip pada alpha2
        mu_high = min(high_tip_membership(z), alpha2)

        # Agregasi: max dari semua rule
        mu_aggregated.append(max(mu_low, mu_high))

    mu_aggregated = np.array(mu_aggregated)

    # 4. Defuzzifikasi (centroid)
    numerator = np.sum(z_values * mu_aggregated)
    denominator = np.sum(mu_aggregated)

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
    # Contoh sesuai soal: Food = 7, Service = 3
    food = 7
    service = 3

    tip, detail = compute_tip(food, service)

    print("=== Fuzzy Tip System ===")
    print(f"Food Quality     = {food}")
    print(f"Service Quality  = {service}\n")

    print("Derajat keanggotaan (fuzzifikasi):")
    print(f"  Food Bad        = {detail['mu_food_bad']:.4f}")
    print(f"  Food Good       = {detail['mu_food_good']:.4f}")
    print(f"  Service Poor    = {detail['mu_service_poor']:.4f}")
    print(f"  Service Excellent = {detail['mu_service_excellent']:.4f}\n")

    print("Derajat aktivasi rule:")
    print(f"  Rule 1 (Low)  = {detail['alpha1_low']:.4f}")
    print(f"  Rule 2 (High) = {detail['alpha2_high']:.4f}\n")

    print(f"Hasil defuzzifikasi Tip = {tip:.4f} %")

    # Bisa juga minta input user
    # food = float(input("Masukkan Food Quality (0-10): "))
    # service = float(input("Masukkan Service Quality (0-10): "))
    # tip, _ = compute_tip(food, service)
    # print(f"Rekomendasi Tip = {tip:.2f} %")


if __name__ == "__main__":
    main()
