# ipimg
Thing where you upload an image then it lets you see IP addresses that they're accessed from

## how to use
Make sure `flask` and `python-dotenv` are installed that's all the dependencies  
Run `app.py`  

#### environment variable options
 - `ADMIN_PASSWORD`: the admin password. Example: "1234"
 - `SERVER_HOST`: the server host. Example: "127.0.0.1"
 - `SERVER_PORT`: the server port. Example: "5000"
 - `SERVER_DEBUG`: whether to use debug server mode. Set to "yes" to enable otherwise it's disabled
 - `IP_ADDR_HEADER`: use a custom ip header. For reverse proxies and stuff. If unset it'll use the request IP otherwise it'll take the IP from the header. Example: "X-Real-Ip" (depends on server setup though)

## setup
`.env` should have `ADMIN_PASSWORD` which is your password for stuff  

Make a `data` folder with
 - An empty `images` folder
 - A file called `images.json` with the text `[]`

That should be all the setup you need
