# AWS_3tier_architecture_terraform

Infrastructure Automation | Deploying a 3-Tier Architecture in AWS Using Terraform

The three-tier architecture is the most popular implementation of a multi-tier architecture and consists of a single presentation tier, logic tier, and data tier.

It is a viable choice for software projects to be started quickly.
aws_3tier_architecture_terraform

Presentation tier : Clinet [ HTML,CSS,PHP]
Logic Tier : python, java, NodeJS
Data Tier : MY SQL , mongo DB etc 

-> So to implement the 3 tier Architecture we will first create a VPC with 2 Public subnets and 1 private subnet .

-> In 2 public subnet our backend application servers will be hosted in 2 AZ and DB servers will be hosted in private subnet 

--> we have to specify route table , security groups , elastic IP's , ingternet Gateway and NAT gateway inside the VPC 

--> NAT gateway will be in public subnet anf only outbound traffic route is enable for Private instance to talk to internet and for public subnet ports 22 , 80 is open for inbound connectivity 

-> we will also create a ALB for ELB inorder to distrubute the traffic from end users to our target groups i.e. backend web servers created in the public subnet. 

-> later we will access our application using DNS URL of the ALB which will automatically point to the backend target groups based on the listerner rules  


### Resources need to be created / installed :

* Custom VPC

* 2 Subnets (Public)

* 1 Subnet (Private)

* 2 EC2 Instances

* Security Group

* Elastic IP

* NAT Gateway

* Internet Gateway

* Route Table

* Application Load Balancer

* Apache Webserver

* MySQL DB

## Logic implemeted to create resources 

1. created a VPC in ap-south-1 region with CIDR : 10.0.0.0/16 with 2 subnets one public subnet with CIDR : "10.0.1.0/24","10.0.2.0/24" in 2 availability Zone ap-south-1a and ap-south-1b and private with CIDR : 10.0.3.0/24 

2. created 2 seperate ec2-instance in 2 public subnet : "10.0.1.0/24","10.0.2.0/24" in each in ap-south-1a and ap-south-1b AZ for high availability and 1 private Ec2-instance for accesing the DB server on the private subnet CIDR : 10.0.3.0/24 without any public IP

3. created 2 security groups --> webserver [ec2-instance --> public subnet--> Allowed ports --> 22,80] and --> DB server [ec2-instance--> private subnet--> 22,3306]

4. created 1 internet gateway & attached it to the VPC for internet-routable traffic

5. now for routing the traffic inside and outside the VPC we have created Route table and attached it to the internet gateway and assoicated it to the public subnet

6. inorder to provide outbound internet access to the private subnet [ ec2-instance --> db server] created a NAT gateway in the public subnet with an Elastic IP and assosciated it to the default route table 

7. for distrubting the end user traffic to the backed Ec2 instance [ public subnet ] created a ALB and attched it to the 2 public subnet created for ec2-instance

8. now install apache web server in both the webserver [ ec2-instance] with DB server as a baackend to store application artifcats & access the Httpd application using default DNS name of the ALB.

