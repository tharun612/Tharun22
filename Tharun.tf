
provider "aws" { 
  access_key = "AKIAVN2D6J7GC4S6KV7Z"
  secret_key = "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"
  region = "ap-south-1"
} 
resource "aws_instance" "myinstance" { 
  ami = "ami-0287a05f0ef0e9d9a" 
  instance_type = "t2.micro" 
  availability_zone = "ap-south-1a" 
  subnet_id = "subnet-0a6fdb0c9acd901f7" 
  vpc_security_group_ids = ["sg-065da31091aed4761"] 
  key_name = "tharun" 
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
