# Fraud-Detection
 A blockchain application to detect certificate fraud using sawtooth framework

 This application is used to detect frauds in certificates.

Certificates of students are added to the block chain network by the issuing organisations. Other organisations or companies willing to verify the correctness of the certificate can put up a request and get it verified.

## Instructions for setting up and running the application
1. Build the necessary components used by the application using docker-compose.yaml file by running :</br>
\>> **docker-compose up** <br/>
in the application directory and make necessary changes in the docker-compose.yaml file for further customisation
***
2. The following operations are currently supported in the application :</br>
<b>  1.Adding certificate to the blockchain network</b></br>
<b>  2.Request verification </br> </b>
*** 
3. Run the client.py file which requires python3 installed as shown below inside the container education-client to add certificates of students onto the network :</br>
\>> **python3 client.py add [usn] [name] [marks]**
***
4. Run the client2.py file which requires python3 installed as shown below inside the container education-client to verify the certificate:</br>
\>> **python3 client2.py req [usn] [name] [marks]**
