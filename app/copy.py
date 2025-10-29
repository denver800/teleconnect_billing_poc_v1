import sys, os
from pathlib import Path
from grpc_tools import protoc

ROOT = Path(__file__).resolve().parents[1]       # project root
PROTO_SRC = ROOT / "src" / "proto"
OUT = ROOT / "src" / "proto_generated"

# collect every .proto under src/proto
proto_files = [str(p) for p in PROTO_SRC.rglob("*.proto")]

# ensure output dir exists
OUT.mkdir(parents=True, exist_ok=True)

args = [
    "protoc",
    f"-I={PROTO_SRC}",
    f"--python_out={OUT}",
    f"--grpc_python_out={OUT}",
]
# run once with the whole list (protoc supports multiple files)
protoc.main(args + proto_files)
print(f"Generated {len(proto_files)} files into {OUT}")
