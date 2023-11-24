provider "aws" { 
  access_key = "AKIAW6KT6TBG5LIPYIP2"
  secret_key = "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" 
  region = "us-east-1" 
} 
resource "aws_instance" "myinstance" { 
  ami = "ami-0fc5d935ebf8bc3bc" 
  instance_type = "t2.micro" 
  availability_zone = "us-east-1a"
  subnet_id = "subnet-09022726d605f2f37" 
  vpc_security_group_ids = ["sg-070848893435179da"]
  key_name = "bhanu" 
  associate_public_ip_address = true
  count = 1  
  tags = { 
    Name="tharun"
  } 
  ebs_block_device { 
  device_name = "/dev/sdb" 
  volume_type = "gp2" 
  volume_size = 10
  }
}
