# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 23:39:01 2023

@author: fwhite
"""

alfons_population = 5000000
velons_population = 9000000
alfons_growth_rate = 0.06
velons_growth_rates = [0.05, 0.02]
war_deaths = 500000
years = 0

while alfons_population < velons_population:
    years += 1
    alfons_population += int(alfons_population * alfons_growth_rate)

    if years % 4 == 0:
        velons_growth_rate = velons_growth_rates[0]
        velons_population += int(velons_population *
                                velons_growth_rate - war_deaths)
    else:
        velons_growth_rate = velons_growth_rates[1]
        velons_population += int(velons_population * velons_growth_rate)

    print(f"Population {years} year:")
    print(f"\tAlfons count: {alfons_population}")
    print(f"\tVelons count: {velons_population}")

print(f"In {years} years, there will be more Alfons than Velons.")
