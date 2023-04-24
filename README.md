# V-Bucks Alerts
- Bot that shares daily V-Bucks mission alerts in Save the World via a Discord webhook with support for many languages.
- You can customize the bot with your language and share daily v-bucks missions to your Discord server!

# How to use
- Make sure you have [Python](https://www.python.org/downloads/) 3.6 or higher installed and added to your PATH.
- Run `packages.bat` or type the following command into the command prompt to install the necessary modules.
```
pip install coloredlogs
pip install requests
pip install logging
```
- Enter your account informations in the `settings.json` file.
- Run `start.bat` to launch the program.
# Configuration
- To share missions in a Discord server of your choice, create a webhook via integrations in the selected channel and copy the webhook URL and paste it into "webhook_url" key in the settings.json file.
- The settings.json file will prompt you to enter information related to your account such as "Account ID", "Device ID", and "Secret". These details are necessary for accessing Save the World missions via the Epic Games API. You can check out the [DeviceAuthGenerator](https://github.com/xMistt/DeviceAuthGenerator) project made by [xMistt](https://github.com/xMistt) to obtain these details.
- You can customize values such as "language" and "title", the supported languages are: `ar`, `de`, `en`, `es`, `es-419`, `fr`, `it`, `ja`, `ko`, `pl`, `pt-BR`, `ru`, `tr`
- Note: The "checkrate" value sets the check of missions in seconds. Default to 30, recommended is >= 30.
## Example
```json
{
  "last_check": "2023-04-23T18:00:00.000Z",
  "checkrate": 30,
  "language": "en",
  "webhook_url": "WEBHOOK_URL",
  "account_id": "ACCOUNT_ID",
  "device_id": "DEVICE_ID",
  "secret": "SECRET",
  "title": "V-Bucks Mission Alerts"
}
```
# Support
If you have a problem, you can seek support from the following links.
- [Twitter](https://twitter.com/Liqutch)
- [Discord](https://discord.gg/nNPrQeqCyf)
- [Contact](https://liqutch.dev/)
