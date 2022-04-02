=========================
django devops try project
=========================

Sandbox project to try devops staff, CI\CD etc.

Steps of work
=============

CircleCI
--------


1. Prepare project with at least one application to run simple test with ``pytest`` for first circleci workflow.

    1.1 Register at https://app.circleci.com/

    1.2 Setup your project

    1.3 Add ``.circleci`` folder with ``config.yml`` file

2. ``config.yml`` - `First working version with comments <https://github.com/LowerDeez/devops-try/blob/7bd2928acd0e23438e7816e846690f00f444e381/.circleci/config.yml>`_
3. ``config.yml`` - `Add some code style checks (black, pylama, isort, migrations linter) <https://github.com/LowerDeez/devops-try/commit/8ed4e02a81c5302bcffb726b7baf0d8bd1d2d5eb>`_
4. `Add invoke tasks to update code style <https://github.com/LowerDeez/devops-try/commit/0c20d8161beb7731d12d2a32217fd5bb2b23d724>`_.
5. `Fix isort <https://github.com/LowerDeez/devops-try/commit/19b440d16fea8bb191c77c5ff89a6092fb2c0cbd>`_.
6. `Fix django-linter <https://github.com/LowerDeez/devops-try/commit/ecd8b3086ee06f150a29558f49c550d634b77ebf>`_.
7. Configure docker for "production"
    7.1 Related articles
        https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
        https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
        https://testdriven.io/blog/django-lets-encrypt/
    7.2 Commands:
        docker-compose -f production.yml run --user root --rm django bash -c "cd server && python manage.py collectstatic --no-input --clear" - collect static
        docker-compose -f production.yml up -d --build
        docker-compose -f production.yml exec django bash -c "cd server && python manage.py migrate --noinput"
        docker-compose -f production.yml exec django bash -c "cd server && python manage.py createsuperuser"
        docker-compose -f production.yml stop
    7.3 `Commit with "ready" docker-compose file <https://github.com/LowerDeez/devops-try/commit/f884276f5ad09816de9a2e64020ef0a3c8ece517>`_.

8. How to setup AWS server (Both tutorials worth a check):
    Articles to read
        `Continuously Deploying Django to AWS EC2 with Docker and GitLab <https://testdriven.io/blog/deploying-django-to-ec2-with-docker-and-gitlab/#gitlab-ci-deploy-stage>`_
        `Deploying Django to AWS with Docker and Let's Encrypt (Main to setup AWS) <https://testdriven.io/blog/django-docker-https-aws/#running-the-containers>`_

    8.1. `Configuring AWS Credentials (Access key ID, Secret access key) <https://www.youtube.com/watch?v=qmtDRmplMG4>`_
    8.2. `Get Account id <https://console.aws.amazon.com/billing/home?#/account>`_

    8.3. Run ``aws configure``
        AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
        AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
        Default region name [None]: us-west-1
        Default output format [None]: json

    8.4. Add postgres production variables to server/.env `with values from AWS <https://testdriven.io/blog/django-docker-https-aws/#aws-rds>`_.
         Postgres section should be removed from docker-compose:

        POSTGRES_HOST=aws.host.us-east-1.rds.amazonaws.com
        POSTGRES_PORT=5432
        POSTGRES_DB=djangoec2
        POSTGRES_USER=webapp
        POSTGRES_PASSWORD=passwordd


    8.5. build, login and push
        docker-compose -f production.yml build
        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
        docker-compose -f production.yml push

9. Configure SSH connection for AWS instance, created along side with some of articles in 8.1 or 8.2
    9.1 SSH into the instance using your Key Pair like so:
        # example:
        # ssh -i ~/.ssh/django.pem ec2-user@100.26.120.143
    9.2 generate a new SSH key:
        [ec2-user]$ ssh-keygen -t rsa
    9.3 Save the key to /home/ec2-user/.ssh/id_rsa and don't set a password. This will generate a public and private key -- id_rsa and id_rsa.pub, respectively. To set up passwordless SSH login, copy the public key over to the `authorized_keys <https://security.stackexchange.com/questions/20706/what-is-the-difference-between-authorized-keys-and-known-hosts-file-for-ssh>`_ file and set the proper permissions:
        [ec2-user]$ cat ~/.ssh/id_rsa.pub
        [ec2-user]$ vi ~/.ssh/authorized_keys
        [ec2-user]$ chmod 600 ~/.ssh/authorized_keys
        [ec2-user]$ chmod 600 ~/.ssh/id_rsa
    9.4 Copy the contents of the private key:
        [ec2-user]$ cat ~/.ssh/id_rsa
    9.5 Exit the remote SSH session. Set the key as an environment variable on your local machine:
        $ export PRIVATE_KEY='-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEA04up8hoqzS1+APIB0RhjXyObwHQnOzhAk5Bd7mhkSbPkyhP1
        ...
        iWlX9HNavcydATJc1f0DpzF0u4zY8PY24RVoW8vk+bJANPp1o2IAkeajCaF3w9nf
        q/SyqAWVmvwYuIhDiHDaV2A==
        -----END RSA PRIVATE KEY-----'
    9.6. Add the key to the `ssh-agent <https://www.ssh.com/ssh/agent>`_:
        $ ssh-add - <<< "${PRIVATE_KEY}"
    9.7. To test, run:
        $ ssh -o StrictHostKeyChecking=no ubuntu@<YOUR_INSTANCE_IP> whoami
        ec2-user
    9.8. If this will not work - use for private key value from cat ~/.ssh/django-devops-try.pem (Key Pair from aws)
    9.9 Create project dir
        ssh -o StrictHostKeyChecking=no ubuntu@18.206.2.247 mkdir /home/ubuntu/devops_try

10. Add env variables to your project in CIRCLECI (Project Settings section)
    AWS_ACCESS_KEY_ID	xxxx24EG
    AWS_ACCOUNT_ID	xxxx7006
    AWS_DEFAULT_REGION	xxxxst-1
    AWS_ECR_ACCOUNT_URL	xxxx-ec2
    AWS_SECRET_ACCESS_KEY	xxxxDI0S
    EC2_PUBLIC_IP_ADDRESS	xxxx.247
    PRIVATE_KEY	xxxx----
    DEFAULT_SERVER	xxxx.247
    DEFAULT_USER	xxxxntu
    DJANGO_DB_URL	xxxxoec2
    DJANGO_SECRET_KEY	xxxxoYHK
    DJANGO_ALLOWED_HOSTS	xxxxp.ua
11. `Update production.yml (remove db section) <https://github.com/LowerDeez/devops-try/commit/87604de7b4f3462cd731f4a6fbe24d42e4886358>`_
12. `Add yml config to build and push docker image <https://github.com/LowerDeez/devops-try/commit/0abac48f23d6dcd17c870456e35699f0acf37651>`_
13. `Add yml config to deploy and task to login to aws in CLI <https://github.com/LowerDeez/devops-try/commit/65b124050ce8e1b4e9b2ba8e9f473a338bc11f26>`_
    13.1 Move env file to ./envs/.production/
    13.2 Added invoke tasks to deploy
    13.3 Skip collect static in Dockerfile
    13.4 Change ``DJANGO_DB_URL`` to DB_URL in Circleci to avoid overriding of default env name for DB with aws connection string
14. Setup SSH connection from CircleCI to your instance (To perform automatic deployments, CircleCI is going to need to log in to our server and pull the latest code from our git repo. )
    If you want to use separate user:
        Related articles:
            1. `How we use CircleCI with Git and DigitalOcean to streamline our deployments <https://medium.com/@tomnashflex/how-we-use-circleci-with-git-and-digitalocean-to-streamline-our-deployments-49a6a02b6dd6>`_
            2. `How To Automate Deployment Using CircleCI and GitHub on Ubuntu 18.04 <https://www.digitalocean.com/community/tutorials/how-to-automate-deployment-using-circleci-and-github-on-ubuntu-18-04>`_
        1. On local Machine
            1.1 ssh-keygen -m PEM -t rsa -f ~/.ssh/id_rsa_circleci
        2. On VPS
            1.1 Add ``circleci`` user
                sudo useradd -m -d /home/circleci -s /bin/bash circleci
                sudo mkdir /home/circleci/.ssh
        3. On local machine
            cat ~/.ssh/id_rsa_circleci.pub - copy value
        4. On VPS
            sudo nano /home/circleci/.ssh/authorized_keys - paste from 3 step
        5. On local machine
            ssh circleci@my.droplet.ip -i ~/.ssh/id_rsa_circleci - test connection
        6. Login to CircleCI
        7. Go to your Project Settings and navigate to SSH Keys
        8. cat ~/.ssh/id_rsa_circleci - copy value on local machine
        9. Add SSH key in Additional SSH Keys section
        10. Update ``DB_USER`` env variable with ``circleci`` at Project Setting Environment Variables section
    If you want to use default user (i.e. ubuntu):
        cat ~/.ssh/django-devops-try.pem - copy (key pair from AWS)
        Add to CircleCI to SSH Keys
        ``DEFAULT_USER`` = ubuntu
15. `Update deploy task with images pull and up <https://github.com/LowerDeez/devops-try/commit/8ee8b68f675c7bec5a8aee529a53a4e1cb4d2451>`_
    15.1 Fixed nginx section in production.yml
    P.S. Don't forget to push build after changes