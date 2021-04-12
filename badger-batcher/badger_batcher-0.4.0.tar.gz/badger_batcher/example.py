from badger_batcher import Batcher
import random


def get_records():
    records = (
        f"""{{
    'id': '{i}', 'body': {('x' * random.randint(100_000, 7_000_000))}
    }}"""
        for i in range(10_000)
    )
    return records


def run_test():
    records = get_records()
    encoded_records = (record.encode("utf-8") for record in records)

    batcher = Batcher(
        encoded_records,
        max_batch_len=500,
        max_record_size=1000 * 1000,
        max_batch_size=5 * 1000 * 1000,
        size_calc_fn=len,
        when_record_size_exceeded="skip",
    )

    for i, batch in enumerate(batcher):
        # do something
        with open(f"/tmp/test_run/{i}", "wb") as f:
            f.write(b"".join(batch))


if __name__ == "__main__":
    run_test()
