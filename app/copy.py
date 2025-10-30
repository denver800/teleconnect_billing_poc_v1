python - <<'PY'
import os, pathlib
base = pathlib.Path("src/proto_generated")
for d,_,_ in os.walk(base):
    p = pathlib.Path(d) / "__init__.py"
    if not p.exists():
        p.write_text("")  # make it a package
print("Init files created under", base)
PY


rmdir /s /q src\proto_generated
mkdir src\proto_generated

python -m grpc_tools.protoc ^
 -I=src/proto ^
 --python_out=src/proto_generated ^
 --grpc_python_out=src/proto_generated ^
 src/proto/apis/billdata/v2025_2_0/billdata_root.proto
