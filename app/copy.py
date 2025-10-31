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
