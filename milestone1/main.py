from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, InternetGateway, ALB, Route53, VPCRouter
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users
from diagrams.aws.security import ACM
from diagrams.onprem.container import Docker  # Importing Docker icon

# Define the cloud architecture diagram with specified size (width * height)
graph_attrs = {
    "size": "50,30"  # Width=11 inches, Height=8.5 inches (adjust as needed)
}

with Diagram("AWS Cloud Architecture", show=False, graph_attr=graph_attrs):

    users = Users("External Users")
    route53 = Route53("Amazon Route 53")

    # VPC with CIDR 10.0.0.0/16
    with Cluster("VPC (10.0.0.0/16)"):

        igw = InternetGateway("Internet Gateway")
        vpc_router = VPCRouter("VPC Router")

        # Availability Zone 1 (AZ1)
        with Cluster("AZ1 (us-east-1a)"):

            # Public Subnet in AZ1 with Dockerized EC2 instances
            with Cluster("Public Subnet (10.0.1.0/24)"):
                ec2_1 = [Docker("Dockerized App") >> EC2("EC2 Instance (AZ1)") for _ in range(2)]  # Two EC2 instances in AZ1

            # Private Subnet in AZ1 for RDS
            with Cluster("Private Subnet (10.0.3.0/24)"):
                rds_1 = RDS("AWS RDS (AZ1)")

        # Availability Zone 2 (AZ2)
        with Cluster("AZ2 (us-east-1b)"):

            # Public Subnet in AZ2 with Dockerized EC2 instances
            with Cluster("Public Subnet (10.0.2.0/24)"):
                ec2_2 = [Docker("Dockerized App") >> EC2("EC2 Instance (AZ2)") for _ in range(2)]  # Two EC2 instances in AZ2

            # Private Subnet in AZ2 for RDS
            with Cluster("Private Subnet (10.0.4.0/24)"):
                rds_2 = RDS("AWS RDS (AZ2)")

        # Secure internal routing between EC2 instances and RDS
        for ec2_instance in ec2_1:
            ec2_instance >> Edge() >> rds_1  # Local access
            ec2_instance >> Edge() >> vpc_router

        for ec2_instance in ec2_2:
            ec2_instance >> Edge() >> rds_2  # Local access
            ec2_instance >> Edge() >> vpc_router

        vpc_router >> Edge() >> rds_1
        vpc_router >> Edge() >> rds_2

        # Auto Scaling Group managing EC2 instances across AZ1 and AZ2
        asg = AutoScaling("Auto Scaling Group")
        asg >> Edge() >> ec2_1
        asg >> Edge() >> ec2_2

    # Elastic Load Balancer with SSL/TLS support
    alb = ALB("Application Load Balancer")
    acm = ACM("AWS ACM (SSL/TLS Certificates)")  # ACM for SSL/TLS

    # Route 53 directs traffic through ALB
    users >> Edge(label="DNS Query") >> route53 >> Edge(label="User Requests") >> alb
    alb >> Edge() >> ec2_1
    alb >> Edge() >> ec2_2

    # CloudWatch monitoring for all components
    cloudwatch = Cloudwatch("CloudWatch Monitoring")
    for component in [alb, asg] + ec2_1 + ec2_2 + [rds_1, rds_2]:
        cloudwatch >> Edge() >> component

    # Connect ACM to ALB for SSL/TLS security
    acm >> Edge() >> alb
