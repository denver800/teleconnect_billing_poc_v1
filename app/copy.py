# src/processor/parser.py
import os
import sys
from pathlib import Path
from google.protobuf.json_format import MessageToJson

ROOT_DIR = Path(__file__).resolve().parents[2]
PROTO_GEN = ROOT_DIR / "src" / "proto_generated"

# Append (do NOT insert at index 0), so we don't shadow google.protobuf
if str(PROTO_GEN) not in sys.path:
    sys.path.append(str(PROTO_GEN))

from apis.billdata.v2025_2_0 import billdata_root_pb2  # now resolves cleanly

def parse_pb_file(file_path: str | None = None) -> str | None:
    # default to your sample file
    if not file_path:
        project_root = os.getcwd()
        file_path = os.path.join(project_root, "local", "incoming", "GF32.pb")

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    base_dir = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(base_dir, f"{file_name}.json")

    try:
        message = billdata_root_pb2.BillData()
        with open(file_path, "rb") as f:
            message.ParseFromString(f.read())

        json_output = MessageToJson(message, indent=2)

        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write(json_output)

        print(f"✅ Parsed {file_path} → {output_file}")
        return output_file

    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None

if __name__ == "__main__":
    parse_pb_file()
