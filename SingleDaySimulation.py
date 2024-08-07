import numpy as np
import matplotlib.pyplot as plt
from datetime import time, datetime, timedelta
import random
from Pharmacy import Pharmacy


# Parameters
hours_open = 11  # Assuming 8 hours of operation per day
average_customers_per_day = 100  # Average customers per day

def generatePoissonProcessArrivals(hours_open, average_customers_per_day):
    lambda_val = average_customers_per_day / hours_open
    total_customers = np.random.poisson(average_customers_per_day)
    arrival_times = np.cumsum(np.random.exponential(1 / lambda_val, total_customers) * 60)
    return arrival_times


arrival_times = generatePoissonProcessArrivals(hours_open, average_customers_per_day)

def generateIncomingDemandTimestamps(arrival_times):
    start_time = datetime.strptime('08:00', '%H:%M')
    arrival_datetimes = [start_time + timedelta(minutes=int(t)) for t in arrival_times]
    arrival_minutes = [(dt - start_time).seconds // 60 for dt in arrival_datetimes]
    # Print arrival timestamps
    print(len(arrival_minutes),"customers arrived!")
    arrival_timestamps = [dt.strftime('%H:%M:%S') for dt in arrival_datetimes]
    
    return arrival_timestamps

arrival_timestamps = generateIncomingDemandTimestamps(arrival_times)

def convert_to_time(timestamp_str):
    return datetime.strptime(timestamp_str, "%H:%M:%S").time()

def isValidArrival(arrival_time):
    if(convert_to_time(arrival_time) >= opening_time and convert_to_time(arrival_time) <= closing_time):
        return True
    else:
        return False
    
def g(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1
    
def get_winner(pharmacy1, pharmacy2):
    if(pharmacy1.balance > pharmacy2.balance):
        return pharmacy1.get_name()
    elif(pharmacy1.balance < pharmacy2.balance):
        return pharmacy2.get_name()
    else:
        return "tie"
    
def calculate_fulfillment_metric(I1, I2, V1, V2, w1 = 1, w2 = 1):

    if max(I1, I2) == 0:
        normalized_inventory_difference = 0
    else:
        normalized_inventory_difference = (g(I1 - I2) * abs(I1 - I2)) / max(I1, I2)
    return w1 * normalized_inventory_difference + w2 * (V1 - V2)


def fulfillIncomingDemand(chosen_pharmacy, other_pharmacy):
    if not chosen_pharmacy.fulfill_demand():
        if not other_pharmacy.fulfill_demand():
            print("Lost sales for both pharmacies")
            return False

def simulate_day(arrival_timestamps):
    invalid_arrivals = []

    pharmacy1 = Pharmacy("1", initial_balance=initial_pharmacy1_balance, initial_new_inventory=initial_pharmacy1_new_inventory,
                         initial_old_inventory= initial_pharmacy1_old_inventory)
    pharmacy2 = Pharmacy("2", initial_balance=initial_pharmacy2_balance, initial_new_inventory=initial_pharmacy2_new_inventory,
                         initial_old_inventory= initial_pharmacy2_old_inventory)

    pharmacy1.replenish(replenish_amount_pharmacy1)
    pharmacy2.replenish(replenish_amount_pharmacy2)

    print("Replenishment is done, Inventory levels at the beginning of day:")
    print(f"Pharmacy 1: {pharmacy1}")
    print(f"Pharmacy 2: {pharmacy2}")
    print("- - - - - - - - -")
    for timestamp in arrival_timestamps:
        if (isValidArrival(timestamp)):
            I1 = pharmacy1.get_inventory_level()
            I2 = pharmacy2.get_inventory_level()
            V1 = pharmacy1.get_shelf_life_value()
            V2 = pharmacy2.get_shelf_life_value()

            fulfillment_metric = calculate_fulfillment_metric(I1, I2, V1, V2)
            print("Fulfillment Metric:", str(round(fulfillment_metric, 3)))

            if fulfillment_metric > 0:
                chosen_pharmacy = pharmacy1
                other_pharmacy = pharmacy1 if chosen_pharmacy == pharmacy2 else pharmacy2
                fulfillIncomingDemand(chosen_pharmacy, other_pharmacy)
            elif fulfillment_metric < 0:
                chosen_pharmacy = pharmacy2
                other_pharmacy = pharmacy1 if chosen_pharmacy == pharmacy2 else pharmacy2
                fulfillIncomingDemand(chosen_pharmacy, other_pharmacy)
            else:
                print("Pharmacy is chosen randomly")
                chosen_pharmacy = random.choice([pharmacy1, pharmacy2])
                other_pharmacy = pharmacy1 if chosen_pharmacy == pharmacy2 else pharmacy2
                fulfillIncomingDemand(chosen_pharmacy, other_pharmacy)


            print(f"At timestamp {timestamp}, chosen pharmacy: {chosen_pharmacy.get_name()}")
            print(f"Pharmacy 1: {pharmacy1}")
            print(f"Pharmacy 2: {pharmacy2}")
            print("- - - - - - - - -")
        else:
            invalid_arrivals.append(timestamp)


    # Process end of day changes
    pharmacy1.process_day_end()
    pharmacy2.process_day_end()

    print("End of day:")
    print(f"Pharmacy 1: {pharmacy1}")
    print(f"Pharmacy 2: {pharmacy2}")
    print(f"# of total incomings: {len(arrival_timestamps)}")
    print(f"# of invalid incomings(time restriction) : {len(invalid_arrivals)}")
    print(f"# of met demand by Pharmacy 1 : {pharmacy1.sales_counter}")
    print(f"# of met demand by Pharmacy 2 : {pharmacy2.sales_counter}")
    print(f"# of unmet demand by Pharmacy 1 : {pharmacy1.lost_sales_counter}")
    print(f"# of unmet demand by Pharmacy 2 : {pharmacy2.lost_sales_counter}")
    print("- - - - - - - - - - - - -")
    print(f"Winner: {get_winner(pharmacy1, pharmacy2)}")


if __name__ == "__main__":

    initial_pharmacy1_balance = 100
    initial_pharmacy2_balance = 100

    initial_pharmacy1_new_inventory = 20
    initial_pharmacy2_new_inventory = 10

    initial_pharmacy1_old_inventory = 10
    initial_pharmacy2_old_inventory = 10

    replenish_amount_pharmacy1 = 5
    replenish_amount_pharmacy2 = 5

    opening_time = time(8, 0, 0)
    closing_time = time(18, 0, 0)



    simulate_day(arrival_timestamps)