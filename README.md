# Widget Generator

A game kind of thing that you interact with through HTTP requests. You can do everything in a web browser, or you could write a cool interface :)

Running locally? `flask run` hosts at `http://localhost:5000`

# Actions

### Log in first

`POST` `username` to `/login` (or `GET /login` in a web browser). There's no password or authentication or anything. This way multiple people can use the same server.

### Assets
##### Actions
* Buy an asset `/asset/<symbol>/buy`
* Sell an asset `/asset/<symbol>/sell`
* Queue an asset for production `/asset/<symbol>/produce`

##### Information
* Get asset price `/asset/<symbol>`
* Get current asset/cash quantities `/info/portfolio`
* Get recipe queue `/info/queue`

# How to play pls

* Use your money to buy assets
* Asset prices change over time (buy low sell high xd)
* Craft assets into other assets
* Sell assets for money
* That's it there's not much to it yet
