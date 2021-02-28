# Algorand automate claim rewards
A docker-compose project that will help you automate claiming your Algorand stake rewards. For this repo, I used the basic examples provided by the Algorand developer team.

By default, a cron job will run every 6 hours when you start the docker container transferring a minimum amount of Algo to the address you want to claim your stake rewards.
## Requirements
- You will need to install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/) if you don't have them already.
- Open an account under [PureStake](https://developer.purestake.io/) and retrieve an API token.

## Installation
1. Clone the project.
2. Copy the `.env.example` file and call it `.env`.
3. Create a temporal Algorand Wallet, save the seed, and transfer just a few Algo. We will use the seed for the next step.
4. Fill the env variables inside `.env` with the required info. (**Warning:** Do not use the seed of the account you want to claim the rewards, use the temporal one we created above)

## Usage

```python
docker-compose up -d
```
Once you run it, by default the docker container will start every time you start the system and it will run in the background.

## Optional
- If you need to change the interval of the transactions, you can do it under the crontab file. Just make sure to rebuild your docker image with `docker-compose build --no-cache` and then use `docker-compose up -d` again. 
