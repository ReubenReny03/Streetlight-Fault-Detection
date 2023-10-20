from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

message_main = ""
total_50_history = []
count = 0
delta = 0
super_pit = 0
message = ""
message_show = "This"
@app.route('/receive_message', methods=['GET','POST'])
def receive_message():
    global message_main
    global total_50_history
    global count
    global delta
    global super_pit
    global message
    print("delta",delta)
    data = request.get_json()
    print(data)
    message = data.get('message', '')
    message_main = message
    a = message_main.split(":")
    val = a[1].replace(" ","")
    val = val.replace("/r","")
    print(f"delta: {delta} val:{val}")
    if delta == int(val):
        super_pit = 9999
        return "Message received: " + str(message)
    elif delta != val:
        
        super_pit = 0
        total_50_history.append(int(val))
        print("Received message:", message)
        
        if (len(total_50_history) >= 50):
            value = total_50_history[0]
            for x in total_50_history:
                if x == value:
                    count +=1
            if (count == 50):
                print(total_50_history)
                print("THIS IS WHAT:",total_50_history[0])
                delta = total_50_history[0]
                total_50_history.clear()
                count = 0
            else:
                count = 0
                total_50_history.clear()
        return "Message received: " + str(message)
    
@app.route('/get_updated_values', methods=['GET'])
def get_updated_values():
    if super_pit == 0:
        a = message_main.split(":")
        val = a[1].replace(" ","")
        val = val.replace("/r","")
        total_50_history.append(int(val))
        print(int(val))
        message_show = ""
        if (int(val) < 1000):
            message_show = "The tube light has a issue"
        else:
            message_show = "The tube light is running good"
    if super_pit == 9999:
        message_show = "The sourse of light has a issue"
    
    print("MESSAGE",message_show)
    return jsonify({
        "super_pit": super_pit,
        "message_main": message_main,
        "total_50_history": total_50_history,
        "message": message_show
    })

    

@app.route('/', methods=['GET','POST'])
def root():
    global message_show
    print("SUPER PIT",super_pit)
    # if super_pit == 0:
    #     a = message_main.split(":")
    #     val = a[1].replace(" ","")
    #     val = val.replace("/r","")
    #     total_50_history.append(int(val))
    #     print(int(val))
    #     message_show = ""
    #     if (int(val) < 960):
    #         message_show = "The tube light has a issue"
    #     else:
    #         message_show = "The tube light is running good"

    #     return render_template("index.html",received_message=message_show)
    # if super_pit == 9999:
    #     message_show = "The sourse of light has a issue"
    #     return render_template("index.html",received_message=message_show)
    
@app.route('/unseen', methods=['GET','POST'])
def unseen():
    return render_template("sike.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)