#! python
# @author Michael Wiesendanger <michael.wiesendanger@gmail.com>
# @description Generate an SSH Key Pair for later use as aws key pair
# Note: Do not use print inside this script. Terraform expects to only see JSON formatted output.

import sys
import json
import os

from Crypto.PublicKey import RSA

def error(message):
    """
    Errors must create non-zero status codes and human-readable, ideally one-line, messages on stderr.
    """
    print(message, file=sys.stderr)
    sys.exit(1)


def parseinputs():
    """
    Parses the input arguments received from terraform as json input and sets proper default values if no value was passed
    """
    input_arguments = json.loads(sys.stdin.read())

    if not input_arguments["application_name"]:
        input_arguments["application_name"] = "none"

    if not input_arguments["organization_name"]:
        input_arguments["organization_name"] = "none"

    if not input_arguments["environment"]:
        input_arguments["environment"] = "none"

    if not input_arguments["passphrase"]:
        input_arguments["passphrase"] = ""

    if not input_arguments["path"]:
        input_arguments["path"] = "./"

    return input_arguments


def checkfileexistence(path, filenname):
    return os.path.isfile(path + filenname)


def generatekey(input_arguments):
    filename = input_arguments["application_name"] + "-" + input_arguments["organization_name"] + "-"\
        + input_arguments["environment"]

    private_key_file_name = filename + ".pem"
    public_key_file_name = filename + ".pub"

    if checkfileexistence(input_arguments["path"], private_key_file_name):
        error("Private keyfile already exists")

    if checkfileexistence(input_arguments["path"], public_key_file_name):
        error("Public keyfile already exists")

    key = RSA.generate(2048)

    # write private key to file
    with open(private_key_file_name, "wb") as private_key_file:
        os.chmod(private_key_file_name, 0o600)
        private_key_content = key.export_key("PEM", input_arguments["passphrase"])
        private_key_file.write(private_key_content)

    # write public key to file
    with open(public_key_file_name, "wb") as public_key_file:
        public_key_content = key.publickey().exportKey("OpenSSH")
        public_key_file.write(public_key_content)

    generateoutput(input_arguments, public_key_content)


def generateoutput(input_arguments, public_key_content):
    json.dump(
        dict(
            public_key = public_key_content.decode(),
            application_name = input_arguments["application_name"],
            organization_name = input_arguments["organization_name"],
            environment = input_arguments["environment"],
            path = input_arguments["path"],
        ),
        sys.stdout
    )


inputs = parseinputs()
generatekey(inputs)
