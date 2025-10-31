#check message names for invoice_summary_pb2.py and bill_info_pb2.py:
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src/proto_generated').resolve())); import apis.billdata.v2025_2_0.invoice_summary_pb2 as m; print([n for n in dir(m) if not n.startswith('_')])"
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src/proto_generated').resolve())); import apis.billdata.v2025_2_0.bill_info_pb2 as m; print([n for n in dir(m) if not n.startswith('_')])"


#check message names for invoice_pb2.py in proto
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src/proto_generated').resolve())); import apis.billdata.v2025_2_0.invoice_pb2 as m; print([n for n in dir(m) if not n.startswith('_')])"

#check message names for statements_root_pb2.py in proto
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src/proto_generated').resolve())); import apis.billdata.v2025_2_0.statements_root_pb2 as m; print([n for n in dir(m) if not n.startswith('_')])"

#check message names in all proto
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src/proto_generated').resolve())); import apis.billdata.v2025_2_0.billdata_root_pb2 as m; print([n for n in dir(m) if not n.startswith('_')])"

## src/processor/parse_pb_file.py
import sys, os
from pathlib import Path
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import DecodeError

# make generated code importable
ROOT_DIR = Path(__file__).resolve().parents[2]
PROTO_GEN = ROOT_DIR / "src" / "proto_generated"
if str(PROTO_GEN) not in sys.path:
    sys.path.insert(0, str(PROTO_GEN))

# import candidate roots
from apis.billdata.v2025_2_0 import (
    billdata_root_pb2,
    statements_root_pb2,
    statement_pb2,
    invoice_pb2,
    invoice_summary_pb2,
    bill_info_pb2,
)

CANDIDATES = [
    ("BillData", billdata_root_pb2.BillData),
    ("StatementsRoot", statements_root_pb2.StatementsRoot),
    ("Statement", statement_pb2.Statement),
    ("Invoice", invoice_pb2.Invoice),
    ("InvoiceSummary", invoice_summary_pb2.InvoiceSummary),
    ("BillInfo", bill_info_pb2.BillInfo),
]

def _read_varint(stream) -> int:
    """Read a protobuf varint (for length-delimited streams)."""
    shift = 0
    result = 0
    while True:
        b = stream.read(1)
        if not b:
            return None
        b = b[0]
        result |= ((b & 0x7F) << shift)
        if not (b & 0x80):
            return result
        shift += 7
        if shift > 64:
            raise ValueError("Bad varint")

def try_single_message(buf: bytes):
    for name, cls in CANDIDATES:
        m = cls()
        try:
            m.ParseFromString(buf)
            return ("single", name, m)
        except DecodeError:
            continue
    return None

def try_delimited(stream_path: str):
    with open(stream_path, "rb") as f:
        length = _read_varint(f)
        if length is None:
            return None
        frame = f.read(length)
    for name, cls in CANDIDATES:
        m = cls()
        try:
            m.ParseFromString(frame)
            return ("delimited", name, m)
        except DecodeError:
            continue
    return None

def parse_pb_file(file_path: str | None = None) -> str | None:
    if not file_path:
        file_path = os.path.join(os.getcwd(), "local", "incoming", "GF32.pb")
    if not os.path.exists(file_path):
        print(f"✘ File not found: {file_path}")
        return None

    # 1) try as a single message
    with open(file_path, "rb") as f:
        buf = f.read()

    res = try_single_message(buf)
    if not res:
        # 2) try as a length-delimited stream (first frame)
        res = try_delimited(file_path)

    if not res:
        print(f"✘ Could not parse {file_path} as any known root type.")
        return None

    mode, root_name, msg = res
    out = Path(file_path).with_suffix(".json")
    json_output = MessageToJson(msg, indent=2)
    out.write_text(json_output, encoding="utf-8")
    print(f"✅ Parsed ({mode}, {root_name}) {file_path} → {out}")
    return str(out)

if __name__ == "__main__":
    parse_pb_file()


#verify command
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path('src/proto_generated').resolve())); import apis.billdata.v2025_2_0.billdata_root_pb2 as m; print('OK', hasattr(m, 'BillData'))"


# scripts/compile_protos.py
import sys
from pathlib import Path
from grpc_tools import protoc
import grpc_tools  # for the include dir

ROOT = Path(__file__).resolve().parents[1]
PROTO_SRC = ROOT / "src" / "proto"
OUT = ROOT / "src" / "proto_generated"

# grpc_tools ships the well-known types here:
GRPC_TOOLS_INCLUDE = Path(grpc_tools.__file__).parent / "_proto"

proto_files = [str(p) for p in PROTO_SRC.rglob("*.proto")]
OUT.mkdir(parents=True, exist_ok=True)

args = [
    "protoc",
    f"-I={PROTO_SRC}",
    f"-I={GRPC_TOOLS_INCLUDE}",
    f"--python_out={OUT}",
    f"--grpc_python_out={OUT}",
]

ret = protoc.main(args + proto_files)
if ret != 0:
    raise SystemExit(f"protoc failed with exit code {ret}")
print(f"Generated {len(proto_files)} files into {OUT}")
