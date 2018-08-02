terraform {
  backend "s3" {
    bucket = "ragedunicorn-backend"
    key    = "ragedunicorn-base.key.terraform.tfstate"
    region = "eu-central-1"
  }
}

###############
# AWS provider
###############
provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.aws_region}"
}

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

resource "aws_key_pair" "load_key_pair" {
  key_name   = "${var.key_name}"
  public_key = "${data.external.generate_key_pair.result.public_key}"
}
