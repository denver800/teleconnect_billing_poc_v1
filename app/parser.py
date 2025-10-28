import os
from google.protobuf.json_format import MessageToJson
from src.apis.billdata.v2025_2_0 import billdata_root_pb2


def parse_pb_file(file_path: str):
    """
    Reads a .pb file from the given path, parses it using the protobuf schema,
    and writes the parsed JSON to the same folder.
    """
    try:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None

        # derive output JSON path
        base_dir = os.path.dirname(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(base_dir, f"{file_name}.json")

        # parse protobuf
        message = billdata_root_pb2.BillData()
        with open(file_path, "rb") as f:
            message.ParseFromString(f.read())

        json_output = MessageToJson(message, indent=2)

        # write JSON file
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write(json_output)

        print(f"✅ Parsed {file_path} → {output_file}")
        return output_file

    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None


if __name__ == "__main__":
    # For standalone testing
    project_root = os.getcwd()
    test_file = os.path.join(project_root, "local", "incoming", "GF32.pb")
    parse_pb_file(test_file)
