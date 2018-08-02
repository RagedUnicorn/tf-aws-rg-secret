# ragedunicorn_base

> Module for ragedunicorn-base

A module for creating key pairs that can be used throughout projects. Usually only for development and testing purposes intended.

## Link

No direct links

## Inputs

| Name              | Description                                                    | Type   | Default        | Required |
|-------------------|----------------------------------------------------------------|--------|----------------|----------|
| access_key        | The AWS access key                                             | string | -              | yes      |
| application_name  | The name of the application the keypair belongs to             | string | -              | yes      |
| aws_region        | AWS region                                                     | string | `eu-central-1` | no       |
| environment       | The environment such as prod/int/test the keypair belongs to   | string | `test`         | no       |
| key_name          | The key pair name.                                             | string | -              | yes      |
| organization_name | The name of the organization the keypair belongs to            | string | -              | yes      |
| passphrase        | The passphrase for the private key                             | string | ``             | no       |
| path              | The path where the generated private and public key are stored | string | `./`           | no       |
| secret_key        | The AWS secret key                                             | string | -              | yes      |


## Outputs

| Name       | Description                                  |
|------------|----------------------------------------------|
| key_name   | The name of the key as it can be used in aws |
| public_key | Content of the generated private key         |
