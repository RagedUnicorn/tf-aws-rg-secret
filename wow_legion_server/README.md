# wow-legion-server

> Module for wow-legion-server

A module for creating key pairs.

## Link

[tf-aws-wow-legion-server](https://github.com/RagedUnicorn/tf-aws-wow-legion-server)

## Inputs

| Name              | Description                                                    | Type   | Default        | Required |
|-------------------|----------------------------------------------------------------|--------|----------------|----------|
| access_key        | The AWS access key                                             | string | -              | yes      |
| secret_key        | The AWS secret key                                             | string | -              | yes      |
| aws_region        | AWS region                                                     | string | `eu-central-1` | no       |
| organization_name | The name of the organization the keypair belongs to            | string | -              | yes      |
| application_name  | The name of the application the keypair belongs to             | string | -              | yes      |
| environment       | The environment such as prod/int/test the keypair belongs to   | string | `test`         | no       |
| path              | The path where the generated private and public key are stored | string | `./`           | no       |
| key_name          | The key pair name                                              | string | -              | yes      |
| passphrase        | The passphrase for the private key                             | string | ``             | no       |

## Outputs

| Name       | Description                                  |
|------------|----------------------------------------------|
| key_name   | The name of the key as it can be used in aws |
| public_key | Content of the generated private key         |
