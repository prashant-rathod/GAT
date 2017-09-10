ec2 GAT Instructions Writeup
6/24/17

AWS Architecture:
The aws boxes that are used are the t2 micro boxes. This should be more than enough for the amount of traffic than we encounter. The aws GAT server is setup as follows. nginx is used to serve our html content at our url, which is accessible from anywhere in the world. Requests to this url are sent to nginx, which listens on port 80 (http). nginx then forwards this request to port 8000 where gunicorn is listening. gunicorn is the server that is serving our dynamic python code. gunicorn gives the request to application.py, where it is processed and then returned to the caller up the call stack, all the way to the url. nginx was chosen over apache. The nginx configuration ended up being simpler and more straightforward.
Gunicorn is currently being run simply as a background process. Improvements to this setup include running gunicorn through some kind of supervisor, supervisord (http://supervisord.org/) for instance. There are many other options as well. This would ensure our server restarts if any errors are encountered, would maintain only one instance of the server, etc.

Instructions on aws operation:
General things:
- Always test locally before you deploy ($ python application.py)
- Always let others know you are doing a deployment
- Have others test once deployment is done
- If errors exist try doing deployment by hand (run commands in shell script by hand)
Prerequisites:
ssh client (preinstalled on unix and mac, recommend putty for windows)
git
sudo access (may not be required, depends on the user)

Set up a new ec2 instance:
1. Follow the following tutorial with modified steps below. http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance
At step 3 choose Ubuntu instead of Amazon Linux
At step 7b add the following security groups: HTTP, anywhere; SSH, anywhere

2. Follow the following tutorial to download .pem file.
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-connect-to-instance-linux

3. Clone GAT project from gitlab
------- Following commands are for *nix, if you have windows your commands will be different but procedure is the same, not sure how putty works--------
4. $ cd /path/to/project/GAT/lifecycle
5. $ mv ~/Downloads/*.pem . DO NOT CHECK THIS FILE INTO GIT
6. $ sudo chmod 400 *.pem
7. $ sudo chmod 755 *.sh
8. Open aws console online
9. Copy the url of the instance
10. Open shell scripts and virtual.conf inside of lifecycle/ and replace INSTANCE_URL value with that copied from online and PEM_NAME to the name of the pem file
11. $ ./setup.sh #(answer y to all questions asked by apt-get)
12. If you wish to deploy current version of the app follow instructions below

Deploy a new version to an existing instance:
1. Follow steps above 8-10.
2. Obtain .pem file, whoever first created the instance has it.
3. $ cd /path/to/project/GAT/lifecycle
4. $ mv /path/to/.pem/*.pem .
5. Open virtual.conf file. Change server_name to url copied from aws console in step 1.
6. Do step 7 above. (only need to be done once per computer)
7. $ ./clean.sh 
8. $ ./deploy.sh #(answer y to all questions asked by apt-get, will take awhile the first time)
13. Should be able to view application at the url specified on aws console.

Troubleshooting:
Having multiple gunicorn processes running at once will lead to 500 errors from front end. How to fix if server errors are happening:
1. $ ssh -i aws-ec2-gat1.pem ubuntu@ec2-52-37-61-214.us-west-2.compute.amazonaws.com "cd ~/Projects/GAT; lifecycle/restart.sh"

If errors persist and the problem was not multiple processes, ssh into the machine, and check out ~/nohup.out, /var/log/nginx/access.log and /var/log/nginx/error.log. The python console prints to nohup.out, while other errors and warnings print to error.log, and all requests are recorded in access.log. These have been made available on the app through the /log/python-out /log/server-error /log/server-access paths.

You can check the status of nginx server by the following command $ sudo service nginx status

You can restart nginx by the following command $ sudo service nginx restart #(note, also kill all gunicorn processes and start a new one (see above) when you do this).

If you are having trouble with ssh, make sure you own the pem file. Otherwise use sudo with ssh or run sudo chown <username> aws-ec2-gat1.pem

