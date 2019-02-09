variable "access_key" {
  description = "The AWS access key"
}

variable "secret_key" {
  description = "The AWS secret key"
}

variable "aws_region" {
  description = "AWS region"
  default     = "eu-central-1"
}

variable "organization_name" {
  description = "The name of the organization the keypair belongs to"
}

variable "application_name" {
  description = "The name of the application the keypair belongs to"
}

variable "environment" {
  description = "The environment such as prod/int/test the keypair belongs to"
  default     = "test"
}

variable "passphrase" {
  description = "The passphrase for the private key"
}

variable "path" {
  description = "The path where the generated private and public key are stored"
  default     = "./"
}

variable "key_name" {
  description = "The key pair name"
}
