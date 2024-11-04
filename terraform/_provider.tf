terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }

  # backend "s3" {
  #   bucket = "terraform_state_bucket"
  #   key = "terraform_state_for_gasprices"
  #   region = "us-west-1"
  # }
}

provider "aws" {
  region = "us-west-1"
}