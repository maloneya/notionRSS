## What
This script reads a configured list of rss feeds and creates rows in a Notion table for each entry in the feed

## How
A few settings need to be added into a local config file 
```
{
    "settings": {
        "notion_token" : <Notion_session_token>,
        "notion_url" : <URL OF Table>
    },
    "feeds": {
        <name>:<url>,
    }
}
```
Expected Notion Table Schema
```
title: string
link: string
source: select 
```
> Note: Currently notion will only allow select options that are configured in the fields schema, these options must be first configured in notion 
