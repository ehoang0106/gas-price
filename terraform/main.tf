resource "aws_dynamodb_table" "GasPrices" {
  name = "GasPricesTracker"
  billing_mode = "PROVISIONED"
  read_capacity = 1
  write_capacity = 1

  hash_key = "date"

  attribute {
    name = "date"
    type = "S"
  }

}