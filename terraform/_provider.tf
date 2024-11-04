terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }

  backend "s3" {
    bucket = "terraform-state-khoahoang"
    key = "terraform_state_for_gasprices"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-west-1"
}