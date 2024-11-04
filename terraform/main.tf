resource "aws_dynamodb_table" "GasPricesTracking" {
  name = "GasPricesTracking"
  billing_mode = "PROVISIONED"
  read_capacity = 5
  write_capacity = 10

  hash_key = "date"

  attribute {
    name = "date"
    type = "S"
  }

}