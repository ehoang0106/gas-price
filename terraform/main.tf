resource "aws_dynamodb_table" "NewGasPricesTracker" {
  name = "NewGasPricesTracker"
  billing_mode = "PROVISIONED"
  read_capacity = 5
  write_capacity = 10

  hash_key = "date"

  attribute {
    name = "date"
    type = "S"
  }

}

resource "aws_cloudwatch_metric_alarm" "dynamodb_write_capacity_alarm" {
  alarm_name          = "DynamoDBWriteCapacityAlarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ConsumedWriteCapacityUnits"
  namespace           = "AWS/DynamoDB"
  period              = 43200  #12 hours
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Alarm when write capacity units exceed 5 in 12 hours"
  dimensions = {
    TableName = aws_dynamodb_table.GasPrices.name
  }

  alarm_actions = [
    aws_sns_topic.DataWriteInDynamoDB.arn
  ]
}

resource "aws_sns_topic" "DataWriteInDynamoDB" {
  name = "DataWriteInDynamoDB"
}