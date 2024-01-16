# WealthTrade
### Project Description
My project, WealthTrade, is a web application developed with Flask that allows users to buy and sell stocks.

## Files
Utilizing the templating language Jinja, I am able to create a file called layout.html as my template and insert elements into the template with other HTML files. In my project, I created nine HTML files excluding the layout.html, which resemble the different pages on my web application.

## CSS Files
### Style.css
In this file, it contains the color and font size of the company logo.

## HTML Files
### Apology.html
When a user submits incorrect information in one of the forms, the apology.html page will be loaded with an image of an angry cat from the website https://memegen.link/, and a message letting the user know what input was inaccurate.

### Buy.html
This file contains a form that asks the user for a valid stock symbol and the number of shares they would like to buy. Once the user fills out the textboxes, they will click the "buy" button.

### History.html
This file contains a table that displays the transactions the user has done. It shows the times, stocks, number of shares, the price, the total value, and whether it was a buy or sell. To keep track of all the users' transactions, I created a table called “history” inside my SQL database that records all the information I listed previously.

### Index.html
This file contains a table that displays the current stocks the user is holding. It includes information like the symbol, the number of shares, the price per share, and the total value. To keep track of the stocks the user currently holds, there is a table inside the SQL database called “transactions” that records all the information I listed previously.

### Layout.html
This file is the official template of all my web pages. It includes the navigation bar, title of tabs, the body where all the elements will then be added through Jinja Templating, and the footer. When the user is signed in, the navigation bar will display the following five different routes: "quote", “buy”, “sell”, “history”, and “log out”. When the user is logged out, the navigation bar will display the following two routes: “register” and “login”. For the title of the tabs, it is dependent on which route the user decided to go and will update upon moving to a different route. For the body, the elements to be displayed will be found in the other HTML files ranging from forms to tables. Lastly, the footer will remain the same everywhere displaying “Ivan Chau’s CLC project”.

### Login.html
This file contains a form that allows a user to submit their login information. The required login information is the user’s username and password. Once the forms are filled, the user will click the “login” button and the app.py file will verify the user's identity.

### Quote.html
This file contains a form asking the user to submit a valid stock symbol to check the price per share. Once the form is filled, the user will click the “quote” button and the app.py file will check if the stock symbol is valid.

### Quoted.html
Once the user’s stock is submitted in the quote.html file, if it exists on the stock market, then it will print a simple statement that lets the user know what the price per share of the stock they inquired about.

### Register.html
This file contains a form that allows a user to create an account by creating a username and password. However, the condition is that the username cannot be taken by another user.

### Sell.html
This file contains a form allowing the user to select a stock and how many shares they want to sell. Once the form is filled out, the user will click the “sell” button.

## SQL Database
### "Users" Table
In this table, it contains all users that have created accounts, including their username, encrypted password, and cash available. To avoid confusion, all users are assigned a unique ID number and are forced to create a unique username.

### “Transactions” Table
In this table, it contains the information about the purchasing transactions a user has made. It includes their unique ID number, the stocks they bought, the number of shares per stock, and the price they bought it at.

### "History" Table
In this table, it contains the information about the buying and selling history of a user. It includes their unique ID number, the time the transaction occurred at, the stock, the number of shares, the price per share, the total value and whether it was a “buy” or “sell”.

## App.py (Possible Routes)
### Index route
In this route, it executes two SQL queries to get the user’s cash and the current stocks being held. In addition, a for-loop is used to calculate the total value of each stock currently held and identify the stocks name, and price per share. Another for-loop is used to convert all the possible integers that should be represented in dollars. After all this is completed, the user’s available cash, current net worth, and the stocks name and price are sent to the index.html file.

### Buy route
In this route, once the user submits the form, the symbol is verified to determine if it exists on the stock market. Next, it checks if the number of shares is valid, based on the submitted number being a positive number and that the user has enough cash available to purchase it. Once it passes all the tests, a SQL query adds or updates the “transaction” table with the information about the stock and value. Another SQL query subtracts money from the user’s account and logs this transaction into the “history” table in the database. The user is redirected to the index page.

### History route
In this route, a SQL query retrieves the transaction history of the user from the database. A for-loop converts all integers that should be represented in dollars. The information from the “history” table is sent to the history.html file.

### Login route
In this route, once a user submits the form, the cookie from the previous user is removed. Later, it verifies that the user submitted an accurate username and password. Once the information is verified, a cookie for the user is created, and the user is redirected to the index page.

### Logout route
In this route, the cookie for the user is removed and is redirected to the login page.

### Quote route
In this route, once a user submits the form, the system checks if the submitted symbol exists on the stock market. Once verification is complete, the price per share is converted into dollars. Then the price of the stock is sent to the quoted.html file.

### Register route
In this route, once a user submits the form, the cookie for the previous user is removed. Later, it verifies that the user submitted a valid username and password. Once verification is complete, their password is encrypted for security reasons. The username, encrypted password, and account number are added to the table “users” in the database. A cookie is created for the user, and the user is redirected to the index page.

### Sell route
In this route, once the user submits the form, a SQL query selects the details of the stock to be sold. It then verifies if there are enough shares available in the user’s account to be sold. If there are enough shares available, the designated number of shares is removed from the user’s account and their cash available is updated. A SQL query adds this transaction into the “history” table, and the user is redirected to the index page with the updated version of current stocks being held.

## Helpers.py (functions)
### apology()
In this function, it takes the message within the parameters (what is inside the brackets), and modifies it so that it meets syntax (coding rules) from this website: https://memegen.link/. The modified text is then sent to the apology.html file to be displayed with the angry cat.

### Login_required()
In this function, the user's cookie is taken and checked if it exists. If the cookie does not exist, it redirects the user to the login page.

### lookup()
In this function, it uses an API (Application Programming Interface). An API is a piece of software that allows two or more computer programs to communicate with each other. In this case, my computer program is communicating with the Yahoo finance website to get current stock prices for a particular stock symbol. When passing a stock symbol inside the parameters (the message in the brackets), it would find the information about the stock on the Yahoo finance website, and return to me a dictionary where the stock symbol is paired with a key called “name”, and the stock price is paired with a key called “price”.
