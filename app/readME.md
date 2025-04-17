# reThread

# Our project
reThread is a community-powered fashion resale app that connects buyers, sellers, trend analysts, and administrators through a data-driven platform focused on sustainability, style, and accessibility. The resale market is booming, yet most platforms lack visibility into what's trending, how pricing changes over time, or how to truly match users with fashion they care about.

reThread addresses those gaps by organizing listings through user-created style groups (based on aesthetic, location, or university), offering detailed item tagging, and surfacing analytics about what’s selling and why. Shoppers can easily browse, save, and message sellers. Sellers gain access to profile and listing analytics to optimize their closet. Admins moderate community behavior and content, and trend analysts study keyword, price, and demographic data to generate fashion insights. From casual thrifters to small business resellers, reThread makes secondhand fashion smarter and more personal.

# Our team
Rowen Latif, Mahika Modi, Fiona Donohue, Lily Hartley, Zoe Jagelshi

## How to build the containers
Before running the containers, make sure you create the following secret file in the `secrets/` directory:

1. `.env`
   - Contains environment variables for MySQL database setup
   - Example contents:
     ```env
     MYSQL_ROOT_PASSWORD=password
     MYSQL_DATABASE=rethread_db
     MYSQL_USER=rethread_user
     MYSQL_PASSWORD=rethread_pass
     ```

### Starting the Containers
To start the backend, database, and frontend:

```bash
docker compose up -d



# Video Demo
https://drive.google.com/file/d/1OwgM4d6-mH9Nv8K5b6SCeOTk5ELJXuie/view?usp=sharing

Inside the root folder, create a .env file with the following contents:
MYSQL_ROOT_PASSWORD=password
MYSQL_DATABASE=rethread_db
MYSQL_USER=rethread_user
MYSQL_PASSWORD=rethread_pass


Start Docker Containers
Use Docker Compose to start all containers:
docker compose up -d
