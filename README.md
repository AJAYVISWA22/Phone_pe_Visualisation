# Phonepe Pulse Data Visualization and Exploration:A User-Friendly Tool Using Streamlit and Plotly

## ABOUT PHONEPE:
![phonepe1](https://github.com/beingbvh/Phonepe-Pulse-Data-Visualization/assets/135937352/fa39d457-d483-495b-bec7-467abfe66e39)

PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer .The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.

The PhonePe app is available in 11 Indian languages. Using PhonePe, users can send and receive money, recharge mobile, DTH, data cards, make utility payments, pay at shops, invest in tax saving funds, liquid funds, buy insurance, mutual funds, and digital gold.

PhonePe is accepted as a payment option by over 3.5 crore offline and online merchant outlets, constituting 99% of pin codes in the country.

## Phonepe Pulse:
![phonepebeat](https://github.com/beingbvh/Phonepe-Pulse-Data-Visualization/assets/135937352/33ddfe70-083a-4d59-b6ec-06eae571cef6)

PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.

PhonePe Pulse provides users with **insights and trends related to their digital transactions** and usage patterns on the PhonePe app. It offers personalized analytics, including spending patterns, transaction history, and popular merchants among PhonePe users. 

This feature aims to help users track their expenses, understand their financial behavior, and make informed decisions.

## Phonepe Pulse Data Visualisation:
Data visualization refers to the **graphical representation of data** using charts, graphs, and other visual elements to facilitate understanding and analysis

These visualizations are designed to present information in a **visually appealing and easily digestible format**, enabling users to quickly grasp trends, patterns, and insights from their transaction history.

## Problem Statement:
The Phonepe pulse Github repository contains a large amount of data related to
various metrics and statistics.The goal is to extract this data and process it to obtain
insights and information that can be visualized in a user-friendly manner.

## Approach:
## 1. Data extraction:
* **Clone the Github** using scripting to fetch the data from the
Phonepe pulse Github repository and store it in a suitable format such as CSV
or JSON.
## 2. Data transformation: 
* Use a scripting language such as **Python**, along with
libraries such as Pandas, to manipulate and pre-process the data.
* This may include cleaning the data, handling missing values, and transforming the data
into a format suitable for analysis and visualization.
## 3. Database insertion:
* Use the **"mysql-connector-python"** library in Python to
connect to a MySQL database and insert the transformed data using SQL
commands.
## 4. Dashboard creation: 
* Use the **Streamlit and Plotly** libraries in Python to create
an interactive and visually appealing dashboard.
* Plotly's built-in **geo map** functions can be used to display the data on a map and Streamlit can be used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.
## 5. Data retrieval:
* Use the **"mysql-connector-python"** library to connect to the
MySQL database and fetch the data into a Pandas dataframe. 
* Use the data in the dataframe to update the dashboard dynamically.
## 6. Deployment: 
* Ensuring the solution is secure, efficient, and user-friendly. 
* Testing the solution thoroughly and **deploy the dashboard** publicly, making it
accessible to users.

# Technologies:
* **Github Cloning**
* **Python**
* **Pandas**
* **sqlite**
* **Streamlit**
* **Plotly**

## Dashboard:
The dashboard consists of:

- **HOME Page:** Offers details about PhonePe Pulse Data Visualization, explaining its purpose, features, and benefits to users.Provides information about PhonePe, including its background, services, and significance in the digital payments landscape.
- **Data Exploration:** Provides comprehensive insights based on various metrics such as all India, States, and Top categories. It includes detailed analysis on transaction and user data within each category, along with insights based on different time periods such as year and quarter.
- **Search:** key findings and trends observed in the data.
- **INSIGHTS Page:** Presents user-friendly and easily understandable insights derived from the analysis. Additionally, it includes an annual report summarizing key findings and trends observed in the data.

- ### To Run
Make sure the changes in the API and Database Connection as mentioned above.
Run the following command in your terminal to start the Streamlit application:
```bash
streamlit run yourscript.py
```
"Ensure the terminal path!"

## Conclusion
In conclusion, PhonePe Pulse Data Visualization harnesses the power of graphical representations to offer users a visually appealing and easily digestible format for understanding and analyzing their transaction history. By presenting information through charts, graphs, and other visual elements, this tool enables users to swiftly discern trends, patterns, and insights within their data, empowering them to make informed decisions and gain deeper insights into their financial behavior.
