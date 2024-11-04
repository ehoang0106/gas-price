terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }

  #save terraform state to a s3 bucket
  backend "s3" {
    bucket = "terraform-state-khoahoang"
    key    = "terraform_state_price_tracker"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-west-1"
}