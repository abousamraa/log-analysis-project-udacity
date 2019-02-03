# Log Analysis project

### Project Overview
>
This the first project on  Udacity's Full Stack Web Developer Nanodegree. 
this project is a  reporting tool to analyze database containing data about articles , authors and logs.
It returns output of plain text about the following :
1- The three most popular articles of all time
2- The most popular authors of all time
3- days which have more than 1% of requests lead to errors

### How to Run program ?

#### PreRequisites:
  * [Python3](https://www.python.org/)
  * [VirtualBox](https://www.virtualbox.org/)
  * [Vagrant](https://www.vagrantup.com/)

#### Setup Project:
  1. Install Vagrant and VirtualBox after dowload it From the links above
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
  3. Download [sql data file ](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)  and unzip it
  4. Copy the newsdata.sql file , Put this file into the vagrant directory, which is shared with your virtual machine.
  
#### Launch your Virtual Machine:
  1. open your terminal ( such as git bash ) , then navigate into the vagrant folder in fullstack-nanodegree-vm folder , then run this command   
  ```
    $ vagrant up
  ```
  2. When vagrant up is finished running, you will get your shell prompt back , Then Log into using this command:
  
  ```
    $ vagrant ssh
  ```
  3. Change directory to /vagrant 
  
#### Creating database and connecting it

  1. Creat news database by running newsdata.sql using this command:
  
  ```
    psql -d news -f newsdata.sql
  ```
 
  2. Use `psql -d news` to connect to database.


#### Creating views :

  1. Create view Requests_count using:
  ```
    CREATE VIEW Requests_count AS  
    select date(time) as daylog , count(status) as requests from log 
    group by daylog
    order by daylog; 
  ```
  | Column  | Type    |
  | :-------| :-------|
  | daylog  | date    |
  | requests| integer |
  
  2. Create view Errors_count using:
  ```
    CREATE VIEW Errors_count AS
    select date(time) as daylog , count(status) as errors from log
    where status='404 NOT FOUND'
    group by daylog
    order by daylog;
  ```
  | Column        | Type    |
  | :-------      | :-------|
  | daylog        | date    |
  | errors        | integers|

  3. Create view errors_percentage using:
  ```
    CREATE VIEW errors_percentage AS  
    select Requests_count.daylog , case 
        when Requests_count.requests = 0
            then null
        else  Round( (errors_count.errors::decimal / Requests_count.requests)*100 , 4 )
        end E_percentage    
    from Requests_count , errors_count 
    where Requests_count.daylog = errors_count.daylog ;

  ```
  | Column        | Type    |
  | :-------      | :-------|
  | daylog        | date    |
  | E_percentage  | decimal |
  
#### Running the python program :
  1. Install psycopg2-binary using this command :
  ```
    $ pip3 install psycopg2-binary
  ```
  2. From the vagrant directory inside the virtual machine, run log.py using:
  ```
    $ python3 log-report.py
  ```
