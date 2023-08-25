import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="your-project-id", location="us-central1")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 512,
    "top_p": 0.8,
    "top_k": 1
}
model = TextGenerationModel.from_pretrained("text-bison@001")

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import json
from collections import Counter

with open("/home/fitbit/output.txt", "r") as text_file:
    texto1=text_file.read()


@app.route('/predict', methods= ['POST'])
def predict():
    if request.get_json():
        x=json.dumps(request.get_json())
        #print('ok')
        x=json.loads(x)
    else:
        x={}
    data=x["text"]  # text
    print(data)

    response = model.predict(
        texto1+"""

Q: How do I set up FitBit ?
A: The Fitbit app is compatible with most popular phones. See fitbit.com/devices to check if your phone is compatible.
To get started:
1. Download the Fitbit app: Apple App Store for iPhones and Google Play Store for Android phones
2. Install the app, and open it.
3. Tap Sign in with Google, and follow the on-screen instructions to set up your
device.
When you're done with setup, read through the guide to learn more about your new
watch and then explore the Fitbit app.

Q: How do I add a new widget ?
A: 1. From the clock face, swipe up to the bottom of the widgets, and tap Manage.
icon next to the widget you want to add.
2. Under More Widgets, tap the
3. Swipe up to the bottom of the page, and tap Done.

Q: How do I open Apps ?
A: From the clock face, swipe left to see the apps installed on your watch. To open an app, tap it.

Q: Which features does FitBit have about the weather ?
A: You can see the weather in your current location, as well as 2 additional locations you
choose, in the Weather app on your watch.
To check the weather, open the Weather app to see conditions in your current
location. Swipe up to view the weather in other locations you added. Tap a location
to see a more detailed report.
You can also add a weather widget to your watch.

Q: I follow your instructions about fixing Wi-Fi but they didn't work:
A: If FitBit still won't connect to Wi-Fi, make sure that you're attempting to connect
your watch to a compatible network. For best results, use your home Wi-Fi network.
FitBit can't connect to 5GHz Wi-Fi, WPA enterprise, or public networks that
require logins, subscriptions, or profiles.
After you verify the network is compatible, restart your watch and try connecting to
Wi-Fi again. If you see other networks appear in the list of available networks, but
not your preferred network, move your watch closer to your router.

Q: Is my FitBit water resistant ?
A: Yes, it is water resistant up to 50 meters

Q: {} ?
A:
""".format(data)

        ,**parameters)
    return jsonify({
        "fulfillment_response": {
            "messages": [{
                "text": {
                    "text": [
                        response.text
                    ]
                }
            }]
        }
    })



if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)


