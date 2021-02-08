Description:

Command line tool to determine next cron job runtime


#Running

You need to have python 3 or above installed. There is no pre requisites to install as we are using built in packages 

~~~
git clone https://github.com/arsar7/cron_parser.git
cd cron_parser
python3 parser hh:mm < config (example python parser 13:13 < config)
~~~


<br>

**Arguments**:

* -t Time in HH:MM **[required]**
* -p Path to a file with operations **[required]**


TESTING
~~~
python -m unittest 
~~~