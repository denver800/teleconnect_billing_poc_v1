#blob_checker.py
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from config.settings import ACCOUNT_URL, ACCOUNT_KEY, CONTAINER_NAME, LOCAL_INCOMING_DIR
from src.db.operations import add_new_pair

def check_new_pairs():
    print("🔍 Checking Azure container for new .pb + control.json pairs...")

    os.makedirs(LOCAL_INCOMING_DIR, exist_ok=True)

    # Connect to Azure
    blob_service_client = BlobServiceClient(account_url=ACCOUNT_URL, credential=ACCOUNT_KEY)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # List all blobs in container
    blobs = [b.name for b in container_client.list_blobs()]
    pb_files = [b for b in blobs if b.endswith(".pb")]
    json_files = [b for b in blobs if b.startswith("control_") and b.endswith(".json")]

    print(f"📦 Found {len(pb_files)} .pb files and {len(json_files)} control files in Azure.\n")

    for pb in pb_files:
        base_name = pb.replace(".pb", "")
        control_file = f"control_{base_name}.json"

        # Check if both files exist
        if control_file not in json_files:
            print(f"⚠️ Skipping {pb}: missing {control_file}")
            continue

        # Check if pair already exists in DB
        file_id, is_new = add_new_pair(pb, control_file)
        if not is_new:
            print(f"⏭️ Pair already exists in DB, skipping download: {pb}")
            continue

        # Download both files
        for blob_name in [pb, control_file]:
            local_path = os.path.join(LOCAL_INCOMING_DIR, blob_name)
            print(f"⬇️ Downloading {blob_name} ...")
            blob_client = container_client.get_blob_client(blob_name)
            with open(local_path, "wb") as f:
                f.write(blob_client.download_blob().readall())
            print(f"✅ Saved {blob_name} to {local_path}")

    print("\n✨ Blob pair check completed.\n")

if __name__ == "__main__":
    check_new_pairs()
