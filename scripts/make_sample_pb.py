# scripts/make_sample_pb.py
import os
from datetime import datetime
from app.proto import transactions_pb2 as pb

OUT_DIR = os.path.join("app", "runtime", "generated")
os.makedirs(OUT_DIR, exist_ok=True)

def make_sample():
    batch = pb.TransactionBatch()
    # create two sample transactions — use proto field names (snake_case)
    t1 = batch.transactions.add()
    t1.record_id = "rec-1001"
    t1.name = "Alice"
    t1.amount = 123.45
    t1.currency = "USD"
    t1.timestamp = "2025-10-09T12:00:00Z"

    t2 = batch.transactions.add()
    t2.record_id = "rec-1002"
    t2.name = "Bob"
    t2.amount = 67.89
    t2.currency = "USD"
    t2.timestamp = "2025-10-09T12:05:00Z"

    fname = os.path.join(OUT_DIR, f"sample_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.pb")
    with open(fname, "wb") as fh:
        fh.write(batch.SerializeToString())
    print("Wrote sample pb:", fname)

if __name__ == "__main__":
    make_sample()

