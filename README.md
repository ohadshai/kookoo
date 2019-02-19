##################  Description  #################


In this program There is a server that yanks as first step function calls from a file
and the client every interval of time, requests for new function from the server.
The server will randomly choose function name from his list and the client will execute
the function and will send the response to the server.

######  Notes  ######

* Compatible to Python2.7/Python3
* In order to add new function calls :
  1. Add the function call in server\functions.txt
  2. Add the function implementation in client\functions_executor.py

** In this Program I used root logger with 2 handlers: 1 for log file 1 for stdout.
   The log file is being rotated by the application (every week, 4 weeks back).

   IMPORTANT: the log file is being written from two processes - Client and Server.
              If there will be more writers for this log or the writing speed to log will be fast enough it could
              trigger locking of the file and messages not will be written in live (from experience)

   My logging for now is good, but Example Solution to this corner case - in Linux (but I am sure it's possible in other OSs):

    * Use syslog process to collect logs from a lot of applications in parallel and dispatch them to relevant
      log file + using the right class (SyslogHandler) in Python apps.

      - Example of configuration for syslog to get logs from different apps:

        $Umask 0000
        $FileOwner root
        $FileGroup kookoo
        $FileCreateMode 0664
        $EscapeControlCharactersOnReceive off

        if ($programname == "kookoo") then {

            $ROOT_FOLDER/kookoo.log
            & stop
        }



    * Use logrotate of linux.

      - Example of logrotate file in /etc/logrotate.d/kookoo:

          "$ROOT_FOLDER/kookoo*.log" {
            daily
            rotate 9
            compress
            missingok
            notifempty
            maxsize 10M
            sharedscripts
            postrotate
                invoke-rc.d rsyslog rotate > /dev/null
            endscript
            create 0664 root kookoo
            su root kookoo
            }



######  Deployment  +  Usage  ######

------ Server ------

1. cd server

2. virtualenv -p /usr/bin/python venv

3. source venv/bin/activate

4. pip install -r requirements.txt

5. python run.py

------ Client ------

1. cd client

2. virtualenv -p /usr/bin/python venv

3. source venv/bin/activate

4. pip install -r requirements.txt

5. python run.py


######  Configuration  ######

File : 'settings.ini'

    * Server ip + port
    * Interval time of request for function
    * log level
