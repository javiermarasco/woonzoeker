# woonzoeker

Small script to check for houses for rent in Pararius webpage, this script is based on the idea of Jasper Ginn (https://github.com/JasperHG90/pararius).

The main objective was to practice some python scripting and getting a tool that helps find for a renting place.

# 
Initially this script creates a database (sqlite3) to maintain the results and only send new ones on each running.

The script should be added into cron to run every hour or so to get new listings 

The new listings found will be emailed but if no new listing is found, an email will not be sent.

Hope you enjoy it!!
