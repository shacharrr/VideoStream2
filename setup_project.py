import json
import socket
import subprocess
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname + "/encryption")

ipv4 = socket.gethostbyname(socket.gethostname())

json_dump_file = {
    "host": ipv4,
    "port": 5000,
    "wsport": 8765,
    "ssl": False,
}

default_cert_config = """
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment

subjectAltName=@alt_names

[alt_names]
IP.1 = 192.168.1.10
DNS.1 = localhost
"""

default_csr_config = """
[req]
default_bits=2048
prompt=no
default_md=sha256
req_extensions=req_ext
distinguished_name=dn

[dn]
countryName=            IL
stateOrProvinceName=    Israel
localityName=           Zur Moshe
organizationName=       Shachar Ltd
organizationalUnitName= Web Server
commonName=             Shachar Server Crt
emailAddress=           shachar262@gmail.com

[req_ext]
subjectAltName=@alt_names

[alt_names]
IP.1 = 192.168.1.10
DNS.1 = localhost
"""

try:
    json_dump_file["port"] = int(input("HTTP Server Port (default: 5000): "))
except:
    pass
try:
    json_dump_file["wsport"] = int(input("WebSocket Server Port (default: 8765): "))
except:
    pass

json_dump_file["ssl"] = True if input("Setup ssl connection (Y/N): ").lower() == "y" else False

with open("../server.json", "w") as f:
    json.dump(json_dump_file, f)

json_string = json.dumps(json_dump_file)
entries = os.listdir("../templates/assets/js")
files = [entry for entry in entries if os.path.isfile(os.path.join("../templates/assets/js", entry))]
for ff in files:
    with open(f"../templates/assets/js/{ff}", 'r') as f:
        file_contents = f.read()

        # Replace the target string with the new string
        if "replace_string_with_real_json" not in file_contents:
            continue
        modified_contents = file_contents.replace("replace_string_with_real_json", json_string)

        # Write the modified contents back to the file
        with open(f"../templates/assets/js/{ff}", 'w') as f:
            f.write(modified_contents)

if json_dump_file["ssl"]:
    with open("cert.conf", "w") as f:
        f.write(default_cert_config)
        f.write(f"IP.2 = {ipv4}")
    with open("csr.conf", "w") as f:
        f.write(default_csr_config)
        f.write(f"IP.2 = {ipv4}")
    subprocess.Popen("Crt_Gen.cmd")