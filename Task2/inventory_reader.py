import csv


def read_in_batches(filename, batch_size=100):

    with open(filename, "r", newline="", encoding="utf-8") as file:
        

        reader = csv.DictReader(file)

        batch = []

        for row in reader:

            batch.append(row)

            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch