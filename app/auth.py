import firebase_admin
from firebase_admin import auth
from flask import Blueprint, request, current_app, redirect, session, flash

bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("")
def auth_base():
    from urllib.parse import quote
    from secrets import token_hex
    state = token_hex(32)
    session["state"] = state
    return redirect(f"https://discordapp.com/api/oauth2/authorize?client_id={current_app.config['DISCORD_CLIENT_ID']}&redirect_uri={quote(current_app.config['DISCORD_REDIRECT_URI'])}&response_type=code&scope=identify&state={state}")

@bp.route("/callback")
def auth_callback():
    try:
        from requests import get, post
        # Obtains code from the callback
        code = request.args.get('code')
        if not code:
            flash("No code sent. Please try again.")
            return redirect("/")
        # Check to make sure the user accepted.
        if request.args.get("error"):
            if request.args["error"] == "access_denied":
                flash("You denied access, which means we can't identify you.")
            return redirect("/")
        # Check state, because we care about security.
        if session.get("state") != request.args.get("state"):
            flash("Mismatch of state parameters. Please try again.")
            return redirect("/")
        data = {
            'client_id': current_app.config['DISCORD_CLIENT_ID'],
            'client_secret': current_app.config['DISCORD_CLIENT_SECRET'],
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': current_app.config['DISCORD_REDIRECT_URI'],
            'scope': 'identify'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # Post to Discord
        r = post('%s/oauth2/token' % current_app.config['DISCORD_API_ENDPOINT'], data=data,headers=headers)
        r.raise_for_status()
        # Parse response data into object
        response_data = r.json()

        # Now, use access token to identify the user.
        headers = {
            "Authorization": "Bearer %s" % response_data['access_token']
        }
        r = get('%s/users/@me' % current_app.config['DISCORD_API_ENDPOINT'], headers=headers)
        r.raise_for_status()
        userdata = r.json()
        # Now we should have valid userdata, and should check if a user exists within firebase.
        if userdata.get('avatar'):
            avatar = f"https://cdn.discordapp.com/avatars/{userdata['id']}/{userdata['avatar']}.png"
        else:
            avatar = f"https://cdn.discordapp.com/embed/avatars/{str(int(userdata['discriminator']) / 5)}.png"
        try:
            user = auth.get_user(userdata['id'])
        except auth.AuthError:
            # User likely does not exist - let us try and create it.
            user = auth.create_user(uid=userdata['id'],
                                    display_name=f"{userdata['username']}#{userdata['discriminator']}",
                                    photo_url=avatar)
            flash("Welcome! We've created an account for you, using your discord account information.")
        # Now we should have a valid user object, and can assign that to our session.
        if not user.disabled:
            session["userID"] = user.uid
            auth.update_user(user.uid,display_name=f"{userdata['username']}#{userdata['discriminator']}",
                                    photo_url=avatar)
            flash("Successfully logged in.")
            return redirect("/")
        else:
            flash("Your account has been disabled. Please contact a Sudo or Root for more information.")
            return redirect("/")
    except Exception as e:
        import traceback
        flash("An unexpected error occurred while processing your login.")
        print(traceback.format_exc())
        return redirect("/")

@bp.route("logout")
def logout():
    auth.revoke_refresh_tokens(request.user.uid)
    session.pop("userID")
    flash("Logged out.")
    return redirect("/")


def get_user(uid):
    try:
        return auth.get_user(uid)
    except auth.AuthError:
        return None

