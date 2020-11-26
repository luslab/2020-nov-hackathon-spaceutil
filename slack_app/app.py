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
      return_dict[row[-1].replace("./", "")] = float(row[0])
  return(return_dict)

@app.command("/luslab-du")
def luslab_du(ack, say, command):
    ack()
    du_table = get_du_table()
    command_arg = command["text"]
    if command_arg == "all" or command_arg == "all bysize":
      du_message = "\n".join([str(t[0]) + "\t" + t[1] for t in sorted([(du_table[key], key) for key in du_table], reverse=True)]) 
    elif command_arg == "all byname":
      du_message = "\n".join([key + "\t" + str(du_table[key]) for key in sorted(du_table.keys())])
    elif command_arg in du_table.keys():
      du_message = command_arg + "\t" + str(du_table[command_arg])
    else:
      du_message = ("Invalid argument. Should be either \"all\" or " +
        "\n".join([key for key in du_table]))
    say(f"{du_message}")

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
