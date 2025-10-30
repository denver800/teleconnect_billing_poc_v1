python - <<'PY'
import os, pathlib
base = pathlib.Path("src/proto_generated")
for d,_,_ in os.walk(base):
    p = pathlib.Path(d) / "__init__.py"
    if not p.exists():
        p.write_text("")  # make it a package
print("Init files created under", base)
PY
