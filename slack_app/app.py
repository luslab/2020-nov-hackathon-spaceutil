import os
import table_utils
from slack_bolt import App
from flask import Flask, request, make_response, Response

flask_app = Flask(__name__)

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Handling events
@app.command("/luslab-du")
def luslab_du(ack, say, command):
    ack()
    du_table = table_utils.get_du_table()
    if "text" in command:
      command_arg = command["text"]
    else:
      command_arg = ""
    if command_arg == "all" or command_arg == "all bysize":
      du_message = "\n".join([table_utils.sizeof_fmt(t[0]) + "\t" + t[1] for t in sorted([(du_table[key], key) for key in du_table], reverse=True)])
      du_message = table_utils.align_first_col(du_message)
    elif command_arg == "all byname":
      du_message = "\n".join([key + "\t" + table_utils.sizeof_fmt(du_table[key]) for key in sorted(du_table.keys())])
      du_message = table_utils.align_first_col(du_message)
    elif command_arg in du_table.keys():
      du_message = command_arg + "\t" + table_utils.sizeof_fmt(du_table[command_arg])
      du_message = table_utils.align_first_col(du_message)
    else:
      du_message = ("Invalid argument. Should be one of the following:\nall\nall bysize\nall byname\n" +
        "\n".join([key for key in du_table]))
    du_message = "/luslab-du " + command_arg + "\n" + du_message
    say({
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "```" + du_message + "```"
			}
		}
	]
    })

@app.command("/luslab-recommend")
def luslab_recommend(ack, say, command):
    ack()
    valid_argument = True
    if "text" in command:
      command_arg = command["text"]
    else:
      valid_argument = False
      command_arg = ""
    try:
      int(command_arg)
    except ValueError:
      valid_argument = False
    if valid_argument:
      blocks = table_utils.get_pretty_recommentations(int(command_arg))
    else:
      blocks = [
        {
          "blurb_str": "No argument or non-integer argument",
          "path_str": None
        }
      ]
    blocks = [
      {
        "blurb_str": "```/luslab-recommend " + command_arg + "```",
        "path_str": None
      }
    ] + blocks
    return_blocks = []
    for block in blocks:
      return_blocks.append(
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": block["blurb_str"]
          }
        }
      )
      if not block["path_str"] == None:
        return_blocks.append(
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click for file paths"
                },
                "value": block["path_str"],
                "action_id": "path_button"
              }
            ]
          }
        )
    say({"blocks": return_blocks})

@app.action("path_button")
def approve_request(ack, body, say):
    # Acknowledge action request
    ack()
    say({
      "blocks": [
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": body["actions"][0]["value"]
          }
        }
      ]
    })

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

# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
from slack_bolt.adapter.flask import SlackRequestHandler
handler = SlackRequestHandler(app)

# Register routes to Flask app
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
  # handler runs App's dispatch method
  return handler.handle(request)

@flask_app.route("/slack/interactive", methods=["POST"])
def slack_interactive():
  # handler runs App's dispatch method
  return handler.handle(request)

if __name__ == "__main__":
  flask_app.run(port=3000)
