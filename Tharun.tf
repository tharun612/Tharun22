resource "aws_instance" "myinstance" { 
  ami = "ami-0fc5d935ebf8bc3bc" 
  instance_type = "t2.micro" 
  availability_zone = "us-east-1a" 
  subnet_id = "subnet-01d6f82fe66937006" 
  vpc_security_group_ids = ["sg-003933068c0bd85eb"] 
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
