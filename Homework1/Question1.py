import logging
import threading

class SuspectedIntrustionException(Exception):
    pass


logging.basicConfig(format='[%(levelname)s]: %(message)s')


def avg_usage(custID):
    """Calculates the customers average time of visit for each day

    Args:
        custID (Integer): The ID of the customer

    Raises:
        SuspectedIntrustionException: Incase of a suspicious average it warns the user

    Returns:
        Dictionary: A dictionary with the average time for each day
    """
    avg_times = []
    avg_times_dict = {}
    margin = 10 # The margin by how high can the average be before it is suspected as an intrusion.
    for day in range(1, 7):
        name = f'Homework1/cloud/cust{custID}-{day}.txt'
        with open(name, "r") as f:
            visits = f.readlines()
            times = []
            for visit in visits:
                time = visit.split()[1]
                times.append(int(time))
        avg_times_dict[day] = ((round(sum(times) / len(times), 2)))
        avg_times.append((round(sum(times) / len(times), 2)))
    user_avg = (round(sum(avg_times) / len(avg_times), 2))
    print(f'Customer {custID}:\n' + str(avg_times_dict))
    for i in avg_times:
        if i > user_avg + margin:
            try:
                raise SuspectedIntrustionException
            except:
                logging.warning(
                    f'Suspected intrusion on day {list(avg_times_dict.keys())[list(avg_times_dict.values()).index(i)]} with value {i}')
    return avg_times_dict



def main():
    threads = []
    for customer in range(1, 3):
        new_thread = threading.Thread(target=avg_usage, args=[customer])
        new_thread.start()
        threads.append(new_thread)
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
