terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_instance" "app" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  tags = {
    Name = "sample-app"
  }
}
