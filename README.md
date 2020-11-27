# 2020-nov-hackathon-spaceutil

## Goals

1. Provide information on storage usage, akin to running the Linux command `du -h -d 1`
2. Have different methods of querying the data

## Future plans

1. Provide suggestions for improving storage usage.
    * Use the MD5 hash of files to determine file duplication
        * `You and user both have copies of file1.bam totalling 1.5GB. Consider a shared resource`
    * Use the file type to identify files to compress
        * `You have 21 “.bam” files totalling 30GB, which can be compressed by running this command: gzip etc.`
2. Provide a dashboard to allow for more detailed representations of the data

## Setting up the development environment

### Setting up the environment variables

Environment variables need to be set to access the database and authorise the app with Slack.
The Slack variables can be found by going to the [app's page](https://api.slack.com/apps), under "Basic Information" (Signing Secret) and under "OAuth & Permissions" (Bot User OAuth Access Token).

```
export URL=<Database URL>
export USR=<Database user>
export PW=<Database password>
export DB=<Database name>
export SLACK_BOT_TOKEN=<Slack Bot User OAuth Access Token>
export SLACK_SIGNING_SECRET=<Slack Signing Secret>
```

### Setting up localtunnel

Set up a conda environment with node.js:

```
conda install nodejs
```

Then enable localtunnel:

```
npx localtunnel --port 3000 -h 'http://serverless.social'
```

This will give you a URL from which your port is available:

```
your url is: https://massive-dodo-83.serverless.social
```

This URL, with `/slack/events` appended to the end, needs to be copied into your [app's page](https://api.slack.com/apps) in two locations:

1. Event Subscriptions > Request URL
2. Slash Commands > Edit the command > Request URL

### Running the Slack app

Set up the conda environment:

```
conda env create -f space_analyser/environment.yml
conda activate space-util
```

Then run the app with:

```
python slack_app/app.py
```
