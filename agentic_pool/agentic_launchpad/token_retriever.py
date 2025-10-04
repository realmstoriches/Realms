import webbrowser

def facebook_guide():
    print("\n🔐 Facebook Token Setup:")
    print("1. Go to https://developers.facebook.com/")
    print("2. Create an app → Add 'Pages API'")
    print("3. Use Graph API Explorer to generate a User Token with:")
    print("   - pages_manage_posts")
    print("   - pages_read_engagement")
    print("4. Exchange for a Page Access Token")
    print("5. Paste into .env as FACEBOOK_PAGE_ACCESS_TOKEN")

def linkedin_guide():
    print("\n🔐 LinkedIn Token Setup:")
    print("1. Go to https://www.linkedin.com/developers/")
    print("2. Create an app → Add 'Marketing Developer Platform'")
    print("3. Use OAuth 2.0 flow:")
    print("   - Redirect URI: https://localhost")
    print("   - Scope: r_liteprofile r_emailaddress w_member_social")
    print("4. Visit this URL to begin:")
    client_id = "[your-client-id]"
    redirect = "https://localhost"
    scope = "r_liteprofile%20r_emailaddress%20w_member_social"
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect}&scope={scope}"
    print(f"🔗 {auth_url}")
    webbrowser.open(auth_url)

def main():
    facebook_guide()
    linkedin_guide()

if __name__ == "__main__":
    main()

