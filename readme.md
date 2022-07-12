# CocoaCollector

## Archive messages from Discord servers

### Usage:

The bot only needs the "Read Message History" permission.

**Note**: The bot will only be able to collect messages from channels it has access to.

In order to generate the necessary token and be able to use the bot, [an application needs to be created on the Discord developer dashboard.](https://discord.com/developers/docs/getting-started)

```shell
# git clone --recurse-submodules https://github.com/Erovia/cocoacollector.git
# python3 -m venv cocoacollector_venv
# source cocoacollector_venv/bin/activate
# python install -r requirements.txt
# mkdir <output_dir>
// To collect messages from every channel the bot has access to
# DISCORD_TOKEN=<token> python cocoacollector/cocoacollector.py <server_id> <output_dir>
// To collect messages from selected channels only
# DISCORD_TOKEN=<token> python cocoacollector/cocoacollector.py <server_id> <output_dir> --channel <channel1_id> <channel2_id>
// To collect messages from a specified user
# DISCORD_TOKEN=<token> python cocoacollector/cocoacollector.py <server_id> <output_dir> --channel <channel1_id> <channel2_id> --user_id <user_id>
```

The output will be one CSV file per channel under the <output_dir> directory.
The CSV files can be imported easily into LibreOffice Calc or MS Office Excel.
