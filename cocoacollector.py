#!/usr/bin/env python

import logging
import sys
import os
import argparse
from pathlib import Path
import csv

import discord

###########################################
#
try:
	DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
except KeyError:
	logging.error('Please make sure to pass the Discord API token (DISCORD_TOKEN) as environmental variable!')
	sys.exit(1)
#
###########################################
#
def output_path_test(path):
	output_dir = Path(path)
	if output_dir.is_dir() and not [f for f in output_dir.iterdir()]:
		return output_dir
	else:
		raise argparse.ArgumentTypeError(f'"{path}" does not exist or is not an empty directory!')
#
parser = argparse.ArgumentParser(description = 'Archive messages from Discord servers')
parser.add_argument('server_id', type = int, help = 'ID of the Discord server')
parser.add_argument('-u', '--user_id', type = int, help = 'grab only messages made by a specified Discord user')
parser.add_argument('output_dir', type = output_path_test, help = 'path of the output file')
parser.add_argument('-c', '--channel', type = int, nargs = '+', help = 'only run on channels with the specified IDs')
#
###########################################

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

@client.event
async def on_ready():
	logging.info(f'We have logged in as {client.user}')
	logging.info(f'Looking for messages from user "{user_id}" on server "{server_id}"...')
	text_channel_list = find_text_channels(client)
	await find_messages(text_channel_list)
	logging.info('Finished running. Shutting down...')
	await client.close()


# Find server
def find_server(servers):
	for server in servers:
		if server.id == server_id:
			return server
	return ValueError('Bot is not a member of server "{server_id}"')


# Find all text channels
def find_text_channels(client):
	server = find_server(client.guilds)
	text_channel_list = list()
	if selected_channels:
		for channel in selected_channels:
			text_channel_list.append(client.get_channel(channel))
	else:
		for channel in server.channels:
			if str(channel.type) == 'text':
				text_channel_list.append(channel)
	return text_channel_list


# Find all the messages for the user
async def find_messages(text_channel_list):
	for channel in text_channel_list:
		logging.info(f'Collecting messages on channel "{channel.name}({channel.id})"...')
		try:
			if user_id:
				messages = [message async for message in channel.history(limit = None) if message.author.id == user_id]
			else:
				messages = [message async for message in channel.history(limit = None)]
			if messages:
				with open(file_path / f'{channel.name}.csv', 'a', newline = '') as output_file:
					msgwriter = csv.writer(output_file, delimiter = ';')
					for message in format_output(messages):
						logging.debug(message)
						msgwriter.writerow(message)
		except discord.errors.Forbidden:
			logging.error(f'The bot has no access to channel "{channel.name}({channel.id})". Skipping...')


def format_output(messages):
	for message in messages:
		yield [message.id, message.created_at, message.author.name, message.channel.name, message.clean_content]


args = parser.parse_args()
server_id = args.server_id
user_id = args.user_id
file_path = args.output_dir
selected_channels = args.channel


client.run(DISCORD_TOKEN)
