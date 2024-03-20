# MetaMarkAgency

Welcome to the **MetaMarkAgency** repository, a cutting-edge solution designed to automate and enhance your Facebook marketing efforts using the power of AI. This SmmA agency is built upon the **Agency Swarm** framework, enabling the creation of specialized agents to handle different aspects of Facebook marketing: generating ad copy, creating images, and managing Facebook posts.

### Agency Structure

The AI SmmA Live Agency is composed of three primary agents:

- **Ad Copy Agent**: Generates compelling ad copy tailored to your campaign's goals.
- **Image Creator Agent**: Utilizes Dalle 3 to create visually appealing images that complement the ad copy.
- **Facebook Manager Agent**: Handles the posting of ads on Facebook, along with campaign and ad set creation.

## Facebook App Setup

To utilize the Facebook Manager Agent for posting ads, you need to set up a Facebook app and obtain the necessary credentials and permissions. Follow these steps to get started:

1. **Create Your Facebook App**:
   - Visit the [Facebook for Developers](https://developers.facebook.com/) site and log in.
   - Click on "My Apps" and select "Create App".
   - Choose "Business" as your app type and provide a name for your app.
   - Follow the prompts to complete the app creation process.

2. **Add the Marketing API**:
   - In your app dashboard, find the "Add a Product" section and select "Marketing API".
   - Click "Set Up" to add the Marketing API to your app.

3. **Configure App Settings**:
   - Navigate to "Settings" > "Basic" in your app dashboard.
   - Note your "App ID" and "App Secret" for later use.
   - Add your app domain, privacy policy URL, and other required details.

4. **Obtain Access Token**:
   - Go to the [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/).
   - Select your app from the "Application" dropdown.
   - Click "Generate Access Token" and grant the necessary permissions for ad management.
   - Copy the generated access token for use in your agency setup.

5. **Update Environment File**:
   - Create an `.env` file in your project directory if you haven't already.
   - Add your "App ID", "App Secret", and "Access Token" to the file as environment variables.

    ```env
    FB_APP_ID=your_app_id
    FB_APP_SECRET=your_app_secret
    FB_ACCESS_TOKEN=your_access_token
    ```

6. **Install Facebook Business SDK** (if required by your tools):
   - Run the following command to install the SDK:

   