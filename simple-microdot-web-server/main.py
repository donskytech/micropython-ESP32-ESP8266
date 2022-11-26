from microdot import Microdot, Response
from microdot_utemplate import render_template

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    return 'Hello, world!'

@app.route('/orders', methods=['GET'])
def index(req):
    name = "donsky"
    orders = ["soap", "shampoo", "powder"]

    return render_template('orders.html', name=name, orders=orders)

if __name__ == '__main__':
    app.run(debug=True)