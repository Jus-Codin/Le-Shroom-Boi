Just a mushroom boi


Breakdown: 

main.py: The main script for the bot
datadump.py: Custom made package for saving and access data from data.json
keep_alive.py (required for Replit hosting): Used with uptimerbot to keep the bot alive (if using free version, the bot will go down every 5 hours). This file can be deleted or ignored if you are using another hosting service such as Railway.app


Admin commands:

edit_count (arguments: new_count): changes the current count to the selected count (new_count)
dev_warning (arguments: target channel ID): sends a dev warning to the target channel - "This bot is currently under maintenance"
remote_send (arguments: target channel ID, message): sends a message to the target channel as the bot
show_save (arguments: nil): displays the current count saved, as well as timestamp