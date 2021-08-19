# Distance Matrix API application (+ Python script)

This application provides you an opportunity to:
- quickly check the functionality of the Distance Matrix API
- use the Distance Matrix API service without programming
- get results directly in Excel
- use this demo as a good example of how to use the API in a Python script

You’ve got no time to deal with coding, or you just need to calculate the travel distances and route time for a large number of similar locations quickly at one time.
Use this Python script or Windows application with little or no code handling.

1. Download this zip archive here on github.

2. Unzip it (extract all) and you should see the following files:

3. Firstly you need to insert your active DM token into the file named token. You can get the token for free here: https://distancematrix.ai/contact

4. You will also need a data.csv file with the set of addresses to run an application or script. If you just want to try how the API works you can leave this file as it is, some addresses are already listed there as an example.

You can always change and add your locations in this file. The number of lines is not limited but we recommend running not more than 10k pairs at a time. 

The file can be opened in Excel. Or any text editor, i.e. Notepad.

In this case, it is important that the delimiter between the 5 variables must be a semicolon ";" , as in this example:
28.43164,77.07254;28.47243,77.05457;driving;best_guess;now

5. It is important to fill in all the fields correctly.

- Into the origin/destination fields you can insert specific addresses, just city names or postcodes/postal indexes/zip as well as geographic coordinates (lat/long).
- In the mode field add the mode you need: driving, walking, bicycling or transit_mode=bus, transit_mode=train|tram|subway
- In the traffic_model field: either leave best_guess, or change to pessimistic or optimistic
- Leave now in the departure_time field, or specify the time converting it to the Unix Timestamp format firstly (it should look like, 1627557223). 
https://www.unixtimestamp.com/ service is convenient to convert time to the required format
- You can also find and add more features from our documentation

6. If the parameters in the data file are specified incorrectly, then the line with the fault request will be skipped and not written to the document. 

7. When the file is ready, choose what is more convenient for you: the application or the script  

Launch by double clicking and the API will start calculating. 
Execution speed is about 1 second per line.

- The requests are performed sequentially one by one. Which means that the next request will not be sent until the previous one is completed and completely recorded.
- The forced termination of the script is performed by the command CTRL + C

8. A file with the results named result.csv will be automatically created when you start the script or application. As a result you should get lines with all the incoming parameters, the results of the API calculations and the time when the request has been made.

9. Using this script you can easily get the API’s results in Excel

We hope you find it convenient to use our Distance Matrix API
