#!/bin/sh

# Install Apache & Amazon EC2 utils
apt update -y
apt install apache2 -y
apt install amazon-ec2-utils -y

# Start the Apache service
systemctl start apache2

# Enable Apache to start on every system boot up
systemctl enable apache2

# Get the current instance's AZ
AZ=`ec2-metadata -z | cut -d':' -f2`

# Create a simple HTML file
# /var/www/html/index.html
# This is the default file that Apache will use
# when render the default page. 

cat > /var/www/html/index.html <<EOF
<html>
<head>
  <title>CSYE 6225 EC2 AZ Demo</title>
</head>

<body>
  <h1>Welcome to the CSYE 6225 EC2 AZ demo page</h1>
  <p>This EC2 instance is located at $AZ</p>
</body>
</html>
EOF