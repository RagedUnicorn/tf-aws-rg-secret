# tf-aws-rg-secret

> Key Pairs is a module for generating key material for use with AWS inside the RagedUnicorn organization

This module is intended to generate key pairs that can be used by other applications. They should not generate their own key pairs.

## Purpose

Key pairs are sensitive material that allow access to certain infrastructure and should be kept secret. To reach this certain level of security this module is responsible for generating such keys for applications. The applications themselves only reference the key pairs by their name but do not now anything else about them.

## Dependency

### Terraform State

This repository and all its applications depend upon the base s3 `tf-ragedunicorn-backend` for state storage.

### Python

This repository relies on python to generate key pairs. It is recommended by Terraform to generate key pairs externally to avoid them showing up in the terraform state.

For development purpose the [tls_private_key](https://www.terraform.io/docs/providers/tls/r/private_key.html) resource can be used but be careful terraform will store the private key unencrypted inside its state file.

##### Python installation

[Python installation](https://www.python.org/downloads/)

##### Pip dependencies
```
pip install pycryptodome necessary for crypto
```

## Applications

A list of applications that are managed by this repository:

| Name               | Description                                                       |
|--------------------|-------------------------------------------------------------------|
| ragedunicorn_base  | The base module for this repository                               |
| wow_vanilla_server | A module for creating the infrastructure for a wow vanilla server |

## Setup

### Credentials

Credentials can be setup in different ways. The modules within this repository either expect the credentials to be available via environment variables or supplied directly to terraform as variables.

```
export AWS_ACCESS_KEY_ID="[acceskey]"
export AWS_SECRET_ACCESS_KEY="[secretkey]"
export AWS_DEFAULT_REGION="eu-central-1"
```

Or directly

```
terraform apply -var 'access_key=[acceskey]' -var 'secret_key=[secretkey]'
```

If none of these are supplied terraform will ask for the variables interactively while preparing the setup

For more details see [documentation](https://www.terraform.io/docs/providers/aws/index.html).

### Setup an Application

Inside the application folder initialize and then apply the terraform configuration

```
# initialize terraform
terraform init

# check what terraform will create
terraform plan

# create resource
terraform apply
```

**Note:** Terraform will always execute `data external` because it has no knowledge about the state. This also means that every time a terraform apply is executed terraform will try to create the configured key pair. This happens even before terraform ask for execution permission. Generating a key pair is usually a one time thing and does not need to be repeated over and over again. Because of this the terraform state is not as important as it is for a whole application setup with a lot of infrastructure. It is nonetheless helpful to be able to also destroy a key with the help of terraform if it is no longer needed.

Once terraform has generated the keypair its public part is upload to the AWS ec2 management console and can be inspected there. The user of this module is responsible for both storing the private key and the optional passphrase that was set on that key.

For storage of those secrets 1Password is used. The private key should be stored as a document and the password should be separately saved as password and link to the document.

Follow the following naming convention for consistency:

`[rg]_[tf]_[application-name]_keypair`

### Creating a new Application

At the root level of the repository create a new folder with the name of the application and the following structure.

```
tf-aws-rg-secret/
├── [application-name]/
│   ├── main.tf
│   ├── variables.tf
│   ├── output.tf
│   ├── terraform.tfvars
│   └── README.md
```

| Name             | Description                                                                    |
|------------------|--------------------------------------------------------------------------------|
| main.tf          | Basic setup for terraform S3 and AWS provider and generation of the keypair(s) |
| variables.tf     | Variables that are needed for the setup                                        |
| output.tf        | Output of terraform after applying the configuration                           |
| terraform.tfvars | Can be used for default values for the terraform variables.                    |
| README.md        | Description of the application and its repository                              |

### Terraform Storing State

All applications should store state inside the base RagedUnicorn s3 store. The key for the state file should starting with the application name and marked with `key` to not clash with the main application state file.

```hcl
terraform {
  backend "s3" {
    bucket = "ragedunicorn-backend"
    key    = "[application].key.terraform.tfstate"
    region = "eu-central-1"
  }
}
```

### Creating a Keypair

Creating a key pair is done with the help of the external terraform provider. Terraform will execute the command and pass in all query parameters as JSON.

```hcl
data "external" "generate_key_pair" {
  program = ["python", "../generate_key_pair.py"]

  query = {
    organization_name = "${var.organization_name}"
    application_name  = "${var.application_name}"
    environment       = "${var.environment}"
    passphrase        = "${var.passphrase}"
    path              = "${var.path}"
  }
}
```

Terraform expects whatever command that was executed to return a JSON response on the standard output. This means that whatever command is executed should not log anything else to standard output. Otherwise terraform will complain about a malformed JSON structure.

### Upload a Keypair to AWS

Uploading the keypair is then done by extracting the public key from the response from the command. This requires the previously executed command to return a JSON that contains the public key content in a JSON key with the name `public_key`. For consistency this should be done for all key generations.

```hcl
resource "aws_key_pair" "load_key_pair" {
  key_name   = "rg-tf-wow-vanilla-server"
  public_key = "${data.external.generate_key_pair.result.public_key}"
}
```

### Gotchas

#### Do not leak secrets

Never store keys in this repository. This repository shall never contain any secrets. It does only know how to create them but never store them.

Do not use terraforms output capabilities to log secrets because terraform will write thing like that into its terraform state and might be leaked unintentionally. Setting a password on the private key is also recommended to avoid such scenarios.

#### Execute once

Usually terraform should only be run once on an application because the external terraform provider will always rerun and generate a new key pair without asking before performing. Terraform will however ask before uploading the new key to AWS. Also the python script will never overwrite existing key pairs.

#### Regenerating a Key Pair

A new key pair can be generated at any point but remember that the ec2 infrastructure does not update its key just because they key changed. For this at least a restart of the instance is needed. Maybe even destroying the infrastructure first and rebuild it.
