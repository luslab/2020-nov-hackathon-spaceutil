import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Handling events

#TEMPORARY FUNCTION
def get_du_table():
  return_dict = {}
  with open("test_data/du.out", "r") as du_in:
    for line in du_in:
      row = line.strip().split()
      return_dict[row[-1]] = row[0]
  return(return_dict)

@app.command("/luslab-du")
def luslab_du(ack, say, command):
    ack()
    du_table = get_du_table()
    command_arg = command["text"]
    if command_arg == "all":
      say(f"{str(du_table)}")
    elif command_arg in du_table.keys():
      say(f"{du_table[command_arg]}")
    else:
      return_text = ("Invalid argument. Should be either \"all\" or " +
        str(du_table.keys()))
      say(f"{return_text}")

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )
  
  except Exception as e:
    logger.error(f"Error opening modal: {e}")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
